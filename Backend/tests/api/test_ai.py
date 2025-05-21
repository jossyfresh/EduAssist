import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.services.content_generator import ContentGenerator

@pytest.mark.usefixtures("client", "test_headers")
def test_generate_quiz(client, test_headers):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "quiz",
            "parameters": {
                "topic": "Python Programming",
                "difficulty": "beginner",
                "num_questions": 3
            },
            "provider": "openai"
        },
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], dict)
    assert "questions" in data["content"]
    assert len(data["content"]["questions"]) > 0

@pytest.mark.usefixtures("client", "test_headers")
def test_generate_quiz_with_gemini(client, test_headers):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "quiz",
            "parameters": {
                "topic": "Python Programming",
                "difficulty": "beginner",
                "num_questions": 3
            },
            "provider": "gemini"
        },
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], dict)
    assert "questions" in data["content"]
    assert len(data["content"]["questions"]) > 0

@pytest.mark.usefixtures("client", "test_headers")
def test_generate_summary(client, test_headers):
    text = """
    Python is a high-level, interpreted programming language known for its simplicity and readability.
    It was created by Guido van Rossum and first released in 1991. Python's design philosophy emphasizes
    code readability with its notable use of significant whitespace. Its syntax allows programmers to
    express concepts in fewer lines of code than would be possible in languages such as C++ or Java.
    """
    
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "summary",
            "parameters": {
                "text": text
            },
            "provider": "openai"
        },
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], str)
    assert len(data["content"]) > 0

@pytest.mark.usefixtures("client", "test_headers")
def test_generate_summary_with_gemini(client, test_headers):
    text = """
    Python is a high-level, interpreted programming language known for its simplicity and readability.
    It was created by Guido van Rossum and first released in 1991. Python's design philosophy emphasizes
    code readability with its notable use of significant whitespace. Its syntax allows programmers to
    express concepts in fewer lines of code than would be possible in languages such as C++ or Java.
    """
    
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "summary",
            "parameters": {
                "text": text
            },
            "provider": "gemini"
        },
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], str)
    assert len(data["content"]) > 0

@pytest.mark.usefixtures("client", "test_headers")
def test_generate_flashcards(client, test_headers):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "flashcard",
            "parameters": {
                "topic": "Python Data Types",
                "num_cards": 5
            },
            "provider": "openai"
        },
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], list)
    assert len(data["content"]) > 0
    assert all("front" in card and "back" in card for card in data["content"])

@pytest.mark.usefixtures("client", "test_headers")
def test_generate_flashcards_with_gemini(client, test_headers):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "flashcard",
            "parameters": {
                "topic": "Python Data Types",
                "num_cards": 5
            },
            "provider": "gemini"
        },
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], list)
    assert len(data["content"]) > 0
    assert all("front" in card and "back" in card for card in data["content"])

@pytest.mark.usefixtures("client", "test_headers")
def test_generate_youtube_suggestions(client, test_headers):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "youtube_suggestions",
            "parameters": {
                "topic": "Python Programming",
                "num_suggestions": 5
            },
            "provider": "openai"
        },
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], list)
    assert len(data["content"]) > 0
    assert all("title" in video and "url" in video for video in data["content"])

@pytest.mark.usefixtures("client", "test_headers")
def test_generate_youtube_suggestions_with_gemini(client, test_headers):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "youtube_suggestions",
            "parameters": {
                "topic": "Python Programming",
                "num_suggestions": 5
            },
            "provider": "gemini"
        },
        headers=test_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], list)
    assert len(data["content"]) > 0
    assert all("title" in video and "url" in video for video in data["content"])

@pytest.mark.usefixtures("client", "test_headers")
def test_invalid_provider(client, test_headers):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "quiz",
            "parameters": {
                "topic": "Python Programming"
            },
            "provider": "invalid_provider"
        },
        headers=test_headers
    )
    assert response.status_code == 400

@pytest.mark.usefixtures("client", "test_headers")
def test_invalid_content_type(client, test_headers):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "content_type": "invalid_type",
            "parameters": {
                "topic": "Python Programming"
            },
            "provider": "openai"
        },
        headers=test_headers
    )
    assert response.status_code == 400 