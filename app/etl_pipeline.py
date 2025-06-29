import httpx
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db, FederalFundsRate
from config import Config, get_logger
import logging

config = Config()
logger = get_logger(__name__)

class FedRateETL:
    def __init__(self):
        self.api_key = config.ALPHA_VANTAGE_API_KEY
        self.base_url = "https://www.alphavantage.co/query"
        
    async def extract_data(self):
        """Extract Federal Funds Rate data from Alpha Vantage API"""
        try:
            params = {
                "function": "FEDERAL_FUNDS_RATE",
                "interval": "monthly",
                "apikey": self.api_key
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
            if "data" not in data:
                raise ValueError("No data found in API response")
                
            return data["data"]
            
        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            raise

    def transform_data(self, raw_data):
        """Transform raw API data into structured format"""
        try:
            df = pd.DataFrame(raw_data)
            df['date'] = pd.to_datetime(df['date']).dt.date
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df.rename(columns={'value': 'rate'})
            df = df.dropna().sort_values('date')
            
            # Calculate rate changes
            df['rate_change'] = df['rate'].diff()
            
            return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error transforming data: {e}")
            raise

    def load_data(self, transformed_data):
        """Load data into PostgreSQL database"""
        try:
            db = next(get_db())
            
            for record in transformed_data:
                existing = db.query(FederalFundsRate).filter(
                    FederalFundsRate.date == record['date']
                ).first()
                
                if not existing:
                    fed_rate = FederalFundsRate(
                        date=record['date'],
                        rate=record['rate'],
                        rate_change=record.get('rate_change')
                    )
                    db.add(fed_rate)
                    
            db.commit()
            logger.info(f"Successfully loaded {len(transformed_data)} records")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error loading data: {e}")
            raise
        finally:
            db.close()

    async def run_pipeline(self):
        """Execute the complete ETL pipeline"""
        try:
            logger.info("Starting ETL pipeline")
            
            # Extract
            raw_data = await self.extract_data()
            logger.info(f"Extracted {len(raw_data)} records")
            
            # Transform
            transformed_data = self.transform_data(raw_data)
            logger.info(f"Transformed {len(transformed_data)} records")
            
            # Load
            self.load_data(transformed_data)
            logger.info("ETL pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            raise
