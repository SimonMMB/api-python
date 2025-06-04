from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from ..models.user import UserRole

# === ESQUEMAS DE USUARIO ===

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.READER
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "secretpassword",
                "role": "reader"
            }
        }

class AdminUserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserWithBooks(UserResponse):
    books: List['BookResponse'] = []

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

# Forward reference que se resolverá después
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .book_schemas import BookResponse