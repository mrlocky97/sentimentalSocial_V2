import logging
from fastapi import FastAPI
from beanie import init_beanie

from app.database import connect_db, close_db
from app.models.user import UserDB
from app.routes import auth, tweet_scraper
from dotenv import load_dotenv
load_dotenv() # Cargar variables de entorno desde el archivo .env
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
    try:
        # Conexión async
        db = await connect_db()

        # Inicializar Beanie con modelos
        await init_beanie(
            database=db,
            document_models=[UserDB]
        )
        logging.info("✅ Conexión a MongoDB establecida")
    except Exception as e:
        logging.error(f"❌ Error al conectar a MongoDB: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_db():
    await close_db()