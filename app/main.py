import logging
from fastapi import FastAPI
from beanie import init_beanie
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.models.tweet import TweetAnalysis
from app.database import connect_db, close_db
from app.models.user import UserDB
from app.routes import auth, tweet_scraper
from dotenv import load_dotenv
from app.core.config import settings
from pymongo.errors import PyMongoError

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
    
    # Inicializar Beanie con modelos
    await init_beanie(
        database=db,
        document_models=[
            UserDB, 
            TweetAnalysis
        ]
    )

    logging.info("✅ Conexión a MongoDB establecida")

@app.on_event("shutdown")
async def shutdown_db():
    await close_db()

@app.exception_handler(PyMongoError)
async def mongo_exception_handler(request: Request, exc: PyMongoError):
    return JSONResponse(
        status_code=500,
        content={"message": "Error de base de datos", "detail": str(exc)}
    )