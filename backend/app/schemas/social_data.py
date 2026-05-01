from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums for validation
class PlatformEnum(str, Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"

class SourceEnum(str, Enum):
    DUMMY = "dummy"
    REAL = "real"

class SentimentEnum(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

# SocialPost Schemas
class SocialPostCreate(BaseModel):
    """Schema for creating a new social post"""
    user_id: int
    platform: PlatformEnum
    content: str
    posted_at: datetime
    likes: int = 0
    comments: int = 0
    shares: int = 0
    reach: int = 0
    post_url: Optional[str] = None
    source: SourceEnum = SourceEnum.DUMMY
    raw_url: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[SentimentEnum] = None
    topics: Optional[List[str]] = None
    summary: Optional[str] = None
    
    @field_validator('sentiment_score')
    @classmethod
    def validate_sentiment_score(cls, v):
        if v is not None and not (-1.0 <= v <= 1.0):
            raise ValueError('sentiment_score must be between -1.0 and 1.0')
        return v

class SocialPostResponse(BaseModel):
    """Schema for returning social post data"""
    id: int
    user_id: int
    platform: str
    content: str
    posted_at: datetime
    likes: int
    comments: int
    shares: int
    reach: int
    post_url: Optional[str] = None
    source: str
    raw_url: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    topics: Optional[List[str]] = None
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Legacy schemas (kept for backward compatibility)
class SocialPostBase(BaseModel):
    platform: str
    content: str
    author: Optional[str] = None
    url: Optional[str] = None
    posted_at: datetime

class SocialPostLegacy(SocialPostBase):
    id: int
    post_id: str
    author_id: Optional[str] = None
    collected_at: datetime
    likes: int
    shares: int
    comments: int
    views: int
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    topics: Optional[List[str]] = None
    entities: Optional[Dict[str, Any]] = None
    language: str = "en"

    class Config:
        from_attributes = True

class AnalyticsData(BaseModel):
    date: datetime
    total_posts: int
    sentiment_positive: float
    sentiment_negative: float
    sentiment_neutral: float
    platform_stats: Dict[str, Any]
    total_engagement: int
    avg_engagement: float
    top_topics: List[Dict[str, Any]]
    trending_keywords: List[Dict[str, Any]]

    class Config:
        from_attributes = True

class ReportBase(BaseModel):
    title: str
    report_type: str

class ReportCreate(ReportBase):
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None

class Report(ReportBase):
    id: int
    user_id: int
    date_range_start: Optional[datetime]
    date_range_end: Optional[datetime]
    generated_at: datetime
    summary: Optional[str]
    insights: List[str]
    recommendations: List[str]
    data_snapshot: Dict[str, Any]
    status: str
    sent_at: Optional[datetime]

    class Config:
        from_attributes = True

class NotificationSettingsBase(BaseModel):
    email_reports: bool = True
    real_time_alerts: bool = False
    sentiment_threshold: float = 0.7
    engagement_threshold: int = 1000
    keywords: List[str] = []
    report_frequency: str = "daily"
    timezone: str = "UTC"

class NotificationSettings(NotificationSettingsBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class NotificationSettingsUpdate(BaseModel):
    email_reports: Optional[bool] = None
    real_time_alerts: Optional[bool] = None
    sentiment_threshold: Optional[float] = None
    engagement_threshold: Optional[int] = None
    keywords: Optional[List[str]] = None
    report_frequency: Optional[str] = None
    timezone: Optional[str] = None