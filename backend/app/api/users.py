from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.core.database import get_db
from app.services.auth import verify_token, get_user_by_email
from app.schemas.user import User, UserUpdate, SocialProfiles
from app.models.user import User as UserModel

router = APIRouter()
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

@router.get("/profile", response_model=User)
def get_user_profile(current_user = Depends(get_current_user)):
    """Get current user's profile including social media profiles"""
    return current_user

@router.put("/profile", response_model=User)
def update_user_profile(
    profile_data: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile including social media profiles"""
    try:
        update_data = profile_data.dict(exclude_unset=True)

        # Handle social profiles separately
        if 'social_profiles' in update_data:
            social_profiles = update_data.pop('social_profiles')
            if social_profiles:
                for field, value in social_profiles.items():
                    if value is not None:
                        update_data[field] = value

        if update_data:
            db.execute(
                update(UserModel)
                .where(UserModel.id == current_user.id)
                .values(**update_data)
            )
            db.commit()

            # Refresh the user data
            updated_user = get_user_by_email(db, current_user.email)
            return updated_user

        return current_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")

@router.put("/social-profiles", response_model=User)
def update_social_profiles(
    social_profiles: SocialProfiles,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's social media profiles"""
    try:
        update_data = {}

        # Map social profiles to database fields
        profile_mapping = {
            'twitter_handle': social_profiles.twitter_handle,
            'linkedin_profile': social_profiles.linkedin_profile,
            'facebook_profile': social_profiles.facebook_profile,
            'instagram_handle': social_profiles.instagram_handle,
            'youtube_channel': social_profiles.youtube_channel,
            'tiktok_handle': social_profiles.tiktok_handle,
        }

        for field, value in profile_mapping.items():
            if value is not None:
                update_data[field] = value

        if update_data:
            db.execute(
                update(UserModel)
                .where(UserModel.id == current_user.id)
                .values(**update_data)
            )
            db.commit()

            # Refresh the user data
            updated_user = get_user_by_email(db, current_user.email)
            return updated_user

        return current_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update social profiles: {str(e)}")

@router.delete("/social-profiles")
def clear_social_profiles(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all social media profiles for the current user"""
    try:
        db.execute(
            update(UserModel)
            .where(UserModel.id == current_user.id)
            .values(
                twitter_handle=None,
                linkedin_profile=None,
                facebook_profile=None,
                instagram_handle=None,
                youtube_channel=None,
                tiktok_handle=None
            )
        )
        db.commit()

        return {"message": "Social profiles cleared successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear social profiles: {str(e)}")