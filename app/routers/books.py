from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from ..core.database import get_db
from ..services import BookService
from ..schemas import BookCreate, BookUpdate, BookResponse, MessageResponse
from ..models import ReadingStatus, UserRole 
from .auth import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear un nuevo libro"""
    book = await BookService.create_book(db, book_data, current_user.id)
    return book

@router.get("/", response_model=List[BookResponse])
async def get_books(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[ReadingStatus] = Query(None, description="Filter by reading status"),
    search: Optional[str] = Query(None, description="Search by title"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener libros del usuario actual"""
    
    if search:
        # Buscar por título
        books = await BookService.search_books_by_title(db, current_user.id, search)
    elif status_filter:
        # Filtrar por estado
        books = await BookService.get_books_by_status(db, current_user.id, status_filter)
    else:
        # Obtener todos los libros del usuario
        books = await BookService.get_books_by_user(db, current_user.id, skip, limit)
    
    return books

@router.get("/all", response_model=List[BookResponse])
async def get_all_books(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener todos los libros de todos los usuarios (solo admins)"""
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required."
        )
    
    books = await BookService.get_all_books(db, skip, limit)
    return books

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener libro por ID"""
    
    book = await BookService.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Verificar permisos: solo el propietario o admin pueden ver el libro
    if current_user.role != UserRole.ADMIN and book.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar libro"""
    
    book = await BookService.update_book(db, book_id, book_update, current_user.id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found or you don't have permission to update it"
        )
    
    return book

@router.delete("/{book_id}", response_model=MessageResponse)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Eliminar libro"""
    
    success = await BookService.delete_book(db, book_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found or you don't have permission to delete it"
        )
    
    return {"message": "Book deleted successfully"}

@router.patch("/{book_id}/status", response_model=BookResponse)
async def update_reading_status(
    book_id: int,
    new_status: ReadingStatus,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar solo el estado de lectura de un libro"""
    
    book = await BookService.update_reading_status(db, book_id, new_status, current_user.id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found or you don't have permission to update it"
        )
    
    return book

@router.patch("/{book_id}/comment", response_model=BookResponse)
async def add_comment(
    book_id: int,
    comment: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Agregar o actualizar comentario de un libro"""
    
    book = await BookService.add_comment(db, book_id, comment, current_user.id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found or you don't have permission to update it"
        )
    
    return book