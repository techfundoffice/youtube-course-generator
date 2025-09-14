import os
import logging
import aiohttp
import asyncio
import json
import re

logger = logging.getLogger(__name__)

class TranscriptService:
    def __init__(self):
        self.apify_token = os.getenv('APIFY_TOKEN', 'default_token')
        
    def is_healthy(self) -> bool:
        """Check if transcript service is available"""
        return bool(self.apify_token and self.apify_token != 'default_token')
    
    async def get_transcript_apify(self, video_id: str) -> str:
        """Extract transcript using Apify service"""
        try:
            if not self.apify_token or self.apify_token == 'default_token':
                raise ValueError("Apify token not configured")
            
            async with aiohttp.ClientSession() as session:
                # Apify YouTube scraper API call
                url = f"https://api.apify.com/v2/acts/apify~youtube-scraper/run-sync-get-dataset-items"
                
                headers = {
                    'Authorization': f'Bearer {self.apify_token}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'startUrls': [f'https://www.youtube.com/watch?v={video_id}'],
                    'maxResults': 1,
                    'subtitlesFormat': 'text',
                    'subtitlesLangs': ['en']
                }
                
                async with session.post(url, json=payload, headers=headers, timeout=60) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data and len(data) > 0:
                            subtitles = data[0].get('subtitles', '')
                            if subtitles:
                                return self._clean_transcript(subtitles)
                    else:
                        logger.error(f"Apify API error: {response.status}")
                        
        except Exception as e:
            logger.error(f"Apify transcript error: {str(e)}")
            raise
        
        return None
    
    async def get_transcript_youtube(self, video_id: str) -> str:
        """Extract transcript using youtube-transcript-api equivalent"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get video page to find transcript data
                url = f"https://www.youtube.com/watch?v={video_id}"
                
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        transcript = self._extract_transcript_from_html(html)
                        if transcript:
                            return self._clean_transcript(transcript)
                            
        except Exception as e:
            logger.error(f"YouTube transcript error: {str(e)}")
            raise
        
        return None
    
    async def get_transcript_backup(self, video_id: str) -> str:
        """Backup transcript extraction method"""
        try:
            # This would use another service like AssemblyAI, Rev.ai, etc.
            # For now, we'll simulate with a placeholder that tries to get captions
            async with aiohttp.ClientSession() as session:
                # Try to get auto-generated captions
                url = f"https://www.youtube.com/api/timedtext?lang=en&v={video_id}"
                
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        xml_content = await response.text()
                        transcript = self._parse_xml_transcript(xml_content)
                        if transcript:
                            return self._clean_transcript(transcript)
                            
        except Exception as e:
            logger.error(f"Backup transcript error: {str(e)}")
            raise
        
        return None
    
    def _extract_transcript_from_html(self, html: str) -> str:
        """Extract transcript data from YouTube page HTML"""
        try:
            # Look for transcript data in the page
            patterns = [
                r'"transcriptRenderer":\s*{[^}]*"content":\s*"([^"]*)"',
                r'"text":\s*"([^"]*)"[^}]*"simpleText"',
            ]
            
            transcript_parts = []
            for pattern in patterns:
                matches = re.findall(pattern, html)
                transcript_parts.extend(matches)
            
            if transcript_parts:
                return ' '.join(transcript_parts)
                
        except Exception as e:
            logger.error(f"HTML transcript extraction error: {str(e)}")
        
        return None
    
    def _parse_xml_transcript(self, xml_content: str) -> str:
        """Parse XML transcript format"""
        try:
            # Extract text from XML captions
            text_pattern = r'<text[^>]*>([^<]*)</text>'
            matches = re.findall(text_pattern, xml_content)
            
            if matches:
                # Clean and join transcript parts
                transcript = ' '.join(matches)
                return transcript
                
        except Exception as e:
            logger.error(f"XML transcript parsing error: {str(e)}")
        
        return None
    
    def _clean_transcript(self, transcript: str) -> str:
        """Clean and format transcript text"""
        if not transcript:
            return ""
        
        # Remove HTML entities
        transcript = re.sub(r'&[a-zA-Z0-9#]+;', ' ', transcript)
        
        # Remove extra whitespace
        transcript = re.sub(r'\s+', ' ', transcript).strip()
        
        # Remove timestamps if present
        transcript = re.sub(r'\d{1,2}:\d{2}(?::\d{2})?\s*', '', transcript)
        
        # Remove common caption artifacts
        transcript = re.sub(r'\[.*?\]', '', transcript)
        transcript = re.sub(r'\(.*?\)', '', transcript)
        
        return transcript
