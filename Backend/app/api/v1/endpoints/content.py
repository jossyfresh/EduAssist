from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_content
from app.models.user import User
from app.schemas.content import (
    Content,
    ContentCreate,
    ContentUpdate,
    VideoContent,
    TextContent
)
from app.services.content_generator import ContentGenerator

router = APIRouter()
content_generator = ContentGenerator()

@router.post("/upload", response_model=Content)
async def upload_file(
    *,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Upload a file.
    
    Example request body:
    {
        "file": "file_data"
    }
    
    Example response:
    {
        "id": 1,
        "title": "Uploaded File",
        "description": "This is an uploaded file.",
        "content_type": "file",
        "content": "file_url",
        "created_by": "uuid",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    """
    content = await crud_content.upload_file(db=db, file=file, user_id=current_user.id)
    return content

@router.post("/text", response_model=TextContent)
def create_text_content(
    *,
    db: Session = Depends(deps.get_db),
    content_in: ContentCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create text content.
    
    Example request body:
    {
        "title": "Example Text Content",
        "description": "This is an example text content.",
        "content_type": "text",
        "content": "This is the content of the text."
    }
    
    Example response:
    {
        "id": 1,
        "title": "Example Text Content",
        "description": "This is an example text content.",
        "content_type": "text",
        "content": "This is the content of the text.",
        "created_by": "uuid",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    """
    content = crud_content.create_text(
        db=db, obj_in=content_in, user_id=current_user.id
    )
    return content

@router.post("/video", response_model=VideoContent)
async def create_video_content(
    *,
    video_url: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create video content from URL.
    
    Example request body:
    {
        "video_url": "https://example.com/video.mp4"
    }
    
    Example response:
    {
        "id": 1,
        "title": "Example Video Content",
        "description": "This is an example video content.",
        "content_type": "video",
        "content": "video_url",
        "created_by": "uuid",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    """
    content = await crud_content.create_video(
        db=db, video_url=video_url, user_id=current_user.id
    )
    return content

@router.get("/{content_id}", response_model=Content)
def read_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get content by ID.
    
    Example response:
    {
        "id": 1,
        "title": "Example Content",
        "description": "This is an example content.",
        "content_type": "text",
        "content": "This is the content of the item.",
        "created_by": "uuid",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    """
    content = crud_content.get(db=db, id=content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.put("/{content_id}", response_model=Content)
def update_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: int,
    content_in: ContentUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update content.
    
    Example request body:
    {
        "title": "Updated Content",
        "description": "This is an updated content.",
        "content_type": "text",
        "content": "This is the updated content of the item."
    }
    
    Example response:
    {
        "id": 1,
        "title": "Updated Content",
        "description": "This is an updated content.",
        "content_type": "text",
        "content": "This is the updated content of the item.",
        "created_by": "uuid",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    """
    content = crud_content.get(db=db, id=content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    content = crud_content.update(db=db, db_obj=content, obj_in=content_in)
    return content

@router.delete("/{content_id}", response_model=Content)
def delete_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete content.
    
    Example response:
    {
        "id": 1,
        "title": "Deleted Content",
        "description": "This is a deleted content.",
        "content_type": "text",
        "content": "This is the content of the item.",
        "created_by": "uuid",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    """
    content = crud_content.get(db=db, id=content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    content = crud_content.remove(db=db, id=content_id)
    return content

@router.post("/generate", response_model=Dict[str, Any])
async def generate_content(
    *,
    content_type: str,
    parameters: Dict[str, Any],
    provider: str = "openai",
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Generate content using AI providers.
    
    Example request body:
    {
        "content_type": "text",
        "parameters": {
            "prompt": "Generate a summary of the given text.",
            "max_tokens": 100
        },
        "provider": "openai"
    }
    
    Example response:
    {
        "content": "Generated content based on the prompt."
    }
    """
    try:
        content = await content_generator.generate_content(
            content_type=content_type,
            parameters=parameters,
            provider=provider
        )
        return content
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@router.get("/youtube-metadata", response_model=Dict[str, Any])
async def get_youtube_metadata(
    video_url: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get metadata for a YouTube video.
    
    Example response:
    {
        "title": "Example YouTube Video",
        "description": "This is an example YouTube video.",
        "duration": "10:00",
        "thumbnail": "thumbnail_url"
    }
    """
    try:
        metadata = await content_generator.get_youtube_metadata(video_url)
        return metadata
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching YouTube metadata: {str(e)}")

@router.get("/combined", response_model=Dict[str, Any])
async def get_combined_content(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get combined content including quiz, flashcard, note, and YouTube suggestions.
    
    Example response:
    {
        "html": "<div>Combined content in HTML format</div>",
        "youtube_iframe": "<iframe src='https://www.youtube.com/embed/example' width='560' height='315' frameborder='0' allowfullscreen></iframe>"
    }
    """
    try:
        # Fetch all content types
        quiz_content = await content_generator.generate_content(content_type="quiz", parameters={})
        flashcard_content = await content_generator.generate_content(content_type="flashcard", parameters={})
        note_content = await content_generator.generate_content(content_type="note", parameters={})
        youtube_suggestions = await content_generator.generate_content(content_type="youtube_suggestions", parameters={})
        
        # Combine into HTML
        html_content = f"<div>{quiz_content}</div><div>{flashcard_content}</div><div>{note_content}</div><div>{youtube_suggestions}</div>"
        
        # Example YouTube iframe
        youtube_iframe = "<iframe src='https://www.youtube.com/embed/example' width='560' height='315' frameborder='0' allowfullscreen></iframe>"
        
        return {"html": html_content, "youtube_iframe": youtube_iframe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating combined content: {str(e)}") 