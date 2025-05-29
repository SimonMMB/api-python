from decouple import config

class Settings:
    # Database
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./book_api.db")
    
    # Security
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-change-this")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    
    # AI Service
    OPENAI_API_KEY: str = config("OPENAI_API_KEY", default="")
    
    # App Info
    APP_NAME: str = "Book AI API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para recomendar libros basados en series de TV usando IA"

settings = Settings()