# EduAssist Technical Specification

## System Architecture

### Backend Stack

- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Storage**: Supabase Storage
- **Real-time**: Supabase Realtime
- **AI Integration**: OpenAI API
- **Video Processing**: yt-dlp
- **File Processing**: Python libraries (PyPDF2, Pillow, etc.)
- **Caching**: Redis (optional, for performance optimization)

### Frontend Stack

- **Framework**: React/Next.js
- **UI Components**: Tailwind CSS + Shadcn/ui
- **State Management**: Zustand
- **Real-time**: Supabase Realtime Client
- **Chat Interface**: Custom Canvas-like UI

## Database Schema (Supabase)

### Tables

#### auth.users

- id (uuid, pk)
- email (unique)
- created_at
- updated_at
- metadata (jsonb)

#### profiles

- id (uuid, pk, references auth.users)
- username
- full_name
- avatar_url
- created_at
- updated_at

#### learning_paths

- id (uuid, pk)
- user_id (uuid, references profiles.id)
- title
- description
- status (enum: draft, active, completed)
- created_at
- updated_at

#### learning_path_steps

- id (uuid, pk)
- learning_path_id (uuid, references learning_paths.id)
- order (int)
- title
- description
- type (enum: text, video, pdf, image, quiz, flashcard, exam)
- content_id (uuid)
- status (enum: not_started, in_progress, completed)
- created_at
- updated_at

#### text_contents

- id (uuid, pk)
- body (text)
- summary (text)
- created_at
- updated_at

#### videos

- id (uuid, pk)
- youtube_url
- title
- description
- transcript (text)
- thumbnail_url
- duration
- created_at
- updated_at

#### files

- id (uuid, pk)
- storage_path
- file_type (enum: pdf, image, other)
- title
- description
- created_at
- updated_at

#### quizzes

- id (uuid, pk)
- title
- description
- questions (jsonb)
- created_at
- updated_at

#### flashcards

- id (uuid, pk)
- front (text)
- back (text)
- learning_path_step_id (uuid, references learning_path_steps.id)
- created_at
- updated_at

#### exams

- id (uuid, pk)
- title
- description
- questions (jsonb)
- created_at
- updated_at

#### user_progress

- id (uuid, pk)
- user_id (uuid, references profiles.id)
- learning_path_id (uuid, references learning_paths.id)
- step_id (uuid, references learning_path_steps.id)
- status (enum: not_started, in_progress, completed)
- score (float, nullable)
- started_at
- completed_at

#### chats

- id (uuid, pk)
- user_id (uuid, references profiles.id)
- learning_path_id (uuid, references learning_paths.id, nullable)
- context (jsonb)
- created_at
- updated_at

#### messages

- id (uuid, pk)
- chat_id (uuid, references chats.id)
- sender (enum: user, agent)
- content (text)
- content_type (enum: text, video, image, etc)
- metadata (jsonb)
- created_at

## FastAPI Endpoints

### Auth

```python
@router.post("/auth/register")
@router.post("/auth/login")
@router.post("/auth/logout")
@router.get("/auth/me")
```

### Learning Paths

```python
@router.get("/learning-paths")
@router.post("/learning-paths")
@router.get("/learning-paths/{id}")
@router.put("/learning-paths/{id}")
@router.delete("/learning-paths/{id}")
```

### Learning Path Steps

```python
@router.post("/learning-paths/{id}/steps")
@router.put("/learning-paths/{id}/steps/{step_id}")
@router.delete("/learning-paths/{id}/steps/{step_id}")
```

### Content

```python
@router.post("/text-contents")
@router.post("/videos")
@router.post("/files")
@router.post("/quizzes")
@router.post("/flashcards")
@router.post("/exams")
```

### Chat

```python
@router.post("/chats")
@router.get("/chats/{id}/messages")
@router.post("/chats/{id}/messages")
@router.websocket("/chats/{id}/stream")
```

### Progress

```python
@router.get("/progress")
@router.get("/learning-paths/{id}/progress")
@router.post("/learning-paths/{id}/steps/{step_id}/progress")
```

## AI Integration

### OpenAI Integration

- GPT-4/3.5 for chat interactions
- Whisper for video transcriptions
- Embeddings for semantic search
- Custom prompt templates for different content types

### Video Processing

- yt-dlp for video downloads
- FFmpeg for video processing
- Whisper for transcription

### File Processing

- PyPDF2 for PDF processing
- Pillow for image processing
- Custom OCR for text extraction

## Storage

### Supabase Storage

- Buckets:
  - public (for shared content)
  - private (for user-specific content)
  - temp (for temporary uploads)

## Security

### Authentication

- JWT-based authentication via Supabase
- Role-based access control
- Row-level security policies

### Data Protection

- Input validation using Pydantic
- File type validation
- Size limits on uploads
- Content scanning for malicious files

## Real-time Features

### Supabase Realtime

- Chat messages
- Progress updates
- Learning path modifications
- Collaborative features

## Performance Optimization

### Caching

- Redis for frequently accessed data
- CDN for static assets
- Browser caching for static content

### Database Optimization

- Indexes on frequently queried columns
- Materialized views for complex queries
- Query optimization using Supabase's query planner

## Monitoring and Logging

### Error Tracking

- Sentry integration
- Custom error handlers
- Log aggregation

### Analytics

- User engagement metrics
- Learning path effectiveness
- Quiz/exam statistics
- Performance metrics

## Development Workflow

### Local Development

- Docker Compose for local environment
- Supabase CLI for local development
- Environment variables management

### Testing

- Pytest for unit/integration tests
- Playwright for E2E tests
- Load testing with k6

### CI/CD

- GitHub Actions for automated testing
- Automated deployments
- Environment-specific configurations

## Deployment

### Production Environment

- Vercel/Netlify for frontend
- Railway/DigitalOcean for backend
- Supabase for database and storage
- Redis for caching (optional)

### Scaling

- Horizontal scaling for API servers
- Database read replicas
- CDN for static assets
- Load balancing

## Future Considerations

### Potential Enhancements

- Offline support
- P2P file sharing
- Custom plugin system
- Advanced analytics
- Machine learning for personalized learning paths
- Multi-language support
- Accessibility improvements
