from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import crud_content, models, schemas
from app.api import deps
from app.models.enums import ContentType
from app.schemas.content import Content, ContentCreate, ContentUpdate, GenerateContentRequest
from app.services.content_generator import ContentGenerator
from app.models.user import User

router = APIRouter()
content_generator = ContentGenerator()

@router.post("/text", response_model=Content)
def create_text_content(
    *,
    db: Session = Depends(deps.get_db),
    content_in: ContentCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new text content."""
    content = crud_content.create_text(db=db, obj_in=content_in, user_id=current_user.id)
    return content

@router.post("/video", response_model=Content)
def create_video_content(
    *,
    db: Session = Depends(deps.get_db),
    content_in: ContentCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new video content."""
    content = crud_content.create_video(db=db, obj_in=content_in, user_id=current_user.id)
    return content

@router.get("/{content_id}", response_model=Content)
def get_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get content by ID."""
    content = crud_content.get(db=db, id=content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.put("/{content_id}", response_model=Content)
def update_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: str,
    content_in: ContentUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update content."""
    content = crud_content.get(db=db, id=content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    content = crud_content.update(db=db, db_obj=content, obj_in=content_in)
    return content

@router.delete("/{content_id}", response_model=Content)
def delete_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete content."""
    content = crud_content.get(db=db, id=content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    content = crud_content.remove(db=db, id=content_id)
    return content

@router.post("/generate", response_model=Content)
def generate_content(
    *,
    db: Session = Depends(deps.get_db),
    request: GenerateContentRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Generate content using AI."""
    try:
        generated_content = content_generator.generate_content(
            content_type=request.content_type,
            parameters=request.parameters,
            provider=request.provider
        )
        
        content_in = ContentCreate(
            title=generated_content.get("title", "Generated Content"),
            content_type=request.content_type,
            content=generated_content.get("content", ""),
            meta=generated_content.get("meta", {})
        )
        
        content = crud_content.create_text(db=db, obj_in=content_in, user_id=current_user.id)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/youtube-metadata")
def get_youtube_metadata(
    *,
    video_url: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get YouTube video metadata."""
    try:
        metadata = content_generator.get_youtube_metadata(video_url)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/combined")
def get_combined_content(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get all content types combined."""
    content = crud_content.get_combined_content(db=db)
    return content

@router.post("/upload", response_model=Content)
async def upload_file(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Upload a file."""
    try:
        content = await file.read()
        content_in = ContentCreate(
            title=file.filename,
            content_type=ContentType.FILE,
            content=content.decode(),
            meta={"content_type": file.content_type}
        )
        content = crud_content.create_file(db=db, obj_in=content_in, user_id=current_user.id)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 