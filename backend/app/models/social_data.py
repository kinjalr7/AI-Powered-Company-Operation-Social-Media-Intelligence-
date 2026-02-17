from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import User

class SocialPost(Base):
    __tablename__ = "social_posts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # twitter, linkedin, facebook, instagram
    post_id = Column(String, unique=True, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String)
    author_id = Column(String)
    url = Column(String)
    posted_at = Column(DateTime(timezone=True), nullable=False)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())

    # Engagement metrics
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    views = Column(Integer, default=0)

    # AI Analysis
    sentiment = Column(String)  # positive, negative, neutral
    sentiment_score = Column(Float)
    topics = Column(JSON)  # Array of topics/tags
    entities = Column(JSON)  # Named entities
    language = Column(String, default="en")

    # Metadata
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User)

class AnalyticsData(Base):
    __tablename__ = "analytics_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)

    # Aggregated metrics
    total_posts = Column(Integer, default=0)
    sentiment_positive = Column(Float, default=0)
    sentiment_negative = Column(Float, default=0)
    sentiment_neutral = Column(Float, default=0)

    # Platform breakdown (JSON)
    platform_stats = Column(JSON)

    # Engagement metrics
    total_engagement = Column(Integer, default=0)
    avg_engagement = Column(Float, default=0)

    # Topics and keywords
    top_topics = Column(JSON)
    trending_keywords = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    report_type = Column(String, nullable=False)  # daily, weekly, monthly
    date_range_start = Column(DateTime(timezone=True))
    date_range_end = Column(DateTime(timezone=True))
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Report content
    summary = Column(Text)
    insights = Column(JSON)  # Array of insights
    recommendations = Column(JSON)  # Array of recommendations
    data_snapshot = Column(JSON)  # Snapshot of analytics data

    # Status
    status = Column(String, default="generated")  # generated, sent, failed
    sent_at = Column(DateTime(timezone=True))

class NotificationSettings(Base):
    __tablename__ = "notification_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Email settings
    email_reports = Column(Boolean, default=True)
    real_time_alerts = Column(Boolean, default=False)

    # Alert thresholds
    sentiment_threshold = Column(Float, default=0.7)  # Alert when sentiment drops below
    engagement_threshold = Column(Integer, default=1000)

    # Keywords to monitor
    keywords = Column(JSON)  # Array of keywords

    # Schedule
    report_frequency = Column(String, default="daily")  # daily, weekly, monthly
    timezone = Column(String, default="UTC")