# EduAssist API Documentation

## Authentication Endpoints

### POST /api/v1/auth/login

Authenticate user and get access token.

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### POST /api/v1/auth/register

Register a new user.

**Request Body:**

```json
{
  "email": "string",
  "username": "string",
  "password": "string"
}
```

**Response:**

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

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

**Response:**

```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "is_public": "boolean",
  "difficulty_level": "string",
  "estimated_duration": "integer",
  "tags": ["string"],
  "created_by": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### GET /api/v1/learning-paths

Get all learning paths.

**Response:**

```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "is_public": "boolean",
    "difficulty_level": "string",
    "estimated_duration": "integer",
    "tags": ["string"],
    "created_by": "uuid",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

### GET /api/v1/learning-paths/my

Get learning paths created by the current user.

**Response:**

```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "is_public": "boolean",
    "difficulty_level": "string",
    "estimated_duration": "integer",
    "tags": ["string"],
    "created_by": "uuid",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

### GET /api/v1/learning-paths/public

Get all public learning paths.

**Response:**

```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "is_public": "boolean",
    "difficulty_level": "string",
    "estimated_duration": "integer",
    "tags": ["string"],
    "created_by": "uuid",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

### GET /api/v1/learning-paths/{path_id}

Get a specific learning path by ID.

**Response:**

```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "is_public": "boolean",
  "difficulty_level": "string",
  "estimated_duration": "integer",
  "tags": ["string"],
  "created_by": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### PUT /api/v1/learning-paths/{path_id}

Update a learning path.

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

**Response:**

```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "is_public": "boolean",
  "difficulty_level": "string",
  "estimated_duration": "integer",
  "tags": ["string"],
  "created_by": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### DELETE /api/v1/learning-paths/{path_id}

Delete a learning path.

**Response:**

```json
{
  "message": "Learning path deleted successfully"
}
```

### POST /api/v1/learning-paths/{path_id}/steps

Create a new step in a learning path.

**Request Body:**

```json
{
  "title": "string",
  "description": "string",
  "content_type": "string",
  "content": "string",
  "order": "integer"
}
```

**Response:**

```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "content_type": "string",
  "content": "string",
  "order": "integer",
  "learning_path_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### GET /api/v1/learning-paths/{path_id}/steps

Get all steps in a learning path.

**Response:**

```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "content_type": "string",
    "content": "string",
    "order": "integer",
    "learning_path_id": "uuid",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

## Progress Tracking Endpoints

### POST /api/v1/learning-paths/progress

Create user progress.

**Request Body:**

```json
{
  "learning_path_id": "uuid",
  "step_id": "uuid",
  "status": "string",
  "completed_at": "datetime"
}
```

**Response:**

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "learning_path_id": "uuid",
  "step_id": "uuid",
  "status": "string",
  "completed_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### GET /api/v1/learning-paths/progress/{path_id}

Get user progress for a learning path.

**Response:**

```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "learning_path_id": "uuid",
    "step_id": "uuid",
    "status": "string",
    "completed_at": "datetime",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

## Authentication

All endpoints except `/api/v1/auth/login` and `/api/v1/auth/register` require authentication using a Bearer token. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Error Responses

All endpoints may return the following error responses:

- 400 Bad Request: Invalid request parameters
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource not found
- 500 Internal Server Error: Server-side error

Error response format:

```json
{
  "detail": "Error message"
}
```
