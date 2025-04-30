from pydantic import BaseModel
from typing import Optional, List
from app.models.tweet import SentimentLabel

class TweetInput(BaseModel):
    content: str
    user: Optional[str] = None
    query: Optional[str] = None

class SentimentOutput(BaseModel):
    content: str
    user: Optional[str]
    query: Optional[str]
    sentiment_label: SentimentLabel
    sentiment_score: float
