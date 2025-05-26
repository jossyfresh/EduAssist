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
    ProgressCreate,
    ProgressUpdate,
    Progress
)

class CRUDLearningPath(CRUDBase[LearningPath, LearningPathCreate, LearningPathUpdate]):
    def create(
        self, db: Session, obj_in: LearningPathCreate, created_by: str
    ) -> LearningPath:
        print(f"[DEBUG] CRUD create called with obj_in: {obj_in.dict()}")
        print(f"[DEBUG] created_by parameter: {created_by}")
        
        obj_in_data = obj_in.dict(exclude={"steps", "created_by"})
        print(f"[DEBUG] obj_in_data after exclude steps and created_by: {obj_in_data}")
        
        try:
            db_obj = LearningPath(**obj_in_data, created_by=created_by)
            print(f"[DEBUG] Created db_obj: {db_obj.__dict__}")
        except Exception as e:
            print(f"[ERROR] Failed to create LearningPath object: {str(e)}")
            print(f"[ERROR] Error type: {type(e)}")
            raise
            
        db.add(db_obj)
        db.flush()  # Get db_obj.id
        print(f"[DEBUG] After flush - db_obj.id: {db_obj.id}")
        
        # Create steps if provided
        steps = obj_in.steps or []
        for step_data in steps:
            step_dict = step_data.dict()
            step_dict["learning_path_id"] = db_obj.id
            print(f"[DEBUG] Creating step with data: {step_dict}")
            db.add(LearningPathStep(**step_dict))
            
        db.commit()
        db.refresh(db_obj)
        print(f"[DEBUG] Final db_obj after commit and refresh: {db_obj.__dict__}")
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
    def create(
        self, db: Session, *, obj_in: LearningPathStepCreate, learning_path_id: str
    ) -> LearningPathStep:
        obj_in_data = obj_in.dict()
        obj_in_data["learning_path_id"] = learning_path_id
        db_obj = LearningPathStep(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_learning_path(self, db: Session, learning_path_id: str) -> List[LearningPathStep]:
        """Get all steps for a learning path."""
        return (
            db.query(self.model)
            .filter(LearningPathStep.learning_path_id == learning_path_id)
            .order_by(LearningPathStep.order)
            .all()
        )

class CRUDProgress(CRUDBase[Progress, ProgressCreate, ProgressUpdate]):
    def get_by_learning_path(self, db: Session, user_id: str, learning_path_id: str) -> List[Progress]:
        """Get all progress entries for a user in a learning path."""
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.learning_path_id == learning_path_id)
            .all()
        )

    def get_by_step(self, db: Session, user_id: str, step_id: str) -> Optional[Progress]:
        """Get progress for a specific step."""
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.step_id == step_id)
            .first()
        )

# Create instances of the CRUD classes
crud_learning_path = CRUDLearningPath(LearningPath)
crud_learning_path_step = CRUDLearningPathStep(LearningPathStep)
crud_progress = CRUDProgress(Progress)