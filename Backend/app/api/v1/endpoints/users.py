from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_user
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter()

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud_user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user

@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a user.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    user = crud_user.remove(db, id=user_id)
    return user 