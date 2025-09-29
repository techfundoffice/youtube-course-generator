#!/usr/bin/env python3
"""
Test script for Cloudinary integration
Tests upload functionality and service configuration
"""
import os
import sys
import asyncio
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.cloudinary_service import cloudinary_service

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_cloudinary_configuration():
    """Test Cloudinary configuration and connectivity"""
    print("🔧 Testing Cloudinary Configuration")
    print("=" * 50)
    
    # Check if configured
    print(f"Configured: {cloudinary_service.configured}")
    
    # Check environment variables
    env_vars = {
        'CLOUDINARY_CLOUD_NAME': bool(os.environ.get('CLOUDINARY_CLOUD_NAME')),
        'CLOUDINARY_API_KEY': bool(os.environ.get('CLOUDINARY_API_KEY')),
        'CLOUDINARY_API_SECRET': bool(os.environ.get('CLOUDINARY_API_SECRET'))
    }
    
    print("Environment Variables:")
    for var, exists in env_vars.items():
        status = "✅ Set" if exists else "❌ Missing"
        print(f"  {var}: {status}")
    
    if cloudinary_service.configured:
        print("\n✅ Cloudinary is properly configured!")
        return True
    else:
        print("\n❌ Cloudinary configuration incomplete")
        print("\nTo configure Cloudinary:")
        print("1. Sign up at https://cloudinary.com")
        print("2. Get your credentials from the dashboard")
        print("3. Set environment variables:")
        print("   - CLOUDINARY_CLOUD_NAME")
        print("   - CLOUDINARY_API_KEY") 
        print("   - CLOUDINARY_API_SECRET")
        return False

async def test_video_upload():
    """Test video upload functionality (requires actual video file)"""
    if not cloudinary_service.configured:
        print("❌ Cannot test upload - Cloudinary not configured")
        return
    
    print("\n📹 Testing Video Upload")
    print("=" * 50)
    
    # Look for any existing MP4 files in temp directories
    import glob
    video_files = glob.glob('/tmp/youtube_dl_*/*.mp4')
    
    if not video_files:
        print("❌ No MP4 files found in temp directories")
        print("   Run a course generation first to download a video")
        return
    
    test_video = video_files[0]
    print(f"Found test video: {test_video}")
    
    # Test upload
    video_metadata = {
        'title': 'Test Video Upload',
        'duration': 60,
        'author': 'Test Author',
        'youtube_url': 'https://www.youtube.com/watch?v=test'
    }
    
    try:
        result = cloudinary_service.upload_video(test_video, 'test_video_123', video_metadata)
        
        if result.get('success'):
            print("✅ Upload successful!")
            print(f"   Cloudinary URL: {result.get('cloudinary_url')}")
            print(f"   Public ID: {result.get('cloudinary_public_id')}")
            print(f"   File Size: {result.get('file_size')} bytes")
        else:
            print(f"❌ Upload failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Upload exception: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_cloudinary_configuration())
    asyncio.run(test_video_upload())