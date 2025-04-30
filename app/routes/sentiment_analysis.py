from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.models.schemas import TweetInput, SentimentOutput
from app.services.nlp_service import NLPService
from app.models.tweet import TweetAnalysis
from app.core.dependencies import get_current_user, get_nlp_service
from pymongo.errors import PyMongoError

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"]
)

@router.post(
    "/sentiment",
    response_model=List[SentimentOutput],
    summary="Analiza sentimientos de un lote de tweets"
)
async def analyze_tweets_endpoint(
    tweets: List[TweetInput],
    nlp_service: NLPService = Depends(get_nlp_service),
    _: str = Depends(get_current_user)
):
    resultados = []
    for t in tweets:
        # Llamada al pipeline de Transformers
        res = nlp_service.analyze_sentiment(t.content)
        label = res["label"]
        score = res["score"]

        # Guardar en MongoDB
        try:
            doc = TweetAnalysis(
                query   = t.query or "",
                content = t.content,
                user    = t.user or "anonymous",
                sentiment_label = label,
                sentiment_score = score,
                processed = True
            )
            await doc.insert()
        except PyMongoError as e:
            # Si falla guardar, continuamos pero lo señalamos
            raise HTTPException(status_code=500, detail=f"Error DB: {e}")

        resultados.append(SentimentOutput(
            content         = t.content,
            user            = t.user,
            query           = t.query,
            sentiment_label = label,
            sentiment_score = score
        ))

    return resultados
