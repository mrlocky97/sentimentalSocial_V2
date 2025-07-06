import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import database and model components conditionally
try:
    from beanie import init_beanie
    from app.models.tweet import TweetAnalysis
    from app.database import connect_db, close_db
    from app.models.user import UserDB
    from app.routes import auth, sentiment_analysis, tweet_scraper
    from pymongo.errors import PyMongoError
    DB_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Database components not available: {e}")
    DB_AVAILABLE = False

app = FastAPI(title="Social Sentiment Analysis API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers only if database components are available
if DB_AVAILABLE:
    app.include_router(auth.router)
    app.include_router(tweet_scraper.router, prefix="/tweets", tags=["tweets"])
    app.include_router(sentiment_analysis.router)
else:
    logging.warning("Database not available - API routes not loaded")

# Root endpoint to serve the HTML interface
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database_available": DB_AVAILABLE,
        "message": "SentimentalSocial V2 API with Menu Interface"
    }

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
    if DB_AVAILABLE:
        try:
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
        except Exception as e:
            logging.error(f"❌ Error conectando a MongoDB: {e}")
    else:
        logging.info("💡 Aplicación iniciada sin conexión a base de datos")

@app.on_event("shutdown")
async def shutdown_db():
    if DB_AVAILABLE:
        await close_db()

if DB_AVAILABLE:
    @app.exception_handler(PyMongoError)
    async def mongo_exception_handler(request: Request, exc: PyMongoError):
        return JSONResponse(
            status_code=500,
            content={"message": "Error de base de datos", "detail": str(exc)}
        )