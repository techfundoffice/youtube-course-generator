"""
Free YouTube MP4 video downloader using yt-dlp as fallback when Apify fails
"""
import os
import logging
import subprocess
import json
from typing import Dict, Any, Optional
import tempfile
import shutil

logger = logging.getLogger(__name__)

def log_processing_step(session_id: str, step_name: str, status: str, message: str, level: str = "INFO"):
    """Import and use log_processing_step function"""
    try:
        from services.log_service import log_processing_step as log_step
        log_step(session_id, step_name, status, message, level)
    except ImportError:
        # Fallback to basic logging if service unavailable
        logger.info(f"[{session_id}] {step_name}: {status} - {message}")

class YouTubeDownloader:
    """Free YouTube video downloader using yt-dlp"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="youtube_dl_")
        
    def __del__(self):
        """Cleanup temp directory"""
        try:
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except:
            pass
    
    def _auto_upload_to_cloudinary(self, local_file_path: str, filename: str, session_id: Optional[str] = None) -> dict:
        """Automatically upload downloaded video to Cloudinary"""
        try:
            if session_id:
                log_processing_step(session_id, "Cloudinary Upload", "STARTING", f"Uploading {filename} to cloud storage")
            
            from services.cloudinary_service import CloudinaryService
            cloudinary_service = CloudinaryService()
            
            # Upload the video file
            upload_result = cloudinary_service.upload_video(local_file_path, filename, {'title': filename})
            
            if upload_result['success']:
                if session_id:
                    log_processing_step(session_id, "Cloudinary Upload", "SUCCESS", f"✓ Video uploaded to premium cloud storage: {upload_result['cloudinary_url']}")
                
                return {
                    'cloudinary_url': upload_result['cloudinary_url'],
                    'cloudinary_public_id': upload_result['public_id'],
                    'cloudinary_upload_status': 'success'
                }
            else:
                if session_id:
                    log_processing_step(session_id, "Cloudinary Upload", "FAILED", f"Upload error: {upload_result['error']}", "WARNING")
                
                return {
                    'cloudinary_url': None,
                    'cloudinary_public_id': None,
                    'cloudinary_upload_status': 'failed',
                    'cloudinary_error': upload_result['error']
                }
                
        except Exception as e:
            error_msg = f"Cloudinary upload exception: {str(e)}"
            logger.error(error_msg)
            
            if session_id:
                log_processing_step(session_id, "Cloudinary Upload", "FAILED", error_msg, "WARNING")
            
            return {
                'cloudinary_url': None,
                'cloudinary_public_id': None,
                'cloudinary_upload_status': 'failed',
                'cloudinary_error': str(e)
            }
    
    def check_ytdlp_available(self) -> bool:
        """Check if yt-dlp is available"""
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def install_ytdlp(self) -> bool:
        """Install yt-dlp if not available"""
        try:
            logger.info("Installing yt-dlp...")
            result = subprocess.run(['pip', 'install', 'yt-dlp'], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                logger.info("yt-dlp installed successfully")
                return True
            else:
                logger.error(f"Failed to install yt-dlp: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error installing yt-dlp: {str(e)}")
            return False
    
    def download_video(self, youtube_url: str, quality: str = "720p", session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Download YouTube video using yt-dlp
        
        Args:
            youtube_url: YouTube video URL
            quality: Video quality (720p, 480p, best, worst)
            
        Returns:
            Dict containing download information
        """
        try:
            # Check if yt-dlp is available
            if not self.check_ytdlp_available():
                logger.info("yt-dlp not found, attempting to install...")
                if session_id:
                    log_processing_step(session_id, "yt-dlp Setup", "INSTALLING", "Installing yt-dlp downloader package")
                if not self.install_ytdlp():
                    if session_id:
                        log_processing_step(session_id, "yt-dlp Setup", "FAILED", "Failed to install yt-dlp package", "ERROR")
                    return {
                        'success': False,
                        'error': 'yt-dlp installation failed - cannot proceed with download'
                    }
                if session_id:
                    log_processing_step(session_id, "yt-dlp Setup", "SUCCESS", "yt-dlp package installed successfully")
            
            # Configure quality selector
            if quality == "720p":
                format_selector = "best[height<=720]"
            elif quality == "480p":
                format_selector = "best[height<=480]"
            elif quality == "best":
                format_selector = "best"
            else:
                format_selector = "worst"
            
            if session_id:
                log_processing_step(session_id, "yt-dlp Metadata", "FETCHING", f"Getting video information from YouTube (quality: {quality})")
            
            # Get video info first
            info_cmd = [
                'yt-dlp',
                '--dump-json',
                '--no-download',
                youtube_url
            ]
            
            logger.info(f"Getting video info for: {youtube_url}")
            info_result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=30)
            
            if info_result.returncode != 0:
                if session_id:
                    log_processing_step(session_id, "yt-dlp Metadata", "FAILED", f"Failed to get video metadata: {info_result.stderr[:100]}", "ERROR")
                return {
                    'success': False,
                    'error': f'Failed to get video info: {info_result.stderr}'
                }
            
            video_info = json.loads(info_result.stdout)
            title = video_info.get('title', 'Unknown Title')[:50]
            duration = video_info.get('duration', 0)
            duration_str = f"{duration//60}m{duration%60}s" if duration else "unknown duration"
            
            if session_id:
                log_processing_step(session_id, "yt-dlp Metadata", "SUCCESS", f"Video: '{title}' ({duration_str})")
            
            # Download the video
            output_template = os.path.join(self.temp_dir, f"%(id)s.%(ext)s")
            download_cmd = [
                'yt-dlp',
                '-f', format_selector,
                '-o', output_template,
                youtube_url
            ]
            
            if session_id:
                log_processing_step(session_id, "yt-dlp Download", "DOWNLOADING", f"Downloading {quality} MP4 video (this may take 10-30 seconds)")
            
            logger.info(f"Downloading video with quality: {quality}")
            download_result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=300)
            
            if download_result.returncode != 0:
                if session_id:
                    log_processing_step(session_id, "yt-dlp Download", "FAILED", f"Download failed: {download_result.stderr[:100]}", "ERROR")
                return {
                    'success': False,
                    'error': f'Download failed: {download_result.stderr}'
                }
            
            # Find the downloaded file
            video_id = video_info.get('id', 'unknown')
            downloaded_files = [f for f in os.listdir(self.temp_dir) if f.startswith(video_id)]
            
            if not downloaded_files:
                if session_id:
                    log_processing_step(session_id, "yt-dlp Download", "FAILED", "Downloaded file not found in temp directory", "ERROR")
                return {
                    'success': False,
                    'error': 'Downloaded file not found'
                }
            
            downloaded_file = os.path.join(self.temp_dir, downloaded_files[0])
            file_size = os.path.getsize(downloaded_file)
            
            # Copy to permanent storage using standardized path
            from app import app
            videos_dir = app.config['VIDEOS_DIR']
            os.makedirs(videos_dir, exist_ok=True)
            permanent_path = os.path.join(videos_dir, downloaded_files[0])
            import shutil
            shutil.copy2(downloaded_file, permanent_path)
            
            logger.info(f"Download completed: {downloaded_file} ({file_size} bytes)")
            
            # Format file size for display
            if file_size > 1024*1024:
                size_str = f"{file_size/(1024*1024):.1f} MB"
            else:
                size_str = f"{file_size/1024:.1f} KB"
            
            if session_id:
                log_processing_step(session_id, "yt-dlp Download", "SUCCESS", f"Downloaded {size_str} MP4 file to local storage")
            
            # Generate HTTP URL for video serving
            video_filename = os.path.basename(downloaded_file)
            http_video_url = f"/video/{video_filename}"
            
            # CORE DOWNLOAD RESULT (works independently of cloudinary)
            download_result = {
                'success': True,
                'mp4_video_url': http_video_url,  # HTTP URL for browser access
                'mp4_download_status': 'completed',
                'mp4_file_size': file_size,
                'local_path': downloaded_file,  # Local file path for Cloudinary upload
                'video_id': video_id,
                'title': video_info.get('title', ''),
                'duration': video_info.get('duration', 0),
                'thumbnail_url': video_info.get('thumbnail', ''),
                'description': video_info.get('description', ''),
                'view_count': video_info.get('view_count', 0),
                'uploader': video_info.get('uploader', ''),
                'upload_date': video_info.get('upload_date', ''),
                'filename': downloaded_files[0],
                'source': 'youtube-downloader'
            }
            
            # TRY CLOUDINARY UPLOAD (optional - doesn't break local download if it fails)
            try:
                cloudinary_result = self._auto_upload_to_cloudinary(downloaded_file, downloaded_files[0], session_id)
                download_result.update(cloudinary_result)
            except Exception as e:
                logger.warning(f"Cloudinary upload failed but local download completed: {str(e)}")
                # Add default cloudinary values
                download_result.update({
                    'cloudinary_url': None,
                    'cloudinary_public_id': None,
                    'cloudinary_upload_status': 'failed',
                    'cloudinary_thumbnail': None
                })
            
            return download_result
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Download timeout (over 5 minutes)'
            }
        except Exception as e:
            logger.error(f"YouTube download error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_video_info_only(self, youtube_url: str) -> Dict[str, Any]:
        """Get video information without downloading"""
        try:
            if not self.check_ytdlp_available():
                if not self.install_ytdlp():
                    return {
                        'success': False,
                        'error': 'yt-dlp installation failed'
                    }
            
            cmd = [
                'yt-dlp',
                '--dump-json',
                '--no-download',
                youtube_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'Failed to get video info: {result.stderr}'
                }
            
            video_info = json.loads(result.stdout)
            
            return {
                'success': True,
                'video_id': video_info.get('id', ''),
                'title': video_info.get('title', ''),
                'duration': video_info.get('duration', 0),
                'thumbnail_url': video_info.get('thumbnail', ''),
                'description': video_info.get('description', ''),
                'view_count': video_info.get('view_count', 0),
                'uploader': video_info.get('uploader', ''),
                'upload_date': video_info.get('upload_date', '')
            }
            
        except Exception as e:
            logger.error(f"YouTube info error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }