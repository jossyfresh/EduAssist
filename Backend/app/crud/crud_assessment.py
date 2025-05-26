from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.base import CRUDBase
from app.models.assessment import Quiz, Flashcard, Exam, QuizAttempt, ExamAttempt
from app.schemas.assessment import (
    QuizCreate,
    QuizUpdate,
    FlashcardCreate,
    FlashcardUpdate,
    ExamCreate,
    ExamUpdate
)

class CRUDAssessment(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
    def create_quiz(
        self, db: Session, *, obj_in: QuizCreate, creator_id: str
    ) -> Quiz:
        obj_in_data = obj_in.dict()
        db_obj = Quiz(**obj_in_data, creator_id=creator_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_quizzes(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Quiz]:
        return db.query(Quiz).offset(skip).limit(limit).all()

    def attempt_quiz(
        self, db: Session, *, quiz_id: str, user_id: str, answers: Dict[str, str]
    ) -> QuizAttempt:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError("Quiz not found")
        
        # Calculate score
        correct_answers = 0
        for question in quiz.questions:
            if answers.get(str(question.id)) == question.correct_answer:
                correct_answers += 1
        
        score = (correct_answers / len(quiz.questions)) * 100
        
        attempt = QuizAttempt(
            quiz_id=quiz_id,
            user_id=user_id,
            score=score,
            answers=answers
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt

class CRUDFlashcard(CRUDBase[Flashcard, FlashcardCreate, FlashcardUpdate]):
    def create_flashcard(
        self, db: Session, *, obj_in: FlashcardCreate, creator_id: str
    ) -> Flashcard:
        obj_in_data = obj_in.dict()
        db_obj = Flashcard(**obj_in_data, creator_id=creator_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_flashcards(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Flashcard]:
        return db.query(Flashcard).offset(skip).limit(limit).all()

class CRUDExam(CRUDBase[Exam, ExamCreate, ExamUpdate]):
    def create_exam(
        self, db: Session, *, obj_in: ExamCreate, creator_id: str
    ) -> Exam:
        obj_in_data = obj_in.dict()
        db_obj = Exam(**obj_in_data, creator_id=creator_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_exams(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Exam]:
        return db.query(Exam).offset(skip).limit(limit).all()

    def attempt_exam(
        self, db: Session, *, exam_id: str, user_id: str, answers: Dict[str, str]
    ) -> ExamAttempt:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise ValueError("Exam not found")
        
        # Calculate score
        correct_answers = 0
        for question in exam.questions:
            if answers.get(str(question.id)) == question.correct_answer:
                correct_answers += 1
        
        score = (correct_answers / len(exam.questions)) * 100
        
        attempt = ExamAttempt(
            exam_id=exam_id,
            user_id=user_id,
            score=score,
            answers=answers
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt

# Create instances
crud_assessment = CRUDAssessment(Quiz)
crud_flashcard = CRUDFlashcard(Flashcard)
crud_exam = CRUDExam(Exam) 