import logging
from typing import Optional
from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, 
    NoTranscriptFound, 
    VideoUnavailable
)

logger = logging.getLogger(__name__)

def log_processing_step(session_id: str, step_name: str, status: str, message: str, level: str = "INFO"):
    """Import and use log_processing_step function"""
    try:
        from services.log_service import log_processing_step as log_step
        log_step(session_id, step_name, status, message, level)
    except ImportError:
        # Fallback to basic logging if service unavailable
        logger.info(f"[{session_id}] {step_name}: {status} - {message}")

class TranscriptService:
    def __init__(self):
        pass
    
    def is_healthy(self) -> bool:
        """Check if transcript service is available"""
        return True  # youtube-transcript-api is always available
    
    def get_transcript_sync(self, video_id: str, session_id: Optional[str] = None) -> str:
        """
        Extract transcript using youtube-transcript-api with fallback hierarchy
        
        Args:
            video_id: YouTube video ID
            session_id: Session ID for logging
            
        Returns:
            Clean transcript text or fallback message
        """
        try:
            if session_id:
                log_processing_step(session_id, "Transcript Extraction", "FETCHING", "Extracting transcript using youtube-transcript-api")
            
            # Try different language combinations with fallback hierarchy
            language_options = [
                ['en'],           # Manual English transcripts first
                ['en-US'],        # US English  
                ['en-GB'],        # UK English
                ['en', 'en-US', 'en-GB'],  # Any English
                None              # Auto-generated (any language)
            ]
            
            for languages in language_options:
                try:
                    if languages:
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
                    else:
                        # Get any available transcript
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    
                    # Combine transcript entries into single text
                    transcript_text = ' '.join([entry['text'] for entry in transcript_list])
                    
                    if transcript_text.strip():
                        if session_id:
                            word_count = len(transcript_text.split())
                            log_processing_step(session_id, "Transcript Extraction", "SUCCESS", f"Extracted transcript with {word_count} words")
                        logger.info(f"Successfully extracted transcript for {video_id}: {len(transcript_text)} characters")
                        return transcript_text
                        
                except (NoTranscriptFound, TranscriptsDisabled):
                    continue  # Try next language option
                    
            # If all language options failed
            if session_id:
                log_processing_step(session_id, "Transcript Extraction", "FAILED", "No transcripts available for this video", "WARNING")
            logger.warning(f"No transcripts found for video {video_id}")
            return f"Transcript for video {video_id} (no transcripts available)"
            
        except VideoUnavailable:
            if session_id:
                log_processing_step(session_id, "Transcript Extraction", "FAILED", "Video is unavailable", "ERROR")
            logger.error(f"Video {video_id} is unavailable")
            return f"Transcript for video {video_id} (video unavailable)"
            
        except Exception as e:
            if "rate limit" in str(e).lower():
                if session_id:
                    log_processing_step(session_id, "Transcript Extraction", "FAILED", "Rate limit exceeded", "ERROR")
                logger.error(f"Rate limit exceeded for video {video_id}")
                return f"Transcript for video {video_id} (rate limit exceeded)"
            else:
                if session_id:
                    log_processing_step(session_id, "Transcript Extraction", "FAILED", f"Error: {str(e)}", "ERROR")
                logger.error(f"Transcript extraction error for {video_id}: {str(e)}")
                return f"Transcript for video {video_id} (extraction error: {str(e)})"