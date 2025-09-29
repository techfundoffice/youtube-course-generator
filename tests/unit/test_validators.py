"""
Unit tests for validation utilities.
"""
import pytest
from utils.validators import validate_youtube_url, extract_video_id, validate_course_structure, sanitize_input

class TestYouTubeValidation:
    """Test YouTube URL validation and processing."""
    
    def test_validate_youtube_url_valid_formats(self):
        """Test validation of valid YouTube URL formats."""
        valid_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtu.be/dQw4w9WgXcQ',
            'https://m.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtube.com/watch?v=dQw4w9WgXcQ'
        ]
        
        for url in valid_urls:
            assert validate_youtube_url(url), f"Should accept valid URL: {url}"

    def test_validate_youtube_url_invalid_formats(self):
        """Test rejection of invalid YouTube URLs."""
        invalid_urls = [
            'https://www.google.com',
            'not_a_url',
            '',
            'https://vimeo.com/123456789',
            'youtube.com/invalid'
        ]
        
        for url in invalid_urls:
            assert not validate_youtube_url(url), f"Should reject invalid URL: {url}"

    def test_extract_video_id_from_various_formats(self):
        """Test extraction of video IDs from different URL formats."""
        test_cases = [
            ('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
            ('https://youtu.be/dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
            ('https://m.youtube.com/watch?v=dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
            ('https://youtube.com/watch?v=ABC123xyz89', 'ABC123xyz89')
        ]
        
        for url, expected_id in test_cases:
            result = extract_video_id(url)
            assert result == expected_id, f"Expected {expected_id}, got {result} for URL: {url}"

    def test_extract_video_id_invalid_urls(self):
        """Test video ID extraction with invalid URLs."""
        invalid_urls = ['https://google.com', 'not_a_url', '']
        
        for url in invalid_urls:
            result = extract_video_id(url)
            assert result is None, f"Should return None for invalid URL: {url}"

class TestCourseStructureValidation:
    """Test course structure validation."""
    
    def test_validate_complete_course_structure(self, sample_course_data):
        """Test validation of complete, valid course structure."""
        assert validate_course_structure(sample_course_data)
        
    def test_validate_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        incomplete_courses = [
            {},  # Empty
            {'course_title': 'Test'},  # Missing description
            {'course_title': 'Test', 'course_description': 'Desc'},  # Missing more fields
        ]
        
        for course in incomplete_courses:
            assert not validate_course_structure(course)
            
    def test_validate_invalid_data_types(self):
        """Test validation fails for incorrect data types."""
        invalid_courses = [
            {'course_title': 123},  # Wrong type
            {'days_structure': 'not_a_list'},  # Wrong type
            {'course_title': 'Test', 'days_structure': [{'invalid': 'structure'}]}  # Invalid structure
        ]
        
        for course in invalid_courses:
            assert not validate_course_structure(course)

class TestInputSanitization:
    """Test input sanitization functionality."""
    
    def test_sanitize_html_tags(self):
        """Test removal of HTML tags from input."""
        test_cases = [
            ('<script>alert("xss")</script>', 'alert("xss")'),
            ('<b>Bold text</b>', 'Bold text'),
            ('Normal text', 'Normal text'),
            ('<div><p>Nested tags</p></div>', 'Nested tags')
        ]
        
        for input_text, expected in test_cases:
            result = sanitize_input(input_text)
            assert result == expected, f"Expected '{expected}', got '{result}'"
    
    def test_sanitize_special_characters(self):
        """Test handling of special characters."""
        test_cases = [
            ('Text with "quotes"', 'Text with "quotes"'),
            ('Text & symbols', 'Text & symbols'),
            ('Unicode: 你好', 'Unicode: 你好')
        ]
        
        for input_text, expected in test_cases:
            result = sanitize_input(input_text)
            assert result == expected
            
    def test_sanitize_empty_and_none(self):
        """Test sanitization of empty and None inputs."""
        assert sanitize_input('') == ''
        assert sanitize_input(None) == ''