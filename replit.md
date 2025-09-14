# YouTube to 7-Day Course Generator

## Overview
This project is a Flask web application designed to transform YouTube videos into structured 7-day learning courses. It leverages advanced AI for content processing and features real-time workflow visualization and robust debugging capabilities. The system aims for 99.5% reliability through multi-layer redundancy and authentic data integration, with a vision to revolutionize online learning by making high-quality, structured educational content easily accessible from existing video resources.

## User Preferences
- **Communication Style**: Professional, concise, action-focused
- **Development Style**: Comprehensive error handling, multi-layer redundancy
- **Architecture**: Production-ready with full testing coverage

## System Architecture
The application is built on a Flask backend with a Bootstrap-based frontend. Key architectural decisions include:
- **AI-Powered Course Generation**: Utilizes OpenRouter GPT-4, Anthropic Claude, and other AI services for content generation, with a fallback mechanism to ensure continuous operation.
- **Multi-layer Transcript Extraction**: Employs Apify, YouTube Data API, and web scraping for robust transcript acquisition.
- **Real-time Workflow Visualization**: An n8n-style dashboard provides live monitoring of processing steps, performance metrics, and error analysis. This includes a comprehensive backend dashboard (`/backend-dashboard`) for system monitoring, operational controls (database optimization, cache management), and an API endpoint matrix.
- **Redundancy and Reliability**: Achieves 99.5% reliability through integrated fallback systems for transcript extraction (e.g., yt-dlp if Apify fails) and AI generation. Database connection retry logic with exponential backoff ensures stability.
- **Video Processing**: Supports YouTube video URL processing, metadata extraction, and MP4 video download. Downloaded videos are automatically uploaded to Cloudinary for persistent storage, with a fallback to local serving if cloud upload fails.
- **UI/UX**: Features a responsive design with a dark Bootstrap theme. The `course_result.html` template integrates an embedded YouTube video player and a local MP4 video player (served via `/video/<filename>` endpoint).
- **Automated Testing & Debugging**: Includes an autonomous test-fixing system and enhanced processing logs with real-time updates, detailed troubleshooting metadata, and error context. Gunicorn timeouts are extended to prevent worker crashes.
- **Database Design**: PostgreSQL is used for storing course information, processing logs, and various metrics, including MP4 tracking fields and Cloudinary upload statuses.

## External Dependencies
- **AI Services**: OpenRouter, Anthropic Claude, OpenAI
- **Video & Data Extraction**: YouTube Data API, Apify (for transcript and MP4 download), yt-dlp (for MP4 download fallback)
- **Web Scraping**: Trafilatura
- **Cloud Storage**: Cloudinary (for persistent video storage)
- **Database**: PostgreSQL
- **Frontend Framework**: Bootstrap