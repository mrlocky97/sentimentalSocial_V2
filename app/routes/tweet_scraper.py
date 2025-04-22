from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from pymongo.errors import PyMongoError

from app.models.tweet import PaginatedResponse, TweetAnalysis
from app.core.dependencies import get_current_user
from app.services import tweet_scraper
from app.database import get_db

router = APIRouter()

@router.get("/scrape-tweets", summary="Scrapea tweets y almacena los resultados")
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
    
@router.get("/search", response_model=PaginatedResponse)
async def search_tweets(
    query: str,
    page: int = 1,
    limit: int = 100,
    db: Database = Depends(get_db),
    _: str = Depends(get_current_user)
):
    try:
        skip = (page - 1) * limit
        total = await TweetAnalysis.find({"query": query}).count()
        
        items = await TweetAnalysis.find({"query": query})\
            .skip(skip)\
            .limit(limit)\
            .to_list()
            
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "items": items
        }
    except PyMongoError as e:
        raise HTTPException(500, detail=f"Database error: {str(e)}")