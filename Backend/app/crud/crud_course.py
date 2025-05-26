from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate

class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):
    def create(
        self, db: Session, *, obj_in: CourseCreate, creator_id: str
    ) -> Course:
        obj_in_data = obj_in.dict()
        # Remove prompt field if it exists
        obj_in_data.pop('prompt', None)
        db_obj = Course(**obj_in_data, creator_id=creator_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_creator(
        self, db: Session, *, creator_id: str, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        return (
            db.query(self.model)
            .filter(Course.creator_id == creator_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_title(
        self, db: Session, *, title: str
    ) -> Optional[Course]:
        return db.query(self.model).filter(Course.title == title).first()

# Create instance
crud_course = CRUDCourse(Course)
