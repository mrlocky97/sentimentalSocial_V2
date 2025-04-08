from fastapi import APIRouter, HTTPException, Depends
from app.core.dependencies import get_current_user
from app.services import tweet_scraper
from app.database import get_db
from pymongo.database import Database

from app.workers.celery_app import process_tweet_analysis

router = APIRouter()

"""
Este endpoint protege la operación y solo permite acceso a usuarios autenticados.
Llama a la tarea de Celery para procesar de forma asíncrona:
    - Scraping de tweets.
    - Análisis de sentimientos.
    - Inserción en MongoDB.
Retorna el task_id para consultar el estado del proceso.
"""
@router.get("/scrape-tweets", summary="Scrapea tweets y almacena los resultados")
async def scrape_tweets_endpoint(
    query: str, 
    min_tweets: int = 500, 
    db: Database = Depends(get_db),
    _: str = Depends(get_current_user) # Dependencia para obtener el usuario autenticado, ignora el valor pero ejecuta la validacion
    ):
    try:
        # Desencadena la tarea asíncrona con Celery
        task = process_tweet_analysis.delay(query, min_tweets)
        return {"status": "processing", "task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
