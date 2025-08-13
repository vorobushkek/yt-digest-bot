# YT Digest Bot

🤖 **YouTube Digest Telegram Bot** - Generate automated daily/weekly digests of your favorite YouTube channels directly in Telegram.

## ✨ Features

- **📺 Channel Subscriptions**: Subscribe to your favorite YouTube channels
- **📊 Automated Digests**: Receive daily, weekly, or custom digest schedules
- **🔍 Smart Summaries**: AI-powered video summaries and highlights
- **⚡ Fast & Lightweight**: Optimized for Render free tier deployment
- **🔐 Secure**: No data storage beyond necessary user preferences
- **📱 Easy to Use**: Simple Telegram bot interface

## 🏗️ Architecture

This project is optimized for **Render free tier** deployment with a clean, modular architecture:

```
├── app/
│   ├── bot/
│   │   └── bot.py              # Aiogram bot implementation
│   ├── web/
│   │   └── main.py            # FastAPI web server
│   ├── database/
│   │   └── models.py          # SQLAlchemy database models
│   ├── config.py              # Configuration management
│   └── main.py                # Application entry point
├── requirements.txt           # Optimized dependencies
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Local development
└── .env.example              # Environment variables template
```

### Key Components:

- **🚀 FastAPI Web Server**: Health checks, webhooks, and cron endpoints
- **🤖 Aiogram Bot**: Modern Telegram bot framework with async support
- **💾 PostgreSQL Database**: User data, subscriptions, and digests
- **📊 SQLAlchemy ORM**: Robust database operations with proper relationships
- **⏰ APScheduler**: Background task scheduling (alternative to Celery for free tier)

## 🛠️ Tech Stack

### Core Technologies:
- **Python 3.11+** - Modern async Python
- **FastAPI** - High-performance API framework
- **Aiogram 3.x** - Telegram Bot API wrapper
- **SQLAlchemy 2.x** - Modern ORM with async support
- **PostgreSQL** - Reliable database
- **APScheduler** - Task scheduling

### Deployment:
- **Render** - Free tier optimized hosting
- **Docker** - Containerized deployment
- **Pydantic 2.6.4** - Pinned to avoid Rust compilation issues

## 🚀 Quick Start

### Prerequisites

1. **Telegram Bot Token**: Get one from [@BotFather](https://t.me/botfather)
2. **YouTube API Key**: Get one from [Google Cloud Console](https://console.cloud.google.com/)
3. **PostgreSQL Database**: Set up locally or use a cloud provider

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vorobushkek/yt-digest-bot.git
   cd yt-digest-bot
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run with Docker Compose** (recommended):
   ```bash
   docker-compose up -d
   ```

5. **Or run locally**:
   ```bash
   # Run FastAPI server
   uvicorn app.web.main:app --host 0.0.0.0 --port 8000
   
   # In another terminal, run bot (for testing)
   python -m app.bot.bot
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_URL=https://your-app.onrender.com
WEBHOOK_SECRET=your_webhook_secret

# YouTube API
YOUTUBE_API_KEY=your_youtube_api_key

# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Web Server
PORT=8000
X_CRON_KEY=your_secret_cron_key

# Optional: OpenAI for summaries
OPENAI_API_KEY=your_openai_key
```

## 📦 Deployment on Render

### Step 1: Prepare Your Repository

This repository is already optimized for Render free tier:
- ✅ Pinned dependencies to avoid build issues
- ✅ Optimized `requirements.txt` without Rust dependencies
- ✅ FastAPI server with proper health checks
- ✅ Environment-based configuration

### Step 2: Deploy to Render

1. **Fork this repository** to your GitHub account

2. **Create a new Web Service** on [Render](https://render.com):
   - Connect your GitHub repository
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m app.web.main`
   - **Environment**: `Python 3`

3. **Set Environment Variables** in Render dashboard:
   - Add all variables from your `.env` file
   - Set `WEBHOOK_URL` to your Render app URL

4. **Set up Database**:
   - Create a PostgreSQL database on Render (or use external)
   - Set `DATABASE_URL` environment variable

### Step 3: Configure Webhook

Your bot will automatically set up the webhook when it starts. The FastAPI server provides these endpoints:

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /webhook` - Telegram webhook
- `POST /cron/digest` - Digest generation (requires `X-CRON-KEY` header)

## 🤖 Bot Commands

- `/start` - Initialize the bot and show welcome message
- `/help` - Display help information
- `/status` - Check bot operational status
- `/digest` - Generate digest (coming soon)

## 📊 Database Schema

The bot uses a comprehensive database schema:

- **Users** - Telegram user information and preferences
- **YouTubeChannels** - Channel metadata and statistics
- **Videos** - Individual video information and metrics
- **Subscriptions** - User-channel subscription relationships
- **Digests** - Generated digest content and metadata
- **DigestVideos** - Many-to-many relationship for digest content

## 🔄 Development Workflow

### Local Development
```bash
# Start services
docker-compose up -d postgres redis

# Run in development mode
uvicorn app.web.main:app --reload --host 0.0.0.0 --port 8000

# Test bot in polling mode
python -m app.bot.bot
```

### Testing
```bash
# Run tests (when available)
pytest

# Check code quality
flake8 app/
black app/ --check
```

## 🚧 Roadmap

- [ ] **YouTube Integration**: Fetch channel videos and metadata
- [ ] **AI Summaries**: OpenAI/Claude integration for video summaries
- [ ] **Digest Generation**: Automated daily/weekly digest creation
- [ ] **User Management**: Subscription management interface
- [ ] **Advanced Scheduling**: Custom digest frequencies
- [ ] **Analytics**: Usage statistics and performance metrics
- [ ] **Multi-language**: Support for multiple languages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/vorobushkek/yt-digest-bot/issues) page
2. Review the [deployment logs](#) on Render
3. Verify your environment variables are set correctly
4. Ensure your bot token and API keys are valid

## 💡 Tips for Render Free Tier

- **Optimize Dependencies**: This repo uses pinned versions to avoid compilation
- **Health Checks**: The FastAPI server includes proper health endpoints
- **Environment Variables**: All configuration is environment-based
- **Database Connections**: Connection pooling and proper cleanup
- **Lightweight**: Minimal resource usage optimized for free tier limits

---

**Built with ❤️ for the open source community**

*Optimized for Render free tier deployment* 🚀
