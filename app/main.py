import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from beanie import init_beanie

from app.models.tweet import TweetAnalysis
from app.database import connect_db, close_db
from app.models.user import UserDB
from app.routes import auth, sentiment_analysis, tweet_scraper
from pymongo.errors import PyMongoError

app = FastAPI(title="Social Sentiment Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tweet_scraper.router, prefix="/tweets", tags=["tweets"])
app.include_router(sentiment_analysis.router)

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