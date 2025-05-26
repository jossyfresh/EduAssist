import json
import re
import time
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import yt_dlp
import requests
import tempfile

def is_valid_youtube_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    # A simple pattern; adjust as needed.
    pattern = r"^https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}$"
    if "shorts" in url:
        pattern = r"^https://www\.youtube\.com/shorts/[A-Za-z0-9_-]{11}$"
    return re.match(pattern, url) is not None

def get_video_title(video_id: str) -> str:
    """Use yt-dlp to extract the video title from YouTube."""
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
    }
    url = f"https://www.youtube.com/watch?v={video_id}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get("title", f"Video {video_id}")
        except Exception:
            return f"Video {video_id}"

def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL."""
    if "shorts" in url:
        return url.split("/")[-1]
    return url.split("v=")[-1].split("&")[0]

def get_single_transcript(youtube_url: str) -> Dict[str, str]:
    """
    Get transcript for a single YouTube video.
    
    Args:
        youtube_url: YouTube video URL
        
    Returns:
        Dict containing video URL, ID, title, and transcript
    """
    if not is_valid_youtube_url(youtube_url):
        raise ValueError(f"Invalid YouTube URL: {youtube_url}")
    
    video_id = extract_video_id(youtube_url)
    video_title = get_video_title(video_id)
    
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get English transcript first
            try:
                transcript = transcript_list.find_transcript(['en'])
            except:
                # If no English transcript, get the first available one
                transcript = transcript_list.find_transcript(['en-US', 'en-GB', 'en-CA'])
            
            # Get the transcript data
            transcript_data = transcript.fetch()
            
            # Combine all transcript pieces
            full_transcript = " ".join([entry['text'] for entry in transcript_data])
            
            return {
                "youtube_url": youtube_url,
                "video_id": video_id,
                "video_title": video_title,
                "transcript": full_transcript
            }
            
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return {
                "youtube_url": youtube_url,
                "video_id": video_id,
                "video_title": video_title,
                "transcript": f"No transcript available: {str(e)}"
            }
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return {
                "youtube_url": youtube_url,
                "video_id": video_id,
                "video_title": video_title,
                "transcript": f"Error retrieving transcript: {str(e)}"
            }
    
    return {
        "youtube_url": youtube_url,
        "video_id": video_id,
        "video_title": video_title,
        "transcript": "Failed to retrieve transcript after multiple attempts."
    }

def get_batch_transcripts(youtube_urls: List[str]) -> List[Dict]:
    entries = []
    for url in youtube_urls:
        sanitized_url = url.strip()
        if not sanitized_url:
            continue
        entry = get_single_transcript(sanitized_url)
        if entry is not None:
            entries.append(entry)
    return entries
