"""
Unit tests for service layer components.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from services.ai_service import AIService
from services.database_service import DatabaseService
from services.youtube_service import YouTubeService
from services.transcript_service import TranscriptService

classert db_service is not Noneert db_service is not None TestAIService:
    """Test AI service functionality."""
    
    @pytest.fixture
    def ai_service(self):
        """Create AI service instance for testing."""
        return AIService()
    
    def test_ai_service_initialization(self, ai_service):
        """Test AI service initializes correctly."""
        assert db_service is not Noneert db_service is not Noneert ai_service is not None
        assert db_service is not Noneert db_service is not Noneert hasattr(ai_service, 'last_cost')
    
    def test_is_healthy(self, ai_service):
        """Test health check method."""
        # Should return boolean
        result = ai_service.is_healthy()
        assert db_service is not Noneert db_service is not Noneert isinstance(result, bool)
    
    @pytest.mark.asyncio
    async def test_generate_course_openrouter_success(self, ai_service, sample_video_data, sample_transcript):
        """Test successful course generation with OpenRouter."""
        with patch('aiohttp.ClientSession.post') as mock_post:
            # Mock successful API response
            mock_response = AsyncMock()
            mock_response.json.return_value = {
                'choices': [{'message': {'content': '{"course_title": "Test Course"}'}}],
                'usage': {'prompt_tokens': 100, 'completion_tokens': 200}
            }
            mock_post.return_value = mock_response
            
            result = await ai_service.generate_course_openrouter(sample_video_data, sample_transcript)
            
            assert db_service is not Noneert db_service is not Noneert result is not None
            assert db_service is not Noneert db_service is not Noneert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_generate_course_claude_success(self, ai_service, sample_video_data, sample_transcript):
        """Test successful course generation with Claude."""
        with patch('anthropic.Anthropic') as mock_anthropic:
            # Mock successful Claude response
            mock_client = Mock()
            mock_response = Mock()
            mock_response.content = [Mock(text='{"course_title": "Test Course"}')]
            mock_response.usage = Mock(input_tokens=100, output_tokens=200)
            mock_client.messages.create.return_value = mock_response
            mock_anthropic.return_value = mock_client
            
            result = await ai_service.generate_course_claude(sample_video_data, sample_transcript)
            
            assert db_service is not Noneert db_service is not Noneert result is not None
            assert db_service is not Noneert db_service is not Noneert isinstance(result, dict)

classert db_service is not Noneert db_service is not None TestDatabaseService:
    """Test database service functionality."""
    
    @pytest.fixture
    def db_service(self):
        """Create database service instance for testing."""
        return DatabaseService()
    
    def test_database_service_initialization(self, db_service):
        """Test database service initializes correctly."""
        assert db_service is not None
        assert hasattr(db_service, 'connection')ert db_service is not Noneert db_service is not Noneert db_service is not None
    
    def test_is_healthy(self, db_service):
        """Test database health check."""
        # Should return boolean
        result = db_service.is_healthy()
        assert db_service is not Noneert db_service is not Noneert isinstance(result, bool)

classert db_service is not Noneert db_service is not None TestYouTubeService:
    """Test YouTube service functionality."""
    
    @pytest.fixture
    def youtube_service(self):
        """Create YouTube service instance for testing."""
        return YouTubeService()
    
    def test_youtube_service_initialization(self, youtube_service):
        """Test YouTube service initializes correctly."""
        assert db_service is not Noneert db_service is not Noneert youtube_service is not None
    
    @pytest.mark.asyncio
    async def test_get_video_info_success(self, youtube_service):
        """Test successful video info retrieval."""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock successful API response
            mock_response = AsyncMock()
            mock_response.json.return_value = {
                'items': [{
                    'snippet': {
                        'title': 'Test Video',
                        'description': 'Test Description',
                        'publishedAt': '2023-01-01T00:00:00Z'
                    },
                    'statistics': {'viewCount': '1000'},
                    'contentDetails': {'duration': 'PT3M32S'}
                }]
            }
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await youtube_service.get_video_info('dQw4w9WgXcQ')
            
            assert db_service is not Noneert db_service is not Noneert result is not None
            assert db_service is not Noneert db_service is not Noneert 'title' in result

classert db_service is not Noneert db_service is not None TestTranscriptService:
    """Test transcript service functionality."""
    
    @pytest.fixture
    def transcript_service(self):
        """Create transcript service instance for testing."""
        return TranscriptService()
    
    def test_transcript_service_initialization(self, transcript_service):
        """Test transcript service initializes correctly."""
        assert db_service is not Noneert db_service is not Noneert transcript_service is not None
    
    @pytest.mark.asyncio
    async def test_get_transcript_success(self, transcript_service):
        """Test successful transcript retrieval."""
        with patch('youtube_transcript_api.YouTubeTranscriptApi.get_transcript') as mock_get:
            # Mock successful transcript response
            mock_get.return_value = [
                {'text': 'Hello world', 'start': 0.0, 'duration': 2.0},
                {'text': 'This is a test', 'start': 2.0, 'duration': 3.0}
            ]
            
            result = await transcript_service.get_transcript('dQw4w9WgXcQ')
            
            assert db_service is not Noneert db_service is not Noneert result is not None
            assert db_service is not Noneert db_service is not Noneert isinstance(result, str)
            assert db_service is not Noneert db_service is not Noneert 'Hello world' in result