from fastapi import APIRouter, HTTPException, Depends
from typing import List
from beanie import PydanticObjectId
from app.models.tweet import TweetPending, TweetAnalysis, TweetStatus, SentimentLabel
from app.services.nlp_service import NLPService
from app.services.tweet_scraper import scrape_tweets

# Añadir estas rutas al router existente
router = APIRouter()

@router.post("/scrape-and-save/", tags=["tweets"])
async def scrape_and_save_tweets(query: str,   count_tweets: int, ):
    try:
        # Ejecutar el scraper existente
        raw_tweets = await scrape_tweets(query, count_tweets)
        
        # Guardar tweets en estado "pending"
        saved_tweets = []
        for tweet in raw_tweets:
            new_tweet = TweetPending(
                content=tweet["text"],
                user=tweet["user"],
                raw_data=tweet,
            )
            await new_tweet.insert()
            saved_tweets.append(new_tweet)
        
        return {"message": f"{len(saved_tweets)} tweets guardados para análisis"}
    
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/analyze-sentiment/", tags=["tweets"], response_model=List[TweetAnalysis])
async def analyze_tweets(tweet_ids: List[PydanticObjectId]):
    nlp_service = NLPService()
    analyzed_tweets = []
    
    for tweet_id in tweet_ids:
        # Obtener tweet pendiente
        tweet = await TweetPending.get(tweet_id)
        if not tweet:
            continue
        
        # Procesar texto (limpieza básica)
        cleaned_content = tweet.content.strip().lower()
        
        # Analizar sentimiento
        analysis = nlp_service.analyze_sentiment(cleaned_content)
        
        # Crear registro de análisis
        analyzed_tweet = TweetAnalysis(
            original_tweet_id=str(tweet.id),
            content=tweet.content,
            cleaned_content=cleaned_content,
            sentiment_label=SentimentLabel(analysis["label"]),
            sentiment_score=analysis["score"]
        )
        await analyzed_tweet.insert()
        
        # Actualizar estado del tweet original
        tweet.status = TweetStatus.ANALYZED
        await tweet.save()
        
        analyzed_tweets.append(analyzed_tweet)
    
    return analyzed_tweets

@router.get("/analyzed-tweets/", tags=["tweets"], response_model=List[TweetAnalysis])
async def get_analyzed_tweets():
    return await TweetAnalysis.find_all().to_list()