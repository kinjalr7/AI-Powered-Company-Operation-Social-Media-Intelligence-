from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import User

class SocialPost(Base):
    __tablename__ = "social_posts"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User association
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship(User)
    
    # Platform and content
    platform = Column(String(20), nullable=False)  # twitter, linkedin, facebook, instagram, youtube, tiktok
    content = Column(Text, nullable=False)
    posted_at = Column(DateTime(timezone=True), nullable=False)
    
    # Engagement metrics
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    
    # URLs
    post_url = Column(String(500), nullable=True)
    raw_url = Column(String(500), nullable=True)  # stores original profile URL when source="real"
    
    # Source tracking
    source = Column(String(10), default="dummy")  # "dummy" or "real"
    
    # AI Analysis
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String(10), nullable=True)  # positive, negative, neutral
    topics = Column(JSON, nullable=True)  # Array of topics/tags
    summary = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Legacy fields (kept for backward compatibility)
    post_id = Column(String, unique=True, nullable=True)
    author = Column(String, nullable=True)
    author_id = Column(String, nullable=True)
    url = Column(String, nullable=True)
    collected_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    views = Column(Integer, default=0)
    sentiment = Column(String, nullable=True)  # positive, negative, neutral
    entities = Column(JSON, nullable=True)  # Named entities
    language = Column(String, default="en")

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