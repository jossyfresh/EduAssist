from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base_class import Base

class YouTubeContent(Base):
    __tablename__ = "youtube_content"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    video_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    transcript = Column(Text, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    video_url = Column(String, nullable=False)
    video_metadata = Column(JSON, default={})
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="youtube_contents")
    chat_messages = relationship("YouTubeChatMessage", back_populates="youtube_content", cascade="all, delete-orphan")

class YouTubeChatMessage(Base):
    __tablename__ = "youtube_chat_messages"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    youtube_content_id = Column(String, ForeignKey("youtube_content.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    youtube_content = relationship("YouTubeContent", back_populates="chat_messages")
    user = relationship("User", back_populates="youtube_chat_messages") 