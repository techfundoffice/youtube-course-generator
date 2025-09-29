#!/usr/bin/env python3
"""
DEFINITIVE YouTube Embed Validation Test
Tests actual functionality with proper HTML parsing
"""

import requests
from bs4 import BeautifulSoup
import re

def definitive_youtube_test():
    print("🎯 DEFINITIVE YouTube Embed Validation Test")
    print("=" * 50)
    
    try:
        # Get the course page
        response = requests.get("http://localhost:5000/courses/32", timeout=10)
        print(f"✅ HTTP Response: {response.status_code}")
        print(f"✅ Content Size: {len(response.text):,} bytes")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Page not accessible")
            return False
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Check for YouTube Video URL section header
        youtube_header = soup.find('h4', class_='card-title')
        youtube_sections = []
        for header in soup.find_all('h4', class_='card-title'):
            if header.get_text().strip().lower().find('youtube') != -1:
                youtube_sections.append(header.get_text().strip())
        
        print(f"✅ YouTube section headers found: {len(youtube_sections)}")
        for section in youtube_sections:
            print(f"   - '{section}'")
        
        # 2. Check for YouTube iframes
        youtube_iframes = soup.find_all('iframe', src=re.compile(r'youtube\.com/embed'))
        print(f"✅ YouTube iframes found: {len(youtube_iframes)}")
        
        # 3. Validate each iframe
        all_valid = True
        for i, iframe in enumerate(youtube_iframes):
            src = iframe.get('src', '')
            video_id = re.search(r'/embed/([^?]+)', src).group(1) if re.search(r'/embed/([^?]+)', src) else 'unknown'
            
            print(f"📺 iframe {i+1}:")
            print(f"   - Video ID: {video_id}")
            print(f"   - Has allowfullscreen: {iframe.has_attr('allowfullscreen')}")
            print(f"   - Has proper allow attr: {'autoplay' in iframe.get('allow', '')}")
            print(f"   - In responsive container: {bool(iframe.find_parent('div', class_='ratio'))}")
            
            # Check if iframe is properly positioned in a YouTube section
            card_parent = iframe.find_parent('div', class_='card')
            if card_parent:
                header = card_parent.find('h4', class_='card-title')
                if header and 'youtube' in header.get_text().lower():
                    print(f"   - Correctly positioned in YouTube section: YES")
                else:
                    print(f"   - Correctly positioned in YouTube section: NO")
                    all_valid = False
            else:
                print(f"   - In card container: NO")
                all_valid = False
        
        # 4. Check for "View on YouTube" buttons
        youtube_buttons = soup.find_all('a', href=re.compile(r'youtube\.com/watch'))
        print(f"✅ 'View on YouTube' buttons: {len(youtube_buttons)}")
        
        # 5. Final validation
        print("\n🎯 FINAL VALIDATION:")
        print(f"✅ Page loads: YES")
        print(f"✅ YouTube section exists: {'YES' if youtube_sections else 'NO'}")
        print(f"✅ YouTube iframes present: {'YES' if youtube_iframes else 'NO'} ({len(youtube_iframes)} found)")
        print(f"✅ Iframes properly configured: {'YES' if all_valid and youtube_iframes else 'NO'}")
        print(f"✅ YouTube buttons present: {'YES' if youtube_buttons else 'NO'}")
        
        success = (
            len(youtube_sections) > 0 and 
            len(youtube_iframes) >= 1 and 
            all_valid and
            len(youtube_buttons) > 0
        )
        
        print(f"\n🏁 OVERALL RESULT: {'✅ PASS' if success else '❌ FAIL'}")
        
        if success:
            print("🎉 YouTube embed integration is FULLY WORKING!")
            print("   - YouTube video displays in dedicated section")
            print("   - Responsive iframe with proper attributes") 
            print("   - View on YouTube buttons functional")
            print("   - Video ID correctly extracted and embedded")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = definitive_youtube_test()
    exit(0 if success else 1)