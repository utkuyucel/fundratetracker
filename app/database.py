from sqlalchemy import create_engine, Column, Integer, Date, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import Config

config = Config()

DATABASE_URL = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FederalFundsRate(Base):
    __tablename__ = "federal_funds_rates"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    rate = Column(Numeric(5, 2), nullable=False)
    rate_change = Column(Numeric(5, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RateAnalytics(Base):
    __tablename__ = "rate_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_date = Column(Date, nullable=False, index=True)
    avg_30_day = Column(Numeric(5, 2))
    avg_90_day = Column(Numeric(5, 2))
    avg_365_day = Column(Numeric(5, 2))
    volatility_30_day = Column(Numeric(8, 4))
    min_rate_ytd = Column(Numeric(5, 2))
    max_rate_ytd = Column(Numeric(5, 2))
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
