import random
from typing import List, Dict, Any
import asyncio

class AIService:
    """Servicio de IA simulado para recomendaciones de libros"""
    
    # Base de datos simulada de libros por género/tema
    BOOKS_DATABASE = {
        "thriller": [
            {"title": "Gone Girl", "author": "Gillian Flynn", "pages": 432},
            {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "pages": 672},
            {"title": "In the Woods", "author": "Tana French", "pages": 429},
            {"title": "Big Little Lies", "author": "Liane Moriarty", "pages": 460},
        ],
        "drama": [
            {"title": "The Seven Husbands of Evelyn Hugo", "author": "Taylor Jenkins Reid", "pages": 400},
            {"title": "Little Fires Everywhere", "author": "Celeste Ng", "pages": 338},
            {"title": "The Silent Patient", "author": "Alex Michaelides", "pages": 336},
            {"title": "Where the Crawdads Sing", "author": "Delia Owens", "pages": 384},
        ],
        "crime": [
            {"title": "The Thursday Murder Club", "author": "Richard Osman", "pages": 368},
            {"title": "Tana French", "author": "The Likeness", "pages": 466},
            {"title": "Louise Penny", "author": "Still Life", "pages": 312},
            {"title": "The Poet", "author": "Michael Connelly", "pages": 512},
        ],
        "psychological": [
            {"title": "Sharp Objects", "author": "Gillian Flynn", "pages": 254},
            {"title": "The Woman in the Window", "author": "A.J. Finn", "pages": 448},
            {"title": "Behind Closed Doors", "author": "B.A. Paris", "pages": 336},
            {"title": "The Guest List", "author": "Lucy Foley", "pages": 320},
        ],
        "mystery": [
            {"title": "The 7½ Deaths of Evelyn Hardcastle", "author": "Stuart Turton", "pages": 448},
            {"title": "The Sanatorium", "author": "Sarah Pearse", "pages": 384},
            {"title": "The Hunting Party", "author": "Lucy Foley", "pages": 352},
            {"title": "The Turn of the Key", "author": "Ruth Ware", "pages": 352},
        ]
    }
    
    # Mapeo de series populares a géneros/temas
    SERIES_MAPPING = {
        "breaking bad": ["crime", "drama", "thriller"],
        "game of thrones": ["fantasy", "drama", "political"],
        "stranger things": ["mystery", "thriller", "supernatural"],
        "the office": ["comedy", "workplace", "light"],
        "friends": ["comedy", "romance", "light"],
        "sherlock": ["mystery", "crime", "detective"],
        "house of cards": ["political", "drama", "thriller"],
        "black mirror": ["dystopian", "psychological", "sci-fi"],
        "westworld": ["sci-fi", "philosophical", "thriller"],
        "true detective": ["crime", "mystery", "psychological"],
        "the crown": ["historical", "drama", "biography"],
        "narcos": ["crime", "drama", "biographical"],
        "mindhunter": ["crime", "psychological", "thriller"],
        "dark": ["mystery", "sci-fi", "psychological"],
        "the witcher": ["fantasy", "adventure", "drama"],
        "money heist": ["crime", "thriller", "drama"],
        "squid game": ["thriller", "drama", "psychological"],
        "ozark": ["crime", "drama", "thriller"],
        "dexter": ["crime", "psychological", "thriller"],
        "homeland": ["thriller", "political", "drama"]
    }
    
    @staticmethod
    async def recommend_books_by_series(
        series_name: str, 
        max_books: int = 5, 
        user_preferences: str = None
    ) -> Dict[str, Any]:
        """
        Simula recomendaciones de IA basadas en similitudes con series de TV
        
        Args:
            series_name: Nombre de la serie de TV
            max_books: Número máximo de libros a recomendar
            user_preferences: Preferencias adicionales del usuario
            
        Returns:
            Dict con recomendaciones y explicación
        """
        
        # Simular tiempo de procesamiento de IA
        await asyncio.sleep(0.5)
        
        # Normalizar nombre de serie
        series_key = series_name.lower().strip()
        
        # Buscar géneros asociados a la serie
        genres = AIService.SERIES_MAPPING.get(series_key, ["mystery", "drama"])
        
        # Seleccionar libros de los géneros relevantes
        recommended_books = []
        for genre in genres[:2]:  # Máximo 2 géneros
            if genre in AIService.BOOKS_DATABASE:
                books = AIService.BOOKS_DATABASE[genre]
                # Seleccionar libros aleatoriamente
                selected = random.sample(books, min(2, len(books)))
                recommended_books.extend(selected)
        
        # Limitar al número máximo solicitado
        if len(recommended_books) > max_books:
            recommended_books = random.sample(recommended_books, max_books)
        
        # Agregar razones simuladas
        for book in recommended_books:
            book["recommendation_reason"] = AIService._generate_reason(series_name, book["title"])
        
        return {
            "series_analyzed": series_name,
            "identified_themes": genres[:2],
            "recommendations": recommended_books,
            "total_found": len(recommended_books),
            "ai_explanation": AIService._generate_explanation(series_name, genres[:2]),
            "user_preferences_considered": user_preferences or "None specified"
        }
    
    @staticmethod
    def _generate_reason(series_name: str, book_title: str) -> str:
        """Genera una razón simulada para la recomendación"""
        reasons = [
            f"Like {series_name}, this book explores complex character development and moral ambiguity",
            f"Shares the psychological tension and narrative style similar to {series_name}",
            f"Features the same dark atmosphere and intricate plotting as {series_name}",
            f"Explores similar themes of power, corruption, and human nature as {series_name}",
            f"Has the same compelling character-driven narrative that made {series_name} captivating"
        ]
        return random.choice(reasons)
    
    @staticmethod
    def _generate_explanation(series_name: str, themes: List[str]) -> str:
        """Genera una explicación simulada del análisis de IA"""
        themes_str = ", ".join(themes)
        return f"Based on my analysis of '{series_name}', I identified key themes including {themes_str}. These books share similar narrative structures, character complexity, and thematic elements that should appeal to fans of the series."
    
    @staticmethod
    async def analyze_series(series_name: str) -> Dict[str, Any]:
        """
        Analiza una serie y extrae temas/géneros (simulado)
        
        Args:
            series_name: Nombre de la serie
            
        Returns:
            Análisis de la serie
        """
        await asyncio.sleep(0.3)
        
        series_key = series_name.lower().strip()
        themes = AIService.SERIES_MAPPING.get(series_key, ["drama", "mystery"])
        
        return {
            "series_name": series_name,
            "identified_themes": themes,
            "confidence_score": random.uniform(0.7, 0.95),
            "analysis_summary": f"'{series_name}' primarily falls into the {themes[0]} genre with elements of {', '.join(themes[1:])}"
        }