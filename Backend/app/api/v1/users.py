from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api import deps
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.crud import crud_user
from typing import List
import uuid

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserSchema])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
    skip: int = 0,
    limit: int = 100
):
    """Get all users. Only accessible by superusers."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/me", response_model=UserSchema)
def get_current_user(
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get current user information."""
    return current_user

@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Update current user information."""
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get a specific user by ID. Users can only access their own profile unless they are superusers."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user

@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """Delete a user. Only accessible by superusers."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return user 