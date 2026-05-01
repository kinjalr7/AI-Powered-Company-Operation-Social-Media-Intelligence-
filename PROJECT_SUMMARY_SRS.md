# Project Summary for SRS Report  
## AI Social Intelligence – Company Operations & Analytics System

This document provides a consolidated summary for preparing a **Software Requirements Specification (SRS)** report. Use the sections below as input for your SRS (overview, tech stack, features, architecture, etc.).

---

## 1. Project Summary / Overview

**Project Name:** AI Social Intelligence – Company Operations & Analytics System  

**Type:** Web application (full-stack)  

**Purpose:** An **AI-powered social media intelligence and company operations analytics platform** that:

- Monitors social media conversations across multiple platforms  
- Performs real-time sentiment analysis and topic modeling  
- Generates automated business intelligence reports  
- Delivers actionable insights, alerts, and dashboards for modern businesses  

**Target Users:** Businesses, marketing teams, and operations managers who need social listening, sentiment tracking, and automated reporting.

**High-Level Value:** Centralized multi-platform social monitoring, AI-driven insights, and automated reporting to support decision-making and brand/engagement tracking.

---

## 2. Technology Stack

### 2.1 Frontend

| Category        | Technology / Tool        | Version / Notes                    |
|----------------|--------------------------|------------------------------------|
| Framework      | Next.js                  | 14.x (App Router)                  |
| UI Library     | React                    | 18.x                               |
| Language       | TypeScript               | 5.x                                |
| Styling        | Tailwind CSS             | 3.3+ with tailwindcss-animate       |
| UI Components  | Radix UI                 | Dialog, Dropdown, Label, Progress, Separator, Select, Tabs |
| Animations     | Framer Motion            | 10.x                               |
| Charts         | Recharts                 | 2.8.x                              |
| Icons          | Lucide React             | 0.294.x                            |
| Utilities      | clsx, tailwind-merge, class-variance-authority | -   |
| Notifications  | Sonner                   | 2.x                                |

