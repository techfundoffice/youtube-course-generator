import os
import logging
import aiohttp
import asyncio
import json
import re
from typing import Dict, Any
from utils.validators import validate_youtube_url, validate_media_url

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.openrouter_key = os.getenv('OPENAI_API_KEY', 'default_key')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY', 'default_key')
        self.last_cost = 0.0
        
    def is_healthy(self) -> bool:
        """Check if AI services are available"""
        return bool(
            (self.openrouter_key and self.openrouter_key != 'default_key') or
            (self.anthropic_key and self.anthropic_key != 'default_key')
        )
    
    def get_last_cost(self) -> float:
        """Get the cost of the last API call"""
        return self.last_cost
    
    async def generate_course_openrouter(self, video_info: dict, transcript: str) -> dict:
        """Generate course using OpenRouter GPT-4"""
        try:
            if not self.openrouter_key or self.openrouter_key == 'default_key':
                raise ValueError("OpenRouter key not configured")
            
            prompt = self._create_course_prompt(video_info, transcript)
            
            async with aiohttp.ClientSession() as session:
                url = "https://openrouter.ai/api/v1/chat/completions"
                
                headers = {
                    'Authorization': f'Bearer {self.openrouter_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://youtube-course-generator.com',
                    'X-Title': 'YouTube Course Generator'
                }
                
                payload = {
                    'model': 'openai/gpt-4',  # Use GPT-4 via OpenRouter
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are an expert educational content creator. Generate structured 7-day learning courses from video content. Always respond with valid JSON.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'max_tokens': 4000,
                    'temperature': 0.7,
                    'response_format': {'type': 'json_object'}
                }
                
                async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Calculate cost (approximate)
                        self.last_cost = self._calculate_openrouter_cost(data)
                        
                        content = data['choices'][0]['message']['content']
                        course = json.loads(content)
                        
                        return self._validate_and_format_course(course)
                    else:
                        error_text = await response.text()
                        logger.error(f"OpenRouter API error: {response.status} - {error_text}")
                        
        except asyncio.TimeoutError:
            logger.error("OpenRouter API timeout after 30 seconds")
            return {'error': 'OpenRouter API timeout after 30 seconds', 'course': None}
        except Exception as e:
            logger.error(f"OpenRouter generation error: {str(e)}")
            return {'error': f'OpenRouter generation error: {str(e)}', 'course': None}
        
        return {'error': 'OpenRouter generation failed', 'course': None}
    
    async def generate_course_claude(self, video_info: dict, transcript: str) -> dict:
        """Generate course using Claude API"""
        try:
            if not self.anthropic_key or self.anthropic_key == 'default_key':
                raise ValueError("Anthropic key not configured")
            
            prompt = self._create_course_prompt(video_info, transcript)
            
            async with aiohttp.ClientSession() as session:
                url = "https://api.anthropic.com/v1/messages"
                
                headers = {
                    'x-api-key': self.anthropic_key,
                    'Content-Type': 'application/json',
                    'anthropic-version': '2023-06-01'
                }
                
                payload = {
                    'model': 'claude-3-5-sonnet-20241022',  # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
                    'max_tokens': 4000,
                    'temperature': 0.7,
                    'messages': [
                        {
                            'role': 'user',
                            'content': f"You are an expert educational content creator. Generate structured 7-day learning courses from video content. Always respond with valid JSON.\n\n{prompt}"
                        }
                    ]
                }
                
                async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Calculate cost (approximate)
                        self.last_cost = self._calculate_claude_cost(data)
                        
                        content = data['content'][0]['text']
                        
                        # Extract JSON from response
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            course = json.loads(json_match.group())
                            return self._validate_and_format_course(course)
                    else:
                        error_text = await response.text()
                        logger.error(f"Claude API error: {response.status} - {error_text}")
                        
        except asyncio.TimeoutError:
            logger.error("Claude API timeout after 30 seconds")
            return {'error': 'Claude API timeout after 30 seconds', 'course': None}
        except Exception as e:
            logger.error(f"Claude generation error: {str(e)}")
            return {'error': f'Claude generation error: {str(e)}', 'course': None}
        
        return {'error': 'Claude generation failed', 'course': None}
    
    def _create_course_prompt(self, video_info: dict, transcript: str) -> str:
        """Create a comprehensive prompt for course generation"""
        title = video_info.get('title', 'Unknown Title')
        author = video_info.get('author', 'Unknown Author')
        description = video_info.get('description', '')
        duration = video_info.get('duration', 'Unknown')
        
        # Truncate transcript if too long
        if len(transcript) > 8000:
            transcript = transcript[:8000] + "... [truncated]"
        
        prompt = f"""
Create a comprehensive 7-day learning course based on this YouTube video:

**Video Information:**
- Title: {title}
- Author: {author}
- Duration: {duration}
- Description: {description[:500]}

**Video Transcript:**
{transcript}

Generate a structured 7-day course with the following JSON format:

{{
    "course_title": "7-Day Course: [Course Name]",
    "course_description": "Brief description of what students will learn",
    "target_audience": "Who this course is for",
    "estimated_total_time": "Total time in hours",
    "difficulty_level": "Beginner/Intermediate/Advanced",
    "days": [
        {{
            "day": 1,
            "title": "Day 1: [Title]",
            "objectives": ["Learning objective 1", "Learning objective 2"],
            "content_summary": "What will be covered this day",
            "activities": [
                {{
                    "type": "watch",
                    "description": "Watch specific video segments",
                    "time_estimate": "30 minutes"
                }},
                {{
                    "type": "practice",
                    "description": "Hands-on exercise",
                    "time_estimate": "45 minutes"
                }},
                {{
                    "type": "reflection",
                    "description": "Reflection questions",
                    "time_estimate": "15 minutes"
                }}
            ],
            "key_takeaways": ["Takeaway 1", "Takeaway 2"],
            "homework": "Optional homework assignment",
            "estimated_time": "1.5 hours"
        }}
        // ... 6 more days
    ],
    "final_project": "Capstone project description",
    "resources": ["Additional resource 1", "Additional resource 2"],
    "assessment_criteria": "How progress will be measured"
}}

Ensure each day builds upon the previous day's content and creates a logical learning progression.
"""
        return prompt
    
    def _validate_and_format_course(self, course: dict) -> dict:
        """Validate and format the generated course"""
        if not isinstance(course, dict):
            raise ValueError("Course must be a dictionary")
        
        # Ensure required fields exist
        required_fields = ['course_title', 'course_description', 'days']
        for field in required_fields:
            if field not in course:
                course[field] = f"Generated {field}"
        
        # Ensure we have 7 days
        if 'days' not in course or not isinstance(course['days'], list):
            course['days'] = []
        
        while len(course['days']) < 7:
            day_num = len(course['days']) + 1
            course['days'].append({
                'day': day_num,
                'title': f'Day {day_num}: Learning Session',
                'objectives': ['Continue learning from the video content'],
                'content_summary': 'Review and practice concepts from the video',
                'activities': [
                    {
                        'type': 'review',
                        'description': 'Review video content',
                        'time_estimate': '30 minutes'
                    }
                ],
                'key_takeaways': ['Key learning points'],
                'estimated_time': '1 hour'
            })
        
        return course
    
    def _calculate_openrouter_cost(self, response_data: dict) -> float:
        """Calculate approximate cost for OpenRouter API call"""
        try:
            usage = response_data.get('usage', {})
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            
            # Approximate GPT-4 pricing via OpenRouter
            prompt_cost = prompt_tokens * 0.00003  # $0.03 per 1K tokens
            completion_cost = completion_tokens * 0.00006  # $0.06 per 1K tokens
            
            return prompt_cost + completion_cost
        except:
            return 1.5  # Default estimate
    
    def _calculate_claude_cost(self, response_data: dict) -> float:
        """Calculate approximate cost for Claude API call"""
        try:
            usage = response_data.get('usage', {})
            input_tokens = usage.get('input_tokens', 0)
            output_tokens = usage.get('output_tokens', 0)
            
            # Claude-3.5-Sonnet pricing
            input_cost = input_tokens * 0.000003  # $3 per 1M tokens
            output_cost = output_tokens * 0.000015  # $15 per 1M tokens
            
            return input_cost + output_cost
        except:
            return 1.0  # Default estimate
    
    async def chat_with_ai(self, messages: list, detect_youtube_urls: bool = True) -> dict:
        """Handle conversational chat with AI, with optional media URL detection"""
        try:
            # Check for media URLs in the latest message if detection is enabled
            media_urls = []
            latest_message = messages[-1]['content'] if messages else ""
            
            # If no URLs found, suggest the default YouTube test video
            if detect_youtube_urls:
                media_urls = self._extract_media_urls(latest_message)
                if not media_urls:
                    # Default YouTube URL for React in 100 Seconds test video
                    default_youtube_url = "https://www.youtube.com/watch?v=SqcY0GlETPk"
                    latest_message += f"\n\nDefault media suggestion: {default_youtube_url}"
                    media_urls = [default_youtube_url]
            
            # Create system prompt for conversational AI that supports YouTube
            system_prompt = """You are a helpful AI assistant. You can have natural conversations and help users with various tasks.

If you detect a YouTube URL in the conversation, offer to download and process the video by showing this exact response:
"I found a video! Would you like me to download it? 

[YOUTUBE_DOWNLOAD_BUTTON]"

If no URLs are detected in the conversation, proactively offer to test the video download functionality with this exact response:
"Want to test video download with this short React tutorial? I can download it as an MP4 file for you to view or save.

[YOUTUBE_DOWNLOAD_BUTTON]"

Be friendly, helpful, and conversational. You can process YouTube videos for course generation and MP4 download."""
            
            # Use OpenRouter for chat (fallback to Claude if needed)
            if self.openrouter_key and self.openrouter_key != 'default_key':
                return await self._chat_openrouter(system_prompt, messages, media_urls)
            elif self.anthropic_key and self.anthropic_key != 'default_key':
                return await self._chat_claude(system_prompt, messages, media_urls)
            else:
                return {
                    'response': 'I apologize, but I am unable to respond right now. No AI service is configured.',
                    'youtube_urls': media_urls,
                    'show_download_button': len(media_urls) > 0
                }
                
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return {
                'response': 'I apologize, but I encountered an error. Please try again.',
                'youtube_urls': [],
                'show_download_button': False
            }
    
    async def _chat_openrouter(self, system_prompt: str, messages: list, youtube_urls: list) -> dict:
        """Chat using OpenRouter API"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://openrouter.ai/api/v1/chat/completions"
                
                headers = {
                    'Authorization': f'Bearer {self.openrouter_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://youtube-course-generator.com',
                    'X-Title': 'YouTube Course Generator Chat'
                }
                
                # Build conversation with system prompt
                chat_messages = [{'role': 'system', 'content': system_prompt}] + messages
                
                payload = {
                    'model': 'openai/gpt-4o-mini',  # Use cheaper model for chat
                    'messages': chat_messages,
                    'max_tokens': 1000,
                    'temperature': 0.7
                }
                
                async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.last_cost = self._calculate_openrouter_cost(data)
                        
                        response_text = data['choices'][0]['message']['content']
                        
                        # Check if response contains download button trigger
                        show_download_button = '[YOUTUBE_DOWNLOAD_BUTTON]' in response_text or len(youtube_urls) > 0
                        
                        return {
                            'response': response_text,
                            'youtube_urls': youtube_urls,
                            'show_download_button': show_download_button
                        }
                    else:
                        logger.error(f"OpenRouter chat error: {response.status}")
                        return await self._chat_claude(system_prompt, messages, youtube_urls)
                        
        except Exception as e:
            logger.error(f"OpenRouter chat error: {str(e)}")
            # Fallback to Claude
            return await self._chat_claude(system_prompt, messages, youtube_urls)
    
    async def _chat_claude(self, system_prompt: str, messages: list, youtube_urls: list) -> dict:
        """Chat using Claude API"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.anthropic.com/v1/messages"
                
                headers = {
                    'x-api-key': self.anthropic_key,
                    'Content-Type': 'application/json',
                    'anthropic-version': '2023-06-01'
                }
                
                # Claude doesn't use system messages in the messages array
                conversation = f"{system_prompt}\n\n"
                for msg in messages:
                    conversation += f"{msg['role']}: {msg['content']}\n"
                
                payload = {
                    'model': 'claude-3-haiku-20240307',  # Use cheaper model for chat
                    'max_tokens': 1000,
                    'temperature': 0.7,
                    'messages': [{'role': 'user', 'content': conversation}]
                }
                
                async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.last_cost = self._calculate_claude_cost(data)
                        
                        response_text = data['content'][0]['text']
                        show_download_button = '[YOUTUBE_DOWNLOAD_BUTTON]' in response_text or len(youtube_urls) > 0
                        
                        return {
                            'response': response_text,
                            'youtube_urls': youtube_urls,
                            'show_download_button': show_download_button
                        }
                    else:
                        logger.error(f"Claude chat error: {response.status}")
                        
        except Exception as e:
            logger.error(f"Claude chat error: {str(e)}")
        
        # Final fallback
        return {
            'response': 'I apologize, but I am unable to respond right now. Please try again later.',
            'youtube_urls': youtube_urls,
            'show_download_button': len(youtube_urls) > 0
        }
    
    def _extract_youtube_urls(self, text: str) -> list:
        """Extract YouTube URLs from text"""
        import re
        patterns = [
            r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'https?://youtu\.be/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/embed/[\w-]+',
            r'youtube\.com/watch\?v=[\w-]+',
            r'youtu\.be/[\w-]+'
        ]
        
        urls = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if not match.startswith('http'):
                    match = 'https://' + match
                if match not in urls:
                    urls.append(match)
        
        return urls
    
    def generate_course_sync(self, video_info: dict, transcript: str) -> dict:
        """Synchronous wrapper for AI course generation with fallback chain"""
        import asyncio
        try:
            # Try to get existing event loop, if not create new one
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, we can't use asyncio.run, use basic fallback
                    logger.warning("Event loop already running, using basic course fallback")
                    return self._generate_basic_course_fallback(video_info, transcript)
                else:
                    return asyncio.run(self._generate_course_async_chain(video_info, transcript))
            except RuntimeError:
                # No event loop, safe to create new one
                return asyncio.run(self._generate_course_async_chain(video_info, transcript))
        except Exception as e:
            logger.error(f"Sync course generation error: {str(e)}")
            return self._generate_basic_course_fallback(video_info, transcript)
    
    async def _generate_course_async_chain(self, video_info: dict, transcript: str) -> dict:
        """Async chain for course generation with full redundancy"""
        # Try OpenRouter first
        try:
            course = await self.generate_course_openrouter(video_info, transcript)
            if course and course.get('course'):
                return course['course']
        except Exception as e:
            logger.warning(f"OpenRouter course generation failed: {str(e)}")
        
        # Try Claude
        try:
            course = await self.generate_course_claude(video_info, transcript)
            if course and course.get('course'):
                return course['course']
        except Exception as e:
            logger.warning(f"Claude course generation failed: {str(e)}")
        
        # Final fallback
        return self._generate_basic_course_fallback(video_info, transcript)
    
    def _generate_basic_course_fallback(self, video_info: dict, transcript: str) -> dict:
        """Generate basic course when all AI services fail"""
        title = video_info.get('title', 'Unknown Video')
        author = video_info.get('author', 'Unknown Creator')
        
        return {
            "course_title": f"7-Day Learning Course: {title}",
            "course_description": f"A comprehensive 7-day course based on '{title}' by {author}",
            "target_audience": "General Audience",
            "estimated_total_time": "8-12 hours",
            "difficulty_level": "Beginner",
            "days": [
                {
                    "day": i,
                    "title": f"Day {i}: Learning Session",
                    "objectives": [f"Learn key concepts from {title}"],
                    "content_summary": f"Review and practice concepts from the video",
                    "activities": [
                        {
                            "type": "watch",
                            "description": "Watch the video content",
                            "time_estimate": "30 minutes"
                        },
                        {
                            "type": "practice", 
                            "description": "Practice the concepts",
                            "time_estimate": "45 minutes"
                        }
                    ],
                    "key_takeaways": ["Key learning points from the session"],
                    "estimated_time": "1.5 hours"
                } for i in range(1, 8)
            ],
            "final_project": f"Complete a project applying concepts from {title}",
            "resources": ["Video content", "Practice exercises"],
            "assessment_criteria": "Completion of daily activities and final project"
        }

    def _extract_media_urls(self, text: str) -> list:
        """Extract YouTube URLs from text"""
        import re
        
        # YouTube patterns only
        youtube_patterns = [
            r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'https?://youtu\.be/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/embed/[\w-]+',
            r'youtube\.com/watch\?v=[\w-]+',
            r'youtu\.be/[\w-]+'
        ]
        
        urls = []
        
        for pattern in youtube_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if not match.startswith('http'):
                    match = 'https://' + match
                if match not in urls:
                    urls.append(match)
        
        return urls
    
    def generate_course_sync(self, video_info: dict, transcript: str) -> dict:
        """Synchronous wrapper for AI course generation with fallback chain"""
        import asyncio
        try:
            # Try to get existing event loop, if not create new one
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, we can't use asyncio.run, use basic fallback
                    logger.warning("Event loop already running, using basic course fallback")
                    return self._generate_basic_course_fallback(video_info, transcript)
                else:
                    return asyncio.run(self._generate_course_async_chain(video_info, transcript))
            except RuntimeError:
                # No event loop, safe to create new one
                return asyncio.run(self._generate_course_async_chain(video_info, transcript))
        except Exception as e:
            logger.error(f"Sync course generation error: {str(e)}")
            return self._generate_basic_course_fallback(video_info, transcript)
    
    async def _generate_course_async_chain(self, video_info: dict, transcript: str) -> dict:
        """Async chain for course generation with full redundancy"""
        # Try OpenRouter first
        try:
            course = await self.generate_course_openrouter(video_info, transcript)
            if course and course.get('course'):
                return course['course']
        except Exception as e:
            logger.warning(f"OpenRouter course generation failed: {str(e)}")
        
        # Try Claude
        try:
            course = await self.generate_course_claude(video_info, transcript)
            if course and course.get('course'):
                return course['course']
        except Exception as e:
            logger.warning(f"Claude course generation failed: {str(e)}")
        
        # Final fallback
        return self._generate_basic_course_fallback(video_info, transcript)
    
    def _generate_basic_course_fallback(self, video_info: dict, transcript: str) -> dict:
        """Generate basic course when all AI services fail"""
        title = video_info.get('title', 'Unknown Video')
        author = video_info.get('author', 'Unknown Creator')
        
        return {
            "course_title": f"7-Day Learning Course: {title}",
            "course_description": f"A comprehensive 7-day course based on '{title}' by {author}",
            "target_audience": "General Audience",
            "estimated_total_time": "8-12 hours",
            "difficulty_level": "Beginner",
            "days": [
                {
                    "day": i,
                    "title": f"Day {i}: Learning Session",
                    "objectives": [f"Learn key concepts from {title}"],
                    "content_summary": f"Review and practice concepts from the video",
                    "activities": [
                        {
                            "type": "watch",
                            "description": "Watch the video content",
                            "time_estimate": "30 minutes"
                        },
                        {
                            "type": "practice", 
                            "description": "Practice the concepts",
                            "time_estimate": "45 minutes"
                        }
                    ],
                    "key_takeaways": ["Key learning points from the session"],
                    "estimated_time": "1.5 hours"
                } for i in range(1, 8)
            ],
            "final_project": f"Complete a project applying concepts from {title}",
            "resources": ["Video content", "Practice exercises"],
            "assessment_criteria": "Completion of daily activities and final project"
        }
