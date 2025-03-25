from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

# Cargar las variables del fichero .env
load_dotenv()

class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv('MONGODB_URL')
    MONGODB_NAME: str = os.getenv('MONGODB_NAME')

    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'
    )

settings = Settings()