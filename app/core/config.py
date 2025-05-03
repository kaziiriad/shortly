import os
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database settings
    DB_URL: str = os.getenv("DB_URL", "mongodb://mongo:27017")
    DB_NAME: str = os.getenv("DB_NAME", "mydatabase")
    
    # Application settings
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT.lower() == "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def dict_config(self) -> Dict[str, Any]:
        """Return configuration as a dictionary for logging purposes."""
        return {
            "DB_URL": self.DB_URL.replace("://", "://**:**@") if "://" in self.DB_URL else self.DB_URL,  # Hide credentials
            "DB_NAME": self.DB_NAME,
            "BASE_URL": self.BASE_URL,
            "ENVIRONMENT": self.ENVIRONMENT,
            "DEBUG": self.DEBUG
        }

# Create settings instance
try:
    settings = Settings()
    # Log configuration (hiding sensitive information)
    logger.info(f"Configuration loaded: {settings.dict_config()}")
except Exception as e:
    logger.error(f"Failed to load configuration: {str(e)}")
    raise
