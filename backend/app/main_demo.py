from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from datetime import datetime, timedelta
import random
import json

app = FastAPI(
    title="AI Social Intelligence Demo API",
    description="Demo version of AI-powered social media intelligence platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
def generate_mock_posts(count=50):
    platforms = ["twitter", "linkedin", "facebook", "instagram"]
    sentiments = ["positive", "negative", "neutral"]
    base_date = datetime.now() - timedelta(days=7)

    posts = []
    for i in range(count):
        post_date = base_date + timedelta(hours=i*2)
        sentiment = random.choice(sentiments)
        platform = random.choice(platforms)

        posts.append({
            "id": i + 1,
            "platform": platform,
            "content": f"Sample post {i+1} about AI and technology. This is a {'great' if sentiment == 'positive' else 'concerning' if sentiment == 'negative' else 'neutral'} development.",
            "author": f"User {i+1}",
            "posted_at": post_date.isoformat(),
            "likes": random.randint(10, 1000),
            "shares": random.randint(0, 100),
            "comments": random.randint(5, 200),
            "sentiment": sentiment,
            "engagement": random.randint(50, 1500)
        })

    return posts

def generate_mock_analytics():
    posts = generate_mock_posts(100)

    # Calculate sentiment distribution
    sentiments = {}
    for post in posts:
        sent = post["sentiment"]
        sentiments[sent] = sentiments.get(sent, 0) + 1

    # Platform breakdown
    platforms = {}
    for post in posts:
        plat = post["platform"]
        platforms[plat] = platforms.get(plat, 0) + 1

    # Generate trend data
    trend_data = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).date().isoformat()
        trend_data.append({
            "date": date,
            "engagement": random.randint(1000, 5000),
            "sentiment": random.uniform(0.3, 0.8)
        })

    return {
        "total_posts": len(posts),
        "sentiment_distribution": sentiments,
        "platform_breakdown": platforms,
        "total_engagement": sum(p["engagement"] for p in posts),
        "avg_engagement_per_post": sum(p["engagement"] for p in posts) / len(posts),
        "trend_data": trend_data,
        "top_topics": [
            {"topic": "AI", "frequency": 45, "sentiment_score": 0.7},
            {"topic": "Technology", "frequency": 38, "sentiment_score": 0.6},
            {"topic": "Innovation", "frequency": 32, "sentiment_score": 0.8},
            {"topic": "Business", "frequency": 28, "sentiment_score": 0.5},
            {"topic": "Future", "frequency": 25, "sentiment_score": 0.7}
        ]
    }

def generate_mock_report():
    analytics = generate_mock_analytics()

    return {
        "title": f"Weekly AI Social Intelligence Report - {datetime.now().strftime('%Y-%m-%d')}",
        "generated_at": datetime.now().isoformat(),
        "summary": "This week's social media analysis shows positive sentiment around AI developments with strong engagement across platforms.",
        "insights": [
            "AI-related content shows 65% positive sentiment",
            "Technology discussions are trending upward",
            "LinkedIn shows highest engagement rates",
            "Innovation topics resonate well with audiences"
        ],
        "recommendations": [
            "Focus content strategy on AI and technology topics",
            "Increase LinkedIn posting frequency",
            "Monitor sentiment for emerging tech discussions",
            "Engage with positive AI conversations"
        ],
        "data_snapshot": analytics
    }

# API Routes

@app.get("/")
async def root():
    return {
        "message": "AI Social Intelligence Demo API",
        "version": "1.0.0",
        "status": "running",
        "mode": "demo"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "demo"}

# Analytics endpoints
@app.get("/api/analytics/dashboard")
async def get_dashboard_analytics(days: int = 7):
    """Get dashboard analytics data"""
    analytics = generate_mock_analytics()

    # Filter by days if needed
    recent_posts = generate_mock_posts(20)

    return {
        "period": {"start_date": "2024-01-01", "end_date": datetime.now().isoformat(), "days": days},
        "insights": analytics,
        "analytics_history": analytics["trend_data"],
        "recent_posts": recent_posts[:10]
    }

