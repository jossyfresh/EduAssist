from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, UUID4, Field
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.base_class import Base
from app.models.enums import ContentType, ProgressStatus

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
    content_id: Optional[UUID4] = None

class LearningPathStepCreate(LearningPathStepBase):
    learning_path_id: UUID4

class LearningPathStepUpdate(LearningPathStepBase):
    title: Optional[str] = None
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

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    description = Column(Text)
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_public = Column(Boolean, default=True)
    difficulty_level = Column(String, nullable=False)
    estimated_duration = Column(Integer, nullable=False)
    tags = Column(JSON, default=lambda: [])
    course_id = Column(String, ForeignKey("courses.id"), nullable=True)
    course = relationship("Course", back_populates="learning_paths")

    # Relationships
    steps = relationship("LearningPathStep", back_populates="learning_path", cascade="all, delete-orphan")