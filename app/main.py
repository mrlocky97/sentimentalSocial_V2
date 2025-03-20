from fastapi import FastAPI
from beanie import init_beanie
from app.database import connect_db, close_db
from app.models.user import UserDB
from app.routes import auth

app = FastAPI(title="Social Sentiment Analysis API")

app.include_router(auth.router)

@app.on_event("startup")
async def startup_db():
    # Conexión async
    db = await connect_db()
    
    # Inicializar Beanie con modelos
    await init_beanie(
        database=db,
        document_models=[UserDB]
    )
    
    # Crear índices (usando Motor directamente)
    # await db.users.create_index("email", unique=True)
    print("✅ Base de datos inicializada")

@app.on_event("shutdown")
async def shutdown_db():
    await close_db()