import os
import logging
import aiohttp
import asyncio
import json
import re
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.openrouter_key = os.getenv('OPENROUTER_KEY', 'default_key')
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
                
                async with session.post(url, json=payload, headers=headers, timeout=10) as response:
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
            return None
        except Exception as e:
            logger.error(f"OpenRouter generation error: {str(e)}")
            return None
        
        return None
    
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
                
                async with session.post(url, json=payload, headers=headers, timeout=10) as response:
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
            return None
        except Exception as e:
            logger.error(f"Claude generation error: {str(e)}")
            return None
        
        return None
    
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
