# app/schemas/__init__.py

# Importar todos los schemas para que estén disponibles
from .user_schemas import (
    UserBase,
    UserCreate, 
    UserUpdate,
    AdminUserUpdate,
    UserResponse,
    UserWithBooks,
    LoginRequest,
    Token,
    TokenData,
    MessageResponse
)

from .book_schemas import (
    BookBase,
    BookCreate,
    BookUpdate, 
    BookResponse,
    BookWithOwner
)

from .ai_schemas import (
    BookRecommendationRequest,
    SeriesAnalysisRequest,
    RecommendedBook,
    BookRecommendationResponse,
    SeriesAnalysisResponse,
    SaveRecommendationRequest,
    AIUsageStats
)

# Resolver referencias circulares
UserWithBooks.model_rebuild()
BookWithOwner.model_rebuild()