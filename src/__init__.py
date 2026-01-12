import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_ROOT = Path(__file__).parent.parent
    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    ADVICE_API_URL = "https://api.adviceslip.com/advice"
    BORED_API_URL = "https://www.boredapi.com/api/activity"
    DOG_API_URL = "https://dog.ceo/api/breeds/image/random"

    @staticmethod
    def get_db_connection_string():
        return f"host={Config.DB_HOST} port={Config.DB_PORT} dbname={Config.DB_NAME} user={Config.DB_USER} password={Config.DB_PASSWORD}"

    @staticmethod
    def validate():
        required_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        for var in required_vars:
            if not os.getenv(var) and var not in ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]:
                raise ValueError(f"Missing required environment variable: {var}")
