from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# ================================
# REQUEST SCHEMAS (Lo que recibe la API)
# ================================

class BookRecommendationRequest(BaseModel):
    """Request para recomendar libros basados en una serie"""
    series_name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Nombre de la serie de TV para buscar similitudes",
        example="Breaking Bad"
    )
    max_books: Optional[int] = Field(
        default=5,
        ge=1,
        le=20,
        description="Número máximo de libros a recomendar",
        example=5
    )
    user_preferences: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Preferencias adicionales del usuario (géneros, autores, temas)",
        example="thriller, suspense, no romance"
    )

class SeriesAnalysisRequest(BaseModel):
    """Request para analizar una serie y extraer temas"""
    series_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre de la serie a analizar",
        example="Game of Thrones"
    )

# ================================
# RESPONSE SCHEMAS (Lo que devuelve la API)
# ================================

class RecommendedBook(BaseModel):
    """Un libro recomendado individual"""
    title: str = Field(..., description="Título del libro")
    author: str = Field(..., description="Autor del libro")
    pages: int = Field(..., description="Número de páginas")
    series_inspiration: str = Field(
        ..., 
        description="Serie que inspiró esta recomendación"
    )
    recommendation_reason: str = Field(
        ..., 
        description="Por qué se recomienda este libro"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Gone Girl",
                "author": "Gillian Flynn", 
                "pages": 432,
                "series_inspiration": "Breaking Bad",
                "recommendation_reason": "Like Breaking Bad, this book explores complex character development and moral ambiguity"
            }
        }

class BookRecommendationResponse(BaseModel):
    """Respuesta completa de recomendación de libros"""
    series_analyzed: str = Field(..., description="Serie que se analizó")
    identified_themes: List[str] = Field(
        ..., 
        description="Temas/géneros identificados en la serie"
    )
    recommendations: List[RecommendedBook] = Field(
        ..., 
        description="Lista de libros recomendados"
    )
    total_found: int = Field(..., description="Total de libros encontrados")
    ai_explanation: str = Field(
        ..., 
        description="Explicación del análisis realizado por la IA"
    )
    user_preferences_considered: str = Field(
        ..., 
        description="Preferencias del usuario que se consideraron"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Momento en que se generó la recomendación"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "series_analyzed": "Breaking Bad",
                "identified_themes": ["crime", "drama", "thriller"],
                "recommendations": [
                    {
                        "title": "Gone Girl",
                        "author": "Gillian Flynn",
                        "pages": 432,
                        "series_inspiration": "Breaking Bad",
                        "recommendation_reason": "Like Breaking Bad, this book explores complex character development and moral ambiguity"
                    }
                ],
                "total_found": 5,
                "ai_explanation": "Based on my analysis of 'Breaking Bad', I identified key themes including crime, drama. These books share similar narrative structures...",
                "user_preferences_considered": "thriller, suspense",
                "timestamp": "2025-05-30T10:30:00"
            }
        }

class SeriesAnalysisResponse(BaseModel):
    """Respuesta del análisis de una serie"""
    series_name: str = Field(..., description="Nombre de la serie analizada")
    identified_themes: List[str] = Field(
        ..., 
        description="Temas principales identificados"
    )
    confidence_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Nivel de confianza del análisis (0-1)"
    )
    analysis_summary: str = Field(
        ..., 
        description="Resumen del análisis realizado"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Momento del análisis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "series_name": "Game of Thrones",
                "identified_themes": ["fantasy", "drama", "political"],
                "confidence_score": 0.92,
                "analysis_summary": "'Game of Thrones' primarily falls into the fantasy genre with elements of drama, political",
                "timestamp": "2025-05-30T10:30:00"
            }
        }

# ================================
# SCHEMAS PARA FUTURAS INTEGRACIONES
# ================================

class SaveRecommendationRequest(BaseModel):
    """Request para guardar una recomendación como libro del usuario"""
    title: str = Field(..., description="Título del libro recomendado")
    author: str = Field(..., description="Autor del libro")
    pages: int = Field(..., description="Páginas del libro")
    series_inspiration: str = Field(
        ..., 
        description="Serie que inspiró la recomendación"
    )
    recommendation_reason: str = Field(
        ..., 
        description="Razón por la cual se recomendó"
    )

class AIUsageStats(BaseModel):
    """Estadísticas de uso de IA (para futuro dashboard)"""
    total_recommendations: int = Field(..., description="Total de recomendaciones hechas")
    most_requested_series: List[str] = Field(..., description="Series más consultadas")
    average_books_per_request: float = Field(..., description="Promedio de libros por consulta")
    user_satisfaction_score: Optional[float] = Field(
        default=None,
        description="Puntuación de satisfacción promedio"
    )