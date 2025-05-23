import asyncio
import schedule
import time
import os
from etl_pipeline import FedRateETL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_etl_job():
    """Run the ETL pipeline"""
    etl = FedRateETL()
    try:
        await etl.run_pipeline()
        logger.info("Scheduled ETL job completed successfully")
    except Exception as e:
        logger.error(f"Scheduled ETL job failed: {e}")

def schedule_etl():
    """Schedule ETL job"""
    interval = int(os.getenv("FETCH_INTERVAL", 3600))  # Default 1 hour
    schedule.every(interval).seconds.do(lambda: asyncio.run(run_etl_job()))
    
    logger.info(f"ETL job scheduled every {interval} seconds")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_etl()
