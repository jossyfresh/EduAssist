import pytest
from uuid import UUID, uuid4
from datetime import datetime
from app.crud.learning_path import learning_path, learning_path_step, content_item, user_progress
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
from app.core.supabase import supabase

@pytest.fixture
def test_user_id():
    return str(uuid4())

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
        content_id=str(uuid4()),
        learning_path_id=str(uuid4())
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
        learning_path_id=str(uuid4()),
        step_id=str(uuid4()),
        user_id=test_user_id
    )

def test_create_learning_path(test_learning_path_data):
    # Create learning path
    created_path = learning_path.create(supabase, obj_in=test_learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    assert created_path.title == test_learning_path_data.title
    assert created_path.description == test_learning_path_data.description
    assert created_path.is_public == test_learning_path_data.is_public
    assert created_path.created_by == UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396")

def test_get_learning_path(test_learning_path_data):
    # Create and then get learning path
    created_path = learning_path.create(supabase, obj_in=test_learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    retrieved_path = learning_path.get(supabase, id=created_path.id)
    assert retrieved_path == created_path

def test_get_learning_paths_by_user(test_learning_path_data, test_user_id):
    # Create learning path
    created_path = learning_path.create(supabase, obj_in=test_learning_path_data, created_by=test_user_id)
    paths = learning_path.get_by_user(supabase, user_id=test_user_id)
    assert len(paths) > 0
    assert created_path in paths

def test_get_public_learning_paths(test_learning_path_data):
    # Create public learning path
    created_path = learning_path.create(supabase, obj_in=test_learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    paths = learning_path.get_public(supabase)
    assert len(paths) > 0
    assert created_path in paths

def test_update_learning_path(test_learning_path_data):
    # Create learning path
    created_path = learning_path.create(supabase, obj_in=test_learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    update_data = LearningPathUpdate(title="Updated Title")
    updated_path = learning_path.update(supabase, id=created_path.id, obj_in=update_data)
    assert updated_path.title == "Updated Title"
    assert updated_path.id == created_path.id

def test_delete_learning_path(test_learning_path_data):
    # Create learning path
    created_path = learning_path.create(supabase, obj_in=test_learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    deleted_path = learning_path.remove(supabase, id=created_path.id)
    assert deleted_path == created_path
    assert learning_path.get(supabase, id=created_path.id) is None

def test_create_learning_path_step(test_learning_path_step_data):
    # Create learning path first
    learning_path_data = LearningPathCreate(
        title="Test Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test"]
    )
    created_path = learning_path.create(supabase, obj_in=learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    
    # Create learning path step
    step_data = LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        step_order=1,
        content_type=ContentType.TEXT,
        content_id=UUID("b8f6e1fc-5f2f-45b9-a884-a794863032ba"),
        learning_path_id=created_path.id
    )
    created_step = learning_path_step.create(supabase, obj_in=step_data)
    assert created_step.title == step_data.title
    assert created_step.learning_path_id == created_path.id

def test_get_learning_path_steps(test_learning_path_step_data):
    # Create learning path first
    learning_path_data = LearningPathCreate(
        title="Test Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test"]
    )
    created_path = learning_path.create(supabase, obj_in=learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    
    # Create learning path step
    step_data = LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        step_order=1,
        content_type=ContentType.TEXT,
        content_id=UUID("f638cfa8-9bf6-4bad-b156-4b088ac02d9c"),
        learning_path_id=created_path.id
    )
    created_step = learning_path_step.create(supabase, obj_in=step_data)
    steps = learning_path_step.get_by_learning_path(supabase, learning_path_id=created_path.id)
    assert len(steps) > 0
    assert created_step in steps

def test_create_content_item(test_content_item_data):
    # Create content item
    created_item = content_item.create(supabase, obj_in=test_content_item_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    assert created_item.title == test_content_item_data.title
    assert created_item.content_type == test_content_item_data.content_type
    assert created_item.created_by == UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396")

def test_get_content_items_by_type(test_content_item_data):
    # Create content item
    created_item = content_item.create(supabase, obj_in=test_content_item_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    items = content_item.get_by_type(supabase, content_type=test_content_item_data.content_type)
    assert len(items) > 0
    assert created_item in items

def test_create_user_progress(test_user_progress_data):
    # Create learning path first
    learning_path_data = LearningPathCreate(
        title="Test Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test"]
    )
    created_path = learning_path.create(supabase, obj_in=learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    
    # Create learning path step
    step_data = LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        step_order=1,
        content_type=ContentType.TEXT,
        content_id=UUID("b8f6e1fc-5f2f-45b9-a884-a794863032ba"),
        learning_path_id=created_path.id
    )
    created_step = learning_path_step.create(supabase, obj_in=step_data)
    
    # Create user progress
    progress_data = UserProgressCreate(
        status=ProgressStatus.IN_PROGRESS,
        started_at=datetime.now(),
        learning_path_id=created_path.id,
        step_id=created_step.id
    )
    created_progress = user_progress.create(supabase, obj_in=progress_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    assert created_progress.status == progress_data.status
    assert created_progress.learning_path_id == created_path.id
    assert created_progress.step_id == created_step.id

def test_get_user_progress(test_user_progress_data):
    # Create learning path first
    learning_path_data = LearningPathCreate(
        title="Test Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test"]
    )
    created_path = learning_path.create(supabase, obj_in=learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    
    # Create learning path step
    step_data = LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        step_order=1,
        content_type=ContentType.TEXT,
        content_id=UUID("f638cfa8-9bf6-4bad-b156-4b088ac02d9c"),
        learning_path_id=created_path.id
    )
    created_step = learning_path_step.create(supabase, obj_in=step_data)
    
    # Create user progress
    progress_data = UserProgressCreate(
        status=ProgressStatus.IN_PROGRESS,
        started_at=datetime.now(),
        learning_path_id=created_path.id,
        step_id=created_step.id
    )
    created_progress = user_progress.create(supabase, obj_in=progress_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    retrieved_progress = user_progress.get_by_learning_path(supabase, learning_path_id=created_path.id)
    assert len(retrieved_progress) > 0
    assert created_progress in retrieved_progress

def test_update_user_progress(test_user_progress_data):
    # Create learning path first
    learning_path_data = LearningPathCreate(
        title="Test Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test"]
    )
    created_path = learning_path.create(supabase, obj_in=learning_path_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    
    # Create learning path step
    step_data = LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        step_order=1,
        content_type=ContentType.TEXT,
        content_id=UUID("659de72f-0a75-49c8-8c58-a86efba99f51"),
        learning_path_id=created_path.id
    )
    created_step = learning_path_step.create(supabase, obj_in=step_data)
    
    # Create user progress
    progress_data = UserProgressCreate(
        status=ProgressStatus.IN_PROGRESS,
        started_at=datetime.now(),
        learning_path_id=created_path.id,
        step_id=created_step.id
    )
    created_progress = user_progress.create(supabase, obj_in=progress_data, created_by=UUID("f53783aa-84ea-4bc0-99e7-b59b9a184396"))
    
    # Update progress
    update_data = UserProgressUpdate(status=ProgressStatus.COMPLETED)
    updated_progress = user_progress.update(supabase, id=created_progress.id, obj_in=update_data)
    assert updated_progress.status == ProgressStatus.COMPLETED
    assert updated_progress.id == created_progress.id 