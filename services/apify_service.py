import os
import logging
import time
from typing import Optional, Dict, Any
from apify_client import ApifyClient

logger = logging.getLogger(__name__)

class ApifyService:
    """Service for downloading YouTube videos using Apify actor"""
    
    def __init__(self):
        self.api_token = os.environ.get('APIFY_API_TOKEN')
        if not self.api_token:
            logger.warning("APIFY_API_TOKEN not configured")
            self.client = None
        else:
            self.client = ApifyClient(self.api_token)
        
        # Track current active run
        self.current_run_id = None
    
    def start_youtube_video_download(self, youtube_url: str) -> Dict[str, Any]:
        """
        Start YouTube video download using Apify actor and return run information
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Dict containing run ID and initial status
        """
        if not self.client:
            raise ValueError("Apify client not configured - missing APIFY_API_TOKEN")
        
        logger.info(f"Starting Apify video download for: {youtube_url}")
        
        try:
            # Using free YouTube Video Downloader by scrapearchitect (includes $5/month free credits)
            actor_id = "scrapearchitect/youtube-video-downloader"
            
            # Configure the actor input for the free alternative
            actor_input = {
                "startUrls": [youtube_url],
                "downloadMode": "video",  # Download video (not just metadata)
                "quality": "720p",
                "onlyUrl": False  # Include video file in response
            }
            
            # Stop current run if one is active
            if self.current_run_id:
                logger.info(f"Stopping previous run: {self.current_run_id}")
                self.stop_run(self.current_run_id)
            
            # Start the actor (don't wait for completion)
            logger.info("Starting Apify actor for video download...")
            run = self.client.actor(actor_id).start(run_input=actor_input)
            
            # Track the new active run
            self.current_run_id = run['id']
            
            return {
                'success': True,
                'run_id': run['id'],
                'status': 'RUNNING',
                'started_at': run.get('startedAt'),
                'actor_id': actor_id
            }
            
        except Exception as e:
            logger.error(f"Apify video download start error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'run_id': None
            }

    def download_youtube_video(self, youtube_url: str) -> Dict[str, Any]:
        """
        Download YouTube video using Apify actor and return video information
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Dict containing video download information
        """
        if not self.client:
            raise ValueError("Apify client not configured - missing APIFY_API_TOKEN")
        
        logger.info(f"Starting Apify video download for: {youtube_url}")
        
        try:
            # Using free YouTube Video Downloader by scrapearchitect (includes $5/month free credits)
            actor_id = "scrapearchitect/youtube-video-downloader"
            
            # Configure the actor input with proper proxy settings
            actor_input = {
                "startUrls": [youtube_url],
                "quality": "720",
                "proxy": {
                    "useApifyProxy": True
                }
            }
            
            # Run the actor
            logger.info("Running Apify actor for video download...")
            run = self.client.actor(actor_id).call(run_input=actor_input, wait_secs=60)
            
            # Wait for completion and get results with a timeout
            results = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(item)
            
            if not results:
                raise ValueError("No results returned from Apify actor")
            
            # Extract the first result (assuming single video)
            video_data = results[0]
            
            # Validate required fields
            if 'videoUrl' not in video_data:
                raise ValueError("Video URL not found in Apify results")
            
            logger.info("Apify video download completed successfully")
            
            return {
                'success': True,
                'video_url': video_data.get('videoUrl'),
                'title': video_data.get('title', ''),
                'duration': video_data.get('duration', ''),
                'file_size': video_data.get('fileSize', 0),
                'thumbnail_url': video_data.get('thumbnailUrl', ''),
                'description': video_data.get('description', ''),
                'view_count': video_data.get('viewCount', 0),
                'channel_name': video_data.get('channelName', ''),
                'published_at': video_data.get('publishedAt', ''),
                'download_time': time.time()
            }
            
        except Exception as e:
            logger.error(f"Apify video download error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'download_time': None
            }
    
    def get_actor_status(self, actor_id: str = "y1IMcEPawMQPafm02") -> Dict[str, Any]:
        """Get status information about the Apify actor"""
        if not self.client:
            return {'available': False, 'error': 'Apify client not configured'}
        
        try:
            actor_info = self.client.actor(actor_id).get()
            return {
                'available': True,
                'name': actor_info.get('name', ''),
                'description': actor_info.get('description', ''),
                'version': actor_info.get('taggedBuilds', {}).get('latest', {}).get('buildNumber', 'unknown')
            }
        except Exception as e:
            return {'available': False, 'error': str(e)}
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate Apify configuration and actor availability"""
        if not self.api_token:
            return {
                'configured': False,
                'error': 'APIFY_API_TOKEN environment variable not set'
            }
        
        if not self.client:
            return {
                'configured': False,
                'error': 'Failed to initialize Apify client'
            }
        
        # Test actor availability
        actor_status = self.get_actor_status()
        
        return {
            'configured': True,
            'actor_available': actor_status.get('available', False),
            'actor_info': actor_status
        }
    
    def get_run_progress(self, run_id: str) -> Dict[str, Any]:
        """
        Get real-time progress of an Apify run
        
        Args:
            run_id: The Apify run ID to monitor
            
        Returns:
            Dict containing progress information
        """
        if not self.client:
            return {'success': False, 'error': 'Apify client not configured'}
        
        try:
            # Get run information
            run_info = self.client.run(run_id).get()
            
            if not run_info:
                return {'success': False, 'error': 'Run not found'}
            
            # Get the log to extract progress percentage
            log_info = self.client.log(run_id).get()
            progress_percentage = 0
            status_message = "Initializing..."
            
            if log_info:
                # Parse the log for download progress
                log_lines = log_info.split('\n') if isinstance(log_info, str) else []
                
                for line in reversed(log_lines):  # Start from the most recent
                    if 'Downloading:' in line and '%' in line:
                        # Extract percentage from lines like "INFO  Downloading: ====                 18.2%"
                        try:
                            percentage_part = line.split('%')[0]
                            percentage_str = percentage_part.split()[-1]
                            progress_percentage = float(percentage_str)
                            status_message = f"Downloading video... {progress_percentage}%"
                            break
                        except (ValueError, IndexError):
                            continue
                    elif 'PHASE -- STARTING ACTOR' in line:
                        status_message = "Starting download actor..."
                    elif 'PHASE -- SETTING UP CRAWLER' in line:
                        status_message = "Setting up video crawler..."
                    elif 'CRAWLER -- Downloading' in line:
                        status_message = "Initializing video download..."
            
            # Determine overall status
            run_status = run_info.get('status', 'UNKNOWN')
            
            if run_status == 'SUCCEEDED':
                progress_percentage = 100
                status_message = "Download completed successfully!"
            elif run_status == 'FAILED':
                status_message = "Download failed"
                progress_percentage = 0
            elif run_status == 'ABORTED':
                status_message = "Download was cancelled"
                progress_percentage = 0
            
            # Get results if completed
            video_url = None
            file_size = None
            filename = None
            
            if run_status == 'SUCCEEDED':
                try:
                    results = []
                    for item in self.client.dataset(run_info["defaultDatasetId"]).iterate_items():
                        results.append(item)
                    
                    if results:
                        video_data = results[0]
                        # Try multiple field names for video URL
                        video_url = (video_data.get('videoUrl') or 
                                   video_data.get('downloadUrl') or
                                   video_data.get('url') or
                                   video_data.get('mp4Url'))
                        
                        # Get file size
                        file_size = (video_data.get('fileSize') or 
                                   video_data.get('size') or 
                                   video_data.get('contentLength') or 0)
                        
                        # Get filename - try to extract from URL or use title
                        filename = video_data.get('filename') or video_data.get('fileName')
                        if not filename and video_url:
                            # Extract filename from URL
                            import re
                            url_match = re.search(r'/([^/]+\.mp4)', video_url)
                            if url_match:
                                filename = url_match.group(1)
                            else:
                                # Get YouTube video ID and use it
                                source_url = video_data.get('sourceUrl', '')
                                video_id_match = re.search(r'[?&]v=([^&]+)', source_url)
                                if video_id_match:
                                    filename = f"{video_id_match.group(1)}.mp4"
                                else:
                                    filename = 'video.mp4'
                        
                        logger.info(f"Extracted MP4 data: URL={video_url}, Size={file_size}, Filename={filename}")
                        logger.info(f"Full video data: {video_data}")
                        
                except Exception as e:
                    logger.warning(f"Could not fetch results: {str(e)}")
            
            return {
                'success': True,
                'run_id': run_id,
                'status': run_status,
                'progress_percentage': progress_percentage,
                'status_message': status_message,
                'started_at': run_info.get('startedAt'),
                'finished_at': run_info.get('finishedAt'),
                'video_url': video_url,
                'file_size': file_size,
                'filename': filename,
                'duration_seconds': self._calculate_duration(run_info.get('startedAt'), run_info.get('finishedAt'))
            }
            
        except Exception as e:
            logger.error(f"Error getting run progress: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'run_id': run_id
            }
    
    def get_run_logs(self, run_id: str) -> str:
        """Get the complete logs for an Apify run"""
        try:
            if not self.client:
                self._initialize_client()
            
            # Get the logs using the requests method since the log client doesn't work directly
            import requests
            
            url = f"https://api.apify.com/v2/logs/{run_id}"
            headers = {
                'Authorization': f'Bearer {self.api_token}'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.text
            else:
                return f"Error retrieving logs: HTTP {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error retrieving logs for run {run_id}: {str(e)}")
            return f"Error retrieving logs: {str(e)}"
    
    def get_run_status(self, run_id: str) -> Dict[str, Any]:
        """Get the status of an Apify run"""
        try:
            if not self.client:
                return {'success': False, 'error': 'Apify client not configured'}
            
            run_info = self.client.run(run_id).get()
            if not run_info:
                return {'success': False, 'error': 'Run not found'}
            
            return {
                'success': True,
                'status': run_info.get('status', 'UNKNOWN'),
                'started_at': run_info.get('startedAt'),
                'finished_at': run_info.get('finishedAt'),
                'run_id': run_id
            }
        except Exception as e:
            logger.error(f"Error getting run status: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_run_results(self, run_id: str) -> Dict[str, Any]:
        """Get the results of a completed Apify run"""
        try:
            if not self.client:
                return {'success': False, 'error': 'Apify client not configured'}
            
            run_info = self.client.run(run_id).get()
            if not run_info:
                return {'success': False, 'error': 'Run not found'}
            
            # Get results from dataset
            results = []
            for item in self.client.dataset(run_info["defaultDatasetId"]).iterate_items():
                results.append(item)
            
            if not results:
                return {'success': False, 'error': 'No results found'}
            
            video_data = results[0]
            video_url = (video_data.get('videoUrl') or 
                        video_data.get('downloadUrl') or
                        video_data.get('url') or
                        video_data.get('mp4Url'))
            
            if not video_url:
                return {'success': False, 'error': 'No video URL found in results'}
            
            return {
                'success': True,
                'video_url': video_url,
                'file_size': video_data.get('fileSize', 0),
                'title': video_data.get('title', ''),
                'duration': video_data.get('duration', ''),
                'results': video_data
            }
            
        except Exception as e:
            logger.error(f"Error getting run results: {str(e)}")
            return {'success': False, 'error': str(e)}

    def stop_run(self, run_id: str) -> bool:
        """
        Stop an active Apify run
        
        Args:
            run_id: The run ID to stop
            
        Returns:
            True if stopped successfully, False otherwise
        """
        try:
            if not self.client:
                self._initialize_client()
            
            logger.info(f"Attempting to stop Apify run: {run_id}")
            
            # First check if run is still active
            run_info = self.client.run(run_id).get()
            status = run_info.get('status', 'UNKNOWN')
            
            if status in ['SUCCEEDED', 'FAILED', 'ABORTED']:
                logger.info(f"Run {run_id} already finished with status: {status}")
                return True
                
            # Abort the run
            self.client.run(run_id).abort()
            logger.info(f"Successfully stopped run: {run_id}")
            
            # Clear current run if it's this one
            if self.current_run_id == run_id:
                self.current_run_id = None
            
            return True
            
        except Exception as e:
            logger.warning(f"Failed to stop run {run_id}: {str(e)}")
            return False
    
    def get_current_run_id(self) -> Optional[str]:
        """Get the currently active run ID"""
        return self.current_run_id
    
    def clear_current_run(self):
        """Clear the current run tracking"""
        self.current_run_id = None

    def _calculate_duration(self, started_at: str, finished_at: str) -> Optional[int]:
        """Calculate duration in seconds between start and finish times"""
        try:
            if not started_at:
                return None
            
            from datetime import datetime
            start_time = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            
            if finished_at:
                end_time = datetime.fromisoformat(finished_at.replace('Z', '+00:00'))
                return int((end_time - start_time).total_seconds())
            else:
                # Still running
                current_time = datetime.now().replace(tzinfo=start_time.tzinfo)
                return int((current_time - start_time).total_seconds())
                
        except Exception:
            return None