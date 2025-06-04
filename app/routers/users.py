from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from typing import Union

from ..core.database import get_db
from ..services import UserService
from ..schemas import UserResponse, UserUpdate, AdminUserUpdate, UserWithBooks, MessageResponse
from ..models import UserRole
from .auth import get_current_user

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

@router.get("/{user_id}", response_model=UserResponse)
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
    user_update: dict,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualizar usuario"""
    # Verificar permisos básicos
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Validar según el role del usuario actual
    if current_user.role == UserRole.ADMIN:
        # Admin puede usar todos los campos
        validated_update = AdminUserUpdate(**user_update)
    else:
        # Usuario normal: verificar que no incluya 'role'
        if 'role' in user_update:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot change user role. Admin privileges required."
            )
        validated_update = UserUpdate(**user_update)
    
    user = await UserService.update_user(db, user_id, validated_update)
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
    current_user = Depends(get_current_user)  # ← Cambio aquí
):
    """Eliminar usuario"""
    
    # LÓGICA DE PERMISOS:
    # - Admins pueden eliminar cualquier usuario (excepto a sí mismos)
    # - Readers solo pueden eliminarse a sí mismos
    
    if current_user.role == UserRole.ADMIN:
        # Admin no puede eliminarse a sí mismo
        if current_user.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admins cannot delete their own account"
            )
    else:
        # Reader solo puede eliminarse a sí mismo
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own account"
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