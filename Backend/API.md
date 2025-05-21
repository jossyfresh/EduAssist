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
- **Response**:
  ```json
  {
    "access_token": "string",
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
- **Response**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized`: Incorrect email or password
  - `400 Bad Request`: Inactive user

## Content Management Endpoints

### POST /api/v1/content/upload

Upload a file.

**Request Body:**

- `file`: File (multipart/form-data)

**Response:**

```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "content_type": "string",
  "content": "string",
  "created_by": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### POST /api/v1/content/text

Create text content.

**Request Body:**

```json
{
  "title": "string",
  "description": "string",
  "content_type": "text",
  "content": "string"
}
```

**Response:**

```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "content_type": "text",
  "content": "string",
  "created_by": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### POST /api/v1/content/video

Create video content from URL.

**Request Body:**

```json
{
  "video_url": "string"
}
```

**Response:**

```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "content_type": "video",
  "content": "string",
  "created_by": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### GET /api/v1/content/{content_id}

Get content by ID.

**Response:**

```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "content_type": "string",
  "content": "string",
  "created_by": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### PUT /api/v1/content/{content_id}

Update content.

**Request Body:**

```json
{
  "title": "string",
  "description": "string",
  "content_type": "string",
  "content": "string"
}
```

**Response:**

```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "content_type": "string",
  "content": "string",
  "created_by": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### DELETE /api/v1/content/{content_id}

Delete content.

**Response:**

```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "content_type": "string",
  "content": "string",
  "created_by": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### POST /api/v1/content/generate

Generate content using AI providers.

**Request Body:**

```json
{
  "content_type": "string",
  "parameters": {
    "prompt": "string",
    "max_tokens": "integer"
  },
  "provider": "string"
}
```

**Response:**

```json
{
  "content": "string"
}
```

## Learning Path Endpoints

### POST /api/v1/learning-paths

Create a new learning path.

**Request Body:**

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
