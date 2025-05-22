# EduAssist API Documentation

## Authentication Endpoints

### Register User

- **URL**: `/auth/register`
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

- **URL**: `/auth/login`
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

## User Endpoints

- **Base Path**: `/users`

### List Users (Superuser only)

- **GET** `/users/`

### Create User (Superuser only)

- **POST** `/users/`

### Get Current User

- **GET** `/users/me`

### Update Current User

- **PUT** `/users/me`

### Get User by ID

- **GET** `/users/{user_id}`

### Delete User by ID (Superuser only)

- **DELETE** `/users/{user_id}`

## Content Management

### Upload Files

- **POST** `/content/upload`
  - Upload multiple files
  - Request: `multipart/form-data` with `files` field
  - Response:
    ```json
    {
      "batch_id": "uuid",
      "files": [
        {
          "id": "uuid",
          "title": "filename",
          "content_type": "FILE",
          "content": "base64_content",
          "meta": {
            "filename": "original_filename",
            "content_type": "mime_type",
            "size": 1234,
            "batch_id": "uuid"
          },
          "description": "Uploaded file: filename",
          "created_by": "user_id",
          "created_at": "timestamp",
          "updated_at": "timestamp"
        }
      ]
    }
    ```

### Batch File Management

#### Get Batch Files

- **GET** `/content/batch/{batch_id}`
  - Get all files in a batch
  - Response:
    ```json
    {
      "batch_id": "uuid",
      "files": [ ...Content objects... ]
    }
    ```

#### Add Files to Batch

- **POST** `/content/batch/{batch_id}/files`
  - Add files to an existing batch
  - Request: `multipart/form-data` with `files` field
  - Response:
    ```json
    {
      "batch_id": "uuid",
      "added_files": [ ...Content objects... ]
    }
    ```

#### Remove File from Batch

- **DELETE** `/content/batch/{batch_id}/files/{file_id}`
  - Remove a file from a batch
  - Response:
    ```json
    {
      "batch_id": "uuid",
      "remaining_files": [ ...Content objects... ]
    }
    ```

### Create YouTube Video Content (with Transcript Extraction)

- **POST** `/content/video`
  - Create new video content from a YouTube URL. Extracts transcript and associates with a course if provided.
  - Request Body:
    ```json
    {
      "video_url": "https://youtube.com/watch?v=...",
      "course_id": "uuid (optional)"
    }
    ```
  - Response:
    ```json
    {
      "id": "uuid",
      "title": "YouTube Video Title",
      "content_type": "VIDEO",
      "content": "https://youtube.com/watch?v=...",
      "meta": {
        "video_url": "...",
        "transcript": "...",
        "youtube_title": "...",
        "youtube_description": "...",
        "duration": "...",
        "thumbnail": "..."
      },
      "description": "YouTube video description",
      "created_by": "user_id",
      "created_at": "timestamp",
      "updated_at": "timestamp",
      "course_id": "uuid (if provided)"
    }
    ```

### Generate Content Using AI

- **POST** `/content/generate`
  - Generate content (quiz, summary, flashcard, etc.) using AI, with a custom prompt and parameters.
  - Request Body:
    ```json
    {
      "content_type": "quiz|summary|flashcard|youtube_suggestions",
      "parameters": { "context": "string", ... },
      "provider": "openai|gemini"
    }
    ```
  - Response:
    ```json
    {
      "content": "...generated content..."
    }
    ```

### Generate Context-Aware Content (Aggregates All Course Context)

- **POST** `/content/generate-contextual`
  - Generate content (quiz, notes, flashcards, etc.) using all course-related context (transcripts, files, text, etc.).
  - Request Body:
    ```json
    {
      "course_id": "uuid (optional)",
      "learning_path_id": "uuid (optional)",
      "content_type": "quiz|summary|flashcard|notes|...",
      "provider": "openai|gemini (default: openai)",
      "extra_parameters": { ... } // Optional, merged into AI prompt
    }
    ```
  - Response:
    ```json
    {
      "content": "...generated content..."
    }
    ```

---

