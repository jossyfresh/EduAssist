import yt_dlp
from yt_dlp import YoutubeDL
import re
import os
import tempfile
from typing import Optional, Dict, Any

def is_valid_youtube_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    pattern = r"^https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}$"
    if "shorts" in url:
        pattern = r"^https://www\.youtube\.com/shorts/[A-Za-z0-9_-]{11}$"
    return re.match(pattern, url) is not None

def download_video(
    url: str,
    savedir: str,
    resolution_dropdown: str = "best",
    progress_callback: Optional[callable] = None
) -> Dict[str, Any]:
    """
    Download a YouTube video with progress tracking.
    
    Args:
        url: YouTube video URL
        savedir: Directory to save the video
        resolution_dropdown: Video resolution ("best", "1080", "720", "360")
        progress_callback: Optional callback function for progress updates
        
    Returns:
        Dict containing video path, title, and ID
    """
    try:
        if not is_valid_youtube_url(url):
            raise ValueError(f"Invalid input URL: {url}")

        # Extract video info without downloading
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get("title", None)
            video_title = re.sub(r"[^a-zA-Z0-9]", " ", video_title)
        
        # Construct a save path
        savepath = os.path.join(savedir, f"{video_title or video_id}.mp4")
        
        def progress_hook(d):
            if d.get('status') == 'downloading':
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded_bytes = d.get('downloaded_bytes', 0)
                if total_bytes and progress_callback:
                    progress = downloaded_bytes / total_bytes
                    progress_callback(progress)
            elif d.get('status') == 'finished':
                if progress_callback:
                    progress_callback(1.0)
        
        # Set yt-dlp options
        ydl_opts = {
            "format": "best[ext=mp4]",
            "outtmpl": savepath,
            "progress_hooks": [progress_hook],
            "noplaylist": True,
            "postprocessors": [],
        }
        
        # Apply resolution filters if specified
        if resolution_dropdown == "1080":
            ydl_opts["format"] = "best[height<=1080][ext=mp4]"
        elif resolution_dropdown == "720":
            ydl_opts["format"] = "best[height<=720][ext=mp4]"
        elif resolution_dropdown == "360":
            ydl_opts["format"] = "best[height<=360][ext=mp4]"
        
        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return {
            "video_path": savepath,
            "video_title": video_title,
            "video_id": video_id
        }
        
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")