@app.get("/api/analytics/sentiment-analysis")
async def get_sentiment_analysis(days: int = 30):
    """Get sentiment analysis data"""
    analytics = generate_mock_analytics()

    return {
        "period": f"{days} days",
        "total_posts": analytics["total_posts"],
        "daily_sentiment": [
            {
                "date": item["date"],
                "positive": random.randint(10, 50),
                "negative": random.randint(5, 20),
                "neutral": random.randint(15, 40),
                "total": random.randint(30, 100),
                "avg_score": item["sentiment"]
            }
            for item in analytics["trend_data"]
        ],
        "platform_breakdown": analytics["platform_breakdown"]
    }

@app.get("/api/analytics/topic-analysis")
async def get_topic_analysis(days: int = 30):
    """Get topic analysis data"""
    analytics = generate_mock_analytics()

    return {
        "period": f"{days} days",
        "total_posts_analyzed": analytics["total_posts"],
        "topics": analytics["top_topics"]
    }

@app.post("/api/analytics/analyze-post")
async def analyze_single_post(content: str):
    """Analyze a single post"""
    # Simple mock analysis
    sentiments = ["positive", "negative", "neutral"]
    sentiment = random.choice(sentiments)

    return {
        "content": content,
        "sentiment": sentiment,
        "confidence": random.uniform(0.6, 0.95),
        "topics": ["AI", "Technology", "Innovation"][:random.randint(1, 3)],
        "summary": f"This post expresses {sentiment} sentiment about technology.",
        "analyzed_at": datetime.now().isoformat()
    }

# Social data endpoints
@app.get("/api/social-data/posts")
async def get_social_posts(limit: int = 50, platform: str = None):
    """Get social media posts"""
    posts = generate_mock_posts(limit)

    if platform:
        posts = [p for p in posts if p["platform"] == platform]

    return posts[:limit]

@app.get("/api/social-data/stats")
async def get_social_data_stats(days: int = 30):
    """Get social data statistics"""
    analytics = generate_mock_analytics()

    return {
        "period": f"{days} days",
        "total_posts": analytics["total_posts"],
        "platform_stats": {
            platform: {
                "count": count,
                "avg_engagement": random.uniform(50, 200)
            }
            for platform, count in analytics["platform_breakdown"].items()
        },
        "sentiment_stats": analytics["sentiment_distribution"],
        "data_freshness": "demo"
    }

@app.post("/api/social-data/collect")
async def collect_social_data(platforms: list = ["twitter", "linkedin"]):
    """Trigger social data collection"""
    return {
        "message": "Demo data collection completed",
        "platforms": platforms,
        "posts_collected": random.randint(50, 200),
        "status": "completed"
    }

# Reports endpoints
@app.post("/api/reports/generate")
async def generate_report(title: str = "AI Social Intelligence Report", report_type: str = "weekly"):
    """Generate a report"""
    report = generate_mock_report()

    return {
        "id": random.randint(1000, 9999),
        "title": title,
        "report_type": report_type,
        "generated_at": datetime.now().isoformat(),
        "summary": report["summary"],
        "insights": report["insights"],
        "recommendations": report["recommendations"],
        "data_snapshot": report["data_snapshot"]
    }

@app.get("/api/reports")
async def get_reports(limit: int = 10):
    """Get reports list"""
    reports = []
    for i in range(min(limit, 5)):
        reports.append({
            "id": 1000 + i,
            "title": f"Report {i+1}",
            "report_type": "weekly",
            "generated_at": (datetime.now() - timedelta(days=i)).isoformat(),
            "summary": f"Weekly report {i+1} summary",
            "insights": ["Key insight 1", "Key insight 2"],
            "recommendations": ["Recommendation 1", "Recommendation 2"],
            "data_snapshot": generate_mock_analytics()
        })

    return reports

# Auth endpoints (mock)
@app.post("/api/auth/login")
async def login(email: str, password: str):
    """Mock login"""
    if email and password:  # Any credentials work in demo
        return {
            "access_token": "demo_token_" + str(random.randint(1000, 9999)),
            "token_type": "bearer"
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/auth/me")
async def get_current_user():
    """Get current user info"""
    return {
        "id": 1,
        "email": "demo@example.com",
        "full_name": "Demo User",
        "plan": "pro",
        "is_active": True
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print("🚀 Starting AI Social Intelligence Demo API")
    print(f"📡 Server will be available at: http://localhost:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print("🎯 Demo mode: Using mock data instead of real AI processing")

    uvicorn.run(
        "app.main_demo:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )