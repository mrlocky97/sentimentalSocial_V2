from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from typing import Optional

client: Optional[AsyncIOMotorClient] = None

async def connect_db():
    global client
    client = AsyncIOMotorClient(
        str(settings.MONGODB_URL),
        serverSelectionTimeoutMS=5000
    )
    return client.get_database(settings.MONGODB_NAME)

async def close_db():
    if client:
        await client.close()

def get_db():
    return client.get_database(settings.MONGODB_NAME) if client else None