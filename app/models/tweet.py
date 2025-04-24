from datetime import datetime
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from enum import Enum
from pymongo import IndexModel, DESCENDING

class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class TweetAnalysis(Document):
    query: str
    content: str
    user: str
    sentiment_label: SentimentLabel
    sentiment_score: float = Field(..., ge=-1, le=1) ## Score entre -1 y 1
    processed: bool = Field(default=False)      
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "tweet_analysis"
        indexes = [
            IndexModel([("query", DESCENDING)]),
            IndexModel([("sentiment_label", DESCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
            IndexModel([("content", "text")], weights={"content": 10})
        ]

class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[TweetAnalysis]