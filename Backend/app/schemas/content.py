from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.enums import ContentType

class ContentBase(BaseModel):
    title: str
    content_type: ContentType
    content: str
    meta: Optional[Dict[str, Any]] = Field(default_factory=dict)
    description: Optional[str] = None
    course_id: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    content_type: Optional[ContentType] = None
    content: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    course_id: Optional[str] = None

class Content(BaseModel):
    id: str
    title: str
    content_type: ContentType
    content: str
    meta: Optional[Dict[str, Any]] = Field(default_factory=dict)
    description: Optional[str] = None
    created_by: str
    created_at: datetime
    updated_at: datetime
    course_id: Optional[str] = None

    class Config:
        orm_mode = True

class GenerateContentRequest(BaseModel):
    content_type: str
    parameters: Dict[str, Any]

class VideoContent(ContentBase):
    video_url: str
    duration: Optional[int] = None
    thumbnail_url: Optional[str] = None

class TextContent(ContentBase):
    pass

class ContentGeneratorResponse(BaseModel):
    content: str

    class Config:
        schema_extra = {
            "example": {
                "content": "Quantum computing is a type of computing that uses quantum bits..."
            }
        }