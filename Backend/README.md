# EduAssist

An AI-powered educational assistant that creates personalized learning paths and provides interactive learning experiences.

## Features

- AI-powered learning path creation
- Interactive chat interface
- Multi-media content support (text, video, PDF, images)
- Real-time progress tracking
- Assessment system (quizzes, flashcards, exams)
- Collaborative learning features

## Tech Stack

### Backend

- FastAPI
- Supabase (PostgreSQL, Auth, Storage)
- OpenAI API
- yt-dlp
- Docker

### Frontend (Coming Soon)

- React/Next.js
- Tailwind CSS
- Shadcn/ui
- Supabase Client

## Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Supabase CLI
- OpenAI API key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/rebumatadele/EduAssist.git
cd EduAssist
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your credentials
```

5. Start the development server:

```bash
uvicorn app.main:app --reload
```

## Project Structure

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Core functionality
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── utils/        # Utility functions
├── tests/            # Test files
├── alembic/          # Database migrations
└── requirements.txt  # Python dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
