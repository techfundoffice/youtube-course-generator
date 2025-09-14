import logging
import asyncio
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)

class CourseGenerator:
    def __init__(self):
        pass
    
    async def generate_structured_fallback(self, video_info: dict, transcript: str) -> dict:
        """Generate a structured course using rule-based approach when AI fails"""
        try:
            logger.info("Generating structured fallback course")
            
            title = video_info.get('title', 'Unknown Video')
            author = video_info.get('author', 'Unknown Creator')
            description = video_info.get('description', '')
            
            # Analyze content to determine course structure
            content_analysis = self._analyze_content(title, description, transcript)
            
            # Generate course based on analysis
            course = {
                "course_title": f"7-Day Learning Course: {title}",
                "course_description": f"A comprehensive 7-day course based on '{title}' by {author}",
                "youtube_url": video_info.get('youtube_url', ''),  # Include original YouTube URL
                "target_audience": content_analysis['target_audience'],
                "estimated_total_time": "8-12 hours",
                "difficulty_level": content_analysis['difficulty_level'],
                "days": self._generate_daily_structure(content_analysis, transcript),
                "final_project": content_analysis['final_project'],
                "resources": self._generate_resources(video_info),
                "assessment_criteria": "Progress through daily activities and completion of final project"
            }
            
            return course
            
        except Exception as e:
            logger.error(f"Structured fallback generation error: {str(e)}")
            raise
    
    def _analyze_content(self, title: str, description: str, transcript: str) -> dict:
        """Analyze content to determine course characteristics"""
        content = f"{title} {description} {transcript}".lower()
        
        # Determine difficulty level
        difficulty_indicators = {
            'beginner': ['intro', 'basic', 'beginner', 'start', 'first', 'simple'],
            'intermediate': ['intermediate', 'improve', 'enhance', 'build', 'develop'],
            'advanced': ['advanced', 'expert', 'master', 'pro', 'complex', 'deep']
        }
        
        difficulty_level = 'Beginner'
        for level, keywords in difficulty_indicators.items():
            if any(keyword in content for keyword in keywords):
                difficulty_level = level.capitalize()
                break
        
        # Determine target audience
        audience_indicators = {
            'developers': ['code', 'programming', 'development', 'software'],
            'designers': ['design', 'ui', 'ux', 'graphics', 'visual'],
            'marketers': ['marketing', 'business', 'sales', 'growth'],
            'students': ['learn', 'study', 'education', 'tutorial'],
            'professionals': ['career', 'work', 'professional', 'industry']
        }
        
        target_audience = 'General learners'
        for audience, keywords in audience_indicators.items():
            if any(keyword in content for keyword in keywords):
                target_audience = audience.capitalize()
                break
        
        # Generate final project idea
        project_types = {
            'tutorial': 'Create your own version following the techniques shown',
            'educational': 'Apply the concepts to a real-world scenario',
            'technical': 'Build a project implementing the discussed concepts',
            'creative': 'Design an original piece using the learned skills'
        }
        
        final_project = project_types.get('educational', 'Apply the concepts to a real-world scenario')
        if 'tutorial' in content:
            final_project = project_types['tutorial']
        elif any(word in content for word in ['code', 'build', 'create']):
            final_project = project_types['technical']
        elif any(word in content for word in ['design', 'art', 'creative']):
            final_project = project_types['creative']
        
        return {
            'difficulty_level': difficulty_level,
            'target_audience': target_audience,
            'final_project': final_project,
            'content_themes': self._extract_themes(content)
        }
    
    def _extract_themes(self, content: str) -> List[str]:
        """Extract main themes from content"""
        common_themes = [
            'productivity', 'creativity', 'technology', 'business', 'health',
            'education', 'communication', 'leadership', 'problem-solving',
            'innovation', 'strategy', 'design', 'development', 'marketing'
        ]
        
        found_themes = []
        for theme in common_themes:
            if theme in content:
                found_themes.append(theme)
        
        return found_themes[:3] if found_themes else ['general knowledge']
    
    def _generate_daily_structure(self, analysis: dict, transcript: str) -> List[dict]:
        """Generate 7-day course structure"""
        themes = analysis['content_themes']
        difficulty = analysis['difficulty_level'].lower()
        
        # Base template for days
        days_template = [
            {
                'focus': 'Introduction and Overview',
                'activities': ['watch', 'note-taking', 'reflection']
            },
            {
                'focus': 'Core Concepts Part 1',
                'activities': ['watch', 'practice', 'discussion']
            },
            {
                'focus': 'Core Concepts Part 2',
                'activities': ['watch', 'hands-on', 'review']
            },
            {
                'focus': 'Practical Application',
                'activities': ['practice', 'experiment', 'document']
            },
            {
                'focus': 'Advanced Techniques',
                'activities': ['watch', 'advanced-practice', 'problem-solving']
            },
            {
                'focus': 'Integration and Synthesis',
                'activities': ['project-work', 'review', 'planning']
            },
            {
                'focus': 'Mastery and Next Steps',
                'activities': ['final-project', 'reflection', 'goal-setting']
            }
        ]
        
        days = []
        for i, day_template in enumerate(days_template):
            day_num = i + 1
            
            activities = self._generate_activities(day_template['activities'], difficulty)
            
            day = {
                'day': day_num,
                'title': f"Day {day_num}: {day_template['focus']}",
                'objectives': self._generate_objectives(day_template['focus'], themes),
                'content_summary': f"Focus on {day_template['focus'].lower()} related to the video content",
                'activities': activities,
                'key_takeaways': self._generate_takeaways(day_template['focus']),
                'homework': self._generate_homework(day_template['focus'], difficulty),
                'estimated_time': self._calculate_day_time(activities)
            }
            
            days.append(day)
        
        return days
    
    def _generate_activities(self, activity_types: List[str], difficulty: str) -> List[dict]:
        """Generate specific activities for a day"""
        activity_library = {
            'watch': {
                'description': 'Watch and analyze the video content',
                'time_estimate': '30-45 minutes'
            },
            'note-taking': {
                'description': 'Take detailed notes on key concepts',
                'time_estimate': '20 minutes'
            },
            'reflection': {
                'description': 'Reflect on learning and write insights',
                'time_estimate': '15 minutes'
            },
            'practice': {
                'description': 'Practice the techniques shown in the video',
                'time_estimate': '45 minutes'
            },
            'hands-on': {
                'description': 'Complete hands-on exercises',
                'time_estimate': '60 minutes'
            },
            'discussion': {
                'description': 'Discuss concepts with peers or research online',
                'time_estimate': '30 minutes'
            },
            'review': {
                'description': 'Review previous concepts and consolidate learning',
                'time_estimate': '25 minutes'
            },
            'advanced-practice': {
                'description': 'Apply advanced techniques and variations',
                'time_estimate': '75 minutes'
            },
            'problem-solving': {
                'description': 'Solve challenges related to the content',
                'time_estimate': '45 minutes'
            },
            'project-work': {
                'description': 'Work on your final project',
                'time_estimate': '90 minutes'
            },
            'experiment': {
                'description': 'Experiment with different approaches',
                'time_estimate': '60 minutes'
            },
            'document': {
                'description': 'Document your progress and learnings',
                'time_estimate': '30 minutes'
            },
            'final-project': {
                'description': 'Complete and finalize your project',
                'time_estimate': '120 minutes'
            },
            'goal-setting': {
                'description': 'Set goals for continued learning',
                'time_estimate': '20 minutes'
            },
            'planning': {
                'description': 'Plan application of learned concepts',
                'time_estimate': '25 minutes'
            }
        }
        
        activities = []
        for activity_type in activity_types:
            if activity_type in activity_library:
                activity = activity_library[activity_type].copy()
                activity['type'] = activity_type
                activities.append(activity)
        
        return activities
    
    def _generate_objectives(self, focus: str, themes: List[str]) -> List[str]:
        """Generate learning objectives for a day"""
        focus_lower = focus.lower()
        
        if 'introduction' in focus_lower:
            return [
                f"Understand the main concepts presented in the video",
                f"Identify key themes: {', '.join(themes[:2])}",
                "Establish learning goals for the week"
            ]
        elif 'core concepts' in focus_lower:
            return [
                "Master fundamental principles",
                "Practice basic techniques",
                "Build foundational understanding"
            ]
        elif 'practical' in focus_lower:
            return [
                "Apply concepts in real-world scenarios",
                "Develop practical skills",
                "Gain hands-on experience"
            ]
        elif 'advanced' in focus_lower:
            return [
                "Explore advanced techniques",
                "Solve complex problems",
                "Push beyond basic understanding"
            ]
        elif 'integration' in focus_lower:
            return [
                "Synthesize all learned concepts",
                "Create comprehensive understanding",
                "Prepare for final application"
            ]
        elif 'mastery' in focus_lower:
            return [
                "Demonstrate mastery of concepts",
                "Complete capstone project",
                "Plan future learning path"
            ]
        else:
            return [
                "Continue building understanding",
                "Practice key skills",
                "Progress toward mastery"
            ]
    
    def _generate_takeaways(self, focus: str) -> List[str]:
        """Generate key takeaways for a day"""
        return [
            f"Key insights about {focus.lower()}",
            "Practical skills developed",
            "Areas for continued improvement"
        ]
    
    def _generate_homework(self, focus: str, difficulty: str) -> str:
        """Generate homework assignment"""
        if difficulty == 'beginner':
            return f"Review today's concepts and practice one technique related to {focus.lower()}"
        elif difficulty == 'intermediate':
            return f"Apply {focus.lower()} concepts to a personal project or interest"
        else:
            return f"Research advanced applications of {focus.lower()} and plan implementation"
    
    def _calculate_day_time(self, activities: List[dict]) -> str:
        """Calculate total estimated time for a day"""
        total_minutes = 0
        
        for activity in activities:
            time_str = activity.get('time_estimate', '30 minutes')
            # Extract numbers from time estimate
            import re
            numbers = re.findall(r'\d+', time_str)
            if numbers:
                # Take the first number or average if range
                if '-' in time_str and len(numbers) >= 2:
                    total_minutes += (int(numbers[0]) + int(numbers[1])) // 2
                else:
                    total_minutes += int(numbers[0])
        
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} {minutes} minutes"
        else:
            return f"{minutes} minutes"
    
    def _generate_resources(self, video_info: dict) -> List[str]:
        """Generate additional resources"""
        resources = [
            f"Original video: {video_info.get('title', 'Unknown Title')}",
            f"Creator: {video_info.get('author', 'Unknown Author')}"
        ]
        
        # Add generic helpful resources
        resources.extend([
            "Online community forums for discussion",
            "Additional tutorials on similar topics",
            "Practice exercises and challenges",
            "Recommended books and articles"
        ])
        
        return resources
