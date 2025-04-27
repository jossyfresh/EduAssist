from typing import List
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.crud.learning_path import learning_path, learning_path_step, content_item, user_progress
from app.models.learning_path import (
    LearningPathCreate,
    LearningPathUpdate,
    LearningPathInDB,
    LearningPathStepCreate,
    LearningPathStepUpdate,
    LearningPathStepInDB,
    ContentItemCreate,
    ContentItemUpdate,
    ContentItemInDB,
    UserProgressCreate,
    UserProgressUpdate,
    UserProgressInDB
)
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=LearningPathInDB)
def create_learning_path(
    learning_path_in: LearningPathCreate,
    current_user: dict = Depends(get_current_user)
):
    learning_path_in.created_by = current_user["id"]
    return learning_path.create(learning_path_in)

@router.get("/", response_model=List[LearningPathInDB])
def get_learning_paths(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    return learning_path.get_multi(skip=skip, limit=limit)

@router.get("/my", response_model=List[LearningPathInDB])
def get_my_learning_paths(current_user: dict = Depends(get_current_user)):
    return learning_path.get_by_user(current_user["id"])

@router.get("/public", response_model=List[LearningPathInDB])
def get_public_learning_paths():
    return learning_path.get_public()

@router.get("/{learning_path_id}", response_model=LearningPathInDB)
def get_learning_path(learning_path_id: UUID):
    db_learning_path = learning_path.get(learning_path_id)
    if not db_learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return db_learning_path

@router.put("/{learning_path_id}", response_model=LearningPathInDB)
def update_learning_path(
    learning_path_id: UUID,
    learning_path_in: LearningPathUpdate,
    current_user: dict = Depends(get_current_user)
):
    db_learning_path = learning_path.get(learning_path_id)
    if not db_learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    if db_learning_path.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this learning path")
    return learning_path.update(learning_path_id, learning_path_in)

@router.delete("/{learning_path_id}")
def delete_learning_path(
    learning_path_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    db_learning_path = learning_path.get(learning_path_id)
    if not db_learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    if db_learning_path.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this learning path")
    learning_path.remove(learning_path_id)
    return {"message": "Learning path deleted successfully"}

@router.post("/{learning_path_id}/steps", response_model=LearningPathStepInDB)
def create_learning_path_step(
    learning_path_id: UUID,
    step_in: LearningPathStepCreate,
    current_user: dict = Depends(get_current_user)
):
    db_learning_path = learning_path.get(learning_path_id)
    if not db_learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    if db_learning_path.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to add steps to this learning path")
    step_in.learning_path_id = learning_path_id
    return learning_path_step.create(step_in)

@router.get("/{learning_path_id}/steps", response_model=List[LearningPathStepInDB])
def get_learning_path_steps(learning_path_id: UUID):
    return learning_path_step.get_by_learning_path(learning_path_id)

@router.put("/{learning_path_id}/steps/{step_id}", response_model=LearningPathStepInDB)
def update_learning_path_step(
    learning_path_id: UUID,
    step_id: UUID,
    step_in: LearningPathStepUpdate,
    current_user: dict = Depends(get_current_user)
):
    db_learning_path = learning_path.get(learning_path_id)
    if not db_learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    if db_learning_path.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update steps in this learning path")
    return learning_path_step.update(step_id, step_in)

@router.delete("/{learning_path_id}/steps/{step_id}")
def delete_learning_path_step(
    learning_path_id: UUID,
    step_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    db_learning_path = learning_path.get(learning_path_id)
    if not db_learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    if db_learning_path.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete steps from this learning path")
    learning_path_step.remove(step_id)
    return {"message": "Step deleted successfully"}

@router.post("/{learning_path_id}/progress", response_model=UserProgressInDB)
def create_user_progress(
    learning_path_id: UUID,
    progress_in: UserProgressCreate,
    current_user: dict = Depends(get_current_user)
):
    progress_in.user_id = current_user["id"]
    progress_in.learning_path_id = learning_path_id
    return user_progress.create(progress_in)

@router.get("/{learning_path_id}/progress", response_model=List[UserProgressInDB])
def get_user_progress(
    learning_path_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    return user_progress.get_by_user_and_path(current_user["id"], learning_path_id)

@router.put("/{learning_path_id}/progress/{step_id}", response_model=UserProgressInDB)
def update_user_progress(
    learning_path_id: UUID,
    step_id: UUID,
    progress_in: UserProgressUpdate,
    current_user: dict = Depends(get_current_user)
):
    db_progress = user_progress.get_by_user_and_step(current_user["id"], step_id)
    if not db_progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return user_progress.update(db_progress.id, progress_in) 