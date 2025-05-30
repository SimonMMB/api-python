# app/models/__init__.py

# Importar modelos principales
from .user import User, UserRole
from .book import Book, ReadingStatus

# Hacer disponibles para import directo
__all__ = [
    "User",
    "UserRole", 
    "Book",
    "ReadingStatus"
]