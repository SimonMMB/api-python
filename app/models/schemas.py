from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .user import UserRole
from .book import ReadingStatus

# ============ USER SCHEMAS ============

class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole = UserRole.reader

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============ BOOK SCHEMAS ============

class BookBase(BaseModel):
    title: str
    author: str
    pages: Optional[int] = None
    reading_status: ReadingStatus = ReadingStatus.pendiente
    user_comments: Optional[str] = None
    series_inspiration: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    pages: Optional[int] = None
    reading_status: Optional[ReadingStatus] = None
    user_comments: Optional[str] = None
    series_inspiration: Optional[str] = None

class BookResponse(BookBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============ AUTH SCHEMAS ============

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# ============ AI RECOMMENDATION SCHEMAS ============

class AIRecommendationRequest(BaseModel):
    series_liked: List[str]  # Lista de series que le gustaron
    additional_preferences: Optional[str] = None  # Preferencias adicionales

class BookRecommendation(BaseModel):
    title: str
    author: str
    reason: str  # Por qué se recomienda basado en las series
    similarity_explanation: str  # Explicación de similitudes

class AIRecommendationResponse(BaseModel):
    recommendations: List[BookRecommendation]