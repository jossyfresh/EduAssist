from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from app.models.enums import ContentType

class ContentType(str, Enum):
    TEXT = "TEXT"
    VIDEO = "VIDEO"
    FILE = "FILE"
    QUIZ = "QUIZ"
    SUMMARY = "SUMMARY"
    FLASHCARD = "FLASHCARD"

class ContentBase(BaseModel):
    title: str
    content: str
    content_type: str
    description: Optional[str] = None
    course_id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class ContentResponse(ContentBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Alias for backward compatibility
Content = ContentResponse

class ContentListResponse(BaseModel):
    items: List[ContentResponse]
    total: int

    class Config:
        orm_mode = True

class ContentGenerateRequest(BaseModel):
    content_type: str
    parameters: Dict[str, Any]
    provider: str = "openai"

# Alias for backward compatibility
GenerateContentRequest = ContentGenerateRequest

class ContentGeneratorResponse(BaseModel):
    content: Dict[str, Any]

class ContentBatchResponse(BaseModel):
    batch_id: str
    files: List[ContentResponse]

class ContentBatchCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ContentBatchUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ContentContextualGenerateRequest(BaseModel):
    course_id: str
    content_type: str
    provider: str = "openai"
    extra_parameters: Optional[Dict[str, Any]] = None

class VideoContent(ContentBase):
    video_url: str
    duration: Optional[int] = None
    thumbnail_url: Optional[str] = None

class TextContent(ContentBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "content": "Quantum computing is a type of computing that uses quantum bits..."
            }
        }