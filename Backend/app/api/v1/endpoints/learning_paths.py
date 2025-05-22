from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.crud_learning_path import (
    crud_learning_path,
    crud_learning_path_step,
    crud_user_progress
)
from app.schemas.learning_path import (
    LearningPathCreate,
    LearningPathUpdate,
    LearningPathInDB,
    LearningPathStepCreate,
    LearningPathStepInDB,
    LearningPathStepUpdate
)
from app.schemas.content import (
    ContentCreate,
    Content
)
from app.schemas.progress import (
    UserProgressCreate,
    UserProgressInDB
)
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=LearningPathInDB, responses={
    200: {"description": "Successfully created learning path", "model": LearningPathInDB},
    400: {"description": "Invalid input data"},
    401: {"description": "Not authenticated"}
})
async def create_learning_path(
    learning_path_in: LearningPathCreate,
    current_user: "User" = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> LearningPathInDB:
    """Create a new learning path.
    
    Example request body:
    {
        "title": "Example Learning Path",
        "description": "This is an example learning path.",
        "is_public": true,
        "difficulty_level": "Intermediate",
        "estimated_duration": 120,
        "tags": ["example", "learning"]
    }
    """
    try:
        created_path = crud_learning_path.create(db, obj_in=learning_path_in, created_by=str(current_user.id))
        return created_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[LearningPathInDB], responses={
    200: {"description": "List of learning paths", "model": List[LearningPathInDB]},
    401: {"description": "Not authenticated"}
})
async def get_learning_paths(
    current_user: "User" = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> List[LearningPathInDB]:
    """Get all learning paths.
    
    Example response:
    [
        {
            "id": "uuid",
            "title": "Example Learning Path",
            "description": "This is an example learning path.",
            "is_public": true,
            "difficulty_level": "Intermediate",
            "estimated_duration": 120,
            "tags": ["example", "learning"],
            "created_by": "uuid",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]
    """
    try:
        paths = crud_learning_path.get_by_user(db, user_id=str(current_user.id))
        return paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my", response_model=List[LearningPathInDB], responses={
    200: {"description": "List of user's learning paths", "model": List[LearningPathInDB]},
    401: {"description": "Not authenticated"}
})
async def get_my_learning_paths(
    current_user: "User" = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> List[LearningPathInDB]:
    """Get learning paths created by the current user.
    
    Example response:
    [
        {
            "id": "uuid",
            "title": "My Learning Path",
            "description": "This is my learning path.",
            "is_public": false,
            "difficulty_level": "Beginner",
            "estimated_duration": 60,
            "tags": ["personal", "learning"],
            "created_by": "uuid",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]
    """
    try:
        paths = crud_learning_path.get_by_user(db, user_id=str(current_user.id))
        return paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/public", response_model=List[LearningPathInDB], responses={
    200: {"description": "List of public learning paths", "model": List[LearningPathInDB]}
})
async def get_public_learning_paths(
    db: Session = Depends(get_db)
) -> List[LearningPathInDB]:
    """Get all public learning paths.
    
    Example response:
    [
        {
            "id": "uuid",
            "title": "Public Learning Path",
            "description": "This is a public learning path.",
            "is_public": true,
            "difficulty_level": "Advanced",
            "estimated_duration": 180,
            "tags": ["public", "learning"],
            "created_by": "uuid",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]
    """
    try:
        paths = crud_learning_path.get_public(db)
        return paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{path_id}", response_model=LearningPathInDB, responses={
    200: {"description": "Learning path details", "model": LearningPathInDB},
    401: {"description": "Not authenticated"},
    403: {"description": "Not authorized to access this learning path"},
    404: {"description": "Learning path not found"}
})
async def get_learning_path(
    path_id: UUID,
    current_user: dict = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> LearningPathInDB:
    """Get a specific learning path by ID.
    
    Example response:
    {
        "id": "uuid",
        "title": "Example Learning Path",
        "description": "This is an example learning path.",
        "is_public": true,
        "difficulty_level": "Intermediate",
        "estimated_duration": 120,
        "tags": ["example", "learning"],
        "created_by": "uuid",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    """
    try:
        path = crud_learning_path.get(db, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if not path.is_public and path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to access this learning path")
        return path
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{path_id}", response_model=LearningPathInDB, responses={
    200: {"description": "Updated learning path", "model": LearningPathInDB},
    401: {"description": "Not authenticated"},
    403: {"description": "Not authorized to update this learning path"},
    404: {"description": "Learning path not found"}
})
async def update_learning_path(
    path_id: UUID,
    learning_path_in: LearningPathUpdate,
    current_user: dict = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> LearningPathInDB:
    """Update a learning path.
    
    Example request body:
    {
        "title": "Updated Learning Path",
        "description": "This is an updated learning path.",
        "is_public": true,
        "difficulty_level": "Advanced",
        "estimated_duration": 150,
        "tags": ["updated", "learning"]
    }
    """
    try:
        path = crud_learning_path.get(db, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to update this learning path")
        updated_path = crud_learning_path.update(db, id=path_id, obj_in=learning_path_in)
        return updated_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{path_id}", responses={
    204: {"description": "Learning path successfully deleted"},
    401: {"description": "Not authenticated"},
    403: {"description": "Not authorized to delete this learning path"},
    404: {"description": "Learning path not found"}
})
async def delete_learning_path(
    path_id: UUID,
    current_user: dict = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a learning path.
    
    Example response:
    {
        "message": "Learning path deleted successfully"
    }
    """
    try:
        path = crud_learning_path.get(db, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to delete this learning path")
        crud_learning_path.remove(db, id=path_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{path_id}/steps", response_model=LearningPathStepInDB, responses={
    200: {"description": "Created learning path step", "model": LearningPathStepInDB},
    401: {"description": "Not authenticated"},
    403: {"description": "Not authorized to add steps to this learning path"},
    404: {"description": "Learning path not found"}
})
async def create_learning_path_step(
    path_id: UUID,
    step_in: LearningPathStepCreate,
    current_user: dict = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> LearningPathStepInDB:
    """Create a new step in a learning path.
    
    Example request body:
    {
        "title": "Example Step",
        "description": "This is an example step.",
        "content_type": "text",
        "content": "This is the content of the step.",
        "order": 1
    }
    """
    try:
        path = crud_learning_path.get(db, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to add steps to this learning path")
        created_step = crud_learning_path_step.create(db, obj_in=step_in, learning_path_id=path_id)
        return created_step
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{path_id}/steps", response_model=List[LearningPathStepInDB], responses={
    200: {"description": "List of learning path steps", "model": List[LearningPathStepInDB]},
    401: {"description": "Not authenticated"},
    403: {"description": "Not authorized to view steps of this learning path"},
    404: {"description": "Learning path not found"}
})
async def get_learning_path_steps(
    path_id: UUID,
    current_user: dict = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> List[LearningPathStepInDB]:
    """Get all steps in a learning path.
    
    Example response:
    [
        {
            "id": 1,
            "title": "Example Step",
            "description": "This is an example step.",
            "content_type": "text",
            "content": "This is the content of the step.",
            "order": 1,
            "learning_path_id": "uuid",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]
    """
    try:
        path = crud_learning_path.get(db, path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        if not path.is_public and path.created_by != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to view steps of this learning path")
        steps = crud_learning_path_step.get_by_learning_path(db, learning_path_id=path_id)
        return steps
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/content", response_model=Content)
async def create_content_item(
    content_in: ContentCreate,
    current_user: dict = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> Content:
    """Create a new content item.
    
    Example request body:
    {
        "title": "Example Content",
        "description": "This is an example content item.",
        "content_type": "text",
        "content": "This is the content of the item."
    }
    """
    try:
        created_content = crud_content.create(db, obj_in=content_in, created_by=UUID(current_user["id"]))
        return created_content
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/progress", response_model=UserProgressInDB)
async def create_user_progress(
    progress_in: UserProgressCreate,
    current_user: dict = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> UserProgressInDB:
    """Create or update user progress.
    
    Example request body:
    {
        "user_id": "uuid",
        "learning_path_id": "uuid",
        "step_id": 1,
        "status": "completed",
        "score": 100
    }
    """
    try:
        if progress_in.user_id != UUID(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized to create progress for another user")
        created_progress = crud_user_progress.create(db, obj_in=progress_in)
        return created_progress
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/progress/{path_id}", response_model=List[UserProgressInDB])
async def get_user_progress(
    path_id: UUID,
    current_user: dict = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> List[UserProgressInDB]:
    """Get user progress for a specific learning path.
    
    Example response:
    [
        {
            "id": 1,
            "user_id": "uuid",
            "learning_path_id": "uuid",
            "step_id": 1,
            "status": "completed",
            "score": 100,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]
    """
    try:
        progress = crud_user_progress.get_by_user_and_path(db, UUID(current_user["id"]), path_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))