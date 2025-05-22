from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from app.db.base_class import Base
from app.models.enums import ContentType
import uuid
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Content(Base):
    __tablename__ = "content"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    content_type = Column(String, default=ContentType.TEXT)
    content = Column(String)
    meta = Column(JSON, default={})
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    description = Column(String, nullable=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=True)
    course = relationship("Course", back_populates="contents")

    def __repr__(self):
        return f"<Content {self.title}>"