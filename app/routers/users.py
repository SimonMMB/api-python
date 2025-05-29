from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..core.database import get_db
from ..services.user_service import UserService
from ..models.schemas import UserResponse, UserUpdate, UserWithBooks, MessageResponse
from ..models.user import UserRole
from ..routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

def require_admin(current_user = Depends(get_current_user)):
    """Verificar que el usuario sea admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required."
        )
    return current_user

@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    admin_user = Depends(require_admin)
):
    """Obtener todos los usuarios (solo admins)"""
    users = await UserService.get_all_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserWithBooks)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener usuario por ID"""
    
    # Los usuarios solo pueden ver su propia información, los admins pueden ver cualquiera
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar usuario"""
    
    # Los usuarios solo pueden actualizar su propia información, los admins pueden actualizar cualquiera
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Si no es admin, no puede cambiar el rol
    if current_user.role != UserRole.ADMIN and user_update.role is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot change user role. Admin privileges required."
        )
    
    user = await UserService.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin_user = Depends(require_admin)
):
    """Eliminar usuario (solo admins)"""
    
    # No permitir que los admins se eliminen a sí mismos
    if admin_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    success = await UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}

@router.get("/{user_id}/books", response_model=List[dict])
async def get_user_books(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener libros de un usuario específico"""
    
    # Los usuarios solo pueden ver sus propios libros, los admins pueden ver cualquiera
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Verificar que el usuario existe
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Importar aquí para evitar circular imports
    from ..services.book_service import BookService
    books = await BookService.get_books_by_user(db, user_id)
    return books