**Port:** Frontend runs on **3002** (e.g. `npm run dev` → http://localhost:3002).

### 2.2 Backend

| Category        | Technology / Tool        | Version / Notes                    |
|----------------|--------------------------|------------------------------------|
| Framework      | FastAPI                  | 0.104.x                            |
| Server         | Uvicorn                  | 0.24.x (ASGI)                      |
| Language       | Python                   | 3.x (3.8+ recommended)             |
| ORM            | SQLAlchemy               | 2.0.x                              |
| Validation     | Pydantic (schemas)       | Via FastAPI                        |
| Auth           | JWT (python-jose), bcrypt, passlib | -                          |
| Migrations     | Alembic                  | 1.13.x                             |
| Task Scheduling| APScheduler              | 3.10.x                             |
| Real-time      | WebSockets, SSE-Starlette| 12.0, 1.8.x                        |
| PDF            | Reportlab                | 4.0.x                              |
| Email          | smtplib3, email-validator| -                                  |
| Social APIs    | Tweepy, linkedin-api     | 4.14, 2.0                          |
| Data / ML      | pandas, numpy, scikit-learn | 2.1, 1.24, 1.3                 |
| NLP / AI       | transformers, torch, NLTK | 4.36, 2.1, 3.8                  |
| Kaggle         | kaggle                   | 1.6.x                              |

**Port:** API runs on **8000** (e.g. http://localhost:8000, docs at `/docs`).

### 2.3 Database & Infrastructure

| Category        | Technology / Tool        | Notes                              |
|----------------|--------------------------|------------------------------------|
| Primary DB     | PostgreSQL               | 13+ (15+ in README); schema in `database/schemas/init.sql` |
| Dev DB         | SQLite                   | Optional via `DATABASE_URL` (e.g. `ai_social_dev.db`) |
| Caching / Jobs | Redis                    | Optional (e.g. background tasks)   |
| Containerization| Docker                   | docker-compose in `database/` for PostgreSQL (and Redis) |
| Setup          | Python script            | `database/setup_db.py` (create DB, init schema, sample data) |

### 2.4 AI / Analytics (Referenced in README and Code)

- **NLP:** spaCy, NLTK, Transformers  
- **Sentiment:** VADER, TextBlob, custom models  
- **LLM / Orchestration:** LangChain; OpenAI, Anthropic, Google AI (keys in config)  
- **Future:** Vector/semantic search noted as enhancement  

---

## 3. Features (for SRS Functional / Non-Functional Requirements)

### 3.1 Core Functional Features

- **AI-Powered Analytics**  
  - Sentiment analysis (positive / negative / neutral; scores)  
  - Topic modeling and extraction  
  - Content summarization  
  - Trend and time-series analysis  
  - Language detection  

- **Live Dashboard**  
  - Real-time or near real-time metrics  
  - Interactive charts (sentiment trends, platform breakdown, engagement, topic frequency, etc.)  
  - Configurable widgets  
  - Export (e.g. PDF/CSV)  

- **Automated Reporting**  
  - AI-generated business intelligence reports  
  - Scheduling (daily, weekly, monthly)  
  - Email delivery (SMTP, HTML templates)  
  - Report history, download, and (planned) search  

- **Multi-Platform Social Monitoring**  
  - Platforms: Twitter, LinkedIn, Facebook, Instagram (and demo data for YouTube, TikTok, Reddit, Threads, Pinterest, Snapchat)  
  - Keyword and hashtag monitoring  
  - Account and brand mention tracking  
  - Data collection: scheduled and on-demand  
  - Monitoring status and keyword/platform configuration via API  

- **User Management & Auth**  
  - JWT-based authentication (login, register, refresh, /me)  
  - User profile and social profile links (Twitter, LinkedIn, Facebook, Instagram, YouTube, TikTok)  
  - Role-based access and subscription plans (Free, Pro, Enterprise)  

- **Social Accounts & Scheduling**  
  - CRUD for social accounts; verification  
  - Post scheduling and “post now”; scheduled posts list  

- **Reports**  
  - Generate, list, get by ID, download, delete  
  - Personal social analysis report  
  - Schedule daily reports  

### 3.2 Non-Functional Aspects (for SRS)

- **Security:** JWT, bcrypt for passwords, CORS configuration, optional RLS in DB  
- **Scalability:** Async backend (FastAPI/Uvicorn), optional Redis, DB indexing and full-text search  
- **Usability:** Animated UI (Framer Motion), responsive layout, Tailwind-based design  
- **Integrability:** REST API, optional WebSockets/SSE for real-time updates  
- **Maintainability:** Structured app (api, core, models, schemas, services), TypeScript frontend, SQL schema and migrations (Alembic)  

---

## 4. Architecture (High-Level)

- **Frontend:** Next.js 14 (React) → talks to Backend API (CORS allowed origins include localhost:3002, 3000).  
- **Backend:** FastAPI app → business logic in `app/services/`, REST in `app/api/`, models/schemas in `app/models/`, `app/schemas/`.  
- **Database:** PostgreSQL (or SQLite in dev) via SQLAlchemy; schema and functions (e.g. sentiment trend, topic frequency) in `database/schemas/init.sql`.  
- **AI:** Used in services (e.g. analytics, report generation); config supports OpenAI, Anthropic, Google API keys.  
- **Optional:** Redis for caching/background jobs; Docker Compose for DB (and Redis).  

**Data flow (conceptual):**  
Social/APIs or demo data → Backend collection → DB (e.g. `social_posts`, `analytics_data`) → AI processing (sentiment, topics) → Analytics/Reports API → Frontend dashboard and reports; email for scheduled reports.

---

## 5. API Modules and Key Endpoints (for SRS)

| Module           | Prefix                     | Example Endpoints (summary) |
|------------------|----------------------------|-----------------------------|
| Authentication   | `/api/auth`                | POST login, register; GET me; POST refresh-token |
| Users            | `/api/users`               | GET/PUT profile; PUT social-profiles; DELETE social-profiles |
| Analytics        | `/api/analytics`           | GET dashboard, sentiment-analysis, topic-analysis; POST analyze-post; GET charts/* (engagement-trends, sentiment-distribution, platform-comparison, topic-frequency, engagement-correlation, performance-overview, config) |
| Reports          | `/api/reports`             | POST generate, GET list, GET by id, GET download, DELETE; POST personal-social-analysis, schedule-daily |
| Social Data      | `/api/social-data`        | GET posts, GET post by id; POST collect, analyze-batch; GET stats; GET monitoring/status; POST monitoring/keywords, monitoring/platforms |
| Social Accounts  | `/api/social-accounts`     | GET/POST/PUT/DELETE accounts; POST verify; GET/POST/PUT/DELETE posts (scheduled); POST post-now |
| Datasets         | `/api/datasets` (optional) | Kaggle status, setup, search, download, sample-data (can be disabled in main app) |

**Root:** GET `/` (API info), GET `/health` (health check).

---

## 6. Database Entities (for SRS / Data Model)

- **users** – Accounts, auth, plan, social profile links, avatar, last_login.  
- **user_plans** – Plan name, price, features (JSONB), limits (JSONB).  
- **social_posts** – user_id, platform, post_id, content, author, url, posted_at, engagement (likes, shares, comments, views), sentiment, sentiment_score, topics, entities, language, search_vector (full-text).  
- **analytics_data** – user_id, date, counts, sentiment distribution, platform_stats (JSONB), engagement, top_topics, trending_keywords.  
- **reports** – user_id, title, report_type, date range, summary, insights, recommendations, data_snapshot, status, sent_at, search_vector.  
- **notification_settings** – user_id, email_reports, real_time_alerts, thresholds, keywords (JSONB), report_frequency, timezone.  

**Notable DB features:** Full-text search (tsvector), JSONB for flexible payloads, indexes on user_id, platform, dates, sentiment; optional RLS commented in schema.

---

## 7. User Roles / Subscription Plans (for SRS)

- **Free:** e.g. 5 social accounts, basic sentiment, weekly reports, community support (limits in `user_plans`).  
- **Pro:** e.g. 25 accounts, advanced NLP, daily AI reports, priority support, real-time alerts, custom dashboards.  
- **Enterprise:** e.g. unlimited accounts, enterprise NLP, 24/7 support, custom integrations, multi-user access.  

Exact limits and feature lists are defined in `database/schemas/init.sql` (user_plans table).

---

## 8. Configuration and Deployment (for SRS)

- **Backend env:** `DATABASE_URL`, `SECRET_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, SMTP_*, `TWITTER_BEARER_TOKEN`, `LINKEDIN_ACCESS_TOKEN`, `REDIS_URL`, `DEBUG`, etc.  
- **Frontend env:** `NEXT_PUBLIC_API_URL` (e.g. http://localhost:8000), `NEXT_PUBLIC_APP_ENV`.  
- **Run:** Database via Docker Compose; backend: `python -m app.main` (port 8000); frontend: `npm run dev` (port 3002).  
- **Docs:** API docs at `http://localhost:8000/docs` when backend is running.

---

## 9. Project Structure (for SRS / Documentation)

```
team/
├── analytics/              # R Markdown reports (e.g. social_media_intelligence.rmd)
├── frontend/               # Next.js app
│   └── src/
│       ├── app/            # App Router: dashboard, analytics, charts, reports, settings, social-data, login
│       ├── components/     # UI (navbar, live-demo, ui primitives)
│       ├── lib/            # Utils
│       ├── styles/         # globals.css
│       └── types/
├── backend/
│   └── app/
│       ├── api/            # auth, users, analytics, reports, social_data, social_accounts, (datasets, realtime)
│       ├── core/           # config, database
│       ├── models/         # user, social_data
│       ├── schemas/        # Pydantic schemas
│       ├── services/       # ai_analytics, auth, email, kaggle, social_collector, social_poster, scheduler, etc.
│       ├── main.py, main_demo.py
│       └── demo_social_data.py
├── database/
│   ├── schemas/init.sql    # Full schema + functions
│   ├── setup_db.py
│   └── docker-compose.yml
├── README.md
├── start.sh, start_frontend.sh
├── test_app.py, test_integration.py
└── PROJECT_SUMMARY_SRS.md  (this file)
```

---

## 10. Use Cases (for SRS)

1. **User:** Register/Login → access dashboard and analytics.  
2. **Analyst:** View sentiment and topic analysis, run ad-hoc post analysis, export charts/reports.  
3. **Operations:** Configure social accounts and monitoring keywords/platforms; trigger collection and batch analysis.  
4. **Manager:** Generate one-off or scheduled AI reports; receive daily/weekly/monthly email reports.  
5. **Admin:** Manage users, plans, and (if enabled) datasets (e.g. Kaggle) and real-time features.

---

## 11. Optional / Future (from README and Code)

- Datasets API and real-time API are present but can be disabled in `main.py`.  
- Vector/semantic search, Alembic migrations in production, Redis for background jobs.  
- Row Level Security (RLS) and advanced multi-tenant isolation (schema prepared, policies commented).

---

You can copy sections from this file directly into your SRS (e.g. Introduction, System Features, Technology Stack, Architecture, Data Model, User Roles, Configuration, Appendices). Adjust wording and depth as required by your SRS template.
