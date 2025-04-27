from typing import List, Optional
from uuid import UUID
from supabase import Client

from app.crud.base import CRUDBase
from app.models.learning_path import (
    LearningPathCreate,
    LearningPathUpdate,
    LearningPathInDB,
    LearningPathStepCreate,
    LearningPathStepUpdate,
    LearningPathStepInDB,
    ContentItemCreate,
    ContentItemUpdate,
    ContentItemInDB,
    UserProgressCreate,
    UserProgressUpdate,
    UserProgressInDB,
    ContentType,
    ProgressStatus
)

class CRUDLearningPath(CRUDBase[LearningPathInDB, LearningPathCreate, LearningPathUpdate]):
    def __init__(self):
        super().__init__(model=LearningPathInDB, table_name="learning_paths")

    def get_by_user(self, supabase: Client, user_id: UUID) -> List[LearningPathInDB]:
        """Get all learning paths created by a user."""
        result = supabase.table(self.table_name).select("*").eq("created_by", str(user_id)).execute()
        return [self.model(**item) for item in result.data]

    def get_public(self, supabase: Client) -> List[LearningPathInDB]:
        """Get all public learning paths."""
        result = supabase.table(self.table_name).select("*").eq("is_public", True).execute()
        return [self.model(**item) for item in result.data]

class CRUDLearningPathStep(CRUDBase[LearningPathStepInDB, LearningPathStepCreate, LearningPathStepUpdate]):
    def __init__(self):
        super().__init__(model=LearningPathStepInDB, table_name="learning_path_steps")

    def get_by_learning_path(self, supabase: Client, learning_path_id: UUID) -> List[LearningPathStepInDB]:
        """Get all steps for a learning path."""
        result = supabase.table(self.table_name).select("*").eq("learning_path_id", str(learning_path_id)).order("step_order").execute()
        return [self.model(**item) for item in result.data]

class CRUDContentItem(CRUDBase[ContentItemInDB, ContentItemCreate, ContentItemUpdate]):
    def __init__(self):
        super().__init__(model=ContentItemInDB, table_name="content_items")

    def get_by_type(self, supabase: Client, content_type: ContentType) -> List[ContentItemInDB]:
        """Get all content items of a specific type."""
        result = supabase.table(self.table_name).select("*").eq("content_type", content_type.value).execute()
        return [self.model(**item) for item in result.data]

class CRUDUserProgress(CRUDBase[UserProgressInDB, UserProgressCreate, UserProgressUpdate]):
    def __init__(self):
        super().__init__(model=UserProgressInDB, table_name="user_progress")

    def get_by_learning_path(self, supabase: Client, user_id: UUID, learning_path_id: UUID) -> List[UserProgressInDB]:
        """Get all progress entries for a user in a learning path."""
        result = supabase.table(self.table_name).select("*").eq("user_id", str(user_id)).eq("learning_path_id", str(learning_path_id)).execute()
        return [self.model(**item) for item in result.data]

    def get_by_step(self, supabase: Client, user_id: UUID, step_id: UUID) -> Optional[UserProgressInDB]:
        """Get progress for a specific step."""
        result = supabase.table(self.table_name).select("*").eq("user_id", str(user_id)).eq("step_id", str(step_id)).execute()
        if result.data:
            return self.model(**result.data[0])
        return None

# Create instances of the CRUD classes
learning_path = CRUDLearningPath()
learning_path_step = CRUDLearningPathStep()
content_item = CRUDContentItem()
user_progress = CRUDUserProgress() 