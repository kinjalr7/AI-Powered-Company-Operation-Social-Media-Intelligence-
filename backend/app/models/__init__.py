# Import all models to ensure they are registered with SQLAlchemy
from app.models.user import User, UserPlan
from app.models.social_data import (
    SocialPost,
    AnalyticsData,
    Report,
    NotificationSettings,
    SocialAccount,
    PostSchedule
)

# This ensures all models are loaded when the package is imported
__all__ = [
    "User",
    "UserPlan",
    "SocialPost",
    "AnalyticsData",
    "Report",
    "NotificationSettings",
    "SocialAccount",
    "PostSchedule"
]