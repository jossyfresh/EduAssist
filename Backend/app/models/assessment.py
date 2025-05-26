from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON, Integer, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base_class import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    questions = Column(JSON, nullable=False)  # List of Question objects
    passing_score = Column(Float, nullable=False)
    time_limit = Column(Integer, nullable=True)  # in minutes
    creator_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attempts = relationship("QuizAttempt", back_populates="quiz")
    creator = relationship("User", back_populates="created_quizzes")
    course = relationship("Course", back_populates="quizzes")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String(36), ForeignKey("quizzes.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=False)
    answers = Column(JSON, nullable=False)  # Dict of question_id: answer
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, default=datetime.utcnow)

    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="quiz_attempts")

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    front = Column(String(1000), nullable=False)
    back = Column(String(1000), nullable=False)
    category = Column(String(100), nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags
    creator_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="created_flashcards")
    course = relationship("Course", back_populates="flashcards")

class Exam(Base):
    __tablename__ = "exams"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    questions = Column(JSON, nullable=False)  # List of Question objects
    passing_score = Column(Float, nullable=False)
    time_limit = Column(Integer, nullable=True)  # in minutes
    is_proctored = Column(Boolean, default=False)
    creator_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attempts = relationship("ExamAttempt", back_populates="exam")
    creator = relationship("User", back_populates="created_exams")
    course = relationship("Course", back_populates="exams")

class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    exam_id = Column(String(36), ForeignKey("exams.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=False)
    answers = Column(JSON, nullable=False)  # Dict of question_id: answer
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, default=datetime.utcnow)
    is_proctored = Column(Boolean, default=False)

    exam = relationship("Exam", back_populates="attempts")
    user = relationship("User", back_populates="exam_attempts") 