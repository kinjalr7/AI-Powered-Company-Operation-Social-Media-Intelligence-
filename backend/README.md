# AI Social Intelligence Backend

A comprehensive AI-powered social media intelligence platform built with FastAPI, LangChain, and PostgreSQL.

## Features

- **AI-Powered Analytics**: Sentiment analysis, topic modeling, and content summarization using LangChain
- **Multi-Platform Social Media Monitoring**: Twitter, LinkedIn, Facebook, Instagram integration
- **Automated Reporting**: Daily/weekly/monthly AI-generated business reports
- **Real-time Alerts**: Configurable notification system for sentiment and engagement changes
- **RESTful API**: Complete API for frontend integration
- **Background Processing**: Asynchronous task processing with proper scheduling

## Tech Stack

- **Framework**: FastAPI (Python)
- **AI/ML**: LangChain, OpenAI/Anthropic/Google AI
- **Database**: PostgreSQL with SQLAlchemy
- **Authentication**: JWT tokens
- **Email**: SMTP integration
- **Background Tasks**: Asyncio with threading
- **Social APIs**: Twitter API v2, LinkedIn, Facebook Graph API

## Installation

1. **Clone and setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment setup**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Database setup**:
   ```bash
   # Make sure PostgreSQL is running
   # Create database: ai_social_db
   # The app will create tables automatically
   ```

4. **Run the application**:
   ```bash
   python -m app.main
   # Or with uvicorn:
   uvicorn app.main:app --reload
   ```

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

- `POST /api/auth/login` - User authentication
- `GET /api/analytics/dashboard` - Get dashboard analytics
- `POST /api/reports/generate` - Generate AI reports
- `GET /api/social-data/posts` - Retrieve social media posts
- `POST /api/social-data/collect` - Trigger data collection

## Project Structure

```
backend/
├── app/
│   ├── api/           # API route handlers
│   │   ├── auth.py
│   │   ├── analytics.py
│   │   ├── reports.py
│   │   └── social_data.py
│   ├── core/          # Core functionality
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/        # Database models
│   │   ├── user.py
│   │   └── social_data.py
│   ├── schemas/       # Pydantic schemas
│   │   ├── user.py
│   │   └── social_data.py
│   ├── services/      # Business logic
│   │   ├── ai_analytics.py
│   │   ├── auth.py
│   │   ├── email_service.py
│   │   ├── scheduler.py
│   │   └── social_collector.py
│   └── utils/         # Utility functions
├── requirements.txt
├── main.py
└── README.md
```

## AI Features

### Sentiment Analysis
- VADER sentiment analysis
- TextBlob polarity scoring
- Configurable sentiment thresholds

### Content Analysis
- Topic extraction and modeling
- Keyword analysis
- Content summarization using LLMs

### Automated Reporting
- Daily business intelligence reports
- Custom report generation
- Email delivery system

## Social Media Integration

The system supports multiple social media platforms:

- **Twitter**: Real-time tweet monitoring with advanced search
- **LinkedIn**: Professional content and company updates
- **Facebook**: Public page and group monitoring
- **Instagram**: Hashtag and account monitoring

## Background Tasks

- **Daily Reports**: Automated report generation and email delivery
- **Data Collection**: Scheduled social media data gathering
- **Alert Monitoring**: Real-time sentiment and engagement alerts

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Database Migrations
```bash
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

## Deployment

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
See `.env.example` for required environment variables.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.