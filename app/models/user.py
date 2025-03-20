from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from pymongo import IndexModel

class UserDB(Document):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password_hash: str
    is_active: bool = True
    email_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None

    class Settings:
        name = "users"
        use_state_management = True
        indexes = [
            IndexModel([("email", 1)], unique=True),  # Índice único en email
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "Str0ngP@ss!",
                "is_active": True,
                "email_verified": False
            }
        }

class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    is_active: bool
    email_verified: bool