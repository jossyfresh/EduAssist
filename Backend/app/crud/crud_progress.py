from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.progress import UserProgress, AssessmentProgress, CourseProgress
from app.schemas.progress import (
    ProgressCreate,
    ProgressUpdate,
    AssessmentProgressCreate,
    AssessmentProgressUpdate,
    CourseProgressCreate,
    CourseProgressUpdate
)

class CRUDProgress(CRUDBase[UserProgress, ProgressCreate, ProgressUpdate]):
    def create(
        self, db: Session, *, obj_in: ProgressCreate, user_id: str
    ) -> UserProgress:
        obj_in_data = obj_in.dict()
        db_obj = UserProgress(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user(
        self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[UserProgress]:
        return (
            db.query(self.model)
            .filter(UserProgress.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_learning_path(
        self, db: Session, *, user_id: str, learning_path_id: str
    ) -> List[UserProgress]:
        return (
            db.query(self.model)
            .filter(
                UserProgress.user_id == user_id,
                UserProgress.learning_path_id == learning_path_id
            )
            .all()
        )

class CRUDAssessmentProgress(CRUDBase[AssessmentProgress, AssessmentProgressCreate, AssessmentProgressUpdate]):
    def create(
        self, db: Session, *, obj_in: AssessmentProgressCreate, user_id: str
    ) -> AssessmentProgress:
        obj_in_data = obj_in.dict()
        db_obj = AssessmentProgress(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_progress(
        self, db: Session, *, user_id: str, assessment_id: str, score: float
    ) -> AssessmentProgress:
        progress = (
            db.query(self.model)
            .filter(
                AssessmentProgress.user_id == user_id,
                AssessmentProgress.assessment_id == assessment_id
            )
            .first()
        )
        
        if not progress:
            return None
            
        progress.attempts += 1
        progress.last_attempt_at = datetime.utcnow()
        progress.score = score
        
        if not progress.best_score or score > progress.best_score:
            progress.best_score = score
            
        db.add(progress)
        db.commit()
        db.refresh(progress)
        return progress

class CRUDCourseProgress(CRUDBase[CourseProgress, CourseProgressCreate, CourseProgressUpdate]):
    def create(
        self, db: Session, *, obj_in: CourseProgressCreate, user_id: str
    ) -> CourseProgress:
        obj_in_data = obj_in.dict()
        db_obj = CourseProgress(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_progress(
        self, db: Session, *, user_id: str, course_id: str, score: float
    ) -> CourseProgress:
        progress = (
            db.query(self.model)
            .filter(
                CourseProgress.user_id == user_id,
                CourseProgress.course_id == course_id
            )
            .first()
        )
        
        if not progress:
            return None
            
        progress.completed_assessments += 1
        progress.last_activity_at = datetime.utcnow()
        
        # Update overall score
        total_score = progress.overall_score * (progress.completed_assessments - 1)
        progress.overall_score = (total_score + score) / progress.completed_assessments
        
        db.add(progress)
        db.commit()
        db.refresh(progress)
        return progress

# Create instances
crud_progress = CRUDProgress(UserProgress)
crud_assessment_progress = CRUDAssessmentProgress(AssessmentProgress)
crud_course_progress = CRUDCourseProgress(CourseProgress) 