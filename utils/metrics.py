import time
from datetime import datetime
from typing import Dict, Any, List

class ProcessingMetrics:
    """Track processing metrics and success rates for reliability scoring"""
    
    def __init__(self):
        self.start_time = time.time()
        self.processing_time = 0.0
        self.total_cost = 0.0
        
        # API Success Tracking
        self.youtube_api_success = False
        self.backup_api_success = False
        self.scraper_success = False
        
        # Transcript Success Tracking
        self.apify_success = False
        self.youtube_transcript_success = False
        self.backup_transcript_success = False
        
        # AI Generation Success Tracking
        self.openrouter_success = False
        self.claude_success = False
        self.fallback_generator_success = False
        
        # MP4 Download Tracking
        self.apify_mp4_success = False
        self.mp4_download_time = 0.0
        
        # Session tracking
        self.session_id = ""
        
        # Quality Metrics
        self.errors = []
        self.warnings = []
        self.retries = 0
        
    def add_error(self, error: str):
        """Add an error to the metrics"""
        self.errors.append({
            'timestamp': datetime.utcnow().isoformat(),
            'error': error
        })
    
    def add_warning(self, warning: str):
        """Add a warning to the metrics"""
        self.warnings.append({
            'timestamp': datetime.utcnow().isoformat(),
            'warning': warning
        })
    
    def add_retry(self):
        """Increment retry counter"""
        self.retries += 1
    
    def add_cost(self, cost: float):
        """Add to total cost"""
        self.total_cost += cost
    
    def set_processing_time(self, processing_time: float):
        """Set the total processing time"""
        self.processing_time = processing_time
    
    def get_metadata_success_rate(self) -> float:
        """Calculate metadata extraction success rate"""
        attempts = 3  # YouTube API, backup API, scraper
        successes = sum([
            self.youtube_api_success,
            self.backup_api_success,
            self.scraper_success
        ])
        return successes / attempts
    
    def get_transcript_success_rate(self) -> float:
        """Calculate transcript extraction success rate"""
        attempts = 3  # Apify, YouTube transcript, backup
        successes = sum([
            self.apify_success,
            self.youtube_transcript_success,
            self.backup_transcript_success
        ])
        return successes / attempts
    
    def get_ai_success_rate(self) -> float:
        """Calculate AI generation success rate"""
        attempts = 3  # OpenRouter, Claude, fallback generator
        successes = sum([
            self.openrouter_success,
            self.claude_success,
            self.fallback_generator_success
        ])
        return successes / attempts
    
    def get_overall_success_rate(self) -> float:
        """Calculate overall success rate"""
        metadata_rate = self.get_metadata_success_rate()
        transcript_rate = self.get_transcript_success_rate()
        ai_rate = self.get_ai_success_rate()
        
        # Weighted average (metadata is most critical)
        return (metadata_rate * 0.4 + transcript_rate * 0.3 + ai_rate * 0.3)
    
    def get_reliability_grade(self) -> str:
        """Get reliability grade based on success rates"""
        success_rate = self.get_overall_success_rate()
        
        if success_rate >= 0.95:
            return "A+"
        elif success_rate >= 0.85:
            return "A"
        elif success_rate >= 0.75:
            return "B"
        elif success_rate >= 0.65:
            return "C"
        else:
            return "D"
    
    def get_cost_category(self) -> str:
        """Categorize the processing cost"""
        if self.total_cost <= 0.75:
            return "Low"
        elif self.total_cost <= 1.50:
            return "Medium"
        else:
            return "High"
    
    def get_speed_category(self) -> str:
        """Categorize the processing speed"""
        if self.processing_time <= 60:
            return "Fast"
        elif self.processing_time <= 120:
            return "Medium"
        else:
            return "Slow"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for JSON serialization"""
        return {
            'processing_time': round(self.processing_time, 2),
            'total_cost': round(self.total_cost, 4),
            'cost_category': self.get_cost_category(),
            'speed_category': self.get_speed_category(),
            'reliability_grade': self.get_reliability_grade(),
            'overall_success_rate': round(self.get_overall_success_rate(), 3),
            'api_success': {
                'youtube_api': self.youtube_api_success,
                'backup_api': self.backup_api_success,
                'scraper': self.scraper_success,
                'metadata_success_rate': round(self.get_metadata_success_rate(), 3)
            },
            'transcript_success': {
                'apify': self.apify_success,
                'youtube_transcript': self.youtube_transcript_success,
                'backup_transcript': self.backup_transcript_success,
                'transcript_success_rate': round(self.get_transcript_success_rate(), 3)
            },
            'ai_success': {
                'openrouter': self.openrouter_success,
                'claude': self.claude_success,
                'fallback_generator': self.fallback_generator_success,
                'ai_success_rate': round(self.get_ai_success_rate(), 3)
            },
            'quality_metrics': {
                'errors_count': len(self.errors),
                'warnings_count': len(self.warnings),
                'retries': self.retries,
                'errors': self.errors[-5:],  # Last 5 errors
                'warnings': self.warnings[-5:]  # Last 5 warnings
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_summary_stats(self) -> Dict[str, str]:
        """Get human-readable summary statistics"""
        return {
            'Processing Time': f"{self.processing_time:.1f} seconds ({self.get_speed_category()})",
            'Total Cost': f"${self.total_cost:.4f} ({self.get_cost_category()})",
            'Reliability Grade': f"{self.get_reliability_grade()} ({self.get_overall_success_rate():.1%} success)",
            'Metadata Extraction': "✓" if any([self.youtube_api_success, self.backup_api_success, self.scraper_success]) else "✗",
            'Transcript Extraction': "✓" if any([self.apify_success, self.youtube_transcript_success, self.backup_transcript_success]) else "✗",
            'AI Generation': "✓" if any([self.openrouter_success, self.claude_success, self.fallback_generator_success]) else "✗",
            'Errors': str(len(self.errors)),
            'Retries': str(self.retries)
        }
