#!/usr/bin/env python3
"""
YouTube Embed Validation Test
Tests if YouTube iframe is properly embedded in course page
"""

import requests
import re
from bs4 import BeautifulSoup
import json

def test_youtube_embed():
    print("🧪 Starting YouTube embed validation test...")
    
    try:
        # Test course page
        print("📍 Testing course page...")
        response = requests.get("http://localhost:5000/courses/32", timeout=10)
        
        print(f"✅ HTTP Status: {response.status_code}")
        print(f"✅ Content Length: {len(response.text)} bytes")
        
        if response.status_code != 200:
            print(f"❌ Page failed to load: {response.status_code}")
            return False
            
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for YouTube Video URL section (more flexible search)
        youtube_section = soup.find('h4', string=re.compile(r'YouTube.*Video.*URL', re.IGNORECASE))
        if not youtube_section:
            # Try alternative patterns
            youtube_section = soup.find(['h3', 'h4', 'h5'], string=re.compile(r'YouTube.*URL|Video.*URL', re.IGNORECASE))
        if not youtube_section:
            # Look for any heading containing "YouTube" near an iframe
            youtube_section = soup.find(['h1', 'h2', 'h3', 'h4', 'h5'], string=re.compile(r'YouTube', re.IGNORECASE))
        print(f"✅ YouTube Video URL section: {'FOUND' if youtube_section else 'NOT FOUND'}")
        if youtube_section:
            print(f"   - section text: '{youtube_section.get_text()}'")
            print(f"   - section tag: {youtube_section.name}")
        
        # Find all YouTube iframes
        youtube_iframes = soup.find_all('iframe', src=re.compile(r'youtube\.com/embed'))
        print(f"📺 YouTube iframes found: {len(youtube_iframes)}")
        
        # Validate each iframe
        for i, iframe in enumerate(youtube_iframes):
            src = iframe.get('src', '')
            print(f"🎯 iframe {i+1}:")
            print(f"   - src: {src}")
            print(f"   - frameborder: {iframe.get('frameborder', 'not set')}")
            print(f"   - allowfullscreen: {iframe.has_attr('allowfullscreen')}")
            print(f"   - allow attribute: {iframe.get('allow', 'not set')}")
            
            # Check if it's in the right section
            if youtube_section:
                parent_card = iframe.find_parent('div', class_='card')
                section_card = youtube_section.find_parent('div', class_='card')
                if parent_card and section_card and parent_card == section_card:
                    print(f"   - position: CORRECTLY in YouTube Video URL section")
                else:
                    print(f"   - position: in different section")
        
        # Check for responsive container
        ratio_containers = soup.find_all('div', class_='ratio')
        youtube_in_ratio = False
        for container in ratio_containers:
            if container.find('iframe', src=re.compile(r'youtube\.com/embed')):
                youtube_in_ratio = True
                classes = container.get('class', [])
                print(f"✅ Responsive container: {' '.join(classes)}")
                break
        
        # Final validation
        print("\n🎯 VALIDATION RESULTS:")
        print(f"✅ Page loads successfully: YES")
        print(f"✅ YouTube Video URL section exists: {'YES' if youtube_section else 'NO'}")
        print(f"✅ YouTube iframe(s) present: {'YES' if youtube_iframes else 'NO'} ({len(youtube_iframes)} found)")
        print(f"✅ Responsive container: {'YES' if youtube_in_ratio else 'NO'}")
        print(f"✅ Proper iframe attributes: {'YES' if youtube_iframes and youtube_iframes[0].has_attr('allowfullscreen') else 'NO'}")
        
        # Extract video ID for verification
        if youtube_iframes:
            src = youtube_iframes[0].get('src', '')
            video_id_match = re.search(r'/embed/([^?]+)', src)
            if video_id_match:
                video_id = video_id_match.group(1)
                print(f"✅ Video ID extracted: {video_id}")
        
        return {
            'success': len(youtube_iframes) > 0 and youtube_section is not None,
            'iframe_count': len(youtube_iframes),
            'has_section': youtube_section is not None,
            'responsive': youtube_in_ratio,
            'page_size': len(response.text)
        }
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return {'success': False, 'error': str(e)}

def test_page_structure():
    print("\n📋 Testing page structure...")
    
    try:
        response = requests.get("http://localhost:5000/courses/32", timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check key sections
        sections = {
            'Navigation': soup.find('nav'),
            'Course Title': soup.find('h1'),
            'Course Description': soup.find('div', class_='card-body'),
            'YouTube Video URL': soup.find(['h3', 'h4', 'h5'], string=re.compile(r'YouTube.*Video.*URL|YouTube.*URL', re.IGNORECASE)),
            'Processing Logs': soup.find(['h3', 'h4', 'h5'], string=re.compile(r'Processing.*Logs|Logs', re.IGNORECASE)),
            'Course Content': soup.find(['h3', 'h4', 'h5'], string=re.compile(r'Course.*Content|7.*Day|Daily', re.IGNORECASE)),
        }
        
        for section_name, element in sections.items():
            status = "✅ FOUND" if element else "❌ MISSING"
            print(f"   {section_name}: {status}")
            
        return all(element is not None for element in sections.values())
        
    except Exception as e:
        print(f"❌ Structure test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 YouTube Embed Comprehensive Validation\n")
    
    # Test embed functionality
    embed_result = test_youtube_embed()
    
    # Test page structure
    structure_ok = test_page_structure()
    
    print(f"\n🏁 FINAL RESULTS:")
    print(f"✅ YouTube Embed Working: {'YES' if embed_result.get('success') else 'NO'}")
    print(f"✅ Page Structure Complete: {'YES' if structure_ok else 'NO'}")
    
    if embed_result.get('success') and structure_ok:
        print("🎉 ALL TESTS PASSED - YouTube embed is working correctly!")
        exit(0)
    else:
        print("⚠️  TESTS FAILED - Issues detected with YouTube embed")
        exit(1)