from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from app.db.base_class import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String(255), nullable=False)
    sub_title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    creator_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    contents = relationship("Content", back_populates="course")
    learning_paths = relationship("LearningPath", back_populates="course")
    quizzes = relationship("Quiz", back_populates="course")
    flashcards = relationship("Flashcard", back_populates="course")
    exams = relationship("Exam", back_populates="course")
    assessment_progress = relationship("AssessmentProgress", back_populates="course")
    course_progress = relationship("CourseProgress", back_populates="course")
