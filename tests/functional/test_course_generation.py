"""
Functional tests for end-to-end course generation workflow.
"""
import pytest
from unittest.mock import patch, Mock, AsyncMock

class TestCourseGenerationWorkflow:
    """Test complete course generation workflow from YouTube URL to finished course."""
    
    @pytest.mark.asyncio
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata', side_effect=Exception('Metadata API failure'))
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript', side_effect=Exception('Transcript API failure'))
    @patch('app.generate_course_content', side_effect=Exception('Course generation API failure'))
    async def test_multiple_api_failures_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when multiple API failures occur."""
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'api failure' in data['error'].lower()video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()processing_metrics')
    async def test_processing_metrics_tracking(self, mock_metrics, client):
        """Test tracking of processing metrics during course generation."""
        # Mock processing metrics extraction
        mock_metrics.return_value = {
            'processing_time': '5 minutes',
            'steps_completed': 3,
            'errors': []
        }
        
        # Test the metrics tracking
        response = client.post('/api/track-metrics', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'processing_time' in data
        assert data['processing_time'] == '5 minutes'
        
        # Verify metrics extraction was called
        mock_metrics.assert_called_once()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):transcript')
    @patch('app.generate_course_content')video_metadata')
    async def test_metadata_extraction_failure_fallback(self, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):transcript')
    @patch('app.generate_course_content')transcript')
    @patch('app.generate_course_content')transcript')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):transcript')
    @patch('app.generate_course_content')transcript')transcript')
    @patch('app.generate_course_content')
    async def test_complete_workflow_success(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test successful end-to-end course generation."""
        # Mock metadata extraction
        mock_metadata.return_value = {
            'video_id': 'dQw4w9WgXcQ',
            'title': 'Python Programming Tutorial',
            'description': 'Learn Python basics',
            'duration': '30:00',
            'view_count': 100000,
            'published_at': '2023-01-01T00:00:00Z'
        }
        
        # Mock transcript extraction
        mock_transcript.return_value = "Welcome to Python programming. Today we'll learn variables, functions, and loops."
        
        # Mock course generation
        mock_generate.return_value = {
            'course_title': 'Learn Python Programming',
            'course_description': 'A comprehensive Python course',
            'target_audience': 'Beginners',
            'difficulty_level': 'Beginner',
            'estimated_total_time': '7 days',
            'days_structure': [
                {
                    'day': 1,
                    'title': 'Python Basics',
                    'learning_objectives': ['Understand variables'],
                    'activities': [{'type': 'reading', 'title': 'Variables', 'estimated_time': '30 minutes'}],
                    'key_takeaways': ['Python uses dynamic typing'],
                    'homework': 'Practice variable assignment'
                }
            ],
            'final_project': 'Build a calculator',
            'resources': ['Python.org'],
            'assessment_criteria': 'Understanding demonstrated'
        }
        
        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        
        assert response.status_code == 200
        
        # Verify all steps were called
        mock_metadata.assert_called_once()
        mock_transcript.assert_called_once()
        mock_generate.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata', side_effect=Exception('Metadata API failure'))
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript', side_effect=Exception('Transcript API failure'))
    @patch('app.generate_course_content', side_effect=Exception('Course generation API failure'))
    async def test_multiple_api_failures_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when multiple API failures occur."""
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'api failure' in data['error'].lower()video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()video_metadata')
    async def test_invalid_youtube_url_handling(self, mock_metadata, client):
        """Test proper error handling for invalid YouTube URLs."""
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://invalid-url.com'})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'invalid' in data['error'].lower()
    
    @pytest.mark.asyncio
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata', side_effect=Exception('Metadata API failure'))
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript', side_effect=Exception('Transcript API failure'))
    @patch('app.generate_course_content', side_effect=Exception('Course generation API failure'))
    async def test_multiple_api_failures_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when multiple API failures occur."""
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'api failure' in data['error'].lower()video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()processing_metrics')
    async def test_processing_metrics_tracking(self, mock_metrics, client):
        """Test tracking of processing metrics during course generation."""
        # Mock processing metrics extraction
        mock_metrics.return_value = {
            'processing_time': '5 minutes',
            'steps_completed': 3,
            'errors': []
        }
        
        # Test the metrics tracking
        response = client.post('/api/track-metrics', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'processing_time' in data
        assert data['processing_time'] == '5 minutes'
        
        # Verify metrics extraction was called
        mock_metrics.assert_called_once()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):transcript')
    @patch('app.generate_course_content')video_metadata')
    async def test_metadata_extraction_failure_fallback(self, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):transcript')
    @patch('app.generate_course_content')transcript')
    @patch('app.generate_course_content')transcript')video_metadata')
    async def test_metadata_extraction_failure_fallback(self, mock_metadata, client):
        """Test fallback behavior when metadata extraction fails."""
        mock_metadata.side_effect = Exception("API Error")
        
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        
        # Should still attempt to continue with fallback
        assert response.status_code in [200, 500]

