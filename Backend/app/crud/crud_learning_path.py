from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.learning_path import LearningPath
from app.models.learning_path_step import LearningPathStep
from app.models.enums import ContentType, ProgressStatus
from app.schemas.learning_path import (
    LearningPathCreate,
    LearningPathUpdate,
    LearningPathInDB,
    LearningPathStepCreate,
    LearningPathStepUpdate,
    LearningPathStepInDB
)
from app.schemas.content import Content, ContentCreate, ContentUpdate
from app.schemas.progress import (
    UserProgressCreate,
    UserProgressUpdate,
    UserProgressInDB
)

class CRUDLearningPath(CRUDBase[LearningPath, LearningPathCreate, LearningPathUpdate]):
    def create_with_steps(
        self, db: Session, *, obj_in: LearningPathCreate, created_by: str
    ) -> LearningPath:
        obj_in_data = obj_in.dict()
        steps = obj_in_data.pop("steps", [])
        db_obj = LearningPath(**obj_in_data, created_by=str(created_by))
        db.add(db_obj)
        db.flush()  # Flush to get the ID

        # Create steps if provided
        for step_data in steps:
            step_dict = step_data.dict()
            step_dict["learning_path_id"] = db_obj.id
            step_dict["order"] = step_dict.pop("order", 1)
            db.add(LearningPathStep(**step_dict))

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_creator(
        self, db: Session, *, creator_id: str, skip: int = 0, limit: int = 100
    ) -> List[LearningPath]:
        return (
            db.query(self.model)
            .filter(LearningPath.created_by == creator_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_with_steps(
        self,
        db: Session,
        *,
        db_obj: LearningPath,
        obj_in: LearningPathUpdate
    ) -> LearningPath:
        obj_data = obj_in.dict(exclude_unset=True)
        if "steps" in obj_data:
            steps = obj_data.pop("steps")
            # Delete existing steps
            db.query(LearningPathStep).filter(
                LearningPathStep.learning_path_id == db_obj.id
            ).delete()
            # Create new steps
            for step_data in steps:
                step = LearningPathStep(**step_data.dict(), learning_path_id=db_obj.id)
                db.add(step)

        for field, value in obj_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user(self, db: Session, user_id: str) -> List[LearningPath]:
        """Get all learning paths created by a user."""
        return db.query(self.model).filter(LearningPath.created_by == user_id).all()

    def get_public(self, db: Session) -> List[LearningPath]:
        """Get all public learning paths."""
        return db.query(self.model).filter(LearningPath.is_public == True).all()

class CRUDLearningPathStep(CRUDBase[LearningPathStep, LearningPathStepCreate, LearningPathStepUpdate]):
    def get_by_learning_path(self, db: Session, learning_path_id: str) -> List[LearningPathStep]:
        """Get all steps for a learning path."""
        return (
            db.query(self.model)
            .filter(LearningPathStep.learning_path_id == learning_path_id)
            .order_by(LearningPathStep.order)
            .all()
        )

class CRUDUserProgress(CRUDBase[UserProgressInDB, UserProgressCreate, UserProgressUpdate]):
    def get_by_learning_path(self, db: Session, user_id: int, learning_path_id: int) -> List[UserProgressInDB]:
        """Get all progress entries for a user in a learning path."""
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.learning_path_id == learning_path_id)
            .all()
        )

    def get_by_step(self, db: Session, user_id: int, step_id: int) -> Optional[UserProgressInDB]:
        """Get progress for a specific step."""
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.step_id == step_id)
            .first()
        )

# Create instances of the CRUD classes
crud_learning_path = CRUDLearningPath(LearningPath)
crud_learning_path_step = CRUDLearningPathStep(LearningPathStep)
crud_user_progress = CRUDUserProgress(UserProgressInDB) 