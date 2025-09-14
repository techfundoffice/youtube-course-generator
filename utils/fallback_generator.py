import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class FallbackGenerator:
    """Generate fallback courses when all other methods fail"""
    
    def __init__(self):
        self.templates = self._load_course_templates()
    
    def create_basic_course(self, youtube_url: str, video_info: dict = None, 
                           transcript: str = None, error_reason: str = "") -> dict:
        """
        Create a basic course structure when all other methods fail
        
        Args:
            youtube_url (str): Original YouTube URL
            video_info (dict): Video metadata if available
            transcript (str): Transcript if available
            error_reason (str): Reason for fallback
            
        Returns:
            dict: Basic course structure
        """
        logger.info(f"Creating fallback course due to: {error_reason}")
        logger.info(f"YouTube URL being set in fallback course: {youtube_url}")
        
        # Extract what information we can
        title = "YouTube Video Course"
        author = "Unknown Creator"
        description = "Learn from this video content"
        
        if video_info:
            title = video_info.get('title', title)
            author = video_info.get('author', author)
            description = video_info.get('description', description)[:200]
        
        # Determine course type based on available information
        course_type = self._determine_course_type(title, description, transcript)
        template = self.templates.get(course_type, self.templates['general'])
        
        # Generate course structure
        course = {
            "course_title": f"7-Day Learning Course: {title}",
            "course_description": f"A structured 7-day course based on the YouTube video '{title}' by {author}. {description}",
            "youtube_url": youtube_url,  # Include original YouTube URL
            "target_audience": template['target_audience'],
            "estimated_total_time": "8-12 hours",
            "difficulty_level": template['difficulty_level'],
            "days": self._generate_fallback_days(template, title, transcript),
            "final_project": template['final_project'].format(title=title),
            "resources": self._generate_fallback_resources(youtube_url, video_info),
            "assessment_criteria": "Complete daily activities and final project",
            "fallback_info": {
                "generated_by": "fallback_generator",
                "reason": error_reason,
                "timestamp": datetime.utcnow().isoformat(),
                "data_available": {
                    "video_info": bool(video_info),
                    "transcript": bool(transcript and len(transcript) > 50)
                }
            }
        }
        
        return course
    
    def _load_course_templates(self) -> Dict[str, Dict]:
        """Load predefined course templates for different content types"""
        return {
            'educational': {
                'target_audience': 'Students and lifelong learners',
                'difficulty_level': 'Beginner to Intermediate',
                'final_project': 'Create a presentation summarizing key concepts from "{title}"',
                'daily_focus': [
                    'Introduction and Overview',
                    'Core Concepts - Part 1',
                    'Core Concepts - Part 2',
                    'Practical Applications',
                    'Advanced Topics',
                    'Integration and Practice',
                    'Mastery and Review'
                ]
            },
            'tutorial': {
                'target_audience': 'Practitioners looking to learn new skills',
                'difficulty_level': 'Beginner',
                'final_project': 'Complete your own version of the project shown in "{title}"',
                'daily_focus': [
                    'Setup and Preparation',
                    'Basic Techniques',
                    'Building Foundation',
                    'Intermediate Skills',
                    'Advanced Techniques',
                    'Project Development',
                    'Completion and Review'
                ]
            },
            'technical': {
                'target_audience': 'Technical professionals and developers',
                'difficulty_level': 'Intermediate to Advanced',
                'final_project': 'Implement the concepts from "{title}" in a real project',
                'daily_focus': [
                    'Technical Overview',
                    'Core Technologies',
                    'Implementation Basics',
                    'Advanced Implementation',
                    'Best Practices',
                    'Optimization and Testing',
                    'Deployment and Maintenance'
                ]
            },
            'creative': {
                'target_audience': 'Creative professionals and enthusiasts',
                'difficulty_level': 'All levels',
                'final_project': 'Create an original work inspired by "{title}"',
                'daily_focus': [
                    'Creative Inspiration',
                    'Fundamental Techniques',
                    'Skill Development',
                    'Creative Process',
                    'Advanced Techniques',
                    'Portfolio Development',
                    'Presentation and Critique'
                ]
            },
            'business': {
                'target_audience': 'Business professionals and entrepreneurs',
                'difficulty_level': 'Intermediate',
                'final_project': 'Develop a business plan incorporating insights from "{title}"',
                'daily_focus': [
                    'Business Overview',
                    'Key Concepts',
                    'Strategy Development',
                    'Implementation Planning',
                    'Advanced Strategies',
                    'Case Study Analysis',
                    'Action Plan Creation'
                ]
            },
            'general': {
                'target_audience': 'General audience interested in learning',
                'difficulty_level': 'Beginner',
                'final_project': 'Apply the main concepts from "{title}" to your personal interests',
                'daily_focus': [
                    'Introduction and Context',
                    'Understanding Key Concepts',
                    'Exploring Applications',
                    'Hands-on Practice',
                    'Deeper Understanding',
                    'Real-world Application',
                    'Integration and Next Steps'
                ]
            }
        }
    
    def _determine_course_type(self, title: str, description: str, transcript: str) -> str:
        """Determine the best course template based on content"""
        content = f"{title} {description} {transcript}".lower()
        
        # Keywords for different course types
        type_keywords = {
            'tutorial': ['tutorial', 'how to', 'step by step', 'guide', 'walkthrough'],
            'technical': ['code', 'programming', 'development', 'api', 'software', 'algorithm'],
            'creative': ['design', 'art', 'creative', 'drawing', 'music', 'video editing'],
            'business': ['business', 'marketing', 'sales', 'entrepreneur', 'strategy', 'finance'],
            'educational': ['learn', 'education', 'study', 'lesson', 'course', 'teach']
        }
        
        # Score each type
        type_scores = {}
        for course_type, keywords in type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content)
            type_scores[course_type] = score
        
        # Return the type with highest score, default to general
        if type_scores:
            best_type = max(type_scores, key=type_scores.get)
            if type_scores[best_type] > 0:
                return best_type
        
        return 'general'
    
    def _generate_fallback_days(self, template: Dict, title: str, transcript: str) -> List[Dict]:
        """Generate 7 days of course content using template"""
        days = []
        daily_focuses = template['daily_focus']
        
        for i, focus in enumerate(daily_focuses):
            day_num = i + 1
            
            # Generate activities based on day and available content
            activities = self._generate_day_activities(day_num, focus, bool(transcript))
            
            day = {
                'day': day_num,
                'title': f"Day {day_num}: {focus}",
                'objectives': self._generate_day_objectives(focus, title),
                'content_summary': f"Focus on {focus.lower()} related to the video content",
                'activities': activities,
                'key_takeaways': self._generate_day_takeaways(focus),
                'homework': self._generate_day_homework(focus, day_num),
                'estimated_time': self._calculate_estimated_time(activities)
            }
            
            days.append(day)
        
        return days
    
    def _generate_day_activities(self, day_num: int, focus: str, has_transcript: bool) -> List[Dict]:
        """Generate activities for a specific day"""
        base_activities = [
            {
                'type': 'watch',
                'description': 'Watch the video content carefully',
                'time_estimate': '30-45 minutes'
            }
        ]
        
        # Add different activities based on day and focus
        if day_num == 1:  # Introduction day
            base_activities.extend([
                {
                    'type': 'note-taking',
                    'description': 'Take notes on main topics and themes',
                    'time_estimate': '20 minutes'
                },
                {
                    'type': 'reflection',
                    'description': 'Reflect on your learning goals',
                    'time_estimate': '15 minutes'
                }
            ])
        elif day_num <= 3:  # Learning phase
            base_activities.extend([
                {
                    'type': 'analysis',
                    'description': f'Analyze the {focus.lower()} presented',
                    'time_estimate': '30 minutes'
                },
                {
                    'type': 'practice',
                    'description': 'Practice key concepts',
                    'time_estimate': '45 minutes'
                }
            ])
        elif day_num <= 5:  # Application phase
            base_activities.extend([
                {
                    'type': 'application',
                    'description': 'Apply concepts to real scenarios',
                    'time_estimate': '60 minutes'
                },
                {
                    'type': 'experimentation',
                    'description': 'Experiment with variations',
                    'time_estimate': '30 minutes'
                }
            ])
        else:  # Mastery phase
            base_activities.extend([
                {
                    'type': 'synthesis',
                    'description': 'Synthesize all learned concepts',
                    'time_estimate': '45 minutes'
                },
                {
                    'type': 'project',
                    'description': 'Work on final project',
                    'time_estimate': '90 minutes'
                }
            ])
        
        # Add transcript-specific activity if available
        if has_transcript and day_num <= 4:
            base_activities.append({
                'type': 'transcript_study',
                'description': 'Study the video transcript for deeper understanding',
                'time_estimate': '25 minutes'
            })
        
        return base_activities
    
    def _generate_day_objectives(self, focus: str, title: str) -> List[str]:
        """Generate learning objectives for a day"""
        focus_lower = focus.lower()
        
        base_objectives = [f"Understand {focus_lower} from the video content"]
        
        if 'introduction' in focus_lower:
            base_objectives.extend([
                "Identify main themes and concepts",
                "Set personal learning goals"
            ])
        elif 'concept' in focus_lower:
            base_objectives.extend([
                "Master key principles",
                "Build foundational understanding"
            ])
        elif 'application' in focus_lower or 'practice' in focus_lower:
            base_objectives.extend([
                "Apply concepts practically",
                "Develop hands-on skills"
            ])
        elif 'advanced' in focus_lower:
            base_objectives.extend([
                "Explore complex topics",
                "Push beyond basics"
            ])
        elif 'integration' in focus_lower or 'mastery' in focus_lower:
            base_objectives.extend([
                "Synthesize all learning",
                "Demonstrate mastery"
            ])
        else:
            base_objectives.extend([
                "Build on previous learning",
                "Develop deeper understanding"
            ])
        
        return base_objectives
    
    def _generate_day_takeaways(self, focus: str) -> List[str]:
        """Generate key takeaways for a day"""
        return [
            f"Key insights about {focus.lower()}",
            "Practical skills and knowledge gained",
            "Areas for continued development"
        ]
    
    def _generate_day_homework(self, focus: str, day_num: int) -> str:
        """Generate homework assignment for a day"""
        if day_num == 1:
            return "Review your notes and identify questions for deeper exploration"
        elif day_num <= 3:
            return f"Practice the concepts learned about {focus.lower()}"
        elif day_num <= 5:
            return f"Apply {focus.lower()} to a personal project or interest"
        else:
            return "Work on your final project and prepare for completion"
    
    def _calculate_estimated_time(self, activities: List[Dict]) -> str:
        """Calculate total estimated time for activities"""
        total_minutes = 0
        
        for activity in activities:
            time_str = activity.get('time_estimate', '30 minutes')
            # Extract minutes from time estimate
            if 'hour' in time_str:
                hours = 1.5  # Default for hour estimates
                total_minutes += hours * 60
            else:
                # Extract number from string like "30 minutes" or "30-45 minutes"
                import re
                numbers = re.findall(r'\d+', time_str)
                if numbers:
                    # Use average for ranges
                    if len(numbers) >= 2:
                        total_minutes += (int(numbers[0]) + int(numbers[1])) // 2
                    else:
                        total_minutes += int(numbers[0])
                else:
                    total_minutes += 30  # Default
        
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} {minutes} minutes"
        else:
            return f"{minutes} minutes"
    
    def _generate_fallback_resources(self, youtube_url: str, video_info: dict = None) -> List[str]:
        """Generate resource list for fallback course"""
        resources = [f"Original video: {youtube_url}"]
        
        if video_info:
            if video_info.get('title'):
                resources.append(f"Video title: {video_info['title']}")
            if video_info.get('author'):
                resources.append(f"Created by: {video_info['author']}")
        
        # Add generic helpful resources
        resources.extend([
            "Online forums and communities for discussion",
            "Additional videos on similar topics",
            "Practice exercises and projects",
            "Recommended reading materials",
            "Online tools and resources"
        ])
        
        return resources