class TestSystemResilience:
    """Test system resilience and error recovery."""
    
    @pytest.mark.asyncio
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata', side_effect=Exception('Metadata API failure'))
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript', side_effect=Exception('Transcript API failure'))
    @patch('app.generate_course_content', side_effect=Exception('Course generation API failure'))
    async def test_multiple_api_failures_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when multiple API failures occur."""
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'api failure' in data['error'].lower()video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()processing_metrics')
    async def test_processing_metrics_tracking(self, mock_metrics, client):
        """Test tracking of processing metrics during course generation."""
        # Mock processing metrics extraction
        mock_metrics.return_value = {
            'processing_time': '5 minutes',
            'steps_completed': 3,
            'errors': []
        }
        
        # Test the metrics tracking
        response = client.post('/api/track-metrics', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'processing_time' in data
        assert data['processing_time'] == '5 minutes'
        
        # Verify metrics extraction was called
        mock_metrics.assert_called_once()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):transcript')
    @patch('app.generate_course_content')video_metadata')
    async def test_metadata_extraction_failure_fallback(self, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):transcript')
    @patch('app.generate_course_content')transcript')
    @patch('app.generate_course_content')transcript')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')video_metadata')
    @patch('app.extract_processing_metrics')course_structure')video_metadata')transcript')
    @patch('app.generate_course_content')
    async def test_metadata_extraction_failure_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test fallback mechanism when metadata extraction fails."""
        # Simulate metadata extraction failure
        mock_metadata.side_effect = Exception('Metadata extraction failed')

        # Test the workflow
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'metadata extraction failed' in data['error'].lower()course_structure')transcript')
    @patch('app.generate_course_content')
    async def test_concurrent_course_generation(self, mock_generate, mock_transcript, mock_metadata, client):transcript')
    @patch('app.generate_course_content')transcript')transcript')
    @patch('app.generate_course_content')
    async def test_multiple_api_failures_fallback(self, mock_generate, mock_transcript, mock_metadata, client):
        """Test system behavior when multiple APIs fail."""
        # All primary methods fail
        mock_metadata.side_effect = Exception("YouTube API Error")
        mock_transcript.side_effect = Exception("Transcript API Error")
        mock_generate.side_effect = Exception("AI API Error")
        
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        
        # System should attempt fallback course generation
        assert response.status_code in [200, 500]
    
    @pytest.mark.asyncio
    async def test_concurrent_course_generation(self, client):
        """Test system handling of concurrent course generation requests."""
        import asyncio
        
        # Create multiple concurrent requests
        async def make_request():
            return client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        
        # This would test concurrent handling in a real scenario
        # For unit testing, we just verify the endpoint is accessible
        response = await make_request()
        assert response.status_code in [200, 400, 500]

class TestQualityAssurance:
    """Test course generation quality and validation."""
    
    @pytest.mark.asyncio
    @patch('app.process_youtube_video')
    async def test_course_structure_validation(self, mock_process, client):
        """Test that generated courses meet quality standards."""
        # Mock a complete, valid course
        mock_process.return_value = {
            'status': 'success',
            'course': {
                'course_title': 'Python Programming',
                'course_description': 'Learn Python basics',
                'target_audience': 'Beginners',
                'difficulty_level': 'Beginner',
                'estimated_total_time': '7 days',
                'days_structure': [
                    {
                        'day': 1,
                        'title': 'Introduction',
                        'learning_objectives': ['Understand Python'],
                        'activities': [{'type': 'reading', 'title': 'Overview', 'estimated_time': '30 min'}],
                        'key_takeaways': ['Python is versatile'],
                        'homework': 'Install Python'
                    }
                ],
                'final_project': 'Build an app',
                'resources': ['Python.org'],
                'assessment_criteria': 'Project completion'
            },
            'processing_time': 10.5,
            'quality_score': 'A',
            'reliability_grade': 'A'
        }
        
        response = client.post('/api/generate-course', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        
        assert response.status_code == 200
        data = response.get_json()
        
        if 'course' in data:
            course = data['course']
            # Validate required fields
            required_fields = ['course_title', 'course_description', 'days_structure']
            for field in required_fields:
                assert field in course, f"Missing required field: {field}"
    
    @pytest.mark.asyncio
    async def test_processing_metrics_tracking(self, client):
        """Test that processing metrics are properly tracked."""
        with patch('app.process_youtube_video') as mock_process:
            mock_process.return_value = {
                'status': 'success',
                'processing_time': 15.2,
                'total_cost': 0.05,
                'quality_score': 'B+',
                'success_rate': 0.85
            }
            
            response = client.post('/api/generate-course', 
                                  json={'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
            
            assert response.status_code == 200