from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.services.auth import verify_token, get_user_by_email
from app.services.ai_analytics import AIAnalyticsService
from app.services.social_collector import SocialDataCollector
from app.models.social_data import SocialPost, AnalyticsData
from app.schemas.social_data import SocialPost as SocialPostSchema, SocialPostCreate

router = APIRouter()
security = HTTPBearer()
ai_service = AIAnalyticsService()
social_collector = SocialDataCollector()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

@router.get("/posts", response_model=List[SocialPostSchema])
async def get_social_posts(
    platform: Optional[str] = None,
    sentiment: Optional[str] = None,
    limit: int = Query(50, description="Number of posts to return"),
    offset: int = Query(0, description="Offset for pagination"),
    days: int = Query(30, description="Number of days to look back"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get social media posts with filtering options"""
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Build query
        query = select(SocialPost).where(
            and_(
                SocialPost.user_id == current_user.id,
                SocialPost.posted_at >= start_date,
                SocialPost.posted_at <= end_date
            )
        )

        if platform:
            query = query.where(SocialPost.platform == platform)

        if sentiment:
            query = query.where(SocialPost.sentiment == sentiment)

        result = await db.execute(
            query.order_by(desc(SocialPost.posted_at))
            .offset(offset)
            .limit(limit)
        )
        posts = result.scalars().all()

        return posts

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch posts: {str(e)}")

@router.get("/posts/{post_id}", response_model=SocialPostSchema)
async def get_social_post(
    post_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific social media post"""
    try:
        result = await db.execute(
            select(SocialPost).where(
                and_(
                    SocialPost.post_id == post_id,
                    SocialPost.user_id == current_user.id
                )
            )
        )
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return post

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch post: {str(e)}")

@router.post("/collect", response_model=dict)
async def collect_social_data(
    background_tasks: BackgroundTasks,
    platforms: List[str] = Query(["twitter", "linkedin"], description="Platforms to collect from"),
    keywords: Optional[List[str]] = Query(None, description="Keywords to search for"),
    days_back: int = Query(7, description="Days to look back for historical data"),
    current_user = Depends(get_current_user)
):
    """Trigger social media data collection"""
    try:
        # Add background task for data collection
        background_tasks.add_task(
            collect_social_data_background,
            current_user.id,
            platforms,
            keywords or ["AI", "machine learning", "technology"],
            days_back
        )

        return {
            "message": "Data collection started",
            "platforms": platforms,
            "keywords": keywords or ["AI", "machine learning", "technology"],
            "status": "processing"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data collection failed: {str(e)}")

@router.get("/stats", response_model=dict)
async def get_social_data_stats(
    days: int = Query(30, description="Number of days to analyze"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get statistics about collected social data"""
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Get post counts by platform
        platform_stats_result = await db.execute(
            select(
                SocialPost.platform,
                func.count(SocialPost.id).label('count'),
                func.avg(SocialPost.likes + SocialPost.shares + SocialPost.comments).label('avg_engagement')
            ).where(
                and_(
                    SocialPost.user_id == current_user.id,
                    SocialPost.posted_at >= start_date,
                    SocialPost.posted_at <= end_date
                )
            ).group_by(SocialPost.platform)
        )

        platform_stats = {}
        for row in platform_stats_result:
            platform_stats[row.platform] = {
                'count': row.count,
                'avg_engagement': float(row.avg_engagement or 0)
            }

        # Get sentiment distribution
        sentiment_stats_result = await db.execute(
            select(
                SocialPost.sentiment,
                func.count(SocialPost.id).label('count')
            ).where(
                and_(
                    SocialPost.user_id == current_user.id,
                    SocialPost.posted_at >= start_date,
                    SocialPost.posted_at <= end_date,
                    SocialPost.sentiment.isnot(None)
                )
            ).group_by(SocialPost.sentiment)
        )

        sentiment_stats = {}
        for row in sentiment_stats_result:
            sentiment_stats[row.sentiment] = row.count

        # Get total counts
        total_result = await db.execute(
            select(func.count(SocialPost.id)).where(
                and_(
                    SocialPost.user_id == current_user.id,
                    SocialPost.posted_at >= start_date,
                    SocialPost.posted_at <= end_date
                )
            )
        )
        total_posts = total_result.scalar()

        return {
            'period': f"{days} days",
            'total_posts': total_posts,
            'platform_stats': platform_stats,
            'sentiment_stats': sentiment_stats,
            'data_freshness': 'current'
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@router.post("/analyze-batch")
async def analyze_posts_batch(
    background_tasks: BackgroundTasks,
    post_ids: Optional[List[str]] = None,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Trigger batch analysis of social posts"""
    try:
        background_tasks.add_task(
            analyze_posts_background,
            current_user.id,
            post_ids
        )

        return {
            "message": "Batch analysis started",
            "status": "processing"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

# Background tasks
async def collect_social_data_background(
    user_id: int,
    platforms: List[str],
    keywords: List[str],
    days_back: int
):
    """Background task for collecting social data"""
    try:
        # This would integrate with actual social media APIs
        # For demo purposes, we'll simulate data collection
        print(f"Collecting data for user {user_id} from platforms: {platforms}")

        # In a real implementation, this would:
        # 1. Connect to social media APIs (Twitter, LinkedIn, etc.)
        # 2. Search for keywords
        # 3. Collect posts and metadata
        # 4. Store in database with AI analysis

    except Exception as e:
        print(f"Background data collection failed: {e}")

async def analyze_posts_background(user_id: int, post_ids: Optional[List[str]] = None):
    """Background task for analyzing posts"""
    try:
        # This would analyze posts that don't have sentiment/topics yet
        print(f"Analyzing posts for user {user_id}")

        # In a real implementation, this would:
        # 1. Fetch posts without analysis
        # 2. Run AI analysis (sentiment, topics, etc.)
        # 3. Update database with results

    except Exception as e:
        print(f"Background post analysis failed: {e}")

@router.get("/monitoring/status")
async def get_monitoring_status(current_user = Depends(get_current_user)):
    """Get the status of social media monitoring"""
    return {
        "monitoring_active": True,  # This would check actual monitoring status
        "last_collection": datetime.utcnow() - timedelta(hours=2),  # Mock last collection time
        "platforms_monitored": ["twitter", "linkedin", "facebook", "instagram"],
        "keywords_tracked": ["AI", "machine learning", "technology", "business intelligence"],
        "total_posts_collected": 15432  # Mock number
    }

@router.post("/monitoring/keywords")
async def update_monitoring_keywords(
    keywords: List[str],
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update keywords to monitor"""
    try:
        # In a real implementation, this would update user settings
        # For now, just return success
        return {
            "message": "Monitoring keywords updated",
            "keywords": keywords,
            "platforms": ["twitter", "linkedin", "facebook", "instagram"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update keywords: {str(e)}")

@router.post("/monitoring/platforms")
async def update_monitoring_platforms(
    platforms: List[str],
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update platforms to monitor"""
    try:
        valid_platforms = ["twitter", "linkedin", "facebook", "instagram"]
        invalid_platforms = [p for p in platforms if p not in valid_platforms]

        if invalid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platforms: {invalid_platforms}. Valid options: {valid_platforms}"
            )

        return {
            "message": "Monitoring platforms updated",
            "platforms": platforms
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update platforms: {str(e)}")

@router.post("/collect")
async def collect_social_data(
    keywords: List[str],
    platforms: List[str] = None,
    days_back: int = 7,
    background_tasks: BackgroundTasks = None,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Manually trigger social media data collection"""
    try:
        if platforms is None:
            platforms = ["twitter", "linkedin", "facebook", "instagram"]

        # Start background collection
        if background_tasks:
            background_tasks.add_task(
                collect_and_save_data,
                current_user.id,
                keywords,
                platforms,
                days_back
            )
            return {"message": "Data collection started in background"}
        else:
            # Synchronous collection for testing
            posts_data = await social_collector.collect_all_platforms(
                keywords=keywords,
                platforms=platforms,
                days_back=days_back,
                max_results_per_platform=50
            )

            saved_count = await social_collector.save_posts_to_database(
                posts_data, current_user.id, db
            )

            return {
                "collected_posts": len(posts_data),
                "saved_posts": saved_count
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data collection failed: {str(e)}")

# Background task function
async def collect_and_save_data(user_id: int, keywords: List[str], platforms: List[str], days_back: int):
    """Background task to collect and save social media data"""
    try:
        posts_data = await social_collector.collect_all_platforms(
            keywords=keywords,
            platforms=platforms,
            days_back=days_back,
            max_results_per_platform=50
        )

        # Get database session
        from app.core.database import get_db_sync
        db = next(get_db_sync())

        try:
            saved_count = await social_collector.save_posts_to_database(
                posts_data, user_id, db
            )
            print(f"Background collection complete: {saved_count} posts saved for user {user_id}")
        finally:
            db.close()

    except Exception as e:
        print(f"Background data collection failed: {e}")