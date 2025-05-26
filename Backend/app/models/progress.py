from sqlalchemy import Column, ForeignKey, Boolean, DateTime, String
from datetime import datetime
import uuid

from app.db.base_class import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    learning_path_id = Column(String(36), ForeignKey("learning_paths.id"), nullable=False)
    step_id = Column(String(36), ForeignKey("learning_path_steps.id"), nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 