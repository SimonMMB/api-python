# app/routers/__init__.py
# Importar routers
from . import auth
from . import users
from . import books
from . import ai  # ← Agregar router de IA

# Hacer disponibles para import directo
__all__ = [
    "auth",
    "users",
    "books",
    "ai"  # ← Agregar a exports
]