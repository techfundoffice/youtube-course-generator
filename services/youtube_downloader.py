"""
YouTube MP4 video downloader using yt-dlp for local storage
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
    """Free video downloader using yt-dlp for YouTube videos"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="youtube_dl_")
        
    def __del__(self):
        """Cleanup temp directory"""
        try:
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except:
            pass
    
    
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
    
    def download_video(self, video_url: str, quality: str = "720p", session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Download video using yt-dlp for YouTube
        
        Args:
            video_url: YouTube video URL
            quality: Video quality (720p, 480p, best, worst)
            session_id: Session ID for logging
            
        Returns:
            Dict containing download information
        """
        # Validate URL type
        try:
            from utils.validators import detect_source
            source = detect_source(video_url)
            
            if source == 'youtube':
                return self._download_youtube_video(video_url, quality, session_id)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported video source: {source}. Only YouTube URLs are supported.'
                }
        except ImportError:
            # Fallback to YouTube-only handling if validators not available
            return self._download_youtube_video(video_url, quality, session_id)
    
    def _download_youtube_video(self, youtube_url: str, quality: str = "720p", session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Download YouTube video using yt-dlp
        
        Args:
            youtube_url: YouTube video URL
            quality: Video quality (720p, 480p, best, worst)
            session_id: Session ID for logging
            
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
            
            # Configure quality selector with SABR fallbacks - avoid problematic formats
            if quality == "720p":
                format_selector = "best[height<=720][protocol!*=dash]/best[height<=480][protocol!*=dash]/best[height<=360]/worst"
            elif quality == "480p":
                format_selector = "best[height<=480][protocol!*=dash]/best[height<=360]/worst"
            elif quality == "best":
                format_selector = "best[protocol!*=dash]/worst"
            else:
                format_selector = "worst[protocol!*=dash]/worst"
            
            if session_id:
                log_processing_step(session_id, "yt-dlp Metadata", "FETCHING", f"Getting video information from YouTube (quality: {quality})")
            
            # Get video info first with comprehensive SABR workarounds
            info_cmd = [
                'yt-dlp',
                '--dump-json',
                '--no-download',
                '--extractor-args', 'youtube:player_client=android,web;skip=dash,hls',
                '--user-agent', 'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36',
                '--no-warnings',
                '--socket-timeout', '30',
                '--retries', '2',
                youtube_url
            ]
            
            logger.info(f"Getting video info for: {youtube_url}")
            info_result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=45)
            
            # If Android client fails, try multiple fallbacks for SABR issues
            if info_result.returncode != 0:
                logger.warning("Android client failed, trying web client...")
                fallback_clients = ['web', 'ios', 'mweb']
                
                for client in fallback_clients:
                    fallback_cmd = [
                        'yt-dlp',
                        '--dump-json',
                        '--no-download',
                        '--extractor-args', f'youtube:player_client={client}',
                        '--no-warnings',
                        youtube_url
                    ]
                    fallback_result = subprocess.run(fallback_cmd, capture_output=True, text=True, timeout=30)
                    if fallback_result.returncode == 0:
                        info_result = fallback_result
                        logger.info(f"Successfully used {client} client for metadata extraction")
                        break
                else:
                    # All clients failed
                    if session_id:
                        log_processing_step(session_id, "yt-dlp Metadata", "FAILED", f"Failed to get video metadata with all clients: {info_result.stderr[:100]}", "ERROR")
                    return {
                        'success': False,
                        'error': f'Failed to get video info with all player clients: {info_result.stderr}'
                    }
            
            video_info = json.loads(info_result.stdout)
            title = video_info.get('title', 'Unknown Title')[:50]
            duration = video_info.get('duration', 0)
            duration_str = f"{duration//60}m{duration%60}s" if duration else "unknown duration"
            
            if session_id:
                log_processing_step(session_id, "yt-dlp Metadata", "SUCCESS", f"Video: '{title}' ({duration_str})")
            
            # Download the video with comprehensive SABR workarounds
            output_template = os.path.join(self.temp_dir, f"%(id)s.%(ext)s")
            download_cmd = [
                'yt-dlp',
                '-f', format_selector,
                '-o', output_template,
                '--extractor-args', 'youtube:player_client=android,web;skip=dash,hls',
                '--user-agent', 'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36',
                '--no-warnings',
                '--socket-timeout', '45',
                '--retries', '2',
                '--fragment-retries', '2',
                '--retry-sleep', '2',
                '--no-continue',
                '--geo-bypass',
                youtube_url
            ]
            
            if session_id:
                log_processing_step(session_id, "yt-dlp Download", "DOWNLOADING", f"Downloading {quality} MP4 video (this may take 10-30 seconds)")
            
            logger.info(f"Downloading video with quality: {quality}")
            download_result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=180)
            
            # If initial download fails due to SABR, try fallback clients
            if download_result.returncode != 0:
                logger.warning("Initial download failed, trying fallback clients for SABR workaround...")
                fallback_clients = ['web', 'ios', 'mweb']
                
                for client in fallback_clients:
                    fallback_download_cmd = [
                        'yt-dlp',
                        '-f', format_selector,
                        '-o', output_template,
                        '--extractor-args', f'youtube:player_client={client}',
                        '--no-warnings',
                        '--retries', '2',
                        '--fragment-retries', '2',
                        '--retry-sleep', '1',
                        youtube_url
                    ]
                    
                    fallback_result = subprocess.run(fallback_download_cmd, capture_output=True, text=True, timeout=300)
                    if fallback_result.returncode == 0:
                        download_result = fallback_result
                        logger.info(f"Successfully downloaded using {client} client")
                        break
                else:
                    # All download attempts failed - return graceful fallback
                    if session_id:
                        log_processing_step(session_id, "yt-dlp Download", "FAILED", f"Download failed with all clients due to SABR streaming restrictions. Continuing without video.", "WARNING")
                    
                    # Return a fallback response that allows course generation to continue
                    return {
                        'success': False,
                        'mp4_video_url': None,
                        'mp4_download_status': 'failed_sabr_restrictions',
                        'mp4_file_size': 0,
                        'local_path': None,
                        'video_id': video_info.get('id', 'unknown'),
                        'title': video_info.get('title', ''),
                        'duration': video_info.get('duration', 0),
                        'thumbnail_url': video_info.get('thumbnail', ''),
                        'description': video_info.get('description', ''),
                        'view_count': video_info.get('view_count', 0),
                        'uploader': video_info.get('uploader', ''),
                        'upload_date': video_info.get('upload_date', ''),
                        'filename': None,
                        'source': 'youtube-downloader-fallback',
                        'error': 'YouTube SABR streaming prevents download - video metadata available for course generation'
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
            
            # LOCAL DOWNLOAD RESULT - Simple and reliable
            return {
                'success': True,
                'mp4_video_url': http_video_url,
                'mp4_download_status': 'completed',
                'mp4_file_size': file_size,
                'local_path': permanent_path,
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
            
        except subprocess.TimeoutExpired:
            if session_id:
                log_processing_step(session_id, "yt-dlp Download", "TIMEOUT", "Download timeout due to SABR streaming issues. Continuing without video.", "WARNING")
            
            # Return fallback response on timeout to allow course generation to continue
            return {
                'success': False,
                'mp4_video_url': None,
                'mp4_download_status': 'timeout_sabr_restrictions',
                'mp4_file_size': 0,
                'local_path': None,
                'video_id': 'unknown',
                'title': 'Unknown Video',
                'duration': 0,
                'thumbnail_url': '',
                'description': '',
                'view_count': 0,
                'uploader': '',
                'upload_date': '',
                'filename': None,
                'source': 'youtube-downloader-timeout',
                'error': 'Download timeout due to YouTube SABR streaming restrictions'
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
                '--extractor-args', 'youtube:player_client=android',
                '--no-warnings',
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