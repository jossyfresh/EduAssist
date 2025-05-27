from typing import List, Optional, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body, Form, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.content import Content, ContentCreate, ContentUpdate, ContentGeneratorResponse, GenerateContentRequest, ContentResponse, ContentListResponse, ContentGenerateRequest, ContentBatchResponse, ContentBatchCreate, ContentBatchUpdate, ContentContextualGenerateRequest, ChatResponse, ChatRequest
from app.crud.crud_content import crud_content
from app.services.content_generator import ContentGenerator
from app.services.content_service import ContentService
from app.models.user import User
from app.models.enums import ContentType
from app.models.course import Course as CourseModel
from app.models.content import Content as ContentModel
from uuid import uuid4
import base64
import json
from datetime import datetime
from pydantic import BaseModel
import re
import asyncio

router = APIRouter()
content_generator = ContentGenerator()
content_service = ContentService()

class OutlineContentRequest(BaseModel):
    outline: str
    course_id: Optional[str] = None

def is_valid_json(text: str) -> bool:
    """Check if a string is valid JSON."""
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

def clean_json_response(response: str) -> str:
    """Clean and extract JSON from response."""
    # Remove markdown code blocks
    cleaned = response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    
    cleaned = cleaned.strip()
    
    # Try to extract JSON using regex
    json_match = re.search(r'\{[\s\S]*\}', cleaned)
    if json_match:
        return json_match.group()
    return cleaned

async def get_valid_json_response(content_generator, prompt: str, max_retries: int = 3) -> Dict:
    """Get valid JSON response with retries."""
    for attempt in range(max_retries):
        try:
            response = await content_generator._generate_with_gemini(prompt)
            print(f"Attempt {attempt + 1} - Raw Response:", response)
            
            cleaned_response = clean_json_response(response)
            print(f"Attempt {attempt + 1} - Cleaned Response:", cleaned_response)
            
            if is_valid_json(cleaned_response):
                return json.loads(cleaned_response)
            
            print(f"Attempt {attempt + 1} - Invalid JSON, retrying...")
            
            # Modify prompt to be more strict about JSON
            prompt = f"""IMPORTANT: Your previous response was not valid JSON. Please try again.
            You must return ONLY a valid JSON object with no additional text, markdown, or formatting.
            The response must be parseable by json.loads().
            
            {prompt}
            
            Remember:
            1. Return ONLY the JSON object
            2. No markdown formatting
            3. No additional text before or after
            4. No code blocks
            5. Valid JSON syntax with proper quotes and commas
            """
            
            # Add delay between retries
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"Attempt {attempt + 1} - Error:", str(e))
            if attempt == max_retries - 1:
                raise
    
    raise HTTPException(
        status_code=500,
        detail={
            "error": "Failed to get valid JSON after multiple attempts",
            "max_retries": max_retries
        }
    )

