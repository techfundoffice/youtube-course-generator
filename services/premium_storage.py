"""
Premium video storage service for subscription users
Handles persistent video storage, user libraries, and storage quotas
"""
import os
import logging
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib
from pathlib import Path

logger = logging.getLogger(__name__)

class PremiumVideoStorage:
    """Manages premium video storage for subscription users"""
    
    def __init__(self, base_storage_path: str = "/home/runner/workspace/premium_videos"):
        self.base_path = Path(base_storage_path)
        self.base_path.mkdir(exist_ok=True)
        
        # Storage quotas by subscription tier (in bytes)
        self.storage_quotas = {
            'basic': 5 * 1024 * 1024 * 1024,    # 5 GB
            'premium': 20 * 1024 * 1024 * 1024,  # 20 GB
            'enterprise': 100 * 1024 * 1024 * 1024  # 100 GB
        }
    
    def store_video_for_user(self, user_id: str, video_id: str, temp_video_path: str, 
                            video_metadata: Dict[str, Any], subscription_tier: str = 'basic') -> Dict[str, Any]:
        """
        Store a video permanently for a premium user
        
        Args:
            user_id: Unique user identifier
            video_id: YouTube video ID
            temp_video_path: Path to temporary downloaded video
            video_metadata: Video metadata (title, duration, etc.)
            subscription_tier: User's subscription level
            
        Returns:
            Storage result with permanent URL and metadata
        """
        try:
            # Create user storage directory
            user_dir = self.base_path / user_id
            user_dir.mkdir(exist_ok=True)
            
            # Check storage quota
            if not self._check_storage_quota(user_id, temp_video_path, subscription_tier):
                return {
                    'success': False,
                    'error': 'Storage quota exceeded',
                    'quota_info': self._get_quota_info(user_id, subscription_tier)
                }
            
            # Generate secure filename
            safe_title = self._sanitize_filename(video_metadata.get('title', 'video'))
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{video_id}_{timestamp}_{safe_title}.mp4"
            
            # Copy video to permanent storage
            permanent_path = user_dir / filename
            shutil.copy2(temp_video_path, permanent_path)
            
            # Store metadata
            metadata_path = user_dir / f"{video_id}_{timestamp}_metadata.json"
            import json
            with open(metadata_path, 'w') as f:
                json.dump({
                    **video_metadata,
                    'stored_at': datetime.now().isoformat(),
                    'file_size': os.path.getsize(permanent_path),
                    'storage_path': str(permanent_path),
                    'user_id': user_id,
                    'subscription_tier': subscription_tier
                }, f, indent=2)
            
            # Generate permanent access URL
            permanent_url = f"/premium/video/{user_id}/{filename}"
            
            logger.info(f"Video {video_id} stored for user {user_id} at {permanent_path}")
            
            return {
                'success': True,
                'permanent_url': permanent_url,
                'file_path': str(permanent_path),
                'file_size': os.path.getsize(permanent_path),
                'metadata_path': str(metadata_path),
                'storage_info': self._get_quota_info(user_id, subscription_tier)
            }
            
        except Exception as e:
            logger.error(f"Error storing video for user {user_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_video_library(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all stored videos for a user"""
        try:
            user_dir = self.base_path / user_id
            if not user_dir.exists():
                return []
            
            videos = []
            for metadata_file in user_dir.glob("*_metadata.json"):
                try:
                    import json
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    # Check if video file still exists
                    video_path = Path(metadata.get('storage_path', ''))
                    if video_path.exists():
                        videos.append({
                            'video_id': metadata.get('id'),
                            'title': metadata.get('title'),
                            'duration': metadata.get('duration'),
                            'file_size': metadata.get('file_size'),
                            'stored_at': metadata.get('stored_at'),
                            'permanent_url': f"/premium/video/{user_id}/{video_path.name}",
                            'thumbnail_url': metadata.get('thumbnail'),
                            'view_count': metadata.get('view_count'),
                            'uploader': metadata.get('uploader')
                        })
                except Exception as e:
                    logger.warning(f"Error reading metadata file {metadata_file}: {e}")
                    continue
            
            # Sort by stored date (newest first)
            videos.sort(key=lambda x: x.get('stored_at', ''), reverse=True)
            return videos
            
        except Exception as e:
            logger.error(f"Error getting video library for user {user_id}: {str(e)}")
            return []
    
    def delete_user_video(self, user_id: str, video_id: str, timestamp: str) -> bool:
        """Delete a specific video from user's library"""
        try:
            user_dir = self.base_path / user_id
            
            # Find and delete video file
            video_pattern = f"{video_id}_{timestamp}_*.mp4"
            video_files = list(user_dir.glob(video_pattern))
            
            # Find and delete metadata file
            metadata_pattern = f"{video_id}_{timestamp}_metadata.json"
            metadata_files = list(user_dir.glob(metadata_pattern))
            
            deleted_files = 0
            for file_path in video_files + metadata_files:
                if file_path.exists():
                    file_path.unlink()
                    deleted_files += 1
            
            logger.info(f"Deleted {deleted_files} files for video {video_id} (user {user_id})")
            return deleted_files > 0
            
        except Exception as e:
            logger.error(f"Error deleting video {video_id} for user {user_id}: {str(e)}")
            return False
    
    def _check_storage_quota(self, user_id: str, new_video_path: str, subscription_tier: str) -> bool:
        """Check if user has enough storage quota for new video"""
        try:
            quota_limit = self.storage_quotas.get(subscription_tier, self.storage_quotas['basic'])
            current_usage = self._calculate_user_storage(user_id)
            new_video_size = os.path.getsize(new_video_path)
            
            return (current_usage + new_video_size) <= quota_limit
            
        except Exception as e:
            logger.error(f"Error checking storage quota for user {user_id}: {str(e)}")
            return False
    
    def _calculate_user_storage(self, user_id: str) -> int:
        """Calculate total storage used by user"""
        try:
            user_dir = self.base_path / user_id
            if not user_dir.exists():
                return 0
            
            total_size = 0
            for file_path in user_dir.rglob("*.mp4"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            
            return total_size
            
        except Exception as e:
            logger.error(f"Error calculating storage for user {user_id}: {str(e)}")
            return 0
    
    def _get_quota_info(self, user_id: str, subscription_tier: str) -> Dict[str, Any]:
        """Get storage quota information for user"""
        quota_limit = self.storage_quotas.get(subscription_tier, self.storage_quotas['basic'])
        current_usage = self._calculate_user_storage(user_id)
        
        return {
            'subscription_tier': subscription_tier,
            'quota_limit_bytes': quota_limit,
            'quota_limit_gb': round(quota_limit / (1024**3), 2),
            'current_usage_bytes': current_usage,
            'current_usage_gb': round(current_usage / (1024**3), 2),
            'available_bytes': quota_limit - current_usage,
            'available_gb': round((quota_limit - current_usage) / (1024**3), 2),
            'usage_percentage': round((current_usage / quota_limit) * 100, 1) if quota_limit > 0 else 0
        }
    
    def _sanitize_filename(self, filename: str) -> str:
        """Create safe filename from video title"""
        # Remove/replace problematic characters
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. "
        safe_filename = ''.join(c if c in safe_chars else '_' for c in filename)
        
        # Limit length and remove multiple spaces/underscores
        safe_filename = '_'.join(safe_filename.split())[:50]
        return safe_filename or 'video'

# Global instance
premium_storage = PremiumVideoStorage()