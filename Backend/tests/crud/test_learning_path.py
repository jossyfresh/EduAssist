import pytest
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.crud_learning_path import crud_learning_path, crud_learning_path_step, crud_content_item, crud_user_progress
from app.models.learning_path import (
    LearningPathCreate,
    LearningPathUpdate,
    LearningPathStepCreate,
    LearningPathStepUpdate,
    ContentItemCreate,
    UserProgressCreate,
    UserProgressUpdate,
    ContentType,
    ProgressStatus
)

@pytest.fixture
def test_user_id():
    return 1  # Using integer ID instead of UUID

@pytest.fixture
def test_learning_path_data(test_user_id):
    return LearningPathCreate(
        title="Test Learning Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test", "python"],
        created_by=test_user_id
    )

@pytest.fixture
def test_learning_path_step_data(test_user_id):
    return LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        step_order=1,
        content_type=ContentType.TEXT,
        content_id=1,  # Using integer ID instead of UUID
        learning_path_id=1  # Using integer ID instead of UUID
    )

@pytest.fixture
def test_content_item_data(test_user_id):
    return ContentItemCreate(
        content_type=ContentType.TEXT,
        title="Test Content",
        content="Test content text",
        metadata={"key": "value"},
        created_by=test_user_id
    )

@pytest.fixture
def test_user_progress_data(test_user_id):
    return UserProgressCreate(
        status=ProgressStatus.IN_PROGRESS,
        started_at=datetime.utcnow(),
        learning_path_id=1,  # Using integer ID instead of UUID
        step_id=1,  # Using integer ID instead of UUID
        user_id=test_user_id
    )

def test_create_learning_path(db: Session, test_learning_path_data):
    # Create learning path
    created_path = crud_learning_path.create_with_steps(db, obj_in=test_learning_path_data, created_by=1)
    assert created_path.title == test_learning_path_data.title
    assert created_path.description == test_learning_path_data.description
    assert created_path.is_public == test_learning_path_data.is_public
    assert created_path.created_by == 1

def test_get_learning_path(db: Session, test_learning_path_data):
    # Create and then get learning path
    created_path = crud_learning_path.create_with_steps(db, obj_in=test_learning_path_data, created_by=1)
    retrieved_path = crud_learning_path.get(db, id=created_path.id)
    assert retrieved_path == created_path

def test_get_learning_paths_by_user(db: Session, test_learning_path_data, test_user_id):
    # Create learning path
    created_path = crud_learning_path.create_with_steps(db, obj_in=test_learning_path_data, created_by=test_user_id)
    paths = crud_learning_path.get_by_user(db, user_id=test_user_id)
    assert len(paths) > 0
    assert created_path in paths

def test_get_public_learning_paths(db: Session, test_learning_path_data):
    # Create public learning path
    created_path = crud_learning_path.create_with_steps(db, obj_in=test_learning_path_data, created_by=1)
    paths = crud_learning_path.get_public(db)
    assert len(paths) > 0
    assert created_path in paths

def test_update_learning_path(db: Session, test_learning_path_data):
    # Create learning path
    created_path = crud_learning_path.create_with_steps(db, obj_in=test_learning_path_data, created_by=1)
    update_data = LearningPathUpdate(title="Updated Title")
    updated_path = crud_learning_path.update(db, db_obj=created_path, obj_in=update_data)
    assert updated_path.title == "Updated Title"
    assert updated_path.id == created_path.id

def test_delete_learning_path(db: Session, test_learning_path_data):
    # Create learning path
    created_path = crud_learning_path.create_with_steps(db, obj_in=test_learning_path_data, created_by=1)
    deleted_path = crud_learning_path.remove(db, id=created_path.id)
    assert deleted_path == created_path
    assert crud_learning_path.get(db, id=created_path.id) is None

def test_create_learning_path_step(db: Session, test_learning_path_step_data):
    # Create learning path first
    learning_path_data = LearningPathCreate(
        title="Test Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test"]
    )
    created_path = crud_learning_path.create_with_steps(db, obj_in=learning_path_data, created_by=1)
    
    # Create learning path step
    step_data = LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        step_order=1,
        content_type=ContentType.TEXT,
        content_id=1,
        learning_path_id=created_path.id
    )
    created_step = crud_learning_path_step.create(db, obj_in=step_data)
    assert created_step.title == step_data.title
    assert created_step.learning_path_id == created_path.id

def test_get_learning_path_steps(db: Session, test_learning_path_step_data):
    # Create learning path first
    learning_path_data = LearningPathCreate(
        title="Test Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test"]
    )
    created_path = crud_learning_path.create_with_steps(db, obj_in=learning_path_data, created_by=1)
    
    # Create learning path step
    step_data = LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        step_order=1,
        content_type=ContentType.TEXT,
        content_id=1,
        learning_path_id=created_path.id
    )
    created_step = crud_learning_path_step.create(db, obj_in=step_data)
    steps = crud_learning_path_step.get_by_learning_path(db, learning_path_id=created_path.id)
    assert len(steps) > 0
    assert created_step in steps

def test_create_content_item(db: Session, test_content_item_data):
    # Create content item
    created_item = crud_content_item.create(db, obj_in=test_content_item_data)
    assert created_item.title == test_content_item_data.title
    assert created_item.content_type == test_content_item_data.content_type
    assert created_item.created_by == 1

def test_get_content_items_by_type(db: Session, test_content_item_data):
    # Create content item
    created_item = crud_content_item.create(db, obj_in=test_content_item_data)
    items = crud_content_item.get_by_type(db, content_type=test_content_item_data.content_type)
    assert len(items) > 0
    assert created_item in items

def test_create_user_progress(db: Session, test_user_progress_data):
    # Create learning path first
    learning_path_data = LearningPathCreate(
        title="Test Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test"]
    )
    created_path = crud_learning_path.create_with_steps(db, obj_in=learning_path_data, created_by=1)
    
    # Create learning path step
    step_data = LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        step_order=1,
        content_type=ContentType.TEXT,
        content_id=1,
        learning_path_id=created_path.id
    )
    created_step = crud_learning_path_step.create(db, obj_in=step_data)
    
    # Create user progress
    progress_data = UserProgressCreate(
        status=ProgressStatus.IN_PROGRESS,
        started_at=datetime.now(),
        learning_path_id=created_path.id,
        step_id=created_step.id,
        user_id=1
    )
    created_progress = crud_user_progress.create(db, obj_in=progress_data)
    assert created_progress.status == progress_data.status
    assert created_progress.learning_path_id == created_path.id
    assert created_progress.step_id == created_step.id 