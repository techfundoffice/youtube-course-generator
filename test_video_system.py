#!/usr/bin/env python3
"""
Comprehensive Video Player System Test
Tests video download, HTTP serving, and HTML integration
"""

import requests
import subprocess
import os
import json
import time
from urllib.parse import urljoin

BASE_URL = "http://0.0.0.0:5000"

def test_video_endpoint():
    """Test if video endpoint serves MP4 files correctly"""
    print("🎬 Testing video endpoint...")
    
    try:
        # Test HEAD request to video endpoint
        response = requests.head(f"{BASE_URL}/video/dQw4w9WgXcQ.mp4", timeout=10)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            content_length = response.headers.get('content-length')
            print(f"✅ Video endpoint working - Type: {content_type}, Size: {content_length} bytes")
            return True
        else:
            print(f"❌ Video endpoint failed - HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Video endpoint error: {str(e)}")
        return False

def test_course_generation_with_video():
    """Test full course generation pipeline with video URLs"""
    print("🔄 Testing course generation with video...")
    
    try:
        # Submit form data
        data = {'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
        response = requests.post(f"{BASE_URL}/generate", data=data, timeout=60)
        
        if response.status_code == 200:
            html = response.text
            
            # Check for video player elements
            video_checks = [
                'source src="/video/' in html,
                'type="video/mp4"' in html,
                'class="video-js' in html,
                'controls' in html
            ]
            
            if all(video_checks):
                print("✅ Course generation includes proper video player HTML")
                
                # Extract video URL from HTML
                start = html.find('source src="') + len('source src="')
                end = html.find('"', start)
                video_url = html[start:end]
                print(f"🎯 Found video URL in HTML: {video_url}")
                
                return True, video_url
            else:
                print("❌ Course generation missing video player elements")
                print(f"Video checks: {video_checks}")
                return False, None
        else:
            print(f"❌ Course generation failed - HTTP {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ Course generation error: {str(e)}")
        return False, None

def test_video_file_access():
    """Test if video files can be downloaded"""
    print("📥 Testing video file download...")
    
    try:
        # Try to download a small portion of the video
        response = requests.get(f"{BASE_URL}/video/dQw4w9WgXcQ.mp4", 
                              headers={'Range': 'bytes=0-1023'}, 
                              timeout=10)
        
        if response.status_code == 206:  # Partial content
            content_type = response.headers.get('content-type')
            content_length = response.headers.get('content-range', 'unknown')
            print(f"✅ Video file accessible - Type: {content_type}, Range: {content_length}")
            return True
        elif response.status_code == 200:
            print("✅ Video file accessible (full content)")
            return True
        else:
            print(f"❌ Video file access failed - HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Video file access error: {str(e)}")
        return False

def test_html_video_integration():
    """Test if HTML properly references video URLs"""
    print("🌐 Testing HTML video integration...")
    
    try:
        # Get the test video player page
        response = requests.get(f"{BASE_URL}/test-video-player", timeout=10)
        
        if response.status_code == 200:
            html = response.text
            
            # Check for proper HTML5 video elements
            integration_checks = [
                '<video' in html,
                'source src="/video/' in html,
                'type="video/mp4"' in html,
                'controls' in html
            ]
            
            if all(integration_checks):
                print("✅ HTML video integration correct")
                return True
            else:
                print("❌ HTML video integration issues")
                print(f"Integration checks: {integration_checks}")
                return False
        else:
            print(f"❌ Test page failed - HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ HTML integration error: {str(e)}")
        return False

def run_comprehensive_test():
    """Run all video system tests"""
    print("🚀 Starting Comprehensive Video Player System Test")
    print("=" * 60)
    
    results = []
    
    # Test 1: Video endpoint
    results.append(("Video Endpoint", test_video_endpoint()))
    
    # Test 2: Course generation
    course_result, video_url = test_course_generation_with_video()
    results.append(("Course Generation", course_result))
    
    # Test 3: Video file access
    results.append(("Video File Access", test_video_file_access()))
    
    # Test 4: HTML integration
    results.append(("HTML Integration", test_html_video_integration()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    success_rate = (passed / len(results)) * 100
    print(f"\nOverall Success Rate: {success_rate:.1f}% ({passed}/{len(results)})")
    
    if success_rate >= 75:
        print("🎉 VIDEO PLAYER SYSTEM IS FUNCTIONAL!")
    else:
        print("⚠️  VIDEO PLAYER SYSTEM NEEDS ATTENTION")
    
    return success_rate >= 75

if __name__ == "__main__":
    run_comprehensive_test()