import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from typing import Optional

client: Optional[AsyncIOMotorClient] = None

async def connect_db():
    global client
    try:
        client = AsyncIOMotorClient(
            str(settings.MONGODB_URL),
            serverSelectionTimeoutMS=5000
        )
        # Verifica que la conexión sea válida
        await client.server_info()
        return client.get_database(settings.MONGODB_NAME)
    except Exception as e:
        logging.error(f"Error de conexión a MongoDB: {str(e)}")
        raise

async def close_db():
    global client
    if client:
        client.close()
        client = None   

def get_db():
    return client.get_database(settings.MONGODB_NAME) if client else None