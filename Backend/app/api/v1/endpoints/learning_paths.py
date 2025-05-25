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
from app.services.content_generator import ContentGenerator
from app.models.course import Course
from app.models.learning_path import LearningPath
from app.models.content import ContentType

router = APIRouter()
content_generator = ContentGenerator()

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
        print(f"[DEBUG] Found {len(paths)} learning paths for user {current_user.id}")
        for path in paths:
            print(f"[DEBUG] Path ID: {path.id}, Title: {path.title}")
        return paths
    except Exception as e:
        print(f"[ERROR] Failed to get learning paths: {str(e)}")
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

@router.post("/generate-outline", response_model=dict)
async def generate_learning_path_outline(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Generate a learning path outline for a course.
    
    Example response:
    {
        "materialTitle": "string",
        "materialDescription": "string",
        "progress": 0,
        "chapters": [
            {
                "title": "string",
                "description": "string",
                "estimatedDuration": "string",
                "keyConcepts": ["string"],
                "resources": [
                    {
                        "type": "string",
                        "title": "string",
                        "url": "string"
                    }
                ]
            }
        ]
    }
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    outline = content_generator.generate_learning_path_outline(course.title, course.description or "")
    return outline

@router.get("/course/{course_id}/outline", response_model=dict)
async def get_course_learning_path_outline(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get the learning path outline for a course.
    
    Example response:
    {
        "materialTitle": "string",
        "materialDescription": "string",
        "progress": 0,
        "chapters": [
            {
                "title": "string",
                "description": "string",
                "estimatedDuration": "string",
                "keyConcepts": ["string"],
                "resources": [
                    {
                        "type": "string",
                        "title": "string",
                        "url": "string"
                    }
                ]
            }
        ]
    }
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if there's an existing learning path for this course
    existing_path = db.query(LearningPath).filter(LearningPath.course_id == course_id).first()
    if existing_path:
        # If there's an existing path, return its outline
        return {
            "materialTitle": existing_path.title,
            "materialDescription": existing_path.description,
            "progress": 0,
            "chapters": [
                {
                    "title": step.title,
                    "description": step.description,
                    "estimatedDuration": "1 hour",  # Default duration
                    "keyConcepts": existing_path.tags or [],
                    "resources": []
                }
                for step in existing_path.steps
            ]
        }
    
    # If no existing path, generate a new outline
    outline = content_generator.generate_learning_path_outline(course.title, course.description or "")
    return outline

@router.post("/course/{course_id}/create-from-outline", response_model=LearningPathInDB)
async def create_learning_path_from_outline(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> LearningPathInDB:
    """Create a learning path from the generated outline for a course."""
    print(f"[DEBUG] Starting create_learning_path_from_outline for course_id: {course_id}")
    print(f"[DEBUG] Current user ID: {current_user.id}")
    
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    print(f"[DEBUG] Found course: {course.title}")
    
    # Check if there's already a learning path for this course
    existing_path = db.query(LearningPath).filter(LearningPath.course_id == course_id).first()
    if existing_path:
        raise HTTPException(status_code=400, detail="Learning path already exists for this course")
    
    # Generate the outline
    outline = content_generator.generate_learning_path_outline(course.title, course.description or "")
    print(f"[DEBUG] Generated outline: {outline}")
    
    # Create the learning path first
    learning_path_in = LearningPathCreate(
        title=outline["materialTitle"],
        description=outline["materialDescription"],
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=int(sum(float(chapter["estimatedDuration"].split()[0]) * 60 for chapter in outline["chapters"])),
        tags=[concept for chapter in outline["chapters"] for concept in chapter["keyConcepts"]],
        course_id=course_id
    )
    print(f"[DEBUG] Created LearningPathCreate object: {learning_path_in.dict()}")
    
    # Create the learning path in the database
    try:
        created_path = crud_learning_path.create(db, obj_in=learning_path_in, created_by=str(current_user.id))
        print(f"[DEBUG] Successfully created learning path with ID: {created_path.id}")
    except Exception as e:
        print(f"[ERROR] Failed to create learning path: {str(e)}")
        print(f"[ERROR] Error type: {type(e)}")
        raise
    
    # Now create the steps
    for idx, chapter in enumerate(outline["chapters"]):
        step_in = LearningPathStepCreate(
            title=chapter["title"],
            description=chapter["description"],
            content_type=ContentType.TEXT,
            content=chapter["description"],
            order=idx + 1
        )
        print(f"[DEBUG] Creating step {idx + 1}: {step_in.dict()}")
        try:
            crud_learning_path_step.create(db, obj_in=step_in, learning_path_id=str(created_path.id))
        except Exception as e:
            print(f"[ERROR] Failed to create step {idx + 1}: {str(e)}")
            print(f"[ERROR] Error type: {type(e)}")
            raise
    
    # Refresh the created path to include steps
    db.refresh(created_path)
    print(f"[DEBUG] Final learning path: {created_path.__dict__}")
    
    # Convert to LearningPathInDB model
    return LearningPathInDB.from_orm(created_path)

@router.get("/course/{course_id}", response_model=LearningPathInDB)
async def get_learning_path_by_course(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> LearningPathInDB:
    """Get the learning path for a specific course."""
    path = db.query(LearningPath).filter(LearningPath.course_id == course_id).first()
    if not path:
        raise HTTPException(status_code=404, detail="Learning path not found for this course")
    print(f"[DEBUG] Found learning path: ID={path.id}, Title={path.title}")
    return path