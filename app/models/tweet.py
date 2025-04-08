from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field
from enum import Enum

class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class TweetAnalysis(Document):
    query: str
    content: str
    user: str
    sentiment_label: SentimentLabel
    sentiment_score: float = Field(..., ge=-1, le=1)
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "tweet_analysis"