import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime
from app.main import app
from app.models.learning_path import (
    LearningPathCreate,
    LearningPathStepCreate,
    ContentType,
    ProgressStatus
)

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "id": str(uuid4()),
        "email": "test@example.com"
    }

@pytest.fixture
def test_learning_path_data(test_user):
    return {
        "title": "Test Learning Path",
        "description": "Test Description",
        "is_public": True,
        "difficulty_level": "beginner",
        "estimated_duration": 60,
        "tags": ["test", "python"],
        "created_by": test_user["id"]
    }

@pytest.fixture
def test_learning_path_step_data():
    return {
        "title": "Test Step",
        "description": "Test Step Description",
        "step_order": 1,
        "content_type": ContentType.TEXT,
        "content_id": str(uuid4()),
        "learning_path_id": str(uuid4())
    }

@pytest.fixture
def test_user_progress_data(test_user):
    return {
        "status": ProgressStatus.IN_PROGRESS,
        "started_at": datetime.utcnow().isoformat(),
        "learning_path_id": str(uuid4()),
        "step_id": str(uuid4()),
        "user_id": test_user["id"]
    }

def test_create_learning_path(test_api_user):
    response = client.post(
        "/api/v1/learning-paths/",
        json={
            "title": "Test Path",
            "description": "Test Description",
            "is_public": True,
            "difficulty_level": "beginner",
            "estimated_duration": 60,
            "tags": ["test"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Path"
    assert data["created_by"] == test_api_user["id"]

def test_get_learning_paths(test_api_user):
    response = client.get(
        "/api/v1/learning-paths/",
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_my_learning_paths(test_api_user):
    response = client.get(
        "/api/v1/learning-paths/my",
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_public_learning_paths():
    response = client.get("/api/v1/learning-paths/public")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_learning_path(test_api_user):
    # First create a learning path
    create_response = client.post(
        "/api/v1/learning-paths/",
        json={
            "title": "Test Path",
            "description": "Test Description",
            "is_public": True,
            "difficulty_level": "beginner",
            "estimated_duration": 60,
            "tags": ["test"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    path_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(
        f"/api/v1/learning-paths/{path_id}",
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == path_id

def test_update_learning_path(test_api_user):
    # First create a learning path
    create_response = client.post(
        "/api/v1/learning-paths/",
        json={
            "title": "Test Path",
            "description": "Test Description",
            "is_public": True,
            "difficulty_level": "beginner",
            "estimated_duration": 60,
            "tags": ["test"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    path_id = create_response.json()["id"]
    
    # Then update it
    update_data = {
        "title": "Updated Path"
    }
    response = client.put(
        f"/api/v1/learning-paths/{path_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]

def test_delete_learning_path(test_api_user):
    # First create a learning path
    create_response = client.post(
        "/api/v1/learning-paths/",
        json={
            "title": "Test Path",
            "description": "Test Description",
            "is_public": True,
            "difficulty_level": "beginner",
            "estimated_duration": 60,
            "tags": ["test"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    path_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(
        f"/api/v1/learning-paths/{path_id}",
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(
        f"/api/v1/learning-paths/{path_id}",
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert get_response.status_code == 404

def test_create_learning_path_step(test_api_user):
    # First create a learning path
    create_path_response = client.post(
        "/api/v1/learning-paths/",
        json={
            "title": "Test Path",
            "description": "Test Description",
            "is_public": True,
            "difficulty_level": "beginner",
            "estimated_duration": 60,
            "tags": ["test"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    path_id = create_path_response.json()["id"]
    
    # Then create a step
    step_data = {
        "title": "Test Step",
        "description": "Test Step Description",
        "step_order": 1,
        "content_type": "text",
        "content": "Test content"
    }
    response = client.post(
        f"/api/v1/learning-paths/{path_id}/steps",
        json=step_data,
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == step_data["title"]
    assert data["step_order"] == step_data["step_order"]

def test_get_learning_path_steps(test_api_user):
    # First create a learning path and step
    create_path_response = client.post(
        "/api/v1/learning-paths/",
        json={
            "title": "Test Path",
            "description": "Test Description",
            "is_public": True,
            "difficulty_level": "beginner",
            "estimated_duration": 60,
            "tags": ["test"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    path_id = create_path_response.json()["id"]
    
    # Create a step
    step_data = {
        "title": "Test Step",
        "description": "Test Step Description",
        "step_order": 1,
        "content_type": "text",
        "content": "Test content"
    }
    client.post(
        f"/api/v1/learning-paths/{path_id}/steps",
        json=step_data,
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    
    # Get steps
    response = client.get(
        f"/api/v1/learning-paths/{path_id}/steps",
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_create_user_progress(test_api_user):
    # First create a learning path and step
    create_path_response = client.post(
        "/api/v1/learning-paths/",
        json={
            "title": "Test Path",
            "description": "Test Description",
            "is_public": True,
            "difficulty_level": "beginner",
            "estimated_duration": 60,
            "tags": ["test"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    path_id = create_path_response.json()["id"]
    
    # Create a step
    step_data = {
        "title": "Test Step",
        "description": "Test Step Description",
        "step_order": 1,
        "content_type": "text",
        "content": "Test content"
    }
    step_response = client.post(
        f"/api/v1/learning-paths/{path_id}/steps",
        json=step_data,
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    step_id = step_response.json()["id"]
    
    # Create progress
    progress_data = {
        "status": "in_progress"
    }
    response = client.post(
        "/api/v1/learning-paths/progress",
        json={
            "learning_path_id": path_id,
            "step_id": step_id,
            "status": progress_data["status"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["learning_path_id"] == path_id
    assert data["step_id"] == step_id
    assert data["status"] == progress_data["status"]

def test_get_user_progress(test_api_user):
    # First create a learning path, step, and progress
    create_path_response = client.post(
        "/api/v1/learning-paths/",
        json={
            "title": "Test Path",
            "description": "Test Description",
            "is_public": True,
            "difficulty_level": "beginner",
            "estimated_duration": 60,
            "tags": ["test"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    path_id = create_path_response.json()["id"]
    
    # Create a step
    step_data = {
        "title": "Test Step",
        "description": "Test Step Description",
        "step_order": 1,
        "content_type": "text",
        "content": "Test content"
    }
    client.post(
        f"/api/v1/learning-paths/{path_id}/steps",
        json=step_data,
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    
    # Create progress
    progress_data = {
        "status": "in_progress"
    }
    client.post(
        "/api/v1/learning-paths/progress",
        json={
            "learning_path_id": path_id,
            "step_id": step_data["step_order"],
            "status": progress_data["status"]
        },
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    
    # Get progress
    response = client.get(
        f"/api/v1/learning-paths/{path_id}/progress",
        headers={"Authorization": f"Bearer {test_api_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0 