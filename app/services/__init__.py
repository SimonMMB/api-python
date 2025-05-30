# app/services/__init__.py

# Importar servicios principales
from .user_service import UserService
from .book_service import BookService
from .ai_service import AIService

# Hacer disponibles para import directo
__all__ = [
    "UserService",
    "BookService",
    "AIService"
]