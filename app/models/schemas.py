from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .user import UserRole
from .book import ReadingStatus

# === ESQUEMAS DE USUARIO ===

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.READER

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserWithBooks(UserResponse):
    books: List['BookResponse'] = []

# === ESQUEMAS DE LIBRO ===

class BookBase(BaseModel):
    title: str
    author: str
    pages: Optional[int] = None
    series_inspiration: Optional[str] = None

class BookCreate(BookBase):
    reading_status: Optional[ReadingStatus] = ReadingStatus.PENDIENTE
    user_comments: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    pages: Optional[int] = None
    series_inspiration: Optional[str] = None
    reading_status: Optional[ReadingStatus] = None
    user_comments: Optional[str] = None

class BookResponse(BookBase):
    id: int
    reading_status: ReadingStatus
    user_comments: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BookWithOwner(BookResponse):
    owner: UserResponse

# === ESQUEMAS DE AUTENTICACIÓN ===

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# === ESQUEMAS DE RESPUESTA GENERAL ===

class MessageResponse(BaseModel):
    message: str

# Solucionar referencias circulares
UserWithBooks.model_rebuild()