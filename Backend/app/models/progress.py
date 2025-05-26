from sqlalchemy import Column, ForeignKey, Boolean, DateTime, String, Float, JSON, Integer
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship

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

class AssessmentProgress(Base):
    __tablename__ = "assessment_progress"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    assessment_type = Column(String(50), nullable=False)  # 'quiz', 'exam', 'flashcard'
    assessment_id = Column(String(36), nullable=False)
    score = Column(Float, nullable=True)
    attempts = Column(Integer, default=0)
    last_attempt_at = Column(DateTime, nullable=True)
    best_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationship
    course = relationship("Course", back_populates="assessment_progress")

class CourseProgress(Base):
    __tablename__ = "course_progress"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    overall_score = Column(Float, default=0.0)
    completed_assessments = Column(Integer, default=0)
    total_assessments = Column(Integer, default=0)
    last_activity_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationship
    course = relationship("Course", back_populates="course_progress") 