"""
Integration tests for Flask application routes.
"""
import pytest
import json
from unittest.mock import patch, Mock

class TestWebRoutes:
    """Test web application routes and endpoints."""
    
    def test_index_page_loads(self, client):
        """Test main page loads correctly."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'YouTube Course Generator' in response.data
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'status' in data
        assert 'timestamp' in data
    
    def test_list_courses_page(self, client):
        """Test courses listing page."""
        response = client.get('/courses')
        assert response.status_code == 200
        assert b'Recent Courses' in response.data or b'No courses available' in response.data or b'No courses available' in response.data
    
    def test_test_dashboard_page(self, client):
        """Test test dashboard page loads."""
        response = client.get('/test-dashboard')
        assert response.status_code == 200
        assert b'Dashboard' in response.data

class TestAPIRoutes:
    """Test API endpoints."""
    
    def test_api_list_courses(self, client):
        """Test API courses listing."""
        response = client.get('/api/courses')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'courses' in data
        assert isinstance(data['courses'], list)
    
    def test_api_stats(self, client):
        """Test API stats endpoint."""
        response = client.get('/api/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'total_courses' in data
        assert 'average_success_rate' in data
    
    @patch('app.TestRunner')
    def test_api_run_tests(self, mock_test_runner, client):
        """Test running tests via API."""
        mock_runner = Mock()
        mock_runner.run_async.return_value = {'success': True}
        mock_test_runner.return_value = mock_runner
        
        response = client.post('/api/tests/run', 
                              json={'coverage': True, 'verbose': True})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'success' in data
    
    def test_api_test_status(self, client):
        """Test test status API endpoint."""
        response = client.get('/api/tests/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'running' in data

class TestCourseGeneration:
    """Test course generation functionality."""
    
    @patch('app.process_youtube_video')
    def test_generate_course_api_valid_url(self, mock_process, client):
        """Test course generation with valid YouTube URL."""
        # Mock successful processing
        mock_process.return_value = {
            'status': 'success',
            'course_id': '12345'
        }
        response = client.post('/api/courses/generate', json={'url': 'https://valid.youtube.url'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'course_id' in data

    @patch('app.process_youtube_video')
    def test_generate_course_api_invalid_url(self, mock_process, client):
        """Test course generation with invalid YouTube URL."""
        # Mock failed processing
        mock_process.side_effect = ValueError('Invalid URL')
        response = client.post('/api/courses/generate', json={'url': 'https://invalid.youtube.url'})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Invalid URL' 'success',
            'course': {'course_title': 'Test Course'}
        }
        
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        assert response.status_code == 200
    
    def test_generate_course_api_invalid_url(self, client):
        """Test course generation with invalid URL."""
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'invalid_url'})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_generate_course_web_form_get(self, client):
        """Test course generation form page."""
        response = client.get('/generate')
        assert response.status_code == 200
        assert b'Generate Course' in response.data
    
    @patch('app.process_youtube_video')
    def test_generate_course_web_form_post(self, mock_process, client):
        """Test course generation form submission."""
        mock_process.return_value = {
            'status': 'success',
            'course_id': '12345'
        }
        response = client.post('/api/courses/generate', json={'url': 'https://valid.youtube.url'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'course_id' in data

    @patch('app.process_youtube_video')
    def test_generate_course_api_invalid_url(self, mock_process, client):
        """Test course generation with invalid YouTube URL."""
        # Mock failed processing
        mock_process.side_effect = ValueError('Invalid URL')
        response = client.post('/api/courses/generate', json={'url': 'https://invalid.youtube.url'})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Invalid URL' 'success',
            'course': {'course_title': 'Test Course'}
        }
        
        response = client.post('/generate', 
                              data={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        # Should redirect to course view
        assert response.status_code in [200, 302]

class TestAIAssistant:
    """Test AI assistant functionality."""
    
    def test_ai_testing_assistant_page(self, client):
        """Test AI testing assistant page loads."""
        response = client.get('/ai-assistant')
        assert response.status_code == 200
        assert b'AI Testing Assistant' in response.data
    
    def test_ai_code_monitor_page(self, client):
        """Test AI code monitor page loads."""
        response = client.get('/ai-monitor')
        assert response.status_code == 200
        assert b'AI Code Monitor' in response.data
    
    @patch('openai.OpenAI')
    def test_ai_testing_assistant_api(self, mock_openai, client):
        """Test AI testing assistant API."""
        # Mock OpenAI response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        response = client.post('/ai-assistant', 
                              json={'action': 'analyze_failures', 'data': {}})
        assert response.status_code == 200

class TestAutonomousFixing:
    """Test autonomous test fixing functionality."""
    
    @patch('app.AutonomousTestFixer')
    def test_start_autonomous_fixer(self, mock_fixer_class, client):
        """Test starting autonomous test fixer."""
        mock_fixer = Mock()
        mock_fixer_class.return_value = mock_fixer
        
        response = client.post('/api/autonomous-fixer/start')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'success' in data
    
    def test_autonomous_fixer_status(self, client):
        """Test autonomous fixer status endpoint."""
        response = client.get('/api/autonomous-fixer/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'running' in data
    
    def test_stop_autonomous_fixer(self, client):
        """Test stopping autonomous fixer."""
        response = client.post('/api/autonomous-fixer/stop')
        assert response.status_code == 200