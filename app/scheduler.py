import asyncio
import schedule
import time
from etl_pipeline import FedRateETL
from config import Config, get_logger

config = Config()
logger = get_logger(__name__)

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
    interval = config.FETCH_INTERVAL
    schedule.every(interval).seconds.do(lambda: asyncio.run(run_etl_job()))
    
    logger.info(f"ETL job scheduled every {interval} seconds")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_etl()
