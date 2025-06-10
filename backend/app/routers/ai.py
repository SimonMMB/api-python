from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from ..core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ..schemas.ai_schemas import (
    BookRecommendationRequest,
    BookRecommendationResponse, 
    SeriesAnalysisRequest,
    SeriesAnalysisResponse,
    SaveRecommendationRequest
)
from ..services.ai_service import AIService
from ..services.book_service import BookService
from ..models.user import User
from .auth import get_current_user

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/ai",
    tags=["AI - Book Recommendations"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

@router.post(
    "/recommend-books",
    response_model=BookRecommendationResponse,
    summary="Recomendar libros basados en series",
    description="""
    🎯 **Endpoint principal de la API** 
    
    Recibe el nombre de una serie de TV y devuelve libros recomendados con tramas similares.
    
    **Flujo:**
    1. Analiza la serie ingresada
    2. Identifica temas/géneros principales  
    3. Busca libros similares en la base de datos
    4. Genera explicaciones personalizadas
    
    **Ejemplos de series soportadas:**
    - Breaking Bad, Game of Thrones, Stranger Things
    - The Office, Friends, Sherlock, House of Cards
    - Black Mirror, Westworld, True Detective
    - Narcos, Mindhunter, Dark, Money Heist
    """
)
async def recommend_books(
    request: BookRecommendationRequest,
    current_user: User = Depends(get_current_user)
) -> BookRecommendationResponse:
    """
    Recomienda libros basados en similitudes con series de TV
    """
    try:
        logger.info(f"User {current_user.username} requesting recommendations for: {request.series_name}")
        
        # Llamar al servicio de IA
        ai_result = await AIService.recommend_books_by_series(
            series_name=request.series_name,
            max_books=request.max_books,
            user_preferences=request.user_preferences
        )
        
        # Convertir a response schema
        response = BookRecommendationResponse(**ai_result)
        
        logger.info(f"Generated {response.total_found} recommendations for {current_user.username}")
        return response
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating book recommendations: {str(e)}"
        )

@router.post(
    "/analyze-series",
    response_model=SeriesAnalysisResponse,
    summary="Analizar una serie de TV",
    description="""
    🔍 **Análisis detallado de series**
    
    Analiza una serie específica y extrae sus temas principales, géneros y características.
    
    **Útil para:**
    - Entender qué temas tiene una serie antes de pedir recomendaciones
    - Verificar si una serie está en nuestra base de conocimiento
    - Obtener análisis detallado con puntuación de confianza
    """
)
async def analyze_series(
    request: SeriesAnalysisRequest,
    current_user: User = Depends(get_current_user)
) -> SeriesAnalysisResponse:
    """
    Analiza una serie de TV y extrae temas/géneros principales
    """
    try:
        logger.info(f"User {current_user.username} analyzing series: {request.series_name}")
        
        # Llamar al servicio de análisis
        analysis_result = await AIService.analyze_series(request.series_name)
        
        # Convertir a response schema
        response = SeriesAnalysisResponse(**analysis_result)
        
        logger.info(f"Series analysis completed for {current_user.username}: {response.confidence_score:.2f} confidence")
        return response
        
    except Exception as e:
        logger.error(f"Error analyzing series: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing series: {str(e)}"
        )

@router.post(
    "/save-recommendation",
    summary="Guardar libro recomendado",
    description="""
    💾 **Guardar recomendación en biblioteca personal**
    
    Permite al usuario guardar un libro recomendado por la IA directamente en su biblioteca personal.
    
    **Flujo típico:**
    1. Usuario pide recomendaciones con `/recommend-books`
    2. Revisa las opciones devueltas
    3. Usa este endpoint para guardar los libros que le interesan
    4. El libro se agrega automáticamente con estado "pendiente"
    """
)

async def save_recommendation(
    request: SaveRecommendationRequest,
    current_user: User = Depends(get_current_user),
    book_service: BookService = Depends(),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Guarda un libro recomendado en la biblioteca personal del usuario
    """
    try:
        logger.info(f"User {current_user.username} saving recommendation: {request.title}")
        
        # Crear el libro usando el servicio de libros
        from ..schemas.book_schemas import BookCreate
        from ..models.book import ReadingStatus
        
        book_data = BookCreate(
            title=request.title,
            author=request.author,
            pages=request.pages,
            reading_status=ReadingStatus.PENDIENTE,
            user_comments=f"Recomendado por IA basado en: {request.series_inspiration}. Razón: {request.recommendation_reason}",
            series_inspiration=request.series_inspiration
        )
        
        # Guardar libro en la base de datos
        saved_book = await book_service.create_book(db, book_data, current_user.id)
                                         
        
        logger.info(f"Book saved successfully for user {current_user.username}: {saved_book.id}")
        
        return {
            "message": "Libro guardado exitosamente en tu biblioteca",
            "book_id": saved_book.id,
            "title": saved_book.title,
            "status": saved_book.reading_status.value,
            "added_to_library": True
        }
        
    except Exception as e:
        logger.error(f"Error saving recommendation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving book recommendation: {str(e)}"
        )

@router.get(
    "/supported-series",
    summary="Ver series soportadas",
    description="""
    📺 **Lista de series disponibles**
    
    Devuelve todas las series que están en nuestra base de conocimiento y pueden ser analizadas.
    
    **Útil para:**
    - Mostrar al usuario qué series puede consultar
    - Implementar autocompletado en el frontend
    - Verificar cobertura de la base de datos
    """
)
async def get_supported_series() -> dict:
    """
    Devuelve la lista de series que pueden ser analizadas
    """
    try:
        series_list = list(AIService.SERIES_MAPPING.keys())
        series_count = len(series_list)
        
        # Organizar por popularidad/alfabéticamente
        popular_series = [
            "breaking bad", "game of thrones", "stranger things", 
            "the office", "friends", "sherlock"
        ]
        
        other_series = [s for s in series_list if s not in popular_series]
        other_series.sort()
        
        return {
            "total_series": series_count,
            "popular_series": popular_series,
            "other_series": other_series,
            "all_series": series_list,
            "message": f"Tenemos {series_count} series en nuestra base de conocimiento"
        }
        
    except Exception as e:
        logger.error(f"Error getting supported series: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving supported series list"
        )