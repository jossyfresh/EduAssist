from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_assessment
from app.models.user import User
from app.schemas.assessment import (
    Quiz,
    QuizCreate,
    QuizUpdate,
    QuizAttempt,
    Flashcard,
    FlashcardCreate,
    FlashcardUpdate,
    Exam,
    ExamCreate,
    ExamUpdate,
    ExamAttempt
)

router = APIRouter()

# Quiz endpoints
@router.post("/quizzes", response_model=Quiz)
def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_in: QuizCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new quiz.
    """
    quiz = crud_assessment.create_quiz(
        db=db, obj_in=quiz_in, creator_id=current_user.id
    )
    return quiz

@router.get("/quizzes", response_model=List[Quiz])
def read_quizzes(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all quizzes.
    """
    quizzes = crud_assessment.get_quizzes(db=db, skip=skip, limit=limit)
    return quizzes

@router.post("/quizzes/{quiz_id}/attempt", response_model=QuizAttempt)
def attempt_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_id: int,
    answers: dict,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Attempt a quiz.
    """
    attempt = crud_assessment.attempt_quiz(
        db=db, quiz_id=quiz_id, user_id=current_user.id, answers=answers
    )
    return attempt

# Flashcard endpoints
@router.post("/flashcards", response_model=Flashcard)
def create_flashcard(
    *,
    db: Session = Depends(deps.get_db),
    flashcard_in: FlashcardCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new flashcard.
    """
    flashcard = crud_assessment.create_flashcard(
        db=db, obj_in=flashcard_in, creator_id=current_user.id
    )
    return flashcard

@router.get("/flashcards", response_model=List[Flashcard])
def read_flashcards(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all flashcards.
    """
    flashcards = crud_assessment.get_flashcards(db=db, skip=skip, limit=limit)
    return flashcards

@router.put("/flashcards/{flashcard_id}", response_model=Flashcard)
def update_flashcard(
    *,
    db: Session = Depends(deps.get_db),
    flashcard_id: int,
    flashcard_in: FlashcardUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a flashcard.
    """
    flashcard = crud_assessment.get_flashcard(db=db, id=flashcard_id)
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    flashcard = crud_assessment.update_flashcard(
        db=db, db_obj=flashcard, obj_in=flashcard_in
    )
    return flashcard

# Exam endpoints
@router.post("/exams", response_model=Exam)
def create_exam(
    *,
    db: Session = Depends(deps.get_db),
    exam_in: ExamCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new exam.
    """
    exam = crud_assessment.create_exam(
        db=db, obj_in=exam_in, creator_id=current_user.id
    )
    return exam

@router.get("/exams", response_model=List[Exam])
def read_exams(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all exams.
    """
    exams = crud_assessment.get_exams(db=db, skip=skip, limit=limit)
    return exams

@router.post("/exams/{exam_id}/attempt", response_model=ExamAttempt)
def attempt_exam(
    *,
    db: Session = Depends(deps.get_db),
    exam_id: int,
    answers: dict,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Attempt an exam.
    """
    attempt = crud_assessment.attempt_exam(
        db=db, exam_id=exam_id, user_id=current_user.id, answers=answers
    )
    return attempt 