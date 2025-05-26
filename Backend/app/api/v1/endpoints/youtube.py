from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.services.youtube.video_downloader.yt_download import download_video, is_valid_youtube_url
from app.services.youtube.transcript_downloader.yt_transcript_download import get_single_transcript
from app.services.youtube.channel_downloader.yt_channel_download import get_channel_videos
from app.services.youtube.thumbnail_downloader.yt_thumbnail_downloader import get_thumbnail
import tempfile
import os
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class VideoDownloadResponse(BaseModel):
    video_path: str
    video_title: str
    video_id: str

class TranscriptResponse(BaseModel):
    youtube_url: str
    video_id: str
    video_title: str
    transcript: str

class ChannelVideosResponse(BaseModel):
    video_ids: List[str]
    video_urls: List[str]
    video_titles: List[str]

class ThumbnailResponse(BaseModel):
    thumbnail_path: str
    video_id: str
    thumbnail_url: str

@router.post("/download", response_model=VideoDownloadResponse)
async def download_youtube_video(
    url: str = Form(...),
    resolution: str = Form("best"),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Download a YouTube video with specified resolution."""
    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = download_video(
                url=url,
                savedir=temp_dir,
                resolution_dropdown=resolution
            )
            
            return VideoDownloadResponse(
                video_path=result["video_path"],
                video_title=result["video_title"],
                video_id=result["video_id"]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcript", response_model=TranscriptResponse)
async def get_video_transcript(
    url: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get transcript for a YouTube video."""
    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        transcript_data = get_single_transcript(url)
        return TranscriptResponse(**transcript_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/channel", response_model=ChannelVideosResponse)
async def get_channel_videos_list(
    channel_name: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get list of videos from a YouTube channel."""
    try:
        video_ids, video_urls, video_titles = get_channel_videos(channel_name)
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
    url: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get thumbnail for a YouTube video."""
    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            thumbnail_path, metadata = get_thumbnail(url, temp_dir)
            return ThumbnailResponse(
                thumbnail_path=thumbnail_path,
                video_id=metadata["video_id"],
                thumbnail_url=metadata["thumbnail_url"]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 