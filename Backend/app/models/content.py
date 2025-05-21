from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from app.models.enums import ContentType
import uuid
from datetime import datetime

class Content(Base):
    __tablename__ = "content"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True)
    content_type = Column(String, default=ContentType.TEXT)
    content = Column(String)
    meta = Column(JSON, default={})
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 