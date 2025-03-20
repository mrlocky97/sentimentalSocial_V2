from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb+srv://sebastianquemasda:zGe1pBqCAnIirjRc@clustersentimentalsocia.tq9fv.mongodb.net/?retryWrites=true&w=majority&appName=ClusterSentimentalSocial"
    MONGODB_NAME: str = "sentimental_social_db"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'
    )

settings = Settings()