from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, UUID4, Field
from enum import Enum

class ContentType(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    QUIZ = "quiz"
    EXERCISE = "exercise"

class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class LearningPathBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = False
    difficulty_level: Optional[str] = None
    estimated_duration: Optional[int] = None
    tags: List[str] = Field(default_factory=list)

class LearningPathCreate(LearningPathBase):
    pass

class LearningPathUpdate(LearningPathBase):
    title: Optional[str] = None

class LearningPathInDB(LearningPathBase):
    id: UUID4
    created_by: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LearningPathStepBase(BaseModel):
    title: str
    description: Optional[str] = None
    step_order: int
    content_type: ContentType
    content_id: Optional[UUID4] = None

class LearningPathStepCreate(LearningPathStepBase):
    learning_path_id: UUID4

class LearningPathStepUpdate(LearningPathStepBase):
    title: Optional[str] = None
    step_order: Optional[int] = None
    content_type: Optional[ContentType] = None

class LearningPathStepInDB(LearningPathStepBase):
    id: UUID4
    learning_path_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContentItemBase(BaseModel):
    content_type: ContentType
    title: str
    content: str
    metadata: dict = Field(default_factory=dict)

class ContentItemCreate(ContentItemBase):
    pass

class ContentItemUpdate(ContentItemBase):
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[dict] = None

class ContentItemInDB(ContentItemBase):
    id: UUID4
    created_by: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserProgressBase(BaseModel):
    status: ProgressStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class UserProgressCreate(UserProgressBase):
    learning_path_id: UUID4
    step_id: UUID4

class UserProgressUpdate(UserProgressBase):
    status: Optional[ProgressStatus] = None

class UserProgressInDB(UserProgressBase):
    id: UUID4
    user_id: UUID4
    learning_path_id: UUID4
    step_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 