@router.post("/text", 
    response_model=ContentResponse,
    summary="Create Text Content",
    description="""
    Create new text content with the following features:
    - Supports markdown formatting
    - Can be associated with a course
    - Includes metadata and description
    
    Example Input:
    ```json
    {
        "title": "Introduction to Python",
        "content": "# Python Basics\n\nPython is a high-level programming language...",
        "content_type": "TEXT",
        "description": "A beginner's guide to Python programming",
        "course_id": "optional-course-id",
        "meta": {
            "tags": ["python", "programming"],
            "difficulty": "beginner"
        }
    }
    ```
    
    Example Output:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Introduction to Python",
        "content": "# Python Basics\n\nPython is a high-level programming language...",
        "content_type": "TEXT",
        "description": "A beginner's guide to Python programming",
        "created_by": "user-id",
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T10:00:00Z",
        "course_id": "optional-course-id",
        "meta": {
            "tags": ["python", "programming"],
            "difficulty": "beginner"
        }
    }
    ```
    """
)
async def create_text_content(
    content: ContentCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Create new text content."""
    return await content_service.create_content(content, current_user.id)

@router.post("/video", 
    response_model=ContentResponse,
    summary="Create Video Content",
    description="""
    Create new video content from a YouTube URL with the following features:
    - Automatically extracts video transcript
    - Fetches video metadata (title, description, duration, thumbnail)
    - Can be associated with a course
    
    Example Input:
    ```json
    {
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "course_id": "optional-course-id"
    }
    ```
    
    Example Output:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Never Gonna Give You Up",
        "content": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "content_type": "VIDEO",
        "description": "Official music video for 'Never Gonna Give You Up' by Rick Astley",
        "created_by": "user-id",
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T10:00:00Z",
        "course_id": "optional-course-id",
        "meta": {
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "transcript": "Never gonna give you up...",
            "youtube_title": "Never Gonna Give You Up",
            "youtube_description": "Official music video...",
            "duration": "3:32",
            "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
        }
    }
    ```
    """
)
async def create_video_content(
    youtube_url: str = Form(...),
    title: str = Form(...),
    course_id: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Create new video content from a YouTube URL."""
    try:
        metadata_dict = json.loads(metadata) if metadata else {}
        metadata_dict["youtube_url"] = youtube_url
        
        # Extract video metadata and transcript
        video_data = await content_generator.extract_youtube_transcript(youtube_url)
        
        content = ContentCreate(
            title=title,
            content=video_data.get("transcript", ""),
            content_type="VIDEO",
            course_id=course_id,
            meta=metadata_dict
        )
        
        return await content_service.create_content(content, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{content_id}", 
    response_model=ContentResponse,
    summary="Get Content by ID",
    description="""
    Retrieve content by its unique ID.
    
    Example Output:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Introduction to Python",
        "content": "# Python Basics\n\nPython is a high-level programming language...",
        "content_type": "TEXT",
        "description": "A beginner's guide to Python programming",
        "created_by": "user-id",
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T10:00:00Z",
        "course_id": "optional-course-id",
        "meta": {
            "tags": ["python", "programming"],
            "difficulty": "beginner"
        }
    }
    ```
    """
)
async def get_content(
    content_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get content by ID."""
    return await content_service.get_content(content_id)

