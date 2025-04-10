import logging
from fastapi import FastAPI
from beanie import init_beanie
import redis

from app.database import connect_db, close_db
from app.models.user import UserDB
from app.routes import auth, tweet_scraper
from dotenv import load_dotenv
from app.core.config import settings

app = FastAPI(title="Social Sentiment Analysis API")

app.include_router(auth.router)
app.include_router(tweet_scraper.router, prefix="/tweets", tags=["tweets"])

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

@app.on_event("startup")
async def startup_db():
    # Conexión async
    db = await connect_db()

    # Conexión a Redis
    app.state.redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    if not app.state.redis.ping():
        raise ConnectionError("No se pudo conectar a Redis")
    logging.info("✅ Conexión a Redis establecida")

    # Inicializar Beanie con modelos
    await init_beanie(
        database=db,
        document_models=[UserDB]
    )
    logging.info("✅ Conexión a MongoDB establecida")

@app.on_event("shutdown")
async def shutdown_db():
    await close_db()
    await app.state.redis.close()