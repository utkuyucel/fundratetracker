import pandas as pd
from sqlalchemy.orm import Session
from database import get_db, FederalFundsRate
from datetime import datetime, timedelta
import numpy as np

class FedRateAnalytics:
    def __init__(self):
        pass
    
    def get_latest_rate(self, db: Session):
        """Get the most recent Federal Funds Rate"""
        latest = db.query(FederalFundsRate).order_by(
            FederalFundsRate.date.desc()
        ).first()
        return latest
    
    def get_historical_data(self, db: Session, start_date=None, end_date=None):
        """Get historical rate data with optional date filtering"""
        query = db.query(FederalFundsRate)
        
        if start_date:
            query = query.filter(FederalFundsRate.date >= start_date)
        if end_date:
            query = query.filter(FederalFundsRate.date <= end_date)
            
        return query.order_by(FederalFundsRate.date.desc()).all()
    
    def calculate_moving_averages(self, db: Session):
        """Calculate moving averages for different periods"""
        data = self.get_historical_data(db)
        df = pd.DataFrame([(r.date, float(r.rate)) for r in data], 
                         columns=['date', 'rate'])
        df = df.sort_values('date')
        
        return {
            'ma_30': df['rate'].rolling(window=30).mean().iloc[-1] if len(df) >= 30 else None,
            'ma_90': df['rate'].rolling(window=90).mean().iloc[-1] if len(df) >= 90 else None,
            'ma_365': df['rate'].rolling(window=365).mean().iloc[-1] if len(df) >= 365 else None,
        }
    
    def calculate_volatility(self, db: Session, days=30):
        """Calculate rate volatility over specified period"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        data = self.get_historical_data(db, start_date, end_date)
        rates = [float(r.rate) for r in data]
        
        if len(rates) < 2:
            return None
            
        return np.std(rates)
    
    def get_rate_summary(self, db: Session):
        """Get comprehensive rate statistics"""
        data = self.get_historical_data(db)
        rates = [float(r.rate) for r in data]
        
        if not rates:
            return None
            
        latest = self.get_latest_rate(db)
        moving_avgs = self.calculate_moving_averages(db)
        volatility = self.calculate_volatility(db)
        
        return {
            'latest_rate': float(latest.rate) if latest else None,
            'latest_date': latest.date.isoformat() if latest else None,
            'min_rate': min(rates),
            'max_rate': max(rates),
            'avg_rate': np.mean(rates),
            'volatility_30d': volatility,
            'moving_averages': moving_avgs,
            'total_records': len(rates)
        }
