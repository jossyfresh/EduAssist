from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from supabase import Client

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
from app.schemas.content import (
    ContentItemCreate,
    ContentItemUpdate,
    ContentItemInDB
)
from app.schemas.progress import (
    UserProgressCreate,
    UserProgressUpdate,
    UserProgressInDB
)

class CRUDLearningPath(CRUDBase[LearningPath, LearningPathCreate, LearningPathUpdate]):
    def create_with_steps(
        self, db: Session, *, obj_in: LearningPathCreate, created_by: int
    ) -> LearningPath:
        obj_in_data = obj_in.dict()
        steps = obj_in_data.pop("steps")
        db_obj = LearningPath(**obj_in_data, created_by=created_by)
        db.add(db_obj)
        db.flush()  # Flush to get the ID

        # Create steps
        for step_data in steps:
            step = LearningPathStep(**step_data.dict(), learning_path_id=db_obj.id)
            db.add(step)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_creator(
        self, db: Session, *, creator_id: int, skip: int = 0, limit: int = 100
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

    def get_by_user(self, supabase: Client, user_id: UUID) -> List[LearningPathInDB]:
        """Get all learning paths created by a user."""
        result = supabase.table("learning_paths").select("*").eq("created_by", str(user_id)).execute()
        return [LearningPathInDB(**item) for item in result.data]

    def get_public(self, supabase: Client) -> List[LearningPathInDB]:
        """Get all public learning paths."""
        result = supabase.table("learning_paths").select("*").eq("is_public", True).execute()
        return [LearningPathInDB(**item) for item in result.data]

class CRUDLearningPathStep(CRUDBase[LearningPathStep, LearningPathStepCreate, LearningPathStepUpdate]):
    def get_by_learning_path(self, supabase: Client, learning_path_id: UUID) -> List[LearningPathStepInDB]:
        """Get all steps for a learning path."""
        result = supabase.table("learning_path_steps").select("*").eq("learning_path_id", str(learning_path_id)).order("step_order").execute()
        return [LearningPathStepInDB(**item) for item in result.data]

class CRUDContentItem(CRUDBase[ContentItemInDB, ContentItemCreate, ContentItemUpdate]):
    def get_by_type(self, supabase: Client, content_type: ContentType) -> List[ContentItemInDB]:
        """Get all content items of a specific type."""
        result = supabase.table("content_items").select("*").eq("content_type", content_type.value).execute()
        return [ContentItemInDB(**item) for item in result.data]

class CRUDUserProgress(CRUDBase[UserProgressInDB, UserProgressCreate, UserProgressUpdate]):
    def get_by_learning_path(self, supabase: Client, user_id: UUID, learning_path_id: UUID) -> List[UserProgressInDB]:
        """Get all progress entries for a user in a learning path."""
        result = supabase.table("user_progress").select("*").eq("user_id", str(user_id)).eq("learning_path_id", str(learning_path_id)).execute()
        return [UserProgressInDB(**item) for item in result.data]

    def get_by_step(self, supabase: Client, user_id: UUID, step_id: UUID) -> Optional[UserProgressInDB]:
        """Get progress for a specific step."""
        result = supabase.table("user_progress").select("*").eq("user_id", str(user_id)).eq("step_id", str(step_id)).execute()
        if result.data:
            return UserProgressInDB(**result.data[0])
        return None

# Create instances of the CRUD classes
crud_learning_path = CRUDLearningPath(LearningPath)
crud_learning_path_step = CRUDLearningPathStep(LearningPathStep)
crud_content_item = CRUDContentItem(ContentItemInDB)
crud_user_progress = CRUDUserProgress(UserProgressInDB) 