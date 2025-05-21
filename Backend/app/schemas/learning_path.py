from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, UUID4, Field
from app.models.enums import ContentType
from uuid import UUID

class LearningPathBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = True
    difficulty_level: str
    estimated_duration: int
    tags: List[str] = []

class LearningPathCreate(LearningPathBase):
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
    class Config:
        schema_extra = {
            "example": {
                "title": "Updated Python Course",
                "description": "An updated comprehensive guide to Python programming",
                "is_public": True,
                "difficulty_level": "intermediate",
                "estimated_duration": 45,
                "tags": ["python", "programming", "intermediate"]
            }
        }

class LearningPathInDBBase(LearningPathBase):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LearningPathInDB(LearningPathInDBBase):
    class Config:
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
                "updated_at": "2024-03-20T10:00:00Z"
            }
        }

class LearningPathStepBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int
    content_id: Optional[UUID] = None

class LearningPathStepCreate(LearningPathStepBase):
    class Config:
        schema_extra = {
            "example": {
                "title": "Introduction to Python",
                "description": "Learn the basics of Python programming",
                "order": 1,
                "content_id": "123e4567-e89b-12d3-a456-426614174002"
            }
        }

class LearningPathStepUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    content_id: Optional[UUID] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated Introduction to Python",
                "description": "Updated basics of Python programming",
                "order": 2,
                "content_id": "123e4567-e89b-12d3-a456-426614174002"
            }
        }

class LearningPathStepInDBBase(LearningPathStepBase):
    id: UUID
    learning_path_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LearningPathStepInDB(LearningPathStepInDBBase):
    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174003",
                "learning_path_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Introduction to Python",
                "description": "Learn the basics of Python programming",
                "order": 1,
                "content_id": "123e4567-e89b-12d3-a456-426614174002",
                "created_at": "2024-03-20T10:00:00Z",
                "updated_at": "2024-03-20T10:00:00Z"
            }
        }

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
    steps: List[LearningPathStep] = []

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
                        "content_id": "123e4567-e89b-12d3-a456-426614174002",
                        "created_at": "2024-03-20T10:00:00Z",
                        "updated_at": "2024-03-20T10:00:00Z"
                    }
                ]
            }
        } 