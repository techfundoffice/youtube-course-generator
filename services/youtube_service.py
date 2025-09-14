import os
import logging
import aiohttp
import asyncio
import re
from urllib.parse import urlparse, parse_qs
import trafilatura
import json

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY', 'default_key')
        self.base_url = 'https://www.googleapis.com/youtube/v3'
        
    def is_healthy(self) -> bool:
        """Check if YouTube service is available"""
        return bool(self.api_key and self.api_key != 'default_key')
    
    async def get_video_info(self, youtube_url: str) -> dict:
        """Extract video information using YouTube Data API"""
        try:
            video_id = self._extract_video_id(youtube_url)
            if not video_id:
                raise ValueError("Could not extract video ID from URL")
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/videos"
                params = {
                    'part': 'snippet,contentDetails,statistics',
                    'id': video_id,
                    'key': self.api_key
                }
                
                async with session.get(url, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('items'):
                            item = data['items'][0]
                            return self._format_video_info(item, video_id)
                    else:
                        logger.error(f"YouTube API error: {response.status}")
                        
        except Exception as e:
            logger.error(f"YouTube API error: {str(e)}")
            raise
        
        return None
    
    async def get_video_info_backup(self, youtube_url: str) -> dict:
        """Backup method using alternative API or service"""
        try:
            video_id = self._extract_video_id(youtube_url)
            if not video_id:
                raise ValueError("Could not extract video ID from URL")
            
            # Using a backup service (example implementation)
            async with aiohttp.ClientSession() as session:
                # This would be replaced with actual backup service
                url = f"https://www.youtube.com/oembed?url={youtube_url}&format=json"
                
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'video_id': video_id,
                            'title': data.get('title', ''),
                            'author': data.get('author_name', ''),
                            'description': '',
                            'duration': 'Unknown',
                            'view_count': 0,
                            'published_at': 'Unknown',
                            'tags': [],
                            'thumbnail_url': data.get('thumbnail_url', '')
                        }
                        
        except Exception as e:
            logger.error(f"Backup API error: {str(e)}")
            raise
        
        return None
    
    async def scrape_video_info(self, youtube_url: str) -> dict:
        """Fallback method using web scraping"""
        try:
            video_id = self._extract_video_id(youtube_url)
            if not video_id:
                raise ValueError("Could not extract video ID from URL")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(youtube_url, timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_youtube_page(html, video_id)
                        
        except Exception as e:
            logger.error(f"Web scraping error: {str(e)}")
            raise
        
        return None
    
    def _extract_video_id(self, youtube_url: str) -> str:
        """Extract video ID from various YouTube URL formats including Shorts"""
        # Import the centralized validator function
        from utils.validators import extract_video_id
        return extract_video_id(youtube_url)
    
    def _format_video_info(self, item: dict, video_id: str) -> dict:
        """Format YouTube API response into standardized format"""
        snippet = item.get('snippet', {})
        statistics = item.get('statistics', {})
        content_details = item.get('contentDetails', {})
        
        return {
            'video_id': video_id,
            'title': snippet.get('title', ''),
            'author': snippet.get('channelTitle', ''),
            'description': snippet.get('description', ''),
            'duration': content_details.get('duration', ''),
            'view_count': int(statistics.get('viewCount', 0)),
            'published_at': snippet.get('publishedAt', ''),
            'tags': snippet.get('tags', []),
            'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
            'category_id': snippet.get('categoryId', ''),
            'language': snippet.get('defaultLanguage', 'en')
        }
    
    def _parse_youtube_page(self, html: str, video_id: str) -> dict:
        """Parse YouTube page HTML for video information"""
        try:
            # Extract title
            title_match = re.search(r'<title>([^<]+)</title>', html)
            title = title_match.group(1) if title_match else 'Unknown Title'
            title = title.replace(' - YouTube', '')
            
            # Extract description using trafilatura
            text_content = trafilatura.extract(html)
            description = text_content[:500] if text_content else ''
            
            # Extract channel name
            channel_match = re.search(r'"ownerChannelName":"([^"]+)"', html)
            author = channel_match.group(1) if channel_match else 'Unknown Channel'
            
            return {
                'video_id': video_id,
                'title': title,
                'author': author,
                'description': description,
                'duration': 'Unknown',
                'view_count': 0,
                'published_at': 'Unknown',
                'tags': [],
                'thumbnail_url': f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg'
            }
            
        except Exception as e:
            logger.error(f"HTML parsing error: {str(e)}")
            raise
