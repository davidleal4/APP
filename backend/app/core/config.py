from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "StudyOS"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/studynos")
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key-here")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # External APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    EMAIL_API_KEY: str = os.getenv("EMAIL_API_KEY", "")
    
    # Plans and limits
    FREE_PLAN_CLASSES_LIMIT: int = 2
    FREE_PLAN_FLASHCARDS_LIMIT: int = 50
    FREE_PLAN_GPA_PREDICTIONS_LIMIT: int = 3
    
    class Config:
        case_sensitive = True

settings = Settings()