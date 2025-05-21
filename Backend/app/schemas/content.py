from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, UUID4, Field
from app.models.enums import ContentType

class ContentItemBase(BaseModel):
    content_type: ContentType
    title: str
    content: str
    metadata: Dict = Field(default_factory=dict)

class ContentItemCreate(ContentItemBase):
    pass

class ContentItemUpdate(ContentItemBase):
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict] = None

class ContentItemInDB(ContentItemBase):
    id: UUID4
    created_by: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VideoContent(ContentItemInDB):
    video_url: str
    duration: Optional[int] = None
    thumbnail_url: Optional[str] = None

class TextContent(ContentItemInDB):
    pass

class Content(ContentItemInDB):
    pass

class ContentCreate(ContentItemCreate):
    class Config:
        schema_extra = {
            "example": {
                "title": "Introduction to Python",
                "description": "A beginner's guide to Python programming",
                "content_type": "text",
                "content": "Python is a high-level programming language..."
            }
        }

class ContentUpdate(ContentItemUpdate):
    class Config:
        schema_extra = {
            "example": {
                "title": "Updated Title",
                "description": "Updated Description",
                "content_type": "text",
                "content": "Updated content..."
            }
        }

class ContentInDBBase(ContentItemBase):
    id: int
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Content(ContentInDBBase):
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Content Title",
                "description": "Content Description",
                "content_type": "text",
                "content": "Content body...",
                "created_by": "user@example.com",
                "created_at": "2024-03-20T10:00:00Z",
                "updated_at": "2024-03-20T10:00:00Z"
            }
        }

class TextContent(Content):
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Introduction to Python",
                "description": "A beginner's guide to Python programming",
                "content_type": "text",
                "content": "Python is a high-level programming language...",
                "created_by": "user@example.com",
                "created_at": "2024-03-20T10:00:00Z",
                "updated_at": "2024-03-20T10:00:00Z"
            }
        }

class VideoContent(Content):
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Video Title",
                "description": "Video Description",
                "content_type": "video",
                "content": "https://example.com/video.mp4",
                "created_by": "user@example.com",
                "created_at": "2024-03-20T10:00:00Z",
                "updated_at": "2024-03-20T10:00:00Z"
            }
        }

class ContentGeneratorRequest(BaseModel):
    content_type: str
    parameters: Dict[str, Any]
    provider: str = "openai"

    class Config:
        schema_extra = {
            "example": {
                "content_type": "text",
                "parameters": {
                    "prompt": "Explain quantum computing in simple terms",
                    "max_tokens": 500
                },
                "provider": "openai"
            }
        }

class ContentGeneratorResponse(BaseModel):
    content: str

    class Config:
        schema_extra = {
            "example": {
                "content": "Quantum computing is a type of computing that uses quantum bits..."
            }
        } 