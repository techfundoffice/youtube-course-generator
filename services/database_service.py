import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        self.connection = None
        self.init_database()
    
    def get_connection(self):
        """Get database connection with retry logic"""
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self.connection or self.connection.closed:
                    self.connection = psycopg2.connect(
                        self.database_url,
                        cursor_factory=psycopg2.extras.RealDictCursor,
                        connect_timeout=10
                    )
                # Test the connection
                cursor = self.connection.cursor()
                cursor.execute('SELECT 1')
                cursor.close()
                return self.connection
            except (psycopg2.OperationalError, psycopg2.DatabaseError) as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    logger.error(f"Database connection failed after {max_retries} attempts: {e}")
                    raise e
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create courses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id SERIAL PRIMARY KEY,
                    youtube_url VARCHAR(500) NOT NULL,
                    video_id VARCHAR(50) NOT NULL,
                    course_title VARCHAR(500) NOT NULL,
                    course_description TEXT,
                    target_audience VARCHAR(200),
                    difficulty_level VARCHAR(50),
                    estimated_total_time VARCHAR(50),
                    video_title VARCHAR(500),
                    video_author VARCHAR(200),
                    video_duration VARCHAR(50),
                    video_view_count INTEGER,
                    video_published_at VARCHAR(50),
                    video_thumbnail_url VARCHAR(500),
                    mp4_video_url VARCHAR(1000),
                    mp4_file_size INTEGER,
                    mp4_download_status VARCHAR(20) DEFAULT 'pending',
                    transcript TEXT,
                    transcript_word_count INTEGER,
                    days_structure JSONB,
                    final_project TEXT,
                    resources JSONB,
                    assessment_criteria TEXT,
                    processing_time FLOAT,
                    total_cost FLOAT,
                    quality_score VARCHAR(5),
                    reliability_grade VARCHAR(5),
                    success_rate FLOAT,
                    status VARCHAR(20) DEFAULT 'completed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create processing_logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processing_logs (
                    id SERIAL PRIMARY KEY,
                    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
                    youtube_api_success BOOLEAN DEFAULT FALSE,
                    backup_api_success BOOLEAN DEFAULT FALSE,
                    scraper_success BOOLEAN DEFAULT FALSE,
                    apify_success BOOLEAN DEFAULT FALSE,
                    youtube_transcript_success BOOLEAN DEFAULT FALSE,
                    backup_transcript_success BOOLEAN DEFAULT FALSE,
                    apify_mp4_success BOOLEAN DEFAULT FALSE,
                    mp4_download_time FLOAT,
                    openrouter_success BOOLEAN DEFAULT FALSE,
                    claude_success BOOLEAN DEFAULT FALSE,
                    fallback_generator_success BOOLEAN DEFAULT FALSE,
                    errors JSONB,
                    warnings JSONB,
                    retries INTEGER DEFAULT 0,
                    metadata_extraction_time FLOAT,
                    transcript_extraction_time FLOAT,
                    ai_generation_time FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create user_sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(100) NOT NULL,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    course_id INTEGER REFERENCES courses(id),
                    youtube_url_requested VARCHAR(500),
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'active',
                    total_requests INTEGER DEFAULT 1,
                    total_processing_time FLOAT,
                    total_cost FLOAT
                );
            """)
            
            # Add transcript columns to existing courses table (migration)
            cursor.execute("""
                ALTER TABLE courses 
                ADD COLUMN IF NOT EXISTS transcript TEXT,
                ADD COLUMN IF NOT EXISTS transcript_word_count INTEGER;
            """)
            
            # Create course_progress table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS course_progress (
                    id SERIAL PRIMARY KEY,
                    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
                    user_session VARCHAR(100) NOT NULL,
                    day_1_completed BOOLEAN DEFAULT FALSE,
                    day_2_completed BOOLEAN DEFAULT FALSE,
                    day_3_completed BOOLEAN DEFAULT FALSE,
                    day_4_completed BOOLEAN DEFAULT FALSE,
                    day_5_completed BOOLEAN DEFAULT FALSE,
                    day_6_completed BOOLEAN DEFAULT FALSE,
                    day_7_completed BOOLEAN DEFAULT FALSE,
                    completion_percentage FLOAT DEFAULT 0.0,
                    days_completed INTEGER DEFAULT 0,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                );
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_courses_youtube_url ON courses(youtube_url);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_courses_video_id ON courses(video_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_courses_created_at ON courses(created_at);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_session_id ON user_sessions(session_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_course_progress_course_id ON course_progress(course_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_course_progress_user_session ON course_progress(user_session);")
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_course_progress_unique ON course_progress(course_id, user_session);")
            
            conn.commit()
            cursor.close()
            logger.info("Database tables initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
            if conn:
                conn.rollback()
    
    def save_course(self, course_data: Dict[str, Any], video_info: Dict[str, Any], 
                   metrics: Dict[str, Any], transcript: Optional[str] = None) -> Optional[int]:
        """Save course data to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Calculate transcript word count if transcript provided
            transcript_word_count = len(transcript.split()) if transcript else 0
            
            # Insert course data with proper field mapping
            cursor.execute("""
                INSERT INTO courses (
                    youtube_url, video_id, course_title, course_description,
                    target_audience, difficulty_level, estimated_total_time,
                    video_title, video_author, video_duration, video_view_count,
                    video_published_at, video_thumbnail_url, transcript, transcript_word_count,
                    days_structure, final_project, resources, assessment_criteria,
                    processing_time, total_cost, quality_score, reliability_grade,
                    success_rate, status, mp4_video_url, mp4_file_size, 
                    mp4_download_status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING id;
            """, (
                video_info.get('youtube_url', ''),
                video_info.get('video_id', ''),
                course_data.get('course_title', 'Untitled Course'),
                course_data.get('course_description', 'Course generated from video'),
                course_data.get('target_audience', 'General Audience'),
                course_data.get('difficulty_level', 'Beginner'),
                course_data.get('estimated_total_time', '7 days'),
                video_info.get('title', 'Untitled Video'),
                video_info.get('author', 'Unknown'),
                video_info.get('duration', 'Unknown'),
                video_info.get('view_count', 0),
                video_info.get('published_at', 'Unknown'),
                video_info.get('thumbnail_url', ''),
                transcript,
                transcript_word_count,
                json.dumps(course_data.get('days', [])),
                course_data.get('final_project', 'Complete a project based on the course content'),
                json.dumps(course_data.get('resources', [])),
                course_data.get('assessment_criteria', 'Completion of daily activities and final project'),
                metrics.get('processing_time', 0.0),
                metrics.get('total_cost', 0.0),
                metrics.get('quality_score', 'C'),
                metrics.get('reliability_grade', 'C'),
                metrics.get('overall_success_rate', 0.0),
                'completed',
                video_info.get('mp4_video_url', ''),
                video_info.get('mp4_file_size', 0),
                video_info.get('mp4_download_status', 'pending')
            ))
            
            result = cursor.fetchone()
            if result is None:
                conn.rollback()
                cursor.close()
                logger.error("INSERT statement failed - no row returned")
                return None
                
            course_id = result['id']
            conn.commit()
            cursor.close()
            
            logger.info(f"Course saved with ID: {course_id}")
            return course_id
            
        except Exception as e:
            logger.error(f"Error saving course: {str(e)}")
            logger.error(f"Course data keys: {list(course_data.keys()) if course_data else 'None'}")
            logger.error(f"Video info keys: {list(video_info.keys()) if video_info else 'None'}")
            logger.error(f"Transcript length: {len(transcript) if transcript else 0}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            if conn:
                conn.rollback()
            return None
    
    def save_processing_log(self, course_id: int, metrics: Dict[str, Any]) -> bool:
        """Save processing log to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Extract API success data
            api_success = metrics.get('api_success', {})
            transcript_success = metrics.get('transcript_success', {})
            ai_success = metrics.get('ai_success', {})
            quality_metrics = metrics.get('quality_metrics', {})
            
            cursor.execute("""
                INSERT INTO processing_logs (
                    course_id, youtube_api_success, backup_api_success, scraper_success,
                    apify_success, youtube_transcript_success, backup_transcript_success,
                    apify_mp4_success, mp4_download_time, openrouter_success, 
                    claude_success, fallback_generator_success, errors, warnings, retries
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                );
            """, (
                course_id,
                api_success.get('youtube_api', False),
                api_success.get('backup_api', False),
                api_success.get('scraper', False),
                transcript_success.get('apify', False),
                transcript_success.get('youtube_transcript', False),
                transcript_success.get('backup_transcript', False),
                metrics.get('apify_mp4_success', False),
                metrics.get('mp4_download_time', None),
                ai_success.get('openrouter', False),
                ai_success.get('claude', False),
                ai_success.get('fallback_generator', False),
                json.dumps(quality_metrics.get('errors', [])),
                json.dumps(quality_metrics.get('warnings', [])),
                quality_metrics.get('retries', 0)
            ))
            
            conn.commit()
            cursor.close()
            logger.info(f"Processing log saved for course ID: {course_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving processing log: {str(e)}")
            if conn:
                conn.rollback()
            return False
    
    def save_user_session(self, session_data: Dict[str, Any]) -> bool:
        """Save user session to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_sessions (
                    session_id, ip_address, user_agent, youtube_url_requested,
                    total_processing_time, total_cost
                ) VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                session_data.get('session_id', ''),
                session_data.get('ip_address', ''),
                session_data.get('user_agent', ''),
                session_data.get('youtube_url', ''),
                session_data.get('processing_time', 0.0),
                session_data.get('total_cost', 0.0)
            ))
            
            conn.commit()
            cursor.close()
            return True
            
        except Exception as e:
            logger.error(f"Error saving user session: {str(e)}")
            if conn:
                conn.rollback()
            return False
    
    def get_course_by_url(self, youtube_url: str) -> Optional[Dict[str, Any]]:
        """Get existing course by YouTube URL"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT * FROM courses 
                WHERE youtube_url = %s 
                ORDER BY created_at DESC 
                LIMIT 1;
            """, (youtube_url,))
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return dict(result)
            return None
            
        except Exception as e:
            logger.error(f"Error getting course by URL: {str(e)}")
            return None
    
    def get_course_by_id(self, course_id: int) -> Optional[Dict[str, Any]]:
        """Get course by ID with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                conn = self.get_connection()
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                cursor.execute("""
                    SELECT * FROM courses 
                    WHERE id = %s;
                """, (course_id,))
                
                result = cursor.fetchone()
                cursor.close()
                
                if result:
                    return dict(result)
                return None
                
            except (psycopg2.OperationalError, psycopg2.DatabaseError) as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Database query attempt {attempt + 1} failed, retrying: {e}")
                    self.connection = None  # Force reconnection
                    import time
                    time.sleep(1)
                    continue
                else:
                    logger.error(f"Error getting course by ID after {max_retries} attempts: {e}")
                    return None
    
    def get_recent_courses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent courses"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT id, course_title, video_title, video_author, quality_score,
                       processing_time, total_cost, created_at
                FROM courses 
                ORDER BY created_at DESC 
                LIMIT %s;
            """, (limit,))
            
            results = cursor.fetchall()
            cursor.close()
            
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"Error getting recent courses: {str(e)}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get total courses
            cursor.execute("SELECT COUNT(*) FROM courses;")
            total_courses = cursor.fetchone()[0]
            
            # Get total processing time
            cursor.execute("SELECT SUM(processing_time) FROM courses WHERE processing_time IS NOT NULL;")
            total_processing_time = cursor.fetchone()[0] or 0
            
            # Get total cost
            cursor.execute("SELECT SUM(total_cost) FROM courses WHERE total_cost IS NOT NULL;")
            total_cost = cursor.fetchone()[0] or 0
            
            # Get average quality score
            cursor.execute("""
                SELECT AVG(
                    CASE quality_score 
                        WHEN 'A+' THEN 95
                        WHEN 'A' THEN 85
                        WHEN 'B' THEN 75
                        WHEN 'C' THEN 65
                        ELSE 50
                    END
                ) FROM courses WHERE quality_score IS NOT NULL;
            """)
            avg_quality = cursor.fetchone()[0] or 0
            
            # Get courses created today
            cursor.execute("""
                SELECT COUNT(*) FROM courses 
                WHERE DATE(created_at) = CURRENT_DATE;
            """)
            courses_today = cursor.fetchone()[0]
            
            cursor.close()
            
            return {
                'total_courses': total_courses,
                'total_processing_time': round(total_processing_time, 2),
                'total_cost': round(total_cost, 4),
                'average_quality_score': round(avg_quality, 1),
                'courses_today': courses_today
            }
            
        except Exception as e:
            logger.error(f"Error getting database stats: {str(e)}")
            return {}
    
    def get_course_progress(self, course_id: int, user_session: str) -> Optional[Dict[str, Any]]:
        """Get course progress for a specific user session and course"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT * FROM course_progress 
                WHERE course_id = %s AND user_session = %s;
            """, (course_id, user_session))
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return dict(result)
            return None
            
        except Exception as e:
            logger.error(f"Error getting course progress: {str(e)}")
            return None
    
    def save_course_progress(self, course_id: int, user_session: str, progress_data: Dict[str, bool]) -> bool:
        """Save or update course progress"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Calculate completion stats
            days_completed = sum(1 for completed in progress_data.values() if completed)
            completion_percentage = (days_completed / 7) * 100
            completed_at = datetime.now() if days_completed == 7 else None
            
            # Use INSERT ... ON CONFLICT for upsert functionality
            cursor.execute("""
                INSERT INTO course_progress (
                    course_id, user_session, 
                    day_1_completed, day_2_completed, day_3_completed, day_4_completed,
                    day_5_completed, day_6_completed, day_7_completed,
                    completion_percentage, days_completed, completed_at, last_updated
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (course_id, user_session) 
                DO UPDATE SET 
                    day_1_completed = EXCLUDED.day_1_completed,
                    day_2_completed = EXCLUDED.day_2_completed,
                    day_3_completed = EXCLUDED.day_3_completed,
                    day_4_completed = EXCLUDED.day_4_completed,
                    day_5_completed = EXCLUDED.day_5_completed,
                    day_6_completed = EXCLUDED.day_6_completed,
                    day_7_completed = EXCLUDED.day_7_completed,
                    completion_percentage = EXCLUDED.completion_percentage,
                    days_completed = EXCLUDED.days_completed,
                    completed_at = EXCLUDED.completed_at,
                    last_updated = CURRENT_TIMESTAMP;
            """, (
                course_id, user_session,
                progress_data.get('day_1', False),
                progress_data.get('day_2', False),
                progress_data.get('day_3', False),
                progress_data.get('day_4', False),
                progress_data.get('day_5', False),
                progress_data.get('day_6', False),
                progress_data.get('day_7', False),
                completion_percentage, days_completed, completed_at
            ))
            
            conn.commit()
            cursor.close()
            logger.info(f"Course progress saved for course {course_id}, session {user_session}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving course progress: {str(e)}")
            if conn:
                conn.rollback()
            return False

    def close_connection(self):
        """Close database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()