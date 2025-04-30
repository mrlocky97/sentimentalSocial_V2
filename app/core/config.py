from pydantic_settings import BaseSettings, SettingsConfigDict
from app.services.nlp_service import NLPService

class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )

settings = Settings()

def get_nlp_service() -> NLPService:
    return NLPService()