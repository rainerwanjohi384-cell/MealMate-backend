from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    database_url: str = "sqlite:///./mealmate.db"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    firebase_credentials_path: str = "./firebase-credentials.json"
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    class Config:
        env_file = ".env"


settings = Settings()
