from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.schemas.course import Course, CourseCreate, CourseUpdate
from app.crud import crud_course
from app.models.user import User
from app.services.content_generator import ContentGenerator

router = APIRouter()
content_generator = ContentGenerator()

@router.post("/", response_model=Course)
async def create_course(
    course_in: CourseCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Call AI to generate title, sub_title, description
    prompt = course_in.prompt
    response = await content_generator.generate_course_content(prompt)
    
    import json as _json
    try:
        ai_content = _json.loads(response["content"])
        title = ai_content.get("title", "Untitled Course")
        sub_title = ai_content.get("sub_title", "A course about " + prompt)
        description = ai_content.get("description", f"This course will help you learn about {prompt}. Join us to explore this topic in depth.")
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        title = "Untitled Course"
        sub_title = "A course about " + prompt
        description = f"This course will help you learn about {prompt}. Join us to explore this topic in depth."

    # Create course with AI-generated content
    course_data = CourseCreate(
        title=title,
        sub_title=sub_title,
        description=description,
        prompt=prompt
    )
    course = crud_course.create(db=db, obj_in=course_data, creator_id=current_user.id)
    return Course.from_orm(course)

@router.get("/{course_id}", response_model=Course)
def get_course(
    course_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/", response_model=List[Course])
def list_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    courses = crud_course.get_multi(db=db, skip=skip, limit=limit)
    return [Course.from_orm(course) for course in courses]

@router.put("/{course_id}", response_model=Course)
def update_course(
    course_id: str,
    course_in: CourseUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this course")
    return crud_course.update(db=db, db_obj=course, obj_in=course_in)

@router.delete("/{course_id}", response_model=Course)
def delete_course(
    course_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this course")
    return crud_course.remove(db=db, id=course_id)
