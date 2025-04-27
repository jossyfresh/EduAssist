from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud import learning_path as crud
from app.schemas.learning_path import LearningPath, LearningPathCreate, LearningPathUpdate

router = APIRouter()

@router.post("/", response_model=LearningPath)
def create_learning_path(
    *,
    db: Session = Depends(deps.get_db),
    learning_path_in: LearningPathCreate,
    current_user: dict = Depends(deps.get_current_user)
):
    return crud.create_learning_path(db=db, obj_in=learning_path_in, user_id=current_user["id"])

@router.get("/", response_model=List[LearningPath])
def read_learning_paths(
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    return crud.get_user_learning_paths(db=db, user_id=current_user["id"])

@router.get("/{learning_path_id}", response_model=LearningPath)
def read_learning_path(
    learning_path_id: int,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    learning_path = crud.get_learning_path(db=db, id=learning_path_id)
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    if learning_path.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return learning_path

@router.put("/{learning_path_id}", response_model=LearningPath)
def update_learning_path(
    *,
    db: Session = Depends(deps.get_db),
    learning_path_id: int,
    learning_path_in: LearningPathUpdate,
    current_user: dict = Depends(deps.get_current_user)
):
    learning_path = crud.get_learning_path(db=db, id=learning_path_id)
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    if learning_path.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.update_learning_path(db=db, id=learning_path_id, obj_in=learning_path_in)

@router.delete("/{learning_path_id}", response_model=LearningPath)
def delete_learning_path(
    *,
    db: Session = Depends(deps.get_db),
    learning_path_id: int,
    current_user: dict = Depends(deps.get_current_user)
):
    learning_path = crud.get_learning_path(db=db, id=learning_path_id)
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    if learning_path.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.delete_learning_path(db=db, id=learning_path_id) 