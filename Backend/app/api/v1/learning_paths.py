from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.supabase import supabase
from app.crud.learning_path import learning_path, learning_path_step, content_item, user_progress
from app.models.learning_path import (
    LearningPathCreate,
    LearningPathUpdate,
    LearningPathInDB,
    LearningPathStepCreate,
    LearningPathStepInDB,
    ContentItemCreate,
    ContentItemInDB,
    UserProgressCreate,
    UserProgressInDB
)
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=LearningPathInDB)
async def create_learning_path(
    learning_path_in: LearningPathCreate,
    current_user: dict = Depends(get_current_user)
) -> LearningPathInDB:
    """Create a new learning path."""
    try:
        created_path = learning_path.create(supabase, obj_in=learning_path_in, created_by=UUID(current_user["id"]))
        return created_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[LearningPathInDB])
async def get_learning_paths(
    current_user: dict = Depends(get_current_user)
) -> List[LearningPathInDB]:
    """Get all learning paths."""
    try:
        paths = learning_path.get_by_user(supabase, UUID(current_user["id"]))
        return paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my", response_model=List[LearningPathInDB])
async def get_my_learning_paths(
    current_user: dict = Depends(get_current_user)
) -> List[LearningPathInDB]:
    """Get learning paths created by the current user."""
    try:
        paths = learning_path.get_by_user(supabase, UUID(current_user["id"]))
        return paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/public", response_model=List[LearningPathInDB])
async def get_public_learning_paths() -> List[LearningPathInDB]:
    """Get all public learning paths."""
    try:
        paths = learning_path.get_public(supabase)
        return paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{path_id}", response_model=LearningPathInDB)
async def get_learning_path(
    path_id: UUID,
    current_user: dict = Depends(get_current_user)
) -> LearningPathInDB:
    """Get a specific learning path by ID."""
    try:
        path = learning_path.get(supabase, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if not path.is_public and path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to access this learning path")
        return path
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{path_id}", response_model=LearningPathInDB)
async def update_learning_path(
    path_id: UUID,
    learning_path_in: LearningPathUpdate,
    current_user: dict = Depends(get_current_user)
) -> LearningPathInDB:
    """Update a learning path."""
    try:
        path = learning_path.get(supabase, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to update this learning path")
        updated_path = learning_path.update(supabase, id=path_id, obj_in=learning_path_in)
        if not updated_path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        return updated_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{path_id}")
async def delete_learning_path(
    path_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """Delete a learning path."""
    try:
        path = learning_path.get(supabase, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to delete this learning path")
        success = learning_path.remove(supabase, id=path_id)
        if not success:
            raise HTTPException(status_code=404, detail="Learning path not found")
        return {"message": "Learning path deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{path_id}/steps", response_model=LearningPathStepInDB)
async def create_learning_path_step(
    path_id: UUID,
    step_in: LearningPathStepCreate,
    current_user: dict = Depends(get_current_user)
) -> LearningPathStepInDB:
    """Create a new step in a learning path."""
    try:
        path = learning_path.get(supabase, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to add steps to this learning path")
        created_step = learning_path_step.create(supabase, obj_in=step_in)
        return created_step
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{path_id}/steps", response_model=List[LearningPathStepInDB])
async def get_learning_path_steps(
    path_id: UUID,
    current_user: dict = Depends(get_current_user)
) -> List[LearningPathStepInDB]:
    """Get all steps in a learning path."""
    try:
        path = learning_path.get(supabase, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if not path.is_public and path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to view steps in this learning path")
        steps = learning_path_step.get_by_learning_path(supabase, path_id)
        return steps
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/content", response_model=ContentItemInDB)
async def create_content_item(
    content_in: ContentItemCreate,
    current_user: dict = Depends(get_current_user)
) -> ContentItemInDB:
    """Create a new content item."""
    try:
        created_content = content_item.create(supabase, obj_in=content_in, created_by=UUID(current_user["id"]))
        return created_content
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/progress", response_model=UserProgressInDB)
async def create_user_progress(
    progress_in: UserProgressCreate,
    current_user: dict = Depends(get_current_user)
) -> UserProgressInDB:
    """Create or update user progress."""
    try:
        if progress_in.user_id != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to create progress for another user")
        created_progress = user_progress.create(supabase, obj_in=progress_in)
        return created_progress
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/progress/{path_id}", response_model=List[UserProgressInDB])
async def get_user_progress(
    path_id: UUID,
    current_user: dict = Depends(get_current_user)
) -> List[UserProgressInDB]:
    """Get user progress for a learning path."""
    try:
        progress = user_progress.get_by_learning_path(supabase, UUID(current_user["id"]), path_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 