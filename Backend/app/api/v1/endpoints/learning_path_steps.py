from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.learning_path import learning_path_step
from app.models.user import User
from app.schemas.learning_path_step import (
    LearningPathStep,
    LearningPathStepCreate,
    LearningPathStepUpdate,
    LearningPathStepReorder
)

router = APIRouter()

@router.get("/{learning_path_id}/steps", response_model=List[LearningPathStep])
def read_learning_path_steps(
    learning_path_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all steps for a learning path.
    """
    steps = learning_path_step.get_multi_by_learning_path(
        db=db, learning_path_id=learning_path_id
    )
    return steps

@router.post("/{learning_path_id}/steps", response_model=LearningPathStep)
def create_learning_path_step(
    *,
    db: Session = Depends(deps.get_db),
    learning_path_id: int,
    step_in: LearningPathStepCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new learning path step.
    """
    step = learning_path_step.create(
        db=db, obj_in=step_in, learning_path_id=learning_path_id
    )
    return step

@router.put("/{learning_path_id}/steps/{step_id}", response_model=LearningPathStep)
def update_learning_path_step(
    *,
    db: Session = Depends(deps.get_db),
    learning_path_id: int,
    step_id: int,
    step_in: LearningPathStepUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a learning path step.
    """
    step = learning_path_step.get(db=db, id=step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    step = learning_path_step.update(db=db, db_obj=step, obj_in=step_in)
    return step

@router.delete("/{learning_path_id}/steps/{step_id}", response_model=LearningPathStep)
def delete_learning_path_step(
    *,
    db: Session = Depends(deps.get_db),
    learning_path_id: int,
    step_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a learning path step.
    """
    step = learning_path_step.get(db=db, id=step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    step = learning_path_step.remove(db=db, id=step_id)
    return step

@router.post("/{learning_path_id}/steps/reorder", response_model=List[LearningPathStep])
def reorder_learning_path_steps(
    *,
    db: Session = Depends(deps.get_db),
    learning_path_id: int,
    reorder_in: LearningPathStepReorder,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Reorder learning path steps.
    """
    steps = learning_path_step.reorder(
        db=db, learning_path_id=learning_path_id, step_orders=reorder_in.step_orders
    )
    return steps 