import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.crud import crud_content
from app.schemas.content import ContentCreate, ContentUpdate
from app.models.enums import ContentType

client = TestClient(app)

@pytest.fixture
def test_content_data():
    return {
        "title": "Test Content",
        "description": "Test Description",
        "content_type": "text",
        "content": "This is test content"
    }

@pytest.fixture
def test_video_url():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def test_create_text_content(db: Session, test_content_data, test_headers):
    response = client.post(
        "/api/v1/content/text",
        json=test_content_data,
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_content_data["title"]
    assert data["description"] == test_content_data["description"]
    assert data["content_type"] == test_content_data["content_type"]
    assert data["content"] == test_content_data["content"]

def test_create_video_content(db: Session, test_video_url, test_headers):
    response = client.post(
        "/api/v1/content/video",
        json={"video_url": test_video_url},
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content_type"] == "video"
    assert "content" in data

def test_get_content(db: Session, test_content_data, test_headers):
    # First create content
    create_response = client.post(
        "/api/v1/content/text",
        json=test_content_data,
        headers=test_headers
    )
    content_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(
        f"/api/v1/content/{content_id}",
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == content_id
    assert data["title"] == test_content_data["title"]

def test_update_content(db: Session, test_content_data, test_headers):
    # First create content
    create_response = client.post(
        "/api/v1/content/text",
        json=test_content_data,
        headers=test_headers
    )
    content_id = create_response.json()["id"]
    
    # Update content
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "content": "Updated content"
    }
    response = client.put(
        f"/api/v1/content/{content_id}",
        json=update_data,
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["content"] == update_data["content"]

def test_delete_content(db: Session, test_content_data, test_headers):
    # First create content
    create_response = client.post(
        "/api/v1/content/text",
        json=test_content_data,
        headers=test_headers
    )
    content_id = create_response.json()["id"]
    
    # Delete content
    response = client.delete(
        f"/api/v1/content/{content_id}",
        headers=test_headers
    )
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(
        f"/api/v1/content/{content_id}",
        headers=test_headers
    )
    assert get_response.status_code == 404

def test_generate_content(db: Session, test_headers):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "quiz",
            "parameters": {
                "topic": "Python Programming",
                "difficulty": "beginner",
                "num_questions": 3
            }
        },
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data

def test_get_youtube_metadata(db: Session, test_video_url, test_headers):
    response = client.get(
        f"/api/v1/content/youtube-metadata?video_url={test_video_url}",
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "description" in data

def test_get_combined_content(db: Session, test_headers):
    response = client.get(
        "/api/v1/content/combined",
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_upload_file(db: Session, test_headers):
    # Create a test file
    test_file_content = b"Test file content"
    files = {
        "file": ("test.txt", test_file_content, "text/plain")
    }
    
    response = client.post(
        "/api/v1/content/upload",
        files=files,
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content_type"] == "file"
    assert "content" in data 