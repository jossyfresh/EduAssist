from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from typing import Optional, List

def get(db: Session, id: str) -> Optional[Course]:
    return db.query(Course).filter(Course.id == id).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
    return db.query(Course).offset(skip).limit(limit).all()

def create(db: Session, obj_in: CourseCreate, user_id: str) -> Course:
    db_obj = Course(
        title=obj_in.title,
        description=obj_in.description,
        created_by=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Course, obj_in: CourseUpdate) -> Course:
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, id: str) -> Optional[Course]:
    obj = db.query(Course).get(id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
