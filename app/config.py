import os
import logging
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fundratetracker.log'),
        logging.StreamHandler()
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    return logging.getLogger(name)

@dataclass(frozen=True)
class Config:
    # API key from environment file
    ALPHA_VANTAGE_API_KEY: Optional[str] = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    # Database configuration - environment variables take precedence
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fundratetracker")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    
    # Application configuration
    FETCH_INTERVAL: int = 3600
    BATCH_SIZE: int = 1000
    TIMEOUT_SECONDS: int = 30
    MAX_RETRIES: int = 3
    
    # Rate limiting
    API_RATE_LIMIT: int = 5  # requests per minute
    
    def __post_init__(self):
        """Validate that required configuration values are not None."""
        logger = get_logger(__name__)
        
        if self.ALPHA_VANTAGE_API_KEY is None:
            error_msg = "Missing required environment variable: ALPHA_VANTAGE_API_KEY"
            logger.error(error_msg)
            raise EnvironmentError(error_msg)
        
        logger.info("Configuration loaded successfully", extra={
            "fetch_interval": self.FETCH_INTERVAL,
            "batch_size": self.BATCH_SIZE,
            "postgres_host": self.POSTGRES_HOST,
            "postgres_port": self.POSTGRES_PORT,
            "has_api_key": bool(self.ALPHA_VANTAGE_API_KEY)
        })
    

