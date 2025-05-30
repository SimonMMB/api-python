from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from ..models.book import Book, ReadingStatus
from ..models.schemas import BookCreate, BookUpdate

class BookService:
    
    @staticmethod
    async def create_book(db: AsyncSession, book_data: BookCreate, owner_id: int) -> Book:
        """Crear un nuevo libro"""
        db_book = Book(
            title=book_data.title,
            author=book_data.author,
            pages=book_data.pages,
            series_inspiration=book_data.series_inspiration,
            reading_status=book_data.reading_status or ReadingStatus.PENDIENTE,
            user_comments=book_data.user_comments,
            owner_id=owner_id
        )
        
        db.add(db_book)
        await db.commit()
        await db.refresh(db_book)
        return db_book
    
    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: int) -> Optional[Book]:
        """Obtener libro por ID"""
        result = await db.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_books_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[Book]:
        """Obtener todos los libros de un usuario"""
        result = await db.execute(
            select(Book)
            .where(Book.owner_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_all_books(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Book]:
        """Obtener todos los libros (solo para admins)"""
        result = await db.execute(select(Book).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def get_books_by_status(db: AsyncSession, user_id: int, status: ReadingStatus) -> List[Book]:
        """Obtener libros de un usuario por estado de lectura"""
        result = await db.execute(
            select(Book)
            .where(Book.owner_id == user_id)
            .where(Book.reading_status == status)
        )
        return result.scalars().all()
    
    @staticmethod
    async def search_books_by_title(db: AsyncSession, user_id: int, title_query: str) -> List[Book]:
        """Buscar libros por título (parcial)"""
        result = await db.execute(
            select(Book)
            .where(Book.owner_id == user_id)
            .where(Book.title.ilike(f"%{title_query}%"))
        )
        return result.scalars().all()
    
    @staticmethod
    async def update_book(db: AsyncSession, book_id: int, book_update: BookUpdate, user_id: int) -> Optional[Book]:
        """Actualizar libro (solo el propietario puede actualizarlo)"""
        # Obtener el libro existente
        book = await BookService.get_book_by_id(db, book_id)
        if not book:
            return None
        
        # Verificar que el usuario sea el propietario
        if book.owner_id != user_id:
            return None
        
        # Actualizar solo los campos que no sean None
        update_data = book_update.dict(exclude_unset=True)
        
        # Aplicar las actualizaciones
        for field, value in update_data.items():
            setattr(book, field, value)
        
        await db.commit()
        await db.refresh(book)
        return book
    
    @staticmethod
    async def delete_book(db: AsyncSession, book_id: int, user_id: int) -> bool:
        """Eliminar libro (solo el propietario puede eliminarlo)"""
        book = await BookService.get_book_by_id(db, book_id)
        if not book:
            return False
        
        # Verificar que el usuario sea el propietario
        if book.owner_id != user_id:
            return False
        
        await db.delete(book)
        await db.commit()
        return True
    
    @staticmethod
    async def update_reading_status(db: AsyncSession, book_id: int, new_status: ReadingStatus, user_id: int) -> Optional[Book]:
        """Actualizar solo el estado de lectura de un libro"""
        book = await BookService.get_book_by_id(db, book_id)
        if not book or book.owner_id != user_id:
            return None
        
        book.reading_status = new_status
        await db.commit()
        await db.refresh(book)
        return book
    
    @staticmethod
    async def add_comment(db: AsyncSession, book_id: int, comment: str, user_id: int) -> Optional[Book]:
        """Agregar o actualizar comentario a un libro"""
        book = await BookService.get_book_by_id(db, book_id)
        if not book or book.owner_id != user_id:
            return None
        
        book.user_comments = comment
        await db.commit()
        await db.refresh(book)
        return book