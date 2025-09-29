"""
Shared test configuration and fixtures for the YouTube Course Generator test suite.
"""
import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from app import app, db

@pytest.fixture(scope='session')
def test_app():
    """Create application instance for testing."""
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(test_app):
    """Create test client."""
    return test_app.test_client()

@pytest.fixture
def runner(test_app):
    """Create test CLI runner."""
    return test_app.test_cli_runner()

@pytest.fixture
def mock_database_service():
    """Mock database service for testing."""
    with patch('services.database_service.DatabaseService') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_youtube_service():
    """Mock YouTube service for testing."""
    with patch('services.youtube_service.YouTubeService') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_ai_service():
    """Mock AI service for testing."""
    with patch('services.ai_service.AIService') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_transcript_service():
    """Mock transcript service for testing."""
    with patch('services.transcript_service.TranscriptService') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def sample_video_data():
    """Sample video data for testing."""
    return {
        'video_id': 'dQw4w9WgXcQ',
        'title': 'Sample Video Title',
        'description': 'Sample video description',
        'duration': '3:32',
        'view_count': 1000000,
        'published_at': '2023-01-01T00:00:00Z',
        'thumbnail_url': 'https://example.com/thumb.jpg'
    }

@pytest.fixture
def sample_course_data():
    """Sample course data for testing."""
    return {
        'course_title': 'Learn Python Programming',
        'course_description': 'A comprehensive Python course',
        'target_audience': 'Beginners',
        'difficulty_level': 'Beginner',
        'estimated_total_time': '7 days',
        'days_structure': [
            {
                'day': 1,
                'title': 'Introduction to Python',
                'learning_objectives': ['Understand Python basics'],
                'activities': [
                    {
                        'type': 'reading',
                        'title': 'Python Overview',
                        'estimated_time': '30 minutes'
                    }
                ],
                'key_takeaways': ['Python is a versatile language'],
                'homework': 'Install Python on your computer'
            }
        ],
        'final_project': 'Build a simple calculator',
        'resources': ['Python.org documentation'],
        'assessment_criteria': 'Project completion and understanding'
    }

@pytest.fixture
def sample_transcript():
    """Sample transcript for testing."""
    return "Hello and welcome to this tutorial. Today we'll learn about Python programming..."