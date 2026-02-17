# 🤖 AI Social Intelligence - Company Operations & Analytics System

<div align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=artificial-intelligence" alt="AI Powered"/>
  <img src="https://img.shields.io/badge/React-18.0+-61dafb?style=for-the-badge&logo=react" alt="React"/>
  <img src="https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/LangChain-0.0.354+-000000?style=for-the-badge&logo=chainlink" alt="LangChain"/>
</div>

## 🌟 Overview

A comprehensive **AI-powered social media intelligence and company operations analytics platform** that monitors social media conversations, provides real-time sentiment analysis, generates automated business reports, and delivers actionable insights for modern businesses.

### ✨ Key Features

- **🎯 AI-Powered Analytics**: Advanced NLP with sentiment analysis, topic modeling, and content summarization
- **📊 Live Dashboard**: Real-time analytics with interactive visualizations
- **📧 Automated Reports**: Daily AI-generated business intelligence reports via email
- **🔍 Multi-Platform Monitoring**: Twitter, LinkedIn, Facebook, Instagram integration
- **🚨 Smart Alerts**: Real-time notifications for sentiment changes and engagement spikes
- **👥 User Management**: Role-based access with subscription plans
- **🎨 Animated UI**: Fully animated interface with modern design
- **⚡ Real-Time Updates**: Live data streaming and instant insights

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React.js      │    │   FastAPI       │    │  PostgreSQL     │
│   Frontend      │◄──►│   Backend       │◄──►│   Database      │
│                 │    │                 │    │                 │
│ • Next.js 14    │    │ • LangChain AI  │    │ • Social Posts  │
│ • Tailwind CSS  │    │ • JWT Auth      │    │ • Analytics     │
│ • Framer Motion │    │ • Background Jobs│    │ • Reports       │
│ • Accernity UI  │    │ • Email Service │    │ • Users         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   AI Services   │
                       │                 │
                       │ • Sentiment     │
                       │ • Summarization │
                       │ • Topic Modeling│
                       │ • Report Gen    │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+** and **npm**
- **Python 3.8+** and **pip**
- **PostgreSQL 13+**
- **Redis** (optional, for background tasks)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd ai-social-intelligence
```

### 2. Database Setup
```bash
cd database
docker-compose up -d  # Start PostgreSQL & Redis
python setup_db.py --all  # Create DB, schema, and sample data
```

### 3. Backend Setup
```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your API keys
python -m app.main
```

### 4. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
ai-social-intelligence/
├── 📊 analytics/           # R Markdown reports & analysis
│   └── social_media_intelligence.rmd
├── 🎨 frontend/            # React.js application
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # Reusable UI components
│   │   ├── lib/           # Utilities & configurations
│   │   └── styles/        # Global styles & animations
│   └── package.json
├── ⚙️ backend/             # FastAPI application
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── core/          # Core functionality
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic & AI
│   │   └── utils/         # Helper functions
│   └── requirements.txt
├── 🗄️ database/            # Database setup & migrations
│   ├── schemas/           # SQL schema files
│   ├── setup_db.py        # Database initialization
│   └── docker-compose.yml # PostgreSQL & Redis
└── 📚 docs/                # Documentation
```

## 🎯 Core Features

### 🤖 AI Analytics Engine
- **Sentiment Analysis**: VADER + TextBlob + Custom models
- **Topic Modeling**: Automatic topic extraction and clustering
- **Content Summarization**: AI-powered text summarization
- **Trend Analysis**: Time-series analysis for engagement patterns
- **Language Detection**: Multi-language support

### 📈 Real-Time Dashboard
- **Live Metrics**: Real-time social media metrics updates
- **Interactive Charts**: Sentiment trends, platform breakdowns
- **Engagement Analytics**: Likes, shares, comments tracking
- **Custom Widgets**: Configurable dashboard layout
- **Export Capabilities**: PDF/CSV report generation

### 📧 Automated Reporting
- **Daily Reports**: AI-generated business intelligence reports
- **Custom Scheduling**: Daily, weekly, monthly options
- **Email Integration**: SMTP with HTML templates
- **Report Templates**: Customizable report formats
- **Historical Archive**: Report history and search

### 🔍 Social Media Monitoring
- **Multi-Platform**: Twitter, LinkedIn, Facebook, Instagram
- **Keyword Tracking**: Real-time keyword and hashtag monitoring
- **Account Monitoring**: Brand mention and competitor tracking
- **Engagement Alerts**: Automated alerts for engagement spikes
- **Data Collection**: Scheduled and on-demand data gathering

### 👥 User Management
- **Authentication**: JWT-based secure authentication
- **Subscription Plans**: Free, Pro, Enterprise tiers
- **Role-Based Access**: Different permission levels
- **User Profiles**: Customizable user settings
- **Team Collaboration**: Multi-user access (Enterprise)

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom animations
- **UI Components**: Radix UI + Custom components
- **Animations**: Framer Motion
- **State Management**: React hooks + Context
- **Charts**: Recharts for data visualization

### Backend
- **Framework**: FastAPI (async Python)
- **AI/ML**: LangChain + OpenAI/Anthropic/Google AI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt
- **Background Jobs**: Asyncio with threading
- **Email**: SMTP with HTML templates

### Database
- **Primary DB**: PostgreSQL 15+
- **ORM**: SQLAlchemy with async support
- **Migrations**: Alembic (future)
- **Caching**: Redis (optional)
- **Full-text Search**: PostgreSQL built-in

### AI/ML Services
- **NLP Models**: spaCy, NLTK, Transformers
- **Sentiment Analysis**: VADER, TextBlob, Custom models
- **LLM Integration**: OpenAI GPT, Anthropic Claude, Google Gemini
- **Vector Search**: Future enhancement for semantic search

## 🔧 Configuration

### Environment Variables

Create `.env` files in both `backend/` and `frontend/` directories:

#### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_social_db

# Security
SECRET_KEY=your-super-secret-key

# AI APIs
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Social APIs (optional)
TWITTER_BEARER_TOKEN=your-twitter-token
LINKEDIN_ACCESS_TOKEN=your-linkedin-token
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_ENV=development
```

## 🚀 Deployment

### Development
```bash
# Start all services
docker-compose -f database/docker-compose.yml up -d
npm run dev --workspace=frontend
python -m app.main --workspace=backend
```

### Production
- **Frontend**: Vercel, Netlify, or Docker
- **Backend**: Docker + Gunicorn/Uvicorn
- **Database**: Managed PostgreSQL (AWS RDS, Google Cloud SQL)
- **Redis**: Managed Redis (AWS ElastiCache, Redis Labs)

### Docker Deployment
```bash
# Build and run
docker-compose up --build
```

## 📊 Data Flow

1. **Data Collection**: Social media APIs → Background jobs → Database
2. **AI Processing**: Raw posts → Sentiment analysis → Topic extraction → Database
3. **Analytics**: Database queries → AI insights → Report generation
4. **Delivery**: API responses → Frontend → User dashboards + Email reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** for AI orchestration
- **FastAPI** for the robust API framework
- **Next.js** for the modern React framework
- **PostgreSQL** for reliable data storage
- **OpenAI/Anthropic** for AI capabilities

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

<div align="center">
  <p>Built with ❤️ for modern businesses</p>
  <p>
    <a href="#overview">Overview</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#features">Features</a> •
    <a href="#contributing">Contributing</a>
  </p>
</div>