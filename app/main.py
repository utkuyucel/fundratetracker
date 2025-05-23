from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from analytics import FedRateAnalytics
from etl_pipeline import FedRateETL
from datetime import datetime
from typing import Optional
import asyncio

app = FastAPI(
    title="Federal Funds Rate Analytics API",
    description="Analytics platform for Federal Reserve interest rate data",
    version="1.0.0"
)

analytics = FedRateAnalytics()
etl = FedRateETL()

@app.get("/")
async def root():
    return {"message": "Federal Funds Rate Analytics API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/rates/latest")
async def get_latest_rate(db: Session = Depends(get_db)):
    latest = analytics.get_latest_rate(db)
    if not latest:
        raise HTTPException(status_code=404, detail="No rate data found")
    
    return {
        "date": latest.date.isoformat(),
        "rate": float(latest.rate),
        "rate_change": float(latest.rate_change) if latest.rate_change else None
    }

@app.get("/api/rates/historical")
async def get_historical_rates(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    data = analytics.get_historical_data(db, start, end)
    
    return {
        "data": [
            {
                "date": r.date.isoformat(),
                "rate": float(r.rate),
                "rate_change": float(r.rate_change) if r.rate_change else None
            }
            for r in data[:limit]
        ],
        "count": len(data[:limit])
    }

@app.get("/api/analytics/summary")
async def get_analytics_summary(db: Session = Depends(get_db)):
    summary = analytics.get_rate_summary(db)
    if not summary:
        raise HTTPException(status_code=404, detail="No data available for analysis")
    
    return summary

@app.get("/api/analytics/moving-averages")
async def get_moving_averages(db: Session = Depends(get_db)):
    return analytics.calculate_moving_averages(db)

@app.post("/api/pipeline/trigger")
async def trigger_etl_pipeline():
    try:
        await etl.run_pipeline()
        return {"status": "success", "message": "ETL pipeline executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
