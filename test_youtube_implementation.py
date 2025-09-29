#!/usr/bin/env python3
"""
Test script to verify YouTube-only implementation
"""
import requests
import json
import sys

def test_ai_chat_default_suggestion():
    """Test that AI chat suggests React tutorial when no URLs detected"""
    print("Testing AI chat default suggestion...")
    
    try:
        # Test the chat endpoint with a simple message
        url = "http://localhost:5000/api/chat"
        data = {
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        }
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')
            show_download_button = result.get('show_download_button', False)
            youtube_urls = result.get('youtube_urls', [])
            
            print(f"AI Response: {ai_response}")
            print(f"Show download button: {show_download_button}")
            print(f"YouTube URLs: {youtube_urls}")
            
            # Check if test video is suggested  
            if "tutorial" in ai_response.lower() or "Tn6-PIqc4UM" in str(youtube_urls):
                print("✅ SUCCESS: AI suggests React tutorial video")
                return True
            else:
                print("❌ FAIL: AI does not suggest React tutorial video")
                return False
        else:
            print(f"❌ FAIL: HTTP {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_video_download():
    """Test that video download works with the React tutorial"""
    print("\nTesting video download...")
    
    try:
        # Test video download endpoint
        url = "http://localhost:5000/api/chat/download"
        data = {
            "youtube_url": "https://www.youtube.com/watch?v=Tn6-PIqc4UM"
        }
        
        response = requests.post(url, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            success = result.get('success', False)
            mp4_url = result.get('mp4_video_url', '')
            
            print(f"Download success: {success}")
            print(f"MP4 URL: {mp4_url}")
            
            if success and mp4_url:
                print("✅ SUCCESS: Video download completed")
                return True
            else:
                print(f"❌ FAIL: Download failed - {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ FAIL: HTTP {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=== Testing YouTube-only Implementation ===\n")
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: AI chat default suggestion
    if test_ai_chat_default_suggestion():
        tests_passed += 1
    
    # Test 2: Video download
    if test_video_download():
        tests_passed += 1
    
    print(f"\n=== Results: {tests_passed}/{total_tests} tests passed ===")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! YouTube-only implementation is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the implementation.")
        sys.exit(1)

if __name__ == "__main__":
    main()