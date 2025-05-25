from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, UUID4, Field
from app.models.enums import ContentType, ProgressStatus
from uuid import UUID

class LearningPathStepBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int
    content_type: ContentType
    content_id: Optional[str] = None
    content: Optional[str] = None

class LearningPathStepCreate(LearningPathStepBase):
    learning_path_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Introduction to Python",
                "description": "Learn the basics of Python programming",
                "order": 1,
                "content_type": "video",
                "content_id": "123e4567-e89b-12d3-a456-426614174002"
            }
        }

class LearningPathBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = False
    difficulty_level: Optional[str] = None
    estimated_duration: Optional[int] = None
    tags: List[str] = Field(default_factory=list)

class LearningPathCreate(LearningPathBase):
    created_by: Optional[str] = None
    steps: Optional[List["LearningPathStepCreate"]] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Python for Beginners",
                "description": "A comprehensive guide to Python programming",
                "is_public": True,
                "difficulty_level": "beginner",
                "estimated_duration": 30,
                "tags": ["python", "programming", "beginner"]
            }
        }

class LearningPathUpdate(LearningPathBase):
    title: Optional[str] = None
    steps: Optional[List["LearningPathStepUpdate"]] = None

class LearningPathInDB(LearningPathBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    steps: Optional[List["LearningPathStepInDB"]] = Field(default_factory=list)

    class Config:
        orm_mode = True
        from_attributes = True

class LearningPathStepUpdate(LearningPathStepBase):
    title: Optional[str] = None
    order: Optional[int] = None
    content_type: Optional[ContentType] = None
    content_id: Optional[str] = None
    content: Optional[str] = None
    learning_path_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated Introduction to Python",
                "description": "Updated basics of Python programming",
                "order": 2,
                "content_type": "video",
                "content_id": "123e4567-e89b-12d3-a456-426614174002"
            }
        }

class LearningPathStepInDB(LearningPathStepBase):
    id: str
    learning_path_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True

class LearningPathStep(LearningPathStepBase):
    id: UUID
    learning_path_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174003",
                "learning_path_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Introduction to Python",
                "description": "Learn the basics of Python programming",
                "order": 1,
                "content_type": "video",
                "content_id": "123e4567-e89b-12d3-a456-426614174002",
                "created_at": "2024-03-20T10:00:00Z",
                "updated_at": "2024-03-20T10:00:00Z"
            }
        }

class LearningPath(LearningPathBase):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    steps: List[LearningPathStep] = Field(default_factory=list)

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Python for Beginners",
                "description": "A comprehensive guide to Python programming",
                "is_public": True,
                "difficulty_level": "beginner",
                "estimated_duration": 30,
                "tags": ["python", "programming", "beginner"],
                "created_by": "123e4567-e89b-12d3-a456-426614174001",
                "created_at": "2024-03-20T10:00:00Z",
                "updated_at": "2024-03-20T10:00:00Z",
                "steps": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174003",
                        "learning_path_id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Introduction to Python",
                        "description": "Learn the basics of Python programming",
                        "order": 1,
                        "content_type": "video",
                        "content_id": "123e4567-e89b-12d3-a456-426614174002",
                        "created_at": "2024-03-20T10:00:00Z",
                        "updated_at": "2024-03-20T10:00:00Z"
                    }
                ]
            }
        }

class ContentItemBase(BaseModel):
    content_type: ContentType
    title: str
    content: str
    meta: dict = Field(default_factory=dict)

class ContentItemCreate(ContentItemBase):
    pass

class ContentItemUpdate(ContentItemBase):
    title: Optional[str] = None
    content: Optional[str] = None
    meta: Optional[dict] = None

class UserProgressBase(BaseModel):
    status: ProgressStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class UserProgressCreate(UserProgressBase):
    learning_path_id: str
    step_id: str
    user_id: str

class UserProgressUpdate(UserProgressBase):
    status: Optional[ProgressStatus] = None
    learning_path_id: Optional[str] = None
    step_id: Optional[str] = None
    user_id: Optional[str] = None

class UserProgressInDB(UserProgressBase):
    id: str
    user_id: str
    learning_path_id: str
    step_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

LearningPathCreate.update_forward_refs()
LearningPathUpdate.update_forward_refs()
LearningPathInDB.update_forward_refs()
LearningPathStepUpdate.update_forward_refs()
LearningPathStepInDB.update_forward_refs()
LearningPath.update_forward_refs() 