from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SocialPostBase(BaseModel):
    platform: str
    content: str
    author: Optional[str] = None
    url: Optional[str] = None
    posted_at: datetime

class SocialPostCreate(SocialPostBase):
    post_id: str
    author_id: Optional[str] = None
    likes: int = 0
    shares: int = 0
    comments: int = 0
    views: int = 0

class SocialPost(SocialPostBase):
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