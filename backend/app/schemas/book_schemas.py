from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.book import ReadingStatus

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
    owner: 'UserResponse'

# Forward reference
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user_schemas import UserResponse