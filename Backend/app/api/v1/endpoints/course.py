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
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Call AI to generate title, sub_title, description
    prompt = course_in.prompt
    ai_prompt = f"Given the following course idea or topic, generate a catchy course title, a concise sub-title, and a detailed description. Respond as JSON: {{'title': ..., 'sub_title': ..., 'description': ...}}.\nPrompt: {prompt}"
    ai_response = content_generator.openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": ai_prompt}]
    )
    import json as _json
    try:
        ai_content = _json.loads(ai_response.choices[0].message.content)
        title = ai_content.get("title", "Untitled Course")
        sub_title = ai_content.get("sub_title", "")
        description = ai_content.get("description", "")
    except Exception:
        title = "Untitled Course"
        sub_title = ""
        description = prompt
    course = crud_course.create(db=db, obj_in=course_in, user_id=current_user.id, title=title, sub_title=sub_title, description=description)
    return course

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
    return crud_course.get_multi(db=db, skip=skip, limit=limit)

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
    if course.created_by != current_user.id:
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
    if course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this course")
    return crud_course.remove(db=db, id=course_id)
