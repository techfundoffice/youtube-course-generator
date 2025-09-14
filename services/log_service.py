"""
Real-time processing logs service for capturing and streaming course generation steps.
"""
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import threading
from collections import deque

class ProcessingLogger:
    def __init__(self, max_logs=1000):
        self.logs = deque(maxlen=max_logs)
        self.session_logs = {}  # session_id -> logs
        self.lock = threading.Lock()
        
    def log_step(self, session_id: str, step: str, status: str, details: str = "", level: str = "INFO"):
        """Log a processing step with timestamp and status"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        log_entry = {
            "timestamp": timestamp,
            "session_id": session_id,
            "step": step,
            "status": status,
            "details": details,
            "level": level
        }
        
        with self.lock:
            # Add to global logs
            self.logs.append(log_entry)
            
            # Add to session-specific logs
            if session_id not in self.session_logs:
                self.session_logs[session_id] = deque(maxlen=100)
            self.session_logs[session_id].append(log_entry)
            
        # Also log to system logger
        logger = logging.getLogger(__name__)
        if level == "ERROR":
            logger.error(f"[{session_id}] {step}: {status} - {details}")
        elif level == "WARNING":
            logger.warning(f"[{session_id}] {step}: {status} - {details}")
        else:
            logger.info(f"[{session_id}] {step}: {status} - {details}")
    
    def get_session_logs(self, session_id: str) -> List[Dict[str, Any]]:
        """Get logs for a specific session"""
        with self.lock:
            if session_id in self.session_logs:
                return list(self.session_logs[session_id])
            return []
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent logs across all sessions"""
        with self.lock:
            return list(self.logs)[-limit:]
    
    def clear_session_logs(self, session_id: str):
        """Clear logs for a specific session"""
        with self.lock:
            if session_id in self.session_logs:
                self.session_logs[session_id].clear()

# Global instance
processing_logger = ProcessingLogger()

def log_processing_step(session_id: str, step: str, status: str, details: str = "", level: str = "INFO", **kwargs):
    """Enhanced logging with troubleshooting context"""
    # Add troubleshooting metadata
    enhanced_details = details
    if kwargs:
        metadata = []
        if 'duration' in kwargs:
            metadata.append(f"Duration: {kwargs['duration']}s")
        if 'error_code' in kwargs:
            metadata.append(f"Error: {kwargs['error_code']}")
        if 'api_status' in kwargs:
            metadata.append(f"API Status: {kwargs['api_status']}")
        if 'retry_count' in kwargs:
            metadata.append(f"Retry: {kwargs['retry_count']}")
        if 'fallback_used' in kwargs:
            metadata.append(f"Fallback: {kwargs['fallback_used']}")
        if 'file_size' in kwargs:
            metadata.append(f"Size: {kwargs['file_size']}")
        
        if metadata:
            enhanced_details = f"{details} | {' | '.join(metadata)}"
    
    processing_logger.log_step(session_id, step, status, enhanced_details, level)

def log_api_call(session_id: str, service: str, endpoint: str, status_code: int, duration: float, error: Optional[str] = None):
    """Log API calls with troubleshooting context"""
    status = "SUCCESS" if 200 <= status_code < 300 else "FAILED"
    level = "INFO" if status == "SUCCESS" else "ERROR"
    
    details = f"{service} API call to {endpoint}"
    if error:
        details += f" - Error: {error}"
    
    log_processing_step(session_id, f"{service} API", status, details, level, 
                       api_status=status_code, duration=round(duration, 2))

def log_fallback_activation(session_id: str, primary_service: str, fallback_service: str, reason: str):
    """Log when fallback systems are activated"""
    log_processing_step(session_id, "Fallback System", "ACTIVATED", 
                       f"Switched from {primary_service} to {fallback_service}: {reason}", 
                       "WARNING", fallback_used=fallback_service)

def log_performance_metric(session_id: str, metric_name: str, value: float, unit: str = ""):
    """Log performance metrics for troubleshooting"""
    log_processing_step(session_id, "Performance", "METRIC", 
                       f"{metric_name}: {value}{unit}", "INFO")

def get_processing_logs(session_id: str) -> List[Dict[str, Any]]:
    """Get processing logs with enhanced troubleshooting data"""
    return processing_logger.get_session_logs(session_id)