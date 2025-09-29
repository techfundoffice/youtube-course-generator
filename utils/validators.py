"""
Validation utilities for YouTube URLs and course structures.
"""
import re
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any

def validate_youtube_url(url: str) -> bool:
    """
    Validate if a URL is a valid YouTube URL.
    
    Args:
        url: The URL to validate
        
    Returns:
        True if valid YouTube URL, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    youtube_patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^https?://youtu\.be/[\w-]+',
        r'^https?://(m\.)?youtube\.com/watch\?v=[\w-]+',
        r'^https?://(www\.)?youtube\.com/shorts/[\w-]+',
        r'^https?://(m\.)?youtube\.com/shorts/[\w-]+'
    ]
    
    return any(re.match(pattern, url) for pattern in youtube_patterns)


def validate_media_url(url: str) -> bool:
    """
    Validate if a URL is a valid media URL (YouTube only).
    
    Args:
        url: The URL to validate
        
    Returns:
        True if valid media URL, False otherwise
    """
    return validate_youtube_url(url)

def detect_source(url: str) -> str:
    """
    Detect the source type of a media URL.
    
    Args:
        url: The URL to analyze
        
    Returns:
        'youtube' or 'unknown'
    """
    if validate_youtube_url(url):
        return 'youtube'
    else:
        return 'unknown'

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from various YouTube URL formats.
    
    Args:
        url: YouTube video URL
        
    Returns:
        Video ID if YouTube URL, None otherwise
    """
    if not validate_youtube_url(url):
        return None
    
    try:
        parsed_url = urlparse(url)
        
        if 'youtu.be' in parsed_url.netloc:
            return parsed_url.path[1:]  # Remove leading slash
        
        if 'youtube.com' in parsed_url.netloc:
            # Handle YouTube Shorts URLs
            if '/shorts/' in parsed_url.path:
                # Extract video ID from path, handle any additional path segments
                video_id = parsed_url.path.split('/shorts/')[-1].split('/')[0].split('?')[0]
                # Remove any query parameters that might be included
                return video_id.split('?')[0] if video_id else None
            
            # Handle regular watch URLs
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
            
    except Exception:
        pass
    
    return None

def validate_course_structure(course: Dict[str, Any]) -> bool:
    """
    Validate that a course has the required structure.
    
    Args:
        course: Course dictionary to validate
        
    Returns:
        True if valid structure, False otherwise
    """
    if not isinstance(course, dict):
        return False
    
    required_fields = [
        'course_title',
        'course_description',
        'target_audience',
        'difficulty_level',
        'estimated_total_time',
        'days_structure',
        'final_project',
        'resources',
        'assessment_criteria'
    ]
    
    # Check required fields exist
    for field in required_fields:
        if field not in course:
            return False
    
    # Validate data types
    if not isinstance(course['course_title'], str):
        return False
    
    if not isinstance(course['days_structure'], list):
        return False
    
    # Validate days structure
    for day in course['days_structure']:
        if not isinstance(day, dict):
            return False
        
        day_required = ['day', 'title', 'learning_objectives', 'activities', 'key_takeaways', 'homework']
        for field in day_required:
            if field not in day:
                return False
    
    return True

def sanitize_input(text: str) -> str:
    """
    Sanitize input by removing HTML tags and dangerous content.
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    if text is None:
        return ""
    
    if not isinstance(text, str):
        return str(text)
    
    # Remove HTML tags
    import re
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    # Remove script tags and their content
    clean_text = re.sub(r'<script.*?</script>', '', clean_text, flags=re.DOTALL | re.IGNORECASE)
    
    return clean_text.strip()