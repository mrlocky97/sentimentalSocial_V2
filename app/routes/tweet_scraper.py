from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from pymongo.errors import PyMongoError
from typing import List

from app.models.tweet import PaginatedResponse, TweetAnalysis, SentimentLabel
from app.core.dependencies import get_current_user
from app.services import tweet_scraper
from app.database import get_db

router = APIRouter()

@router.post("/scrape-tweets", summary="Scrapea tweets y almacena los resultados")
async def scrape_tweets_endpoint(
    query: str,
    min_tweets: int = 500,
    db: Database = Depends(get_db),
    _: str = Depends(get_current_user)
    ):
    try:
        tweets_data = await tweet_scraper.scrape_tweets(query, min_tweets)
        return tweets_data  # Devuelve lista completa con análisis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get(
    "/unprocessed",
    summary="Obtiene tweets pendientes de análisis",
    response_model=List[TweetAnalysis]
)
async def get_unprocessed_tweets(
    db: Database = Depends(get_db),
    _: str = Depends(get_current_user)
):
    try:
        tweets = await TweetAnalysis.find({"processed": False}).to_list()
        return tweets
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
