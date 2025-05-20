from datetime import datetime
from typing import Optional, Dict, List
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
    pass

class ContentUpdate(ContentItemUpdate):
    pass 