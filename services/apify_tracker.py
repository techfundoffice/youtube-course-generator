"""
Real-time Apify actor status tracking service for integration with processing logs
"""
import os
import time
import asyncio
import logging
from typing import Dict, Any, Optional
from apify_client import ApifyClient
from services.log_service import log_processing_step

logger = logging.getLogger(__name__)

class ApifyActorTracker:
    """Track Apify actor runs and integrate status updates into processing logs"""
    
    def __init__(self):
        self.api_token = os.environ.get('APIFY_API_TOKEN')
        if not self.api_token:
            logger.warning("APIFY_API_TOKEN not configured")
            self.client = None
        else:
            self.client = ApifyClient(self.api_token)
    
    def get_detailed_run_status(self, run_id: str) -> Dict[str, Any]:
        """
        Get comprehensive Apify run status using real API endpoints
        
        Returns detailed information about:
        - Run status (READY, RUNNING, SUCCEEDED, FAILED, TIMED-OUT, ABORTED)
        - Runtime statistics (duration, compute units, data transfer)
        - Dataset results (if completed successfully)
        - Error information (if failed)
        """
        if not self.client:
            return {
                'run_id': run_id,
                'status': 'ERROR',
                'error': 'Apify client not configured - missing APIFY_API_TOKEN'
            }
        
        try:
            # Get run information from Apify API
            run_info = self.client.run(run_id).get()
            
            status = run_info.get('status', 'UNKNOWN')
            stats = run_info.get('stats', {})
            
            # Base result with all API data
            result = {
                'run_id': run_id,
                'status': status,
                'started_at': run_info.get('startedAt'),
                'finished_at': run_info.get('finishedAt'),
                'actor_id': run_info.get('actId'),
                'build_id': run_info.get('buildId'),
                'build_number': run_info.get('buildNumber'),
                'exit_code': run_info.get('exitCode'),
                'container_url': run_info.get('containerUrl'),
                'status_message': run_info.get('statusMessage'),
                'meta': run_info.get('meta', {}),
                'options': run_info.get('options', {}),
                'usage': {
                    'duration_millis': stats.get('durationMillis', 0),
                    'run_duration_millis': stats.get('runDurationMillis', 0),
                    'metamorph_millis': stats.get('metamorphMillis', 0),
                    'compute_units': stats.get('computeUnits', 0),
                    'data_transfer_bytes': stats.get('dataTransferBytes', 0)
                }
            }
            
            # Add human-readable status information
            duration_str = self._format_duration(stats.get('durationMillis', 0))
            compute_units = stats.get('computeUnits', 0)
            data_transfer = self._format_bytes(stats.get('dataTransferBytes', 0))
            
            if status == 'RUNNING':
                result['display_message'] = f"YouTube MP4 download running ({duration_str}, {compute_units:.4f} CU, {data_transfer})"
                result['progress_details'] = f"Actor processing video for {duration_str}"
                
            elif status == 'SUCCEEDED':
                # Get dataset results for successful runs
                try:
                    dataset_id = run_info.get('defaultDatasetId')
                    if dataset_id:
                        dataset_client = self.client.dataset(dataset_id)
                        items = list(dataset_client.iterate_items())
                        
                        if items and len(items) > 0:
                            video_data = items[0]  # First video result
                            
                            # Extract data according to actor documentation
                            source_url = video_data.get('sourceUrl', '')
                            download_url = video_data.get('downloadUrl', '')
                            
                            # Try to get file size from download URL or metadata
                            file_size = 0
                            if download_url:
                                # Extract potential file size info or make HEAD request
                                try:
                                    import requests
                                    response = requests.head(download_url, timeout=5)
                                    if 'content-length' in response.headers:
                                        file_size = int(response.headers['content-length'])
                                except:
                                    pass
                            
                            result.update({
                                'success': True,
                                'video_data': video_data,
                                'source_url': source_url,
                                'download_url': download_url,
                                'mp4_video_url': download_url,
                                'file_size': file_size,
                                'display_message': f"MP4 download completed ({self._format_bytes(file_size)}, {duration_str}, {compute_units:.4f} CU)",
                                'success_details': f"Video available at: {download_url}"
                            })
                        else:
                            result['display_message'] = f"Download completed but no video data found ({duration_str})"
                    else:
                        result['display_message'] = f"Download completed ({duration_str}, {compute_units:.4f} CU)"
                        
                except Exception as e:
                    logger.warning(f"Could not retrieve dataset for run {run_id}: {str(e)}")
                    result['display_message'] = f"Download completed but data retrieval failed ({duration_str})"
                    result['dataset_error'] = str(e)
            
            elif status == 'FAILED':
                exit_code = run_info.get('exitCode', 'unknown')
                status_msg = run_info.get('statusMessage', 'Unknown failure')
                result['display_message'] = f"MP4 download failed (exit code: {exit_code}, {duration_str})"
                result['error_details'] = f"Failure reason: {status_msg}"
                
            elif status == 'ABORTED':
                result['display_message'] = f"MP4 download aborted ({duration_str})"
                result['abort_details'] = run_info.get('statusMessage', 'Manual abort')
                
            elif status == 'TIMED-OUT':
                result['display_message'] = f"MP4 download timed out ({duration_str})"
                result['timeout_details'] = "Actor exceeded maximum runtime"
                
            elif status == 'READY':
                result['display_message'] = "MP4 download queued, waiting to start"
                
            else:
                result['display_message'] = f"MP4 download status: {status} ({duration_str})"
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting Apify run status for {run_id}: {str(e)}")
            return {
                'run_id': run_id,
                'status': 'ERROR',
                'error': str(e),
                'display_message': f"Error checking MP4 download status: {str(e)}"
            }
    
    async def track_run_with_logging(self, run_id: str, session_id: str, max_checks: int = 30, check_interval: int = 10):
        """
        Track an Apify run and log status updates to processing logs
        
        Args:
            run_id: Apify run ID to track
            session_id: Session ID for logging
            max_checks: Maximum number of status checks
            check_interval: Seconds between status checks
        """
        logger.info(f"Starting Apify run tracking for {run_id} (session: {session_id})")
        
        for check_num in range(max_checks):
            try:
                status_info = self.get_detailed_run_status(run_id)
                
                status = status_info.get('status', 'UNKNOWN')
                display_message = status_info.get('display_message', f'Status: {status}')
                
                # Log current status
                if status == 'RUNNING':
                    log_processing_step(session_id, "Apify MP4 Download", "RUNNING", display_message)
                elif status == 'SUCCEEDED':
                    log_processing_step(session_id, "Apify MP4 Download", "SUCCESS", display_message)
                    logger.info(f"Apify run {run_id} completed successfully")
                    return status_info
                elif status in ['FAILED', 'ABORTED', 'TIMED-OUT']:
                    log_processing_step(session_id, "Apify MP4 Download", "FAILED", display_message, "ERROR")
                    logger.error(f"Apify run {run_id} failed with status: {status}")
                    return status_info
                elif status == 'READY':
                    log_processing_step(session_id, "Apify MP4 Download", "QUEUED", display_message)
                else:
                    log_processing_step(session_id, "Apify MP4 Download", "UNKNOWN", display_message, "WARNING")
                
                # Wait before next check
                if check_num < max_checks - 1:  # Don't wait after last check
                    await asyncio.sleep(check_interval)
                    
            except Exception as e:
                error_msg = f"Error tracking run {run_id}: {str(e)}"
                log_processing_step(session_id, "Apify MP4 Download", "ERROR", error_msg, "ERROR")
                logger.error(error_msg)
                return {'run_id': run_id, 'status': 'ERROR', 'error': str(e)}
        
        # If we've reached max_checks, log timeout
        timeout_msg = f"Stopped tracking after {max_checks} checks ({max_checks * check_interval / 60:.1f} minutes)"
        log_processing_step(session_id, "Apify MP4 Download", "TIMEOUT", timeout_msg, "WARNING")
        logger.warning(f"Stopped tracking Apify run {run_id} after {max_checks} checks")
        
        # Return final status
        return self.get_detailed_run_status(run_id)
    
    def _format_duration(self, millis: int) -> str:
        """Format duration in milliseconds to human readable format"""
        if millis < 1000:
            return f"{millis}ms"
        seconds = millis // 1000
        if seconds < 60:
            return f"{seconds}s"
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if minutes < 60:
            return f"{minutes}m {remaining_seconds}s"
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m"
    
    def _format_bytes(self, bytes_count: int) -> str:
        """Format bytes to human readable format"""
        if bytes_count == 0:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_count < 1024:
                return f"{bytes_count:.1f} {unit}"
            bytes_count /= 1024
        return f"{bytes_count:.1f} TB"

# Global instance
apify_tracker = ApifyActorTracker()