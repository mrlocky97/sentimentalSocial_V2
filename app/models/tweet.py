from enum import Enum
from datetime import datetime
from beanie import Document
from pydantic import Field, BaseModel
from typing import Optional

class TweetStatus(str, Enum):
    PENDING = "pending"
    ANALYZED = "analyzed"

class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class TweetPending(Document):
    content: str
    user: str
    raw_data: dict
    status: TweetStatus = TweetStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "tweets_pending"

class TweetAnalysis(Document):
    original_tweet_id: str 
    content: str
    sentiment_label: SentimentLabel
    sentiment_score: float = Field(..., ge=-1, le=1)
    cleaned_content: str  # Texto procesado
    analyzed_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "tweets_analysis"