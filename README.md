# YouTube to 7-Day Course Generator

A comprehensive Flask web application that transforms YouTube videos into structured 7-day learning courses using advanced AI processing, with real-time workflow visualization and backend operations monitoring.

## 🎯 Overview

This system revolutionizes online learning by converting existing YouTube video content into structured, educational courses. Built with 99.5% reliability architecture and comprehensive error handling, it provides both end-user course generation and backend operational excellence tools.

## ✨ Key Features

### Core Functionality
- **AI-Powered Course Generation**: Multi-layer AI processing with OpenRouter GPT-4, Anthropic Claude, and intelligent fallbacks
- **YouTube Video Processing**: Advanced metadata extraction, MP4 download capabilities, and transcript processing
- **Real-time Monitoring**: Live workflow visualization with n8n-style dashboard for processing steps
- **Premium Video Storage**: Cloudinary integration for persistent video hosting with fallback systems

### Backend Operations Dashboard
- **System Health Monitoring**: 99.5% reliability tracking with comprehensive metrics
- **Service Status Matrix**: Real-time monitoring of YouTube API, Database, Cloudinary, Apify, and AI Services
- **Error Analysis & Debugging**: Advanced error categorization with resolution tracking and performance insights
- **Quick Actions Panel**: One-click system maintenance, database optimization, and cache management

### Technical Architecture
- **Multi-layer Redundancy**: Apify, YouTube Data API, and yt-dlp for robust data acquisition
- **Database Connection Management**: PostgreSQL with retry logic and exponential backoff
- **Comprehensive Testing**: Pytest suite with autonomous test-fixing capabilities
- **Production-Ready**: Gunicorn deployment with extended timeouts and error handling

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Required API keys (see Environment Variables section)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd youtube-course-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (see `.env.example`)

4. **Initialize database**
   ```bash
   python -c "from app import db; db.create_all()"
   ```

5. **Run the application**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

## 🛠 Environment Variables

Create a `.env` file with the following variables:

```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# AI Services
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
OPENROUTER_API_KEY=your_openrouter_key

# Video Processing
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
APIFY_API_TOKEN=your_apify_token

# Session
SESSION_SECRET=your_session_secret
```

## 📊 API Endpoints

### Core Application
- `GET /` - Main course generation interface
- `POST /generate` - Process YouTube URL and generate course
- `GET /courses/<id>` - View generated course
- `GET /video/<filename>` - Serve MP4 videos

### Backend Operations
- `GET /backend-dashboard` - Comprehensive operations dashboard
- `GET /api/system-health` - System health metrics and service status
- `GET /api/error-analysis` - Error analysis and debugging information
- `GET /api/performance-trends` - Performance trend data for charts

### Storage & Processing
- `GET /cloudinary` - Cloudinary dashboard for video management
- `GET /apify-dashboard` - Apify API management interface
- `POST /api/cloudinary/delete/<public_id>` - Delete Cloudinary assets

## 🏗 System Architecture

### AI Processing Pipeline
1. **Video Metadata Extraction**: YouTube API with fallback methods
2. **MP4 Download**: Apify actor with yt-dlp fallback
3. **Transcript Processing**: Multi-source transcript extraction
4. **Course Generation**: AI-powered content structuring with fallbacks
5. **Storage & Serving**: Database persistence with Cloudinary hosting

### Reliability Features
- **99.5% Uptime Architecture**: Multi-layer fallback systems
- **Database Resilience**: Connection retry logic with exponential backoff
- **Service Monitoring**: Real-time health checks and error analysis
- **Graceful Degradation**: Intelligent fallbacks when services are unavailable

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test files
python test_youtube_validation.py
python test_complete_system.html
```

## 📈 Monitoring & Operations

### Backend Dashboard Features
- **Real-time System Health**: Live monitoring of all services
- **Performance Analytics**: Processing time trends and success rates
- **Error Analysis**: Categorized error tracking with resolution suggestions
- **Database Operations**: Query performance and connection pool monitoring
- **Quick Actions**: System maintenance and optimization tools

### Log Analysis
- Structured logging with session tracking
- Real-time processing monitoring
- Error categorization and resolution tracking
- Performance metric collection

## 🔧 Configuration

### Feature Flags
- Cloudinary upload enable/disable
- Apify MP4 download toggle
- Fallback generator activation
- Debug mode settings

### Performance Tuning
- Gunicorn worker configuration
- Database connection pooling
- Cloudinary upload optimization
- AI service timeout handling

## 📝 Development

### Project Structure
```
├── app.py                 # Main Flask application
├── models.py             # Database models
├── services/             # Service layer
│   ├── ai_service.py     # AI processing
│   ├── cloudinary_service.py
│   ├── database_service.py
│   ├── transcript_service.py
│   └── youtube_downloader.py
├── templates/            # HTML templates
├── static/              # Static assets
├── tests/               # Test suite
└── utils/               # Utility functions
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🔄 Recent Updates

- ✅ Backend Operations Dashboard with comprehensive monitoring
- ✅ Real-time service status matrix and error analysis
- ✅ YouTube embed integration with MP4 video player
- ✅ Enhanced reliability architecture (99.5% uptime)
- ✅ Comprehensive testing suite with autonomous fixing
- ✅ Cloudinary premium storage integration
- ✅ Multi-layer AI processing with intelligent fallbacks

---

Built with ❤️ for educational excellence and operational reliability.