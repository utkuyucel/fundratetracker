import os
import logging
from dataclasses import dataclass

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard.log'),
        logging.StreamHandler()
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    return logging.getLogger(name)

@dataclass(frozen=True)
class DashboardConfig:
    # API configuration
    API_BASE_URL: str = os.environ.get("API_BASE_URL", "http://app:8000")
    
    # Dashboard configuration
    HOST: str = "0.0.0.0"
    PORT: int = 5001
    DEBUG: bool = True
    
    # Chart configuration
    DEFAULT_CHART_PERIOD: str = "1year"
    MAX_DATA_POINTS: int = 500
