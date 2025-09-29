#!/usr/bin/env python3
"""
Test YouTube button functionality specifically
"""

import requests
import re

BASE_URL = "http://0.0.0.0:5000"

def test_youtube_button():
    """Test if YouTube button has correct URL and attributes"""
    print("🔗 Testing YouTube button functionality...")
    
    try:
        # Generate a course
        data = {'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
        response = requests.post(f"{BASE_URL}/generate", data=data, timeout=60)
        
        if response.status_code == 200:
            html = response.text
            
            # Find the specific YouTube button (not navigation links)
            youtube_button_pattern = r'<a[^>]*href="(https://www\.youtube\.com/watch\?v=[^"]*)"[^>]*target="_blank"[^>]*rel="noopener noreferrer"[^>]*>.*?View on YouTube.*?</a>'
            youtube_buttons_full = re.findall(youtube_button_pattern, html, re.DOTALL)
            
            print(f"Found {len(youtube_buttons_full)} YouTube button(s)")
            
            youtube_buttons = youtube_buttons_full
            
            for i, url in enumerate(youtube_buttons, 1):
                print(f"Button {i} URL: '{url}'")
            
            for i, url in enumerate(youtube_buttons, 1):
                if url and url.startswith('https://www.youtube.com/watch?v='):
                    print(f"✅ Button {i}: Correct YouTube URL")
                elif url == "":
                    print(f"❌ Button {i}: Empty URL - BROKEN")
                else:
                    print(f"⚠️  Button {i}: Unexpected URL format")
            
            # Check for target="_blank" attribute
            target_blank_buttons = re.findall(r'<a[^>]*target="_blank"[^>]*>.*?View on YouTube.*?</a>', html, re.DOTALL)
            print(f"Buttons with target='_blank': {len(target_blank_buttons)}")
            
            # Check for rel="noopener noreferrer"
            security_buttons = re.findall(r'<a[^>]*rel="noopener noreferrer"[^>]*>.*?View on YouTube.*?</a>', html, re.DOTALL)
            print(f"Buttons with security attributes: {len(security_buttons)}")
            
            # Overall assessment
            if youtube_buttons and all(url.startswith('https://www.youtube.com/watch?v=') for url in youtube_buttons):
                print("🎉 ALL YOUTUBE BUTTONS WORKING CORRECTLY!")
                return True
            else:
                print("❌ YOUTUBE BUTTONS HAVE ISSUES")
                return False
                
        else:
            print(f"❌ Course generation failed - HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

if __name__ == "__main__":
    test_youtube_button()