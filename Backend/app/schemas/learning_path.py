from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, UUID4, Field
from app.models.enums import ContentType

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
    content_type: ContentType
    content: str
    order: int

class LearningPathStepCreate(LearningPathStepBase):
    pass

class LearningPathStepUpdate(LearningPathStepBase):
    title: Optional[str] = None
    content_type: Optional[ContentType] = None
    content: Optional[str] = None
    order: Optional[int] = None

class LearningPathStep(LearningPathStepBase):
    id: int
    learning_path_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LearningPathStepInDB(LearningPathStep):
    pass

class LearningPath(LearningPathBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    steps: List[LearningPathStep]

    class Config:
        from_attributes = True 