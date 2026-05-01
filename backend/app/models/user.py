from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    plan = Column(String, default="free")  # free, pro, enterprise
    avatar_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Social media profiles
    twitter_handle = Column(String)
    linkedin_profile = Column(String)
    facebook_profile = Column(String)
    instagram_handle = Column(String)
    youtube_channel = Column(String)
    tiktok_handle = Column(String)

class UserPlan(Base):
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    features = Column(Text)  # JSON string
    limits = Column(Text)    # JSON string
    is_active = Column(Boolean, default=True)