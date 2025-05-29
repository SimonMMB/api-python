from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base

class ReadingStatus(enum.Enum):
    PENDIENTE = "pendiente"
    EMPEZADO = "empezado"
    ACABADO = "acabado"

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False)
    pages = Column(Integer, nullable=True)
    reading_status = Column(Enum(ReadingStatus), default=ReadingStatus.PENDIENTE, nullable=False)
    user_comments = Column(Text, nullable=True)
    series_inspiration = Column(Text, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Key hacia User
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relación con usuario (muchos libros pertenecen a un usuario)
    owner = relationship("User", back_populates="books")