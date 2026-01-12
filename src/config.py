"""
Configuration module for ETL pipeline.
Loads environment variables and provides centralized configuration.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class for database and logging settings."""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'etl_pipeline')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # API Endpoints
    ADVICE_API_URL = 'https://api.adviceslip.com/advice'
    QUOTABLE_API_URL = 'https://zenquotes.io/api/random'
    DOG_API_URL = 'https://dog.ceo/api/breeds/image/random'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = Path(__file__).parent.parent / 'logs'
    
    # Pipeline Configuration
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    
    @classmethod
    def get_db_connection_string(cls):
        """Generate PostgreSQL connection string."""
        return f"host={cls.DB_HOST} port={cls.DB_PORT} dbname={cls.DB_NAME} user={cls.DB_USER} password={cls.DB_PASSWORD}"
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        required = ['DB_HOST', 'DB_NAME', 'DB_USER']
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        # Create logs directory if it doesn't exist
        cls.LOG_DIR.mkdir(exist_ok=True)
        
        return True