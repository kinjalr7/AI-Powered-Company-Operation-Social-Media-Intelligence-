from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from sqlalchemy import select, and_, desc
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.services.auth import verify_token, get_user_by_email
from app.services.social_poster import SocialPosterService
from app.models.social_data import SocialAccount, PostSchedule
from app.schemas.social_data import (
    SocialAccount as SocialAccountSchema,
    SocialAccountCreate,
    SocialAccountUpdate,
    PostSchedule as PostScheduleSchema,
    PostScheduleCreate,
    PostScheduleUpdate
)

router = APIRouter()
security = HTTPBearer()
social_poster = SocialPosterService()

async def get_current_user(
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

@router.get("/accounts", response_model=List[SocialAccountSchema])
async def get_social_accounts(
    platform: Optional[str] = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Get user's connected social media accounts"""
    try:
        query = select(SocialAccount).where(SocialAccount.user_id == current_user.id)

        if platform:
            query = query.where(SocialAccount.platform == platform)

        result = db.execute(query.order_by(desc(SocialAccount.created_at)))
        accounts = result.scalars().all()

        return accounts

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch social accounts: {str(e)}")

@router.post("/accounts", response_model=SocialAccountSchema)
async def create_social_account(
    account_data: SocialAccountCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Add a new social media account"""
    try:
        # Validate platform
        valid_platforms = ["twitter", "instagram", "facebook", "linkedin", "youtube", "tiktok"]
        if account_data.platform not in valid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Supported platforms: {', '.join(valid_platforms)}"
            )

        # Check if account already exists for this platform
        existing = db.execute(

            select(SocialAccount).where(
                and_(
                    SocialAccount.user_id == current_user.id,
                    SocialAccount.platform == account_data.platform
                )
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"Account already exists for platform: {account_data.platform}"
            )

        # Create social account
        db_account = SocialAccount(
            user_id=current_user.id,
            platform=account_data.platform,
            username=account_data.username,
            display_name=account_data.display_name,
            profile_url=account_data.profile_url,
            avatar_url=account_data.avatar_url,
            access_token=account_data.access_token,
            refresh_token=account_data.refresh_token,
            token_expires_at=account_data.token_expires_at,
            is_active=account_data.is_active
        )

        db.add(db_account)
        db.commit()

        db.refresh(
db_account)

        return db_account

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=500, detail=f"Failed to create social account: {str(e)}")

@router.get("/accounts/{account_id}", response_model=SocialAccountSchema)
async def get_social_account(
    account_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Get a specific social account"""
    try:
        result = db.execute(

            select(SocialAccount).where(
                and_(
                    SocialAccount.id == account_id,
                    SocialAccount.user_id == current_user.id
                )
            )
        )
        account = result.scalar_one_or_none()

        if not account:
            raise HTTPException(status_code=404, detail="Social account not found")

        return account

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch social account: {str(e)}")

@router.put("/accounts/{account_id}", response_model=SocialAccountSchema)
async def update_social_account(
    account_id: int,
    account_data: SocialAccountUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Update a social account"""
    try:
        result = db.execute(

            select(SocialAccount).where(
                and_(
                    SocialAccount.id == account_id,
                    SocialAccount.user_id == current_user.id
                )
            )
        )
        account = result.scalar_one_or_none()

        if not account:
            raise HTTPException(status_code=404, detail="Social account not found")

        # Update fields
        for field, value in account_data.dict(exclude_unset=True).items():
            setattr(account, field, value)

        account.updated_at = datetime.utcnow()

        db.commit()

        db.refresh(
account)

        return account

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=500, detail=f"Failed to update social account: {str(e)}")

@router.delete("/accounts/{account_id}")
async def delete_social_account(
    account_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Delete a social account"""
    try:
        result = db.execute(

            select(SocialAccount).where(
                and_(
                    SocialAccount.id == account_id,
                    SocialAccount.user_id == current_user.id
                )
            )
        )
        account = result.scalar_one_or_none()

        if not account:
            raise HTTPException(status_code=404, detail="Social account not found")

        db.delete(
account)
        db.commit()


        return {"message": "Social account deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=500, detail=f"Failed to delete social account: {str(e)}")

@router.post("/accounts/{account_id}/verify")
async def verify_social_account(
    account_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Verify connection to a social account"""
    try:
        result = db.execute(

            select(SocialAccount).where(
                and_(
                    SocialAccount.id == account_id,
                    SocialAccount.user_id == current_user.id
                )
            )
        )
        account = result.scalar_one_or_none()

        if not account:
            raise HTTPException(status_code=404, detail="Social account not found")

        # Attempt to verify the account connection
        verification_result = await social_poster.verify_account(account)

        # Update account status
        account.is_verified = verification_result['verified']
        if verification_result['verified']:
            account.follower_count = verification_result.get('follower_count', 0)
            account.following_count = verification_result.get('following_count', 0)
            account.account_id = verification_result.get('account_id')
            account.display_name = verification_result.get('display_name')
            account.username = verification_result.get('username')
            account.avatar_url = verification_result.get('avatar_url')

        account.updated_at = datetime.utcnow()

        db.commit()

        db.refresh(
account)

        return {
            "verified": verification_result['verified'],
            "message": verification_result['message'],
            "account_info": {
                "follower_count": account.follower_count,
                "following_count": account.following_count,
                "display_name": account.display_name,
                "username": account.username
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=500, detail=f"Account verification failed: {str(e)}")

# Post scheduling endpoints
@router.get("/posts/scheduled", response_model=List[PostScheduleSchema])
async def get_scheduled_posts(
    account_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 50,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Get scheduled posts"""
    try:
        query = select(PostSchedule).where(PostSchedule.user_id == current_user.id)

        if account_id:
            query = query.where(PostSchedule.social_account_id == account_id)

        if status:
            query = query.where(PostSchedule.status == status)

        result = db.execute(

            query.order_by(desc(PostSchedule.scheduled_at)).limit(limit)
        )
        posts = result.scalars().all()

        return posts

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch scheduled posts: {str(e)}")

@router.post("/posts/schedule", response_model=PostScheduleSchema)
async def schedule_post(
    post_data: PostScheduleCreate,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Schedule a post for a social account"""
    try:
        # Verify the social account belongs to the user
        account_result = db.execute(

            select(SocialAccount).where(
                and_(
                    SocialAccount.id == post_data.social_account_id,
                    SocialAccount.user_id == current_user.id,
                    SocialAccount.is_active == True
                )
            )
        )
        account = account_result.scalar_one_or_none()

        if not account:
            raise HTTPException(status_code=404, detail="Social account not found or inactive")

        # Create scheduled post
        db_post = PostSchedule(
            user_id=current_user.id,
            social_account_id=post_data.social_account_id,
            content=post_data.content,
            media_urls=post_data.media_urls,
            post_type=post_data.post_type,
            scheduled_at=post_data.scheduled_at,
            timezone=post_data.timezone
        )

        db.add(db_post)
        db.commit()

        db.refresh(
db_post)

        # Schedule the posting task
        background_tasks.add_task(
            schedule_posting_task,
            db_post.id,
            post_data.scheduled_at
        )

        return db_post

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=500, detail=f"Failed to schedule post: {str(e)}")

@router.put("/posts/{post_id}", response_model=PostScheduleSchema)
async def update_scheduled_post(
    post_id: int,
    post_data: PostScheduleUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Update a scheduled post"""
    try:
        result = db.execute(

            select(PostSchedule).where(
                and_(
                    PostSchedule.id == post_id,
                    PostSchedule.user_id == current_user.id
                )
            )
        )
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Scheduled post not found")

        # Update fields
        for field, value in post_data.dict(exclude_unset=True).items():
            setattr(post, field, value)

        post.updated_at = datetime.utcnow()

        db.commit()

        db.refresh(
post)

        return post

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=500, detail=f"Failed to update scheduled post: {str(e)}")

@router.delete("/posts/{post_id}")
async def delete_scheduled_post(
    post_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    """Delete a scheduled post"""
    try:
        result = db.execute(

            select(PostSchedule).where(
                and_(
                    PostSchedule.id == post_id,
                    PostSchedule.user_id == current_user.id
                )
            )
        )
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Scheduled post not found")

        db.delete(
post)
        db.commit()


        return {"message": "Scheduled post deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=500, detail=f"Failed to delete scheduled post: {str(e)}")

@router.post("/posts/{post_id}/post-now")
async def post_now(
    post_id: int,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Post a scheduled post immediately"""
    try:
        result = db.execute(

            select(PostSchedule).where(
                and_(
                    PostSchedule.id == post_id,
                    PostSchedule.user_id == current_user.id
                )
            )
        )
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Scheduled post not found")

        # Post immediately
        background_tasks.add_task(post_scheduled_content, post.id)

        return {"message": "Post queued for immediate publishing"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to queue post: {str(e)}")

# Background tasks
async def schedule_posting_task(post_id: int, scheduled_time: datetime):
    """Schedule a posting task"""
    try:
        # Calculate delay until posting time
        now = datetime.utcnow()
        if scheduled_time > now:
            delay = (scheduled_time - now).total_seconds()
            # In a real implementation, you'd use a proper scheduler
            # For now, we'll just mark it as scheduled
            print(f"Post {post_id} scheduled for {scheduled_time}")

    except Exception as e:
        print(f"Failed to schedule posting task: {e}")

async def post_scheduled_content(post_id: int):
    """Post scheduled content to social media"""
    try:
        # Get database session
        from app.core.database import get_db_sync
        db = next(get_db_sync())

        try:
            # Get the post
            from sqlalchemy import select
            result = db.execute(
select(PostSchedule).where(PostSchedule.id == post_id))
            post = result.scalar_one_or_none()

            if not post:
                print(f"Post {post_id} not found")
                return

            # Get the social account
            account_result = db.execute(

                select(SocialAccount).where(SocialAccount.id == post.social_account_id)
            )
            account = account_result.scalar_one_or_none()

            if not account:
                print(f"Account {post.social_account_id} not found")
                return

            # Post the content
            post_result = await social_poster.post_content(
                account=account,
                content=post.content,
                media_urls=post.media_urls,
                post_type=post.post_type
            )

            # Update post status
            post.status = "posted" if post_result['success'] else "failed"
            post.posted_at = datetime.utcnow()
            post.platform_post_id = post_result.get('post_id')
            post.updated_at = datetime.utcnow()

            db.commit()


            print(f"Posted content for post {post_id}: {post_result}")

        finally:
            db.close()

    except Exception as e:
        print(f"Failed to post scheduled content: {e}")