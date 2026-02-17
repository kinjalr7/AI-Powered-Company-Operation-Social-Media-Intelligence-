from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class SocialProfiles(BaseModel):
    twitter_handle: Optional[str] = None
    linkedin_profile: Optional[str] = None
    facebook_profile: Optional[str] = None
    instagram_handle: Optional[str] = None
    youtube_channel: Optional[str] = None
    tiktok_handle: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    plan: str = "free"
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    plan: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None
    social_profiles: Optional[SocialProfiles] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    social_profiles: Optional[SocialProfiles] = None

    class Config:
        from_attributes = True

class UserPlan(BaseModel):
    id: int
    name: str
    price: float
    features: List[str]
    limits: dict

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None