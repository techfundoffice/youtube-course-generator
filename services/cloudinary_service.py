"""
Cloudinary service for premium video storage and delivery
Handles MP4 upload, management, and secure URL generation
"""
import os
import logging
import cloudinary
import cloudinary.uploader
import cloudinary.utils
from typing import Dict, Any, Optional
import hashlib
from pathlib import Path

logger = logging.getLogger(__name__)

class CloudinaryService:
    """Manages video uploads and storage with Cloudinary"""
    
    def __init__(self):
        # Configure Cloudinary with environment variables
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
            secure=True
        )
        
        self.configured = self._check_configuration()
        if not self.configured:
            logger.warning("Cloudinary not configured - missing environment variables")
    
    def _check_configuration(self) -> bool:
        """Check if Cloudinary is properly configured"""
        required_vars = ['CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET']
        return all(os.environ.get(var) for var in required_vars)
    
    def upload_video(self, local_video_path: str, video_id: str, video_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload MP4 video to Cloudinary with optimization
        
        Args:
            local_video_path: Path to local MP4 file
            video_id: YouTube video ID for naming
            video_metadata: Video metadata for tags and context
            
        Returns:
            Upload result with Cloudinary URLs and metadata
        """
        if not self.configured:
            return {
                'success': False,
                'error': 'Cloudinary not configured - missing environment variables'
            }
        
        try:
            if not os.path.exists(local_video_path):
                return {
                    'success': False,
                    'error': f'Video file not found: {local_video_path}'
                }
            
            # Generate public ID for Cloudinary
            safe_title = self._sanitize_filename(video_metadata.get('title', 'video'))
            public_id = f"youtube_courses/{video_id}_{safe_title}"
            
            logger.info(f"Uploading video to Cloudinary: {video_id}")
            
            # Upload with video optimization settings for large files
            upload_result = cloudinary.uploader.upload_large(
                local_video_path,
                resource_type="video",
                public_id=public_id,
                folder="youtube_courses",
                overwrite=True,
                # Video optimization settings
                quality="auto:good",
                format="mp4",
                # Handle large videos asynchronously
                eager_async=True,
                eager=[
                    {"quality": "auto:good", "format": "mp4"}
                ],
                # Add metadata as tags
                tags=[
                    f"video_id:{video_id}",
                    f"duration:{video_metadata.get('duration', 'unknown')}",
                    "youtube_course"
                ],
                # Context metadata
                context={
                    "video_id": video_id,
                    "title": video_metadata.get('title', ''),
                    "author": video_metadata.get('author', ''),
                    "uploaded_by": "youtube_course_generator"
                }
            )
            
            if upload_result:
                # Generate secure streaming URL
                streaming_url = cloudinary.utils.cloudinary_url(
                    upload_result['public_id'],
                    resource_type="video",
                    secure=True,
                    quality="auto:good",
                    format="mp4"
                )[0]
                
                # Generate thumbnail URL
                thumbnail_url = cloudinary.utils.cloudinary_url(
                    upload_result['public_id'],
                    resource_type="video",
                    secure=True,
                    format="jpg",
                    transformation=[
                        {"width": 640, "height": 360, "crop": "fill"},
                        {"quality": "auto:good"}
                    ]
                )[0]
                
                logger.info(f"Video uploaded successfully: {upload_result['public_id']}")
                
                return {
                    'success': True,
                    'cloudinary_url': streaming_url,
                    'cloudinary_public_id': upload_result['public_id'],
                    'cloudinary_thumbnail': thumbnail_url,
                    'cloudinary_upload_status': 'completed',
                    'file_size': upload_result.get('bytes', 0),
                    'secure_url': upload_result['secure_url'],
                    'duration': upload_result.get('duration', 0),
                    'format': upload_result.get('format', 'mp4'),
                    'version': upload_result.get('version', 1)
                }
            else:
                return {
                    'success': False,
                    'error': 'Upload failed - no result returned from Cloudinary'
                }
                
        except Exception as e:
            logger.error(f"Cloudinary upload error: {str(e)}")
            return {
                'success': False,
                'error': f'Cloudinary upload failed: {str(e)}'
            }
    
    def delete_video(self, public_id: str) -> bool:
        """Delete video from Cloudinary"""
        if not self.configured:
            return False
        
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type="video")
            return result.get('result') == 'ok'
        except Exception as e:
            logger.error(f"Error deleting video {public_id}: {str(e)}")
            return False
    
    def get_video_info(self, public_id: str) -> Optional[Dict[str, Any]]:
        """Get video information from Cloudinary"""
        if not self.configured:
            return None
        
        try:
            from cloudinary import api
            result = api.resource(public_id, resource_type="video")
            return {
                'public_id': result['public_id'],
                'secure_url': result['secure_url'],
                'duration': result.get('duration', 0),
                'file_size': result.get('bytes', 0),
                'format': result.get('format', 'mp4'),
                'created_at': result.get('created_at'),
                'version': result.get('version', 1)
            }
        except Exception as e:
            logger.error(f"Error getting video info for {public_id}: {str(e)}")
            return None
    
    def generate_streaming_url(self, public_id: str, quality: str = "auto:good") -> str:
        """Generate optimized streaming URL for video"""
        if not self.configured:
            return ""
        
        try:
            return cloudinary.utils.cloudinary_url(
                public_id,
                resource_type="video",
                secure=True,
                quality=quality,
                format="mp4"
            )[0]
        except Exception as e:
            logger.error(f"Error generating streaming URL: {str(e)}")
            return ""
    
    def _sanitize_filename(self, filename: str) -> str:
        """Create safe filename for Cloudinary public ID"""
        # Remove/replace problematic characters
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        safe_filename = ''.join(c if c in safe_chars else '_' for c in filename)
        
        # Limit length and remove multiple underscores
        safe_filename = '_'.join(safe_filename.split('_'))[:30]
        return safe_filename or 'video'

# Global instance
cloudinary_service = CloudinaryService()