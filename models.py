from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    # Google OAuth specific fields
    google_id = Column(String(100), unique=True)
    profile_picture = Column(String(500))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    youtube_url = Column(String(500), nullable=False, index=True)
    video_id = Column(String(50), nullable=False, index=True)
    course_title = Column(String(500), nullable=False)
    course_description = Column(Text)
    target_audience = Column(String(200))
    difficulty_level = Column(String(50))
    estimated_total_time = Column(String(50))
    
    # Video metadata
    video_title = Column(String(500))
    video_author = Column(String(200))
    video_duration = Column(String(50))
    video_view_count = Column(Integer)
    video_published_at = Column(String(50))
    video_thumbnail_url = Column(String(500))
    
    # MP4 video file
    mp4_video_url = Column(String(1000))  # URL to downloaded MP4 file
    mp4_file_size = Column(Integer)  # File size in bytes
    mp4_download_status = Column(String(20), default='pending')  # pending, downloading, completed, failed
    
    # Cloudinary premium storage
    cloudinary_url = Column(String(1000))  # Cloudinary streaming URL
    cloudinary_public_id = Column(String(500))  # Cloudinary video ID for management
    cloudinary_upload_status = Column(String(20), default='pending')  # pending, uploading, completed, failed
    
    # Course structure (JSON)
    days_structure = Column(JSON)
    final_project = Column(Text)
    resources = Column(JSON)
    assessment_criteria = Column(Text)
    
    # Processing metadata
    processing_time = Column(Float)
    total_cost = Column(Float)
    quality_score = Column(String(5))
    reliability_grade = Column(String(5))
    success_rate = Column(Float)
    
    # Status tracking
    status = Column(String(20), default='completed')  # processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    processing_logs = relationship("ProcessingLog", back_populates="course", cascade="all, delete-orphan")
    user_sessions = relationship("UserSession", back_populates="course")

class ProcessingLog(db.Model):
    __tablename__ = 'processing_logs'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    
    # API success tracking
    youtube_api_success = Column(Boolean, default=False)
    backup_api_success = Column(Boolean, default=False)
    scraper_success = Column(Boolean, default=False)
    
    # Transcript extraction
    apify_success = Column(Boolean, default=False)
    youtube_transcript_success = Column(Boolean, default=False)
    backup_transcript_success = Column(Boolean, default=False)
    
    # MP4 download tracking
    apify_mp4_success = Column(Boolean, default=False)
    mp4_download_time = Column(Float)
    
    # AI generation
    openrouter_success = Column(Boolean, default=False)
    claude_success = Column(Boolean, default=False)
    fallback_generator_success = Column(Boolean, default=False)
    
    # Error tracking
    errors = Column(JSON)
    warnings = Column(JSON)
    retries = Column(Integer, default=0)
    
    # Performance metrics
    metadata_extraction_time = Column(Float)
    transcript_extraction_time = Column(Float)
    ai_generation_time = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="processing_logs")

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), nullable=False, index=True)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Course generation
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)
    youtube_url_requested = Column(String(500))
    
    # Session tracking
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    status = Column(String(20), default='active')  # active, completed, abandoned, failed
    
    # Usage metrics
    total_requests = Column(Integer, default=1)
    total_processing_time = Column(Float)
    total_cost = Column(Float)
    
    # Relationships
    course = relationship("Course", back_populates="user_sessions")

class CourseProgress(db.Model):
    __tablename__ = 'course_progress'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    user_session = Column(String(100), nullable=False, index=True)  # Using session ID to track anonymous users
    
    # Progress tracking for 7 days
    day_1_completed = Column(Boolean, default=False)
    day_2_completed = Column(Boolean, default=False)
    day_3_completed = Column(Boolean, default=False)
    day_4_completed = Column(Boolean, default=False)
    day_5_completed = Column(Boolean, default=False)
    day_6_completed = Column(Boolean, default=False)
    day_7_completed = Column(Boolean, default=False)
    
    # Calculated progress
    completion_percentage = Column(Float, default=0.0)
    days_completed = Column(Integer, default=0)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)  # When all 7 days are completed
    
    # Relationships
    course = relationship("Course")

class SystemMetrics(db.Model):
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Daily aggregates
    total_courses_generated = Column(Integer, default=0)
    total_processing_time = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    average_quality_score = Column(Float)
    
    # Success rates
    overall_success_rate = Column(Float)
    api_success_rate = Column(Float)
    transcript_success_rate = Column(Float)
    ai_success_rate = Column(Float)
    
    # Performance metrics
    average_processing_time = Column(Float)
    fastest_processing_time = Column(Float)
    slowest_processing_time = Column(Float)
    
    # Error tracking
    total_errors = Column(Integer, default=0)
    total_warnings = Column(Integer, default=0)
    total_retries = Column(Integer, default=0)
    
    # API usage
    youtube_api_calls = Column(Integer, default=0)
    openrouter_api_calls = Column(Integer, default=0)
    claude_api_calls = Column(Integer, default=0)
    apify_api_calls = Column(Integer, default=0)