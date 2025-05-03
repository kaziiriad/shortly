from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


load_dotenv()

class Settings(BaseSettings):

    DB_URL: str = os.getenv("DB_URL", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "mydatabase")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")


settings = Settings()