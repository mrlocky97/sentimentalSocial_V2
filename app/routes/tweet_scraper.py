from fastapi import APIRouter, HTTPException, Depends
from app.services import tweet_scraper
from app.database import get_db
from pymongo.database import Database

router = APIRouter()

"""
Endpoint que recibe un parámetro 'query' (por ejemplo, '#JustDoIt') y opcionalmente 'min_tweets' para indicar el número mínimo de tweets a recolectar.
Realiza el scraping y, opcionalmente, inserta los datos en la colección 'tweets' de MongoDB.
"""
@router.get("/scrape-tweets", summary="Scrapea tweets y almacena los resultados")
async def scrape_tweets_endpoint(query: str, min_tweets: int = 500, db: Database = Depends(get_db)):
    try:
        tweets_data = await tweet_scraper.scrape_tweets(query, min_tweets)
        # Insertar en MongoDB (si se desea almacenar)
        collection = db.get_collection("tweets")
        if tweets_data:
            collection.insert_many(tweets_data)
        return {"status": "success", "data": tweets_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
