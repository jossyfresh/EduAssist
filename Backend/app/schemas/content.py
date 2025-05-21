from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from app.models.enums import ContentType

class ContentBase(BaseModel):
    title: str
    content_type: ContentType
    content: str
    meta: Optional[Dict[str, Any]] = {}

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class Content(ContentBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class GenerateContentRequest(BaseModel):
    content_type: str
    parameters: Dict[str, Any]
    provider: str = "openai"

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