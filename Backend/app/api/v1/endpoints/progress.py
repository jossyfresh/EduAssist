from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_progress
from app.models.user import User
from app.schemas.progress import (
    Progress,
    ProgressCreate,
    ProgressUpdate,
    Achievement,
    ProgressAnalytics
)

router = APIRouter()

@router.post("/record", response_model=Progress)
def record_progress(
    *,
    db: Session = Depends(deps.get_db),
    progress_in: ProgressCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Record progress for a learning path step.
    """
    progress = crud_progress.create(
        db=db, obj_in=progress_in, user_id=current_user.id
    )
    return progress

@router.get("/user/{user_id}", response_model=List[Progress])
def read_user_progress(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all progress records for a user.
    """
    if user_id != current_user.id and not crud_progress.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    progress = crud_progress.get_multi_by_user(db=db, user_id=user_id)
    return progress

@router.get("/learning-path/{learning_path_id}", response_model=List[Progress])
def read_learning_path_progress(
    *,
    db: Session = Depends(deps.get_db),
    learning_path_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get progress for a specific learning path.
    """
    progress = crud_progress.get_multi_by_learning_path(
        db=db, learning_path_id=learning_path_id, user_id=current_user.id
    )
    return progress

@router.get("/achievements", response_model=List[Achievement])
def read_achievements(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user achievements.
    """
    achievements = crud_progress.get_achievements(db=db, user_id=current_user.id)
    return achievements

@router.get("/analytics", response_model=ProgressAnalytics)
def get_progress_analytics(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get progress analytics for the user.
    """
    analytics = crud_progress.get_analytics(db=db, user_id=current_user.id)
    return analytics 