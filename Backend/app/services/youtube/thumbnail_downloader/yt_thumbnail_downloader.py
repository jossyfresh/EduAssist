import re
import requests
import os
from typing import Dict, Tuple, Optional

def is_valid_youtube_url(url: str) -> bool:
    """Checks if the URL is a valid YouTube video URL"""
    if not isinstance(url, str):
        return False
    pattern = r"^https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}$"
    if "shorts" in url:
        pattern = r"^https://www\.youtube\.com/shorts/[A-Za-z0-9_-]{11}$"
    return re.match(pattern, url) is not None

def extract_video_id(url: str) -> str:
    """Extracts the video ID from a YouTube URL"""
    if "shorts" in url:
        return url.split("/")[-1]
    return url.split("v=")[-1].split("&")[0]

def get_youtube_thumbnail_url(video_id: str) -> Dict[str, str]:
    """Returns all possible thumbnail URLs for a given video ID"""
    return {
        "default": f"https://img.youtube.com/vi/{video_id}/default.jpg",
        "mqdefault": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
        "hqdefault": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        "sddefault": f"https://img.youtube.com/vi/{video_id}/sddefault.jpg",
        "maxresdefault": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
    }

def download_thumbnail(url: str, savepath: str) -> None:
    """Downloads a thumbnail from a URL and saves it to the specified path"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(savepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def get_thumbnail(url: str, savedir: str) -> Tuple[str, Dict[str, str]]:
    """
    Fetches the best available YouTube thumbnail and saves it.
    Tries in order: maxresdefault, hqdefault, mqdefault.
    
    Args:
        url: YouTube video URL
        savedir: Directory to save the thumbnail
        
    Returns:
        Tuple of (thumbnail_path, metadata)
    """
    if not is_valid_youtube_url(url):
        raise ValueError(f"Invalid YouTube URL: {url}")
        
    video_id = extract_video_id(url)
    thumbnails = get_youtube_thumbnail_url(video_id)
    
    for key in ["maxresdefault", "hqdefault", "mqdefault"]:
        savepath = os.path.join(savedir, f"{video_id}_{key}.jpg")
        try:
            download_thumbnail(thumbnails[key], savepath)
            return savepath, {
                "video_id": video_id,
                "thumbnail_url": thumbnails[key]
            }
        except Exception as e:
            continue
            
    raise ValueError(f"Could not download any thumbnail for {url}")

def get_batch_thumbnails(yt_urls: list, savedir: str):
    """
    Downloads thumbnails for a batch of YouTube URLs.
    Returns a tuple: (list of savepaths, list of data entries).
    """
    thumbnail_savepaths = []
    entries = []
    for url in yt_urls:
        try:
            savepath, data_entry = get_thumbnail(url, savedir)
            thumbnail_savepaths.append(savepath)
            entries.append(data_entry)
        except Exception as e:
            print(f"❌ Failed to fetch thumbnail for {url}: {e}")
    return thumbnail_savepaths, entries
