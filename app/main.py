from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, users, books
from .core.config import settings

# Crear la aplicación FastAPI
app = FastAPI(
    title="SIMON Book API",
    description="API para recomendaciones de libros basadas en series de TV usando IA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Welcome to Book Recommendation API", 
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}