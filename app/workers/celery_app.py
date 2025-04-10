from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.celery_app"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"]
)

@celery_app.task(name="process_tweet_analysis")
def process_tweet_analysis(query: str, min_tweets: int):
    """
    Esta tarea realiza:
      - Scraping de tweets basado en el query y cantidad mínima solicitada.
      - Analiza el sentimiento de cada tweet.
      - Guarda los resultados en la colección 'tweet_analysis' de MongoDB.
    """
    import asyncio
    from app.services.tweet_scraper import scrape_tweets  # Función asíncrona para obtener tweets.
    from app.services.nlp_service import NLPService     # Servicio para análisis de sentimientos.
    from app.database import get_db
    # Ejecutamos la función asíncrona en forma síncrona para la tarea.
    tweets_data = asyncio.run(scrape_tweets(query, min_tweets))
    
    nlp = NLPService()
    results = []
    
    for tweet in tweets_data:
        # Aplicamos el análisis de sentimientos usando el NLPService.
        sentiment = nlp.analyze_sentiment(tweet["text"])
        tweet_result = {
            "query": query,
            "content": tweet["text"],
            "user": tweet["user"],
            "sentiment_label": sentiment["label"],
            "sentiment_score": sentiment["score"]
        }
        results.append(tweet_result)
    
    # Insertamos los resultados en la colección 'tweet_analysis' de MongoDB.
    db = get_db()
    collection = db.get_collection("tweet_analysis")
    if results:
        collection.insert_many(results)
    
    return results