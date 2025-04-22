from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from typing import Optional

from app.models.tweet import TweetAnalysis

client: Optional[AsyncIOMotorClient] = None

async def connect_db():
    global client
    client = AsyncIOMotorClient(
        str(settings.MONGODB_URL),
        serverSelectionTimeoutMS=5000
    )
    return client.get_database(settings.MONGODB_NAME)

async def close_db():
    global client
    if client:
        client.close()
        client = None   

def get_db():
    return client.get_database(settings.MONGODB_NAME) if client else None

async def create_indexes():
    pass