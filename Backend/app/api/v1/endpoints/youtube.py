from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File, Query
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.youtube_content import YouTubeContent, YouTubeChatMessage
from app.services.youtube.video_downloader.yt_download import download_video, is_valid_youtube_url
from app.services.youtube.transcript_downloader.yt_transcript_download import get_single_transcript
from app.services.youtube.channel_downloader.yt_channel_download import get_channel_videos
from app.services.youtube.thumbnail_downloader.yt_thumbnail_downloader import get_thumbnail
from app.services.ai.chat import get_ai_response
import tempfile
import os
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class VideoDownloadResponse(BaseModel):
    video_path: str
    video_title: str
    video_id: str

class VideoDownloadRequest(BaseModel):
    url: str
    resolution: str = "best"

class TranscriptResponse(BaseModel):
    youtube_url: str
    video_id: str
    video_title: str
    transcript: str

class TranscriptRequest(BaseModel):
    url: str

class ChannelVideosResponse(BaseModel):
    video_ids: List[str]
    video_urls: List[str]
    video_titles: List[str]

class ChannelRequest(BaseModel):
    channel_name: str

class ThumbnailResponse(BaseModel):
    thumbnail_path: str
    video_id: str
    thumbnail_url: str

class ThumbnailRequest(BaseModel):
    url: str

class ChatMessageRequest(BaseModel):
    message: str
    video_id: str

class ChatMessageResponse(BaseModel):
    id: str
    message: str
    ai_response: str
    created_at: str
    user_id: str

class YouTubeVideoList(BaseModel):
    id: str
    video_id: str
    title: str
    thumbnail_url: Optional[str]
    video_url: str
    transcript: str
    created_at: str

class YouTubeVideoListResponse(BaseModel):
    videos: List[YouTubeVideoList]
    total: int
    page: int
    page_size: int
    total_pages: int

@router.post("/download", response_model=VideoDownloadResponse)
async def download_youtube_video(
    request: VideoDownloadRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Download a YouTube video with specified resolution."""
    if not is_valid_youtube_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = download_video(
                url=request.url,
                savedir=temp_dir,
                resolution_dropdown=request.resolution
            )
            
            # Store video info in database
            youtube_content = YouTubeContent(
                video_id=result["video_id"],
                title=result["video_title"],
                video_url=request.url,
                created_by=current_user.id
            )
            db.add(youtube_content)
            db.commit()
            
            return VideoDownloadResponse(
                video_path=result["video_path"],
                video_title=result["video_title"],
                video_id=result["video_id"]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcript", response_model=TranscriptResponse)
async def get_video_transcript(
    request: TranscriptRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get transcript for a YouTube video."""
    if not is_valid_youtube_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        transcript_data = get_single_transcript(request.url)
        
        # Store transcript in database
        youtube_content = db.query(YouTubeContent).filter(YouTubeContent.video_id == transcript_data["video_id"]).first()
        if youtube_content:
            youtube_content.transcript = transcript_data["transcript"]
            db.commit()
        else:
            youtube_content = YouTubeContent(
                video_id=transcript_data["video_id"],
                title=transcript_data["video_title"],
                transcript=transcript_data["transcript"],
                video_url=request.url,
                created_by=current_user.id
            )
            db.add(youtube_content)
            db.commit()
        
        return TranscriptResponse(**transcript_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/channel", response_model=ChannelVideosResponse)
async def get_channel_videos_list(
    request: ChannelRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get list of videos from a YouTube channel."""
    try:
        video_ids, video_urls, video_titles = get_channel_videos(request.channel_name)
        if not video_ids:
            raise HTTPException(status_code=404, detail="No videos found for this channel")
        
        return ChannelVideosResponse(
            video_ids=video_ids,
            video_urls=video_urls,
            video_titles=video_titles
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/thumbnail", response_model=ThumbnailResponse)
async def get_video_thumbnail(
    request: ThumbnailRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get thumbnail for a YouTube video."""
    if not is_valid_youtube_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            thumbnail_path, metadata = get_thumbnail(request.url, temp_dir)
            
            # Store thumbnail info in database
            youtube_content = db.query(YouTubeContent).filter(YouTubeContent.video_id == metadata["video_id"]).first()
            if youtube_content:
                youtube_content.thumbnail_url = metadata["thumbnail_url"]
                youtube_content.video_metadata = metadata
                db.commit()
            else:
                youtube_content = YouTubeContent(
                    video_id=metadata["video_id"],
                    title=metadata.get("title", ""),
                    thumbnail_url=metadata["thumbnail_url"],
                    video_url=request.url,
                    video_metadata=metadata,
                    created_by=current_user.id
                )
                db.add(youtube_content)
                db.commit()
            
            return ThumbnailResponse(
                thumbnail_path=thumbnail_path,
                video_id=metadata["video_id"],
                thumbnail_url=metadata["thumbnail_url"]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatMessageResponse)
async def chat_about_video(
    request: ChatMessageRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Chat about a YouTube video using its transcript or title."""
    youtube_content = db.query(YouTubeContent).filter(YouTubeContent.video_id == request.video_id).first()
    if not youtube_content:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Prepare context for AI
    context = {
        "video_title": youtube_content.title,
        "video_url": youtube_content.video_url,
        "user_message": request.message
    }
    
    # Add transcript if available
    if youtube_content.transcript:
        context["transcript"] = youtube_content.transcript
    
    # Get AI response
    try:
        ai_response = await get_ai_response(context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting AI response: {str(e)}")
    
    # Create chat message
    chat_message = YouTubeChatMessage(
        youtube_content_id=youtube_content.id,
        user_id=current_user.id,
        message=request.message
    )
    db.add(chat_message)
    db.commit()
    
    return ChatMessageResponse(
        id=chat_message.id,
        message=chat_message.message,
        ai_response=ai_response,
        created_at=chat_message.created_at.isoformat(),
        user_id=chat_message.user_id
    )

@router.get("/videos", response_model=YouTubeVideoListResponse)
async def list_youtube_videos(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """List all stored YouTube videos that have transcripts."""
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Get total count of videos with transcripts
    total = db.query(YouTubeContent).filter(YouTubeContent.transcript.isnot(None)).count()
    
    # Get paginated videos with transcripts
    videos = db.query(YouTubeContent)\
        .filter(YouTubeContent.transcript.isnot(None))\
        .order_by(YouTubeContent.created_at.desc())\
        .offset(offset)\
        .limit(page_size)\
        .all()
    
    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size
    
    return YouTubeVideoListResponse(
        videos=[
            YouTubeVideoList(
                id=video.id,
                video_id=video.video_id,
                title=video.title,
                thumbnail_url=video.thumbnail_url,
                video_url=video.video_url,
                transcript=video.transcript,
                created_at=video.created_at.isoformat()
            ) for video in videos
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    ) 