@router.put("/{content_id}", 
    response_model=ContentResponse,
    summary="Update Content",
    description="""
    Update existing content. Only the content owner can update it.
    
    Example Input:
    ```json
    {
        "title": "Updated Python Introduction",
        "content": "# Updated Python Basics\n\nPython is a versatile programming language...",
        "description": "An updated beginner's guide to Python programming",
        "meta": {
            "tags": ["python", "programming", "updated"],
            "difficulty": "beginner",
            "last_updated": "2024-03-20"
        }
    }
    ```
    
    Example Output:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Updated Python Introduction",
        "content": "# Updated Python Basics\n\nPython is a versatile programming language...",
        "content_type": "TEXT",
        "description": "An updated beginner's guide to Python programming",
        "created_by": "user-id",
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T11:00:00Z",
        "course_id": "optional-course-id",
        "meta": {
            "tags": ["python", "programming", "updated"],
            "difficulty": "beginner",
            "last_updated": "2024-03-20"
        }
    }
    ```
    """
)
async def update_content(
    content_id: str,
    content: ContentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Update content."""
    return await content_service.update_content(content_id, content)

@router.delete("/{content_id}", 
    response_model=ContentResponse,
    summary="Delete Content",
    description="""
    Delete content by ID. Only the content owner can delete it.
    
    Example Output:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Introduction to Python",
        "content": "# Python Basics\n\nPython is a high-level programming language...",
        "content_type": "TEXT",
        "description": "A beginner's guide to Python programming",
        "created_by": "user-id",
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T10:00:00Z",
        "course_id": "optional-course-id",
        "meta": {
            "tags": ["python", "programming"],
            "difficulty": "beginner"
        }
    }
    ```
    """
)
async def delete_content(
    content_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete content."""
    return await content_service.delete_content(content_id)

@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentGenerateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Generate AI content (quiz, summary, flashcards, etc.) and store it in the database.
    
    Request Body Examples:
    
    1. Quiz Generation:
    ```json
    {
        "content_type": "quiz",
        "parameters": {
            "topic": "Python Basics",
            "difficulty": "beginner",
            "num_questions": 5,
            "question_types": ["multiple_choice", "true_false"]
        }
    }
    ```
    
    2. Summary Generation:
    ```json
    {
        "content_type": "summary",
        "parameters": {
            "text": "Your text to summarize here...",
            "max_length": 200,
            "focus_points": ["key concepts", "main arguments"]
        }
    }
    ```
    
    3. Flashcard Generation:
    ```json
    {
        "content_type": "flashcard",
        "parameters": {
            "topic": "Python Data Structures",
            "num_cards": 10,
            "difficulty": "intermediate",
            "include_examples": true
        }
    }
    ```
    
    4. YouTube Suggestions:
    ```json
    {
        "content_type": "youtube_suggestions",
        "parameters": {
            "topic": "Machine Learning Basics",
            "num_suggestions": 5,
            "difficulty": "beginner",
            "include_description": true
        }
    }
    ```
    
    5. Course Content Generation:
    ```json
    {
        "content_type": "course",
        "parameters": {
            "topic": "Web Development",
            "level": "beginner",
            "duration": "8 weeks",
            "include_prerequisites": true,
            "include_learning_objectives": true
        }
    }
    ```
    
    6. Practice Exercises:
    ```json
    {
        "content_type": "exercises",
        "parameters": {
            "topic": "Python Functions",
            "difficulty": "intermediate",
            "num_exercises": 5,
            "include_solutions": true,
            "include_hints": true
        }
    }
    ```
    
    7. Code Examples:
    ```json
    {
        "content_type": "code_examples",
        "parameters": {
            "language": "Python",
            "concept": "Decorators",
            "num_examples": 3,
            "include_comments": true,
            "include_explanations": true
        }
    }
    ```
    
    8. Learning Path:
    ```json
    {
        "content_type": "learning_path",
        "parameters": {
            "topic": "Data Science",
            "level": "beginner",
            "duration": "12 weeks",
            "include_resources": true,
            "include_milestones": true
        }
    }
    ```
    """
    try:
        # Generate content using AI
        generated_content = await content_generator.generate_content(
            content_type=request.content_type,
            parameters=request.parameters,
            provider=request.provider
        )
        
        # Create content object for database storage
        content_obj = ContentCreate(
            title=f"Generated {request.content_type.title()}",
            content=json.dumps(generated_content),
            content_type=request.content_type.upper(),
            description=f"AI-generated {request.content_type} about {request.parameters.get('topic', 'general topic')}",
            meta={
                "generator": request.provider,
                "parameters": request.parameters,
                "generated_at": datetime.utcnow().isoformat()
            }
        )
        
        # Store in database
        stored_content = await content_service.create_content(content_obj, current_user.id)
        
        return stored_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", 
    response_model=ContentResponse,
    summary="Upload Files",
    description="""
    Upload multiple files with the following features:
    - Files are stored as base64 strings
    - Supports multiple file types
    - Files are grouped by batch_id
    - Includes file metadata
    
    Example Input:
    ```
    Form Data:
    files: [file1.pdf, file2.docx]
    ```
    
    Example Output:
    ```json
    {
        "batch_id": "550e8400-e29b-41d4-a716-446655440000",
        "files": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "title": "file1.pdf",
                "content_type": "FILE",
                "content": "base64_encoded_content",
                "meta": {
                    "filename": "file1.pdf",
                    "content_type": "application/pdf",
                    "size": 1024,
                    "batch_id": "550e8400-e29b-41d4-a716-446655440000"
                }
            }
        ]
    }
    ```
    """
)
async def upload_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    course_id: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Upload multiple files."""
    try:
        metadata_dict = json.loads(metadata) if metadata else {}
        content = ContentCreate(
            title=title,
            content=file.filename,  # Store file path/URL
            content_type="FILE",
            course_id=course_id,
            meta=metadata_dict
        )
        return await content_service.create_content(content, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/batch/{batch_id}", 
    response_model=ContentBatchResponse,
    summary="Get Batch Files",
    description="""
    Retrieve all files in a batch by batch_id.
    
    Example Output:
    ```json
    {
        "batch_id": "550e8400-e29b-41d4-a716-446655440000",
        "files": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "title": "file1.pdf",
                "content_type": "FILE",
                "content": "base64_encoded_content",
                "meta": {
                    "filename": "file1.pdf",
                    "content_type": "application/pdf",
                    "size": 1024,
                    "batch_id": "550e8400-e29b-41d4-a716-446655440000"
                }
            }
        ]
    }
    ```
    """
)
async def get_batch_files(
    batch_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get all files in a batch."""
    try:
        query = db.query(ContentModel).filter(
            ContentModel.meta['batch_id'].astext == batch_id,
            ContentModel.created_by == current_user.id
        )
        
        files = query.all()
        
        if not files:
            raise HTTPException(status_code=404, detail="Batch not found")
            
        return {
            "batch_id": batch_id,
            "files": [Content.from_orm(file) for file in files]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch/{batch_id}/files", 
    response_model=ContentBatchResponse,
    summary="Add Files to Batch",
    description="""
    Add new files to an existing batch.
    
    Example Input:
    ```
    Form Data:
    files: [file3.pdf, file4.docx]
    ```
    
    Example Output:
    ```json
    {
        "batch_id": "550e8400-e29b-41d4-a716-446655440000",
        "added_files": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440003",
                "title": "file3.pdf",
                "content_type": "FILE",
                "content": "base64_encoded_content",
                "meta": {
                    "filename": "file3.pdf",
                    "content_type": "application/pdf",
                    "size": 1024,
                    "batch_id": "550e8400-e29b-41d4-a716-446655440000"
                }
            }
        ]
    }
    ```
    """
)
async def add_files_to_batch(
    batch_id: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Add files to an existing batch."""
    try:
        existing_files = db.query(ContentModel).filter(
            ContentModel.meta['batch_id'].astext == batch_id,
            ContentModel.created_by == current_user.id
        ).first()
        
        if not existing_files:
            raise HTTPException(status_code=404, detail="Batch not found")
            
        uploaded_contents = []
        for file in files:
            content = await file.read()
            content_b64 = base64.b64encode(content).decode('utf-8')
            
            content_obj = ContentCreate(
                title=file.filename,
                content_type=ContentType.FILE,
                content=content_b64,
                meta={
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "size": len(content),
                    "batch_id": batch_id
                },
                description=f"Uploaded file: {file.filename}"
            )
            
            content = crud_content.create_file(db=db, obj_in=content_obj, user_id=current_user.id)
            uploaded_contents.append(Content.from_orm(content))
            
        return {
            "batch_id": batch_id,
            "added_files": uploaded_contents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-contextual", 
    response_model=Dict[str, Any],
    summary="Generate Contextual Content",
    description="""
    Generate content using AI based on course context:
    - Uses all course-related content (transcripts, files, text)
    - Supports multiple content types
    - Can be customized with extra parameters
    
    Example Input:
    ```json
    {
        "course_id": "550e8400-e29b-41d4-a716-446655440000",
        "content_type": "quiz",
        "provider": "openai",
        "extra_parameters": {
            "difficulty": "intermediate",
            "num_questions": 10
        }
    }
    ```
    
    Example Output:
    ```json
    {
        "content": {
            "questions": [
                {
                    "question": "Based on the course content, what is...",
                    "options": [...],
                    "correct_answer": 0,
                    "explanation": "..."
                }
            ]
        }
    }
    ```
    """
)
async def generate_contextual_content(
    request: ContentContextualGenerateRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Generate content using course context."""
    if not request.course_id:
        raise HTTPException(status_code=400, detail="Must provide course_id.")

    query = db.query(ContentModel)
    if request.course_id:
        query = query.filter(ContentModel.course_id == request.course_id)
    contents = query.all()

    context_parts = []
    for c in contents:
        if c.content_type == ContentType.TEXT:
            context_parts.append(c.content)
        elif c.content_type == ContentType.VIDEO:
            transcript = c.meta.get("transcript") if c.meta else None
            if transcript:
                context_parts.append(transcript)
        elif c.content_type == ContentType.FILE:
            pass

    context = "\n\n".join(context_parts)
    parameters = {"context": context}
    parameters.update(request.extra_parameters or {})

    try:
        result = await content_generator.generate_content(
            request.content_type,
            parameters,
            request.provider
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-from-outline", 
    response_model=Dict[str, Any],
    summary="Generate Comprehensive Content from Outline",
    description="""
    Generate comprehensive educational content from an outline using AI.
    The content will be structured as a list of chapters with detailed content.
    
    Example Input:
    ```json
    {
        "outline": "Chapter 1: Introduction to Python\n- What is Python?\n- Why learn Python?\n- Setting up Python\n\nChapter 2: Basic Syntax\n- Variables and Data Types\n- Operators\n- Control Flow",
        "course_id": "optional-course-id",
        "provider": "gemini"
    }
    ```
    
    Example Output:
    ```json
    {
        "chapters": [
            {
                "title": "Introduction to Python",
                "sections": [
                    {
                        "title": "What is Python?",
                        "content": "Python is a high-level, interpreted programming language...",
                        "key_points": ["Easy to learn", "Versatile", "Large community"],
                        "examples": ["print('Hello, World!')", "x = 5"]
                    },
                    {
                        "title": "Why learn Python?",
                        "content": "Python has become one of the most popular programming languages...",
                        "key_points": ["High demand", "Easy syntax", "Rich ecosystem"],
                        "examples": ["Data science", "Web development", "AI/ML"]
                    }
                ]
            }
        ]
    }
    ```
    """
)
async def generate_from_outline(
    request: OutlineContentRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Generate comprehensive content from an outline using AI."""
    try:
        # Prepare the prompt for Gemini
        prompt = f"""Generate comprehensive educational content based on the following outline. 
        The content should be at least three pages long and include detailed explanations, examples, and key points.
        IMPORTANT: Your response must be a valid JSON object with no extra text before or after.
        Format the response as a JSON object with the following structure:
        {{
            "chapters": [
                {{
                    "title": "Chapter Title",
                    "sections": [
                        {{
                            "title": "Section Title",
                            "content": "Detailed content with explanations and examples",
                            "key_points": ["Key point 1", "Key point 2", ...],
                            "examples": ["Example 1", "Example 2", ...]
                        }}
                    ]
                }}
            ]
        }}

        Outline:
        {request.outline}

        Requirements:
        1. Each section should have detailed explanations
        2. Include relevant examples for each concept
        3. List key points for easy reference
        4. Use clear and concise language
        5. Ensure the content is comprehensive and educational
        6. Maintain a logical flow between sections
        7. Include practical applications where relevant
        8. IMPORTANT: Return ONLY the JSON object, no additional text or formatting
        9. Ensure all JSON syntax is valid (proper quotes, commas, brackets)
        10. No markdown formatting or code blocks
        """

        # Get valid JSON response with retries
        content = await get_valid_json_response(content_generator, prompt)
        return content

    except Exception as e:
        print(f"General Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Error generating content",
                "message": str(e),
                "type": type(e).__name__
            }
        )

@router.post("/chat", 
    response_model=ChatResponse,
    summary="Chat with Course AI",
    description="""
    Chat with an AI tutor about course content. The AI will use the course content as context for its responses.
    
    Example Input:
    ```json
    {
        "course_id": "550e8400-e29b-41d4-a716-446655440000",
        "prompt": "Can you explain the concept of quantum computing?",
        "history": [
            {
                "role": "user",
                "content": "What is quantum computing?"
            },
            {
                "role": "assistant",
                "content": "Quantum computing is a type of computing that uses quantum bits..."
            }
        ]
    }
    ```
    
    Example Output:
    ```json
    {
        "response": "Quantum computing uses quantum bits (qubits) that can exist in multiple states simultaneously...",
        "history": [
            {
                "role": "user",
                "content": "What is quantum computing?"
            },
            {
                "role": "assistant",
                "content": "Quantum computing is a type of computing that uses quantum bits..."
            },
            {
                "role": "user",
                "content": "Can you explain the concept of quantum computing?"
            },
            {
                "role": "assistant",
                "content": "Quantum computing uses quantum bits (qubits) that can exist in multiple states simultaneously..."
            }
        ]
    }
    ```
    """
)
async def chat_with_course(
    request: ChatRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Chat with an AI tutor about course content."""
    try:
        result = await content_generator.generate_chat_response(
            course_id=request.course_id,
            prompt=request.prompt,
            history=request.history
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))