from typing import List
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.crud_learning_path import (
    crud_learning_path,
    crud_learning_path_step
)
from app.schemas.learning_path import (
    LearningPathCreate,
    LearningPathInDB,
    LearningPathStepCreate
)
from app.schemas.progress import Progress
from app.api import deps
from app.models.user import User
from app.services.content_generator import ContentGenerator
from app.models.course import Course
from app.models.learning_path import LearningPath
from app.models.learning_path_step import LearningPathStep
from app.models.progress import UserProgress
from app.models.content import ContentType

router = APIRouter()
content_generator = ContentGenerator()

@router.post("/generate-outline", response_model=dict)
async def generate_learning_path_outline(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Generate a new learning path outline for a course, regardless of existing paths."""
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
    """Get the learning path outline for a course. Returns existing path outline if available."""
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
                    "estimatedDuration": "1 hour",
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
    
    # First check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        print(f"[DEBUG] Course not found with ID: {course_id}")
        raise HTTPException(status_code=404, detail=f"Course not found with ID: {course_id}")
    print(f"[DEBUG] Found course: {course.title}")
    
    # Check if there's already a learning path for this course
    existing_path = db.query(LearningPath).filter(LearningPath.course_id == course_id).first()
    if existing_path:
        print(f"[DEBUG] Learning path already exists with ID: {existing_path.id}")
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
        print(f"[DEBUG] Learning path details: {created_path.__dict__}")
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
            created_step = crud_learning_path_step.create(db, obj_in=step_in, learning_path_id=str(created_path.id))
            print(f"[DEBUG] Successfully created step {idx + 1} with ID: {created_step.id}")
        except Exception as e:
            print(f"[ERROR] Failed to create step {idx + 1}: {str(e)}")
            print(f"[ERROR] Error type: {type(e)}")
            raise
    
    # Refresh the created path to include steps
    db.refresh(created_path)
    print(f"[DEBUG] Final learning path: {created_path.__dict__}")
    print(f"[DEBUG] Number of steps: {len(created_path.steps)}")
    
    # Convert to LearningPathInDB model
    result = LearningPathInDB.from_orm(created_path)
    print(f"[DEBUG] Returning learning path with ID: {result.id}")
    return result

@router.get("/course/{course_id}", response_model=LearningPathInDB)
async def get_learning_path_by_course(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> LearningPathInDB:
    """Get the learning path for a specific course."""
    print(f"[DEBUG] Looking for learning path with course_id: {course_id}")
    
    # First check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        print(f"[DEBUG] Course not found with ID: {course_id}")
        raise HTTPException(status_code=404, detail=f"Course not found with ID: {course_id}")
    print(f"[DEBUG] Found course: {course.title}")
    
    # Then look for the learning path
    path = db.query(LearningPath).filter(LearningPath.course_id == course_id).first()
    if not path:
        print(f"[DEBUG] Learning path not found for course: {course_id}")
        raise HTTPException(status_code=404, detail=f"Learning path not found for course: {course_id}")
    
    print(f"[DEBUG] Found learning path: ID={path.id}, Title={path.title}")
    return path

@router.get("/progress/{path_id}", response_model=List[Progress])
async def get_user_progress(
    path_id: str,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> List[Progress]:
    """Get user progress for a specific learning path."""
    try:
        # Get all progress entries for this user and path
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.learning_path_id == path_id
        ).all()
        return progress
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/progress/{path_id}/step/{step_id}", response_model=Progress)
async def update_step_progress(
    path_id: str,
    step_id: str,
    completed: bool,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
) -> Progress:
    """Update progress for a specific step in a learning path."""
    try:
        # Check if learning path and step exist
        learning_path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
        if not learning_path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        
        step = db.query(LearningPathStep).filter(
            LearningPathStep.id == step_id,
            LearningPathStep.learning_path_id == path_id
        ).first()
        if not step:
            raise HTTPException(status_code=404, detail="Step not found in this learning path")

        # Get or create progress entry
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.learning_path_id == path_id,
            UserProgress.step_id == step_id
        ).first()

        if progress:
            # Update existing progress
            progress.completed = completed
            progress.completed_at = datetime.utcnow() if completed else None
        else:
            # Create new progress entry
            progress = UserProgress(
                user_id=current_user.id,
                learning_path_id=path_id,
                step_id=step_id,
                completed=completed,
                completed_at=datetime.utcnow() if completed else None
            )
            db.add(progress)

        db.commit()
        db.refresh(progress)
        return progress
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/course/{course_id}/steps", response_model=List[dict])
async def get_learning_path_steps(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> List[dict]:
    """Get all steps for a learning path by course ID."""
    # Get the learning path
    path = db.query(LearningPath).filter(LearningPath.course_id == course_id).first()
    if not path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    # Return steps with their IDs
    return [
        {
            "id": str(step.id),
            "title": step.title,
            "description": step.description,
            "order": step.order
        }
        for step in path.steps
    ]