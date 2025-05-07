from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from app.models.tweet import SentimentLabel
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    role: UserRole
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):  
    message: str
    user: UserBase

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