## Course Management

### Create Course

- **POST** `/courses/`
  - Request Body:
    ```json
    {
      "title": "string",
      "description": "string (optional)"
    }
    ```
  - Response: Course object

### Get Course

- **GET** `/courses/{course_id}`
  - Response: Course object

### List Courses

- **GET** `/courses/`
  - Response: List of Course objects

### Update Course

- **PUT** `/courses/{course_id}`
  - Request Body:
    ```json
    {
      "title": "string (optional)",
      "description": "string (optional)"
    }
    ```
  - Response: Updated Course object

### Delete Course

- **DELETE** `/courses/{course_id}`
  - Response: Deleted Course object

### List Course Content

- **GET** `/courses/{course_id}/contents`
  - Response: List of Content objects

### Add Content to Course

- **POST** `/courses/{course_id}/contents/{content_id}`
  - Response: Content object (now associated with course)

### Remove Content from Course

- **DELETE** `/courses/{course_id}/contents/{content_id}`
  - Response: Content object (disassociated from course)

### List Course Learning Paths

- **GET** `/courses/{course_id}/learning-paths`
  - Response: List of LearningPath objects

### Add Learning Path to Course

- **POST** `/courses/{course_id}/learning-paths/{learning_path_id}`
  - Response: LearningPath object (now associated with course)

### Remove Learning Path from Course

- **DELETE** `/courses/{course_id}/learning-paths/{learning_path_id}`
  - Response: LearningPath object (disassociated from course)

---

## Learning Path Management

### Create Learning Path

- **POST** `/learning-paths/`
  - Request Body:
    ```json
    {
      "title": "string",
      "description": "string (optional)",
      "is_public": true,
      "difficulty_level": "string (optional)",
      "estimated_duration": 120,
      "tags": ["string", ...]
    }
    ```
  - Response: LearningPathInDB object

### List All Learning Paths (for current user)

- **GET** `/learning-paths/`
  - Response: List of LearningPathInDB objects

### List My Learning Paths

- **GET** `/learning-paths/my`
  - Response: List of LearningPathInDB objects

### List Public Learning Paths

- **GET** `/learning-paths/public`
  - Response: List of LearningPathInDB objects

### Get Learning Path by ID

- **GET** `/learning-paths/{path_id}`
  - Response: LearningPathInDB object

### Update Learning Path

- **PUT** `/learning-paths/{path_id}`
  - Request Body:
    ```json
    {
      "title": "string (optional)",
      "description": "string (optional)",
      "is_public": true,
      "difficulty_level": "string (optional)",
      "estimated_duration": 120,
      "tags": ["string", ...]
    }
    ```
  - Response: Updated LearningPathInDB object

### Delete Learning Path

- **DELETE** `/learning-paths/{path_id}`
  - Response: `{ "status": "success" }`

### Add Step to Learning Path

- **POST** `/learning-paths/{path_id}/steps`
  - Request Body:
    ```json
    {
      "title": "string",
      "description": "string (optional)",
      "content_type": "text|video|file|other",
      "content": "string (optional)",
      "order": 1
    }
    ```
  - Response: LearningPathStepInDB object

### List Steps in Learning Path

- **GET** `/learning-paths/{path_id}/steps`
  - Response: List of LearningPathStepInDB objects

### Create Content Item

- **POST** `/learning-paths/content`
  - Request Body:
    ```json
    {
      "title": "string",
      "description": "string (optional)",
      "content_type": "text|video|file|other",
      "content": "string"
    }
    ```
  - Response: Content object

### Create or Update User Progress

- **POST** `/learning-paths/progress`
  - Request Body:
    ```json
    {
      "user_id": "uuid",
      "learning_path_id": "uuid",
      "step_id": 1,
      "status": "completed|in_progress|not_started",
      "score": 100
    }
    ```
  - Response: UserProgressInDB object

### Get User Progress for a Learning Path

- **GET** `/learning-paths/progress/{path_id}`
  - Response: List of UserProgressInDB objects

---

All endpoints require authentication. See the main API documentation for authentication and error response details.
