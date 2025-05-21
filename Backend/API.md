# EduAssist API Documentation

## Authentication Endpoints

### Register User

- **URL**: `/api/v1/auth/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "string",
    "username": "string",
    "password": "string",
    "full_name": "string (optional)",
    "is_active": "boolean (optional, default: true)",
    "is_superuser": "boolean (optional, default: false)"
  }
  ```
- **Example Request**:
  ```json
  {
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: Email already registered
  - `400 Bad Request`: Username already taken

### Login

- **URL**: `/api/v1/auth/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Example Request**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized`: Incorrect email or password
  - `400 Bad Request`: Inactive user

## Content Management Endpoints

### Upload File

- **URL**: `/api/v1/content/upload`
- **Method**: `POST`
- **Headers**:
  - `Authorization`: Bearer {token}
- **Request Body**:
  - `file`: File (multipart/form-data)
- **Example Request**:

  ```
  Content-Type: multipart/form-data
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

  file: [PDF/Image/Video file]
  ```

- **Response**:
  ```json
  {
    "id": 1,
    "title": "uploaded_file.pdf",
    "description": "Uploaded file description",
    "content_type": "pdf",
    "content": "file_url_or_content",
    "created_by": "user@example.com",
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T10:00:00Z"
  }
  ```

### Create Text Content

- **URL**: `/api/v1/content/text`
- **Method**: `POST`
- **Headers**:
  - `Authorization`: Bearer {token}
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "content_type": "text",
    "content": "string"
  }
  ```
- **Example Request**:
  ```json
  {
    "title": "Introduction to Python",
    "description": "A beginner's guide to Python programming",
    "content_type": "text",
    "content": "Python is a high-level programming language..."
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Introduction to Python",
    "description": "A beginner's guide to Python programming",
    "content_type": "text",
    "content": "Python is a high-level programming language...",
    "created_by": "user@example.com",
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T10:00:00Z"
  }
  ```

### Create Video Content

- **URL**: `/api/v1/content/video`
- **Method**: `POST`
- **Headers**:
  - `Authorization`: Bearer {token}
- **Request Body**:
  ```json
  {
    "video_url": "string"
  }
  ```
- **Example Request**:
  ```json
  {
    "video_url": "https://example.com/video.mp4"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Video Title",
    "description": "Video Description",
    "content_type": "video",
    "content": "https://example.com/video.mp4",
    "created_by": "user@example.com",
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T10:00:00Z"
  }
  ```

### Get Content

- **URL**: `/api/v1/content/{content_id}`
- **Method**: `GET`
- **Headers**:
  - `Authorization`: Bearer {token}
- **Example Request**:
  ```
  GET /api/v1/content/1
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Content Title",
    "description": "Content Description",
    "content_type": "text",
    "content": "Content body...",
    "created_by": "user@example.com",
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T10:00:00Z"
  }
  ```

### Update Content

- **URL**: `/api/v1/content/{content_id}`
- **Method**: `PUT`
- **Headers**:
  - `Authorization`: Bearer {token}
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "content_type": "string",
    "content": "string"
  }
  ```
- **Example Request**:
  ```json
  {
    "title": "Updated Title",
    "description": "Updated Description",
    "content_type": "text",
    "content": "Updated content..."
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Updated Title",
    "description": "Updated Description",
    "content_type": "text",
    "content": "Updated content...",
    "created_by": "user@example.com",
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T11:00:00Z"
  }
  ```

### Delete Content

- **URL**: `/api/v1/content/{content_id}`
- **Method**: `DELETE`
- **Headers**:
  - `Authorization`: Bearer {token}
- **Example Request**:
  ```
  DELETE /api/v1/content/1
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Deleted Content",
    "description": "Content Description",
    "content_type": "text",
    "content": "Content body...",
    "created_by": "user@example.com",
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T10:00:00Z"
  }
  ```

### Generate Content

- **URL**: `/api/v1/content/generate`
- **Method**: `POST`
- **Headers**:
  - `Authorization`: Bearer {token}
- **Request Body**:
  ```json
  {
    "content_type": "string",
    "parameters": {
      "prompt": "string",
      "max_tokens": "integer"
    },
    "provider": "string (optional, default: openai)"
  }
  ```
- **Example Request**:
  ```json
  {
    "content_type": "quiz",
    "parameters": {
      "topic": "Python Programming",
      "difficulty": "beginner",
      "num_questions": 3
    },
    "provider": "openai"
  }
  ```
- **Response**:
  ```json
  {
    "content": "...AI generated content..."
  }
  ```

## Learning Path Endpoints

### Create Learning Path

- **URL**: `/api/v1/learning-paths`
- **Method**: `POST`
- **Headers**:
  - `Authorization`: Bearer {token}
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "is_public": "boolean",
    "difficulty_level": "string",
    "estimated_duration": "integer",
    "tags": ["string"]
  }
  ```
- **Example Request**:
  ```json
  {
    "title": "Python for Beginners",
    "description": "A comprehensive guide to Python programming",
    "is_public": true,
    "difficulty_level": "beginner",
    "estimated_duration": 30,
    "tags": ["python", "programming", "beginner"]
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Python for Beginners",
    "description": "A comprehensive guide to Python programming",
    "is_public": true,
    "difficulty_level": "beginner",
    "estimated_duration": 30,
    "tags": ["python", "programming", "beginner"],
    "created_by": "user@example.com",
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T10:00:00Z"
  }
  ```
