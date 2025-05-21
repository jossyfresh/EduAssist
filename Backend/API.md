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

## Content Endpoints

- **Base Path**: `/content`

### Create Text Content

- **URL**: `/content/text`
- **Method**: `POST`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "string",
    "content_type": "text",
    "content": "string",
    "meta": {},
    "description": "string (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "id": "string",
    "title": "string",
    "content_type": "text",
    "content": "string",
    "meta": {},
    "description": "string",
    "created_by": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized`: Not authenticated
  - `400 Bad Request`: Invalid input data

### Create Video Content

- **URL**: `/content/video`
- **Method**: `POST`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "video_url": "string"
  }
  ```
- **Response**: Same as Create Text Content
- **Error Responses**:
  - `401 Unauthorized`: Not authenticated
  - `400 Bad Request`: Invalid input data

### Upload File

- **URL**: `/content/upload`
- **Method**: `POST`
- **Auth Required**: Yes
- **Request Body**: `multipart/form-data`
  - `file`: File to upload
- **Response**: Same as Create Text Content
- **Error Responses**:
  - `401 Unauthorized`: Not authenticated
  - `400 Bad Request`: Invalid file
  - `413 Payload Too Large`: File too large
  - `500 Internal Server Error`: Upload failed

### Get Content by ID

- **URL**: `/content/{content_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **Response**: Same as Create Text Content
- **Error Responses**:
  - `401 Unauthorized`: Not authenticated
  - `404 Not Found`: Content not found

### Update Content

- **URL**: `/content/{content_id}`
- **Method**: `PUT`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "string (optional)",
    "content_type": "string (optional)",
    "content": "string (optional)",
    "meta": {} (optional),
    "description": "string (optional)"
  }
  ```
- **Response**: Same as Create Text Content
- **Error Responses**:
  - `401 Unauthorized`: Not authenticated
  - `403 Forbidden`: Not authorized to update this content
  - `404 Not Found`: Content not found

### Delete Content

- **URL**: `/content/{content_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes
- **Response**: Same as Create Text Content
- **Error Responses**:
  - `401 Unauthorized`: Not authenticated
  - `404 Not Found`: Content not found

### Generate Content (AI)

- **URL**: `/content/generate`
- **Method**: `POST`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "content_type": "string",
    "parameters": {},
    "provider": "string (default: openai)"
  }
  ```
- **Response**:
  ```json
  {
    "content": "string"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized`: Not authenticated
  - `400 Bad Request`: Invalid input data
  - `500 Internal Server Error`: Generation failed

### Get YouTube Metadata

- **URL**: `/content/youtube-metadata`
- **Method**: `GET`
- **Auth Required**: No
- **Query Parameters**:
  - `video_url`: YouTube video URL
- **Response**:
  ```json
  {
    "title": "string",
    "video_url": "string",
    "duration": "integer",
    "description": "string"
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: Invalid video URL

### Get Combined Content

- **URL**: `/content/combined`
- **Method**: `GET`
- **Auth Required**: Yes
- **Response**:
  ```json
  {
    "items": [
      {
        "id": "string",
        "title": "string"
      }
    ]
  }
  ```
- **Error Responses**:
  - `401 Unauthorized`: Not authenticated

## Learning Path Endpoints

- **Base Path**: `/learning-paths`

### Create Learning Path

- **POST** `/learning-paths/`

### List Learning Paths

- **GET** `/learning-paths/`

### List My Learning Paths

- **GET** `/learning-paths/my`

### Get Learning Path by ID

- **GET** `/learning-paths/{path_id}`

### Delete Learning Path by ID

- **DELETE** `/learning-paths/{path_id}`

### Get User Progress for a Learning Path

- **GET** `/learning-paths/progress/{path_id}`

## Learning Path Step Endpoints

- **Base Path**: `/learning-path-steps`

### List Steps for a Learning Path

- **GET** `/learning-path-steps/{learning_path_id}/steps`

### Create Step for a Learning Path

- **POST** `/learning-path-steps/{learning_path_id}/steps`

### Update Step for a Learning Path

- **PUT** `/learning-path-steps/{learning_path_id}/steps/{step_id}`

### Delete Step for a Learning Path

- **DELETE** `/learning-path-steps/{learning_path_id}/steps/{step_id}`

### Reorder Steps

- **POST** `/learning-path-steps/{learning_path_id}/steps/reorder`

## Progress Endpoints

- **Base Path**: `/progress`

### Record Progress

- **POST** `/progress/record`

### Get User Progress

- **GET** `/progress/user/{user_id}`

### Get Progress for a Learning Path

- **GET** `/progress/learning-path/{learning_path_id}`

### Get Progress Analytics

- **GET** `/progress/analytics`

## Assessment Endpoints

- **Base Path**: `/assessment`

### Create Quiz

- **POST** `/assessment/quizzes`

### List Quizzes

- **GET** `/assessment/quizzes`

### Get Quiz by ID

- **GET** `/assessment/quizzes/{quiz_id}`

### Update Quiz

- **PUT** `/assessment/quizzes/{quiz_id}`

### Delete Quiz

- **DELETE** `/assessment/quizzes/{quiz_id}`

### List Flashcards

- **GET** `/assessment/flashcards`

### Create Flashcard

- **POST** `/assessment/flashcards`

### Update Flashcard

- **PUT** `/assessment/flashcards/{flashcard_id}`

### Delete Flashcard

- **DELETE** `/assessment/flashcards/{flashcard_id}`

### Create Exam

- **POST** `/assessment/exams`

### List Exams

- **GET** `/assessment/exams`

### Get Exam by ID

- **GET** `/assessment/exams/{exam_id}`

### Update Exam

- **PUT** `/assessment/exams/{exam_id}`

### Delete Exam

- **DELETE** `/assessment/exams/{exam_id}`

**All endpoints requiring authentication expect:**

- `Authorization: Bearer <token>` header

**All IDs are UUID strings unless otherwise noted.**

**Request/response schemas match the Pydantic models in the codebase.**
