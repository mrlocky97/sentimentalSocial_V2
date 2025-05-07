from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.tweet import TweetAnalysis, SentimentLabel
from app.models.schemas import TweetInput, SentimentOutput
from app.services.nlp_service import NLPService
# Use config's provider for NLPService
from app.core.config import get_nlp_service
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"]
)

@router.put(
    "/sentiment",
    response_model=List[SentimentOutput],
    status_code=status.HTTP_200_OK,
    summary="Analiza multiples tweets y guarda los resultado en la base de datos"
)
async def analyze_tweet_endpoint(
    tweet: List[TweetInput],
    nlp_service: NLPService = Depends(get_nlp_service),
    current_user=Depends(get_current_user)
):
    results: List[SentimentOutput] = []
    for tweet in tweet:
        # Análisis de sentimiento
        nlp_result = nlp_service.analyze_sentiment(tweet.content)
        label = nlp_result["label"]
        score = nlp_result["score"]

        try:
            # Buscar documento existente
            existing = await TweetAnalysis.find_one({
                "content": tweet.content,
                "user": tweet.user or "anonymous",
                "query": tweet.query or ""
            })

            if existing:
                existing.sentiment_label = SentimentLabel(label)
                existing.sentiment_score = score
                existing.processed = True
                await existing.save()
                doc = existing
            else:
                doc = TweetAnalysis(
                    query=tweet.query or "",
                    content=tweet.content,
                    user=tweet.user or "anonymous",
                    sentiment_label=SentimentLabel(label),
                    sentiment_score=score,
                    processed=True
                )
                await doc.insert()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar tweet '{tweet.content}': {e}"
            )

        # Agregar resultado al array de respuestas
        results.append(SentimentOutput(
            content=doc.content,
            user=doc.user,
            query=doc.query,
            sentiment_label=doc.sentiment_label,
            sentiment_score=doc.sentiment_score
        ))

    return results