import yt_dlp
import scrapetube
from typing import Tuple, List, Optional
import tempfile
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_channel_id_from_name(channel_name: str) -> Optional[str]:
    """
    Uses yt-dlp to search for the channel by name and returns its channel_id.
    """
    logger.debug(f"Searching for channel: {channel_name}")
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "force_generic_extractor": True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{channel_name}", download=False)
            logger.debug(f"Search result: {result}")
            if result and 'entries' in result and result['entries']:
                channel_id = result['entries'][0].get('channel_id')
                logger.debug(f"Found channel ID: {channel_id}")
                return channel_id
    except Exception as e:
        logger.error(f"Error getting channel ID: {str(e)}")
        raise Exception(f"Failed to get channel ID: {str(e)}")
    
    return None

def extract_title(raw_title: str) -> str:
    """Clean and format video title."""
    logger.debug(f"Extracting title from: {raw_title}")
    if not isinstance(raw_title, str):
        logger.error(f"Invalid title type: {type(raw_title)}")
        return "No Title"
    return raw_title.strip()

def get_videourl_from_channel_id(channel_id: str) -> Tuple[List[str], List[str], List[str]]:
    """
    Get video URLs, IDs, and titles from a channel ID.
    
    Returns:
        Tuple of (video_ids, video_urls, video_titles)
    """
    try:
        logger.debug(f"Getting videos for channel ID: {channel_id}")
        videos = list(scrapetube.get_channel(channel_id))
        logger.debug(f"Found {len(videos)} videos")
        video_urls = []
        video_ids = []
        video_titles = []
        
        for video in videos:
            logger.debug(f"Processing video: {video}")
            vid = video["videoId"]
            raw_title = video.get("title", "No Title")
            logger.debug(f"Raw title: {raw_title}, type: {type(raw_title)}")
            title = extract_title(raw_title)
            vurl = f"https://www.youtube.com/watch?v={vid}"
            
            video_ids.append(vid)
            video_urls.append(vurl)
            video_titles.append(title)
            
        return video_ids, video_urls, video_titles
    except Exception as e:
        logger.error(f"Error getting channel videos: {str(e)}")
        raise Exception(f"Failed to get channel videos: {str(e)}")

def get_channel_videos(channel_name: str) -> Tuple[List[str], List[str], List[str]]:
    """
    Get all videos from a YouTube channel by name.
    
    Args:
        channel_name: Name of the YouTube channel
        
    Returns:
        Tuple of (video_ids, video_urls, video_titles)
    """
    try:
        logger.debug(f"Getting videos for channel: {channel_name}")
        channel_id = get_channel_id_from_name(channel_name)
        if not channel_id:
            logger.error(f"Channel not found: {channel_name}")
            raise Exception(f"Channel not found: {channel_name}")
            
        return get_videourl_from_channel_id(channel_id)
    except Exception as e:
        logger.error(f"Error in get_channel_videos: {str(e)}")
        raise Exception(f"Failed to get channel videos: {str(e)}")
