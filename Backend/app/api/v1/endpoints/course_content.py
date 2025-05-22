from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.schemas.content import Content
from app.schemas.learning_path import LearningPath
from app.models.course import Course as CourseModel
from app.models.content import Content as ContentModel
from app.models.learning_path import LearningPath as LearningPathModel
from app.crud import crud_course
from app.models.user import User

router = APIRouter()

@router.get("/{course_id}/contents", response_model=List[Content])
def list_course_contents(
    course_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    contents = db.query(ContentModel).filter(ContentModel.course_id == course_id).all()
    return [Content.from_orm(c) for c in contents]

@router.get("/{course_id}/learning-paths", response_model=List[LearningPath])
def list_course_learning_paths(
    course_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    learning_paths = db.query(LearningPathModel).filter(LearningPathModel.course_id == course_id).all()
    return [LearningPath.from_orm(lp) for lp in learning_paths]

@router.post("/{course_id}/contents/{content_id}", response_model=Content)
def add_content_to_course(
    course_id: str,
    content_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    content = db.query(ContentModel).filter(ContentModel.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    content.course_id = course_id
    db.commit()
    db.refresh(content)
    return Content.from_orm(content)

@router.delete("/{course_id}/contents/{content_id}", response_model=Content)
def remove_content_from_course(
    course_id: str,
    content_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    content = db.query(ContentModel).filter(ContentModel.id == content_id, ContentModel.course_id == course_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found in this course")
    content.course_id = None
    db.commit()
    db.refresh(content)
    return Content.from_orm(content)

@router.post("/{course_id}/learning-paths/{learning_path_id}", response_model=LearningPath)
def add_learning_path_to_course(
    course_id: str,
    learning_path_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    learning_path = db.query(LearningPathModel).filter(LearningPathModel.id == learning_path_id).first()
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    learning_path.course_id = course_id
    db.commit()
    db.refresh(learning_path)
    return LearningPath.from_orm(learning_path)

@router.delete("/{course_id}/learning-paths/{learning_path_id}", response_model=LearningPath)
def remove_learning_path_from_course(
    course_id: str,
    learning_path_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    learning_path = db.query(LearningPathModel).filter(LearningPathModel.id == learning_path_id, LearningPathModel.course_id == course_id).first()
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found in this course")
    learning_path.course_id = None
    db.commit()
    db.refresh(learning_path)
    return LearningPath.from_orm(learning_path)
