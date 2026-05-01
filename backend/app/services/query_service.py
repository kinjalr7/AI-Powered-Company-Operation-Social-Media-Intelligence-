"""
Centralized query service for social posts data.
Single source of truth for all post-related queries across the application.
All modules must use these functions instead of writing their own queries.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.social_data import SocialPost


async def get_post_count(
    db: AsyncSession,
    user_id: int,
    platform: Optional[str] = None,
    days: Optional[int] = None
) -> int:
    """
    Get total count of posts for a user.
    
    Args:
        db: Database session
        user_id: User ID to filter by
        platform: Optional platform filter (e.g., 'twitter', 'linkedin')
        days: Optional number of days to look back (default: all time)
    
    Returns:
        Total count of posts matching criteria
    """
    query = select(func.count(SocialPost.id)).where(
        SocialPost.user_id == user_id
    )
    
    if platform:
        query = query.where(SocialPost.platform == platform)
    
    if days:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        query = query.where(
            and_(
                SocialPost.posted_at >= start_date,
                SocialPost.posted_at <= end_date
            )
        )
    
    result = await db.execute(query)
    return result.scalar() or 0


async def get_sentiment_distribution(
    db: AsyncSession,
    user_id: int,
    platform: Optional[str] = None,
    days: Optional[int] = None
) -> Dict[str, int]:
    """
    Get sentiment distribution (positive, negative, neutral counts) for a user.
    Queries directly from social_posts table.
    
    Args:
        db: Database session
        user_id: User ID to filter by
        platform: Optional platform filter
        days: Optional number of days to look back
    
    Returns:
        Dictionary with sentiment counts: {'positive': int, 'negative': int, 'neutral': int}
    """
    query = select(
        SocialPost.sentiment_label,
        func.count(SocialPost.id).label('count')
    ).where(
        and_(
            SocialPost.user_id == user_id,
            SocialPost.sentiment_label.isnot(None)
        )
    ).group_by(SocialPost.sentiment_label)
    
    if platform:
        query = query.where(SocialPost.platform == platform)
    
    if days:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        query = query.where(
            and_(
                SocialPost.posted_at >= start_date,
                SocialPost.posted_at <= end_date
            )
        )
    
    result = await db.execute(query)
    rows = result.all()
    
    # Initialize with zeros
    distribution = {
        'positive': 0,
        'negative': 0,
        'neutral': 0
    }
    
    # Populate from query results
    for row in rows:
        sentiment_label = row[0]
        count = row[1]
        if sentiment_label in distribution:
            distribution[sentiment_label] = count
    
    return distribution


async def get_recent_posts(
    db: AsyncSession,
    user_id: int,
    limit: int = 20,
    platform: Optional[str] = None,
    days: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Get recent posts for a user with all relevant data.
    
    Args:
        db: Database session
        user_id: User ID to filter by
        limit: Maximum number of posts to return (default: 20)
        platform: Optional platform filter
        days: Optional number of days to look back
    
    Returns:
        List of post dictionaries with all relevant fields
    """
    query = select(SocialPost).where(
        SocialPost.user_id == user_id
    )
    
    if platform:
        query = query.where(SocialPost.platform == platform)
    
    if days:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        query = query.where(
            and_(
                SocialPost.posted_at >= start_date,
                SocialPost.posted_at <= end_date
            )
        )
    
    result = await db.execute(
        query.order_by(SocialPost.posted_at.desc()).limit(limit)
    )
    posts = result.scalars().all()
    
    # Convert to dictionaries
    return [
        {
            'id': post.id,
            'user_id': post.user_id,
            'platform': post.platform,
            'content': post.content,
            'posted_at': post.posted_at.isoformat() if post.posted_at else None,
            'likes': post.likes or 0,
            'comments': post.comments or 0,
            'shares': post.shares or 0,
            'reach': post.reach or 0,
            'sentiment_score': post.sentiment_score,
            'sentiment_label': post.sentiment_label,
            'topics': post.topics,
            'summary': post.summary,
            'source': post.source,
            'post_url': post.post_url,
            'created_at': post.created_at.isoformat() if post.created_at else None,
        }
        for post in posts
    ]


async def get_platform_breakdown(
    db: AsyncSession,
    user_id: int,
    days: Optional[int] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Get post counts and sentiment distribution by platform.
    
    Args:
        db: Database session
        user_id: User ID to filter by
        days: Optional number of days to look back
    
    Returns:
        Dictionary with platform breakdown data
    """
    query = select(
        SocialPost.platform,
        func.count(SocialPost.id).label('total_posts'),
        func.sum(SocialPost.likes).label('total_likes'),
        func.sum(SocialPost.comments).label('total_comments'),
        func.sum(SocialPost.shares).label('total_shares'),
        func.avg(SocialPost.sentiment_score).label('avg_sentiment_score')
    ).where(
        SocialPost.user_id == user_id
    ).group_by(SocialPost.platform)
    
    if days:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        query = query.where(
            and_(
                SocialPost.posted_at >= start_date,
                SocialPost.posted_at <= end_date
            )
        )
    
    result = await db.execute(query)
    rows = result.all()
    
    breakdown = {}
    for row in rows:
        platform = row[0]
        breakdown[platform] = {
            'total_posts': row[1] or 0,
            'total_likes': row[2] or 0,
            'total_comments': row[3] or 0,
            'total_shares': row[4] or 0,
            'avg_sentiment_score': float(row[5]) if row[5] else 0.0,
            'total_engagement': (row[2] or 0) + (row[3] or 0) + (row[4] or 0)
        }
    
    return breakdown


async def get_sentiment_by_platform(
    db: AsyncSession,
    user_id: int,
    platform: Optional[str] = None,
    days: Optional[int] = None
) -> Dict[str, Dict[str, int]]:
    """
    Get sentiment distribution by platform.
    
    Args:
        db: Database session
        user_id: User ID to filter by
        platform: Optional specific platform to filter
        days: Optional number of days to look back
    
    Returns:
        Dictionary with sentiment counts per platform
    """
    query = select(
        SocialPost.platform,
        SocialPost.sentiment_label,
        func.count(SocialPost.id).label('count')
    ).where(
        and_(
            SocialPost.user_id == user_id,
            SocialPost.sentiment_label.isnot(None)
        )
    ).group_by(SocialPost.platform, SocialPost.sentiment_label)
    
    if platform:
        query = query.where(SocialPost.platform == platform)
    
    if days:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        query = query.where(
            and_(
                SocialPost.posted_at >= start_date,
                SocialPost.posted_at <= end_date
            )
        )
    
    result = await db.execute(query)
    rows = result.all()
    
    breakdown = {}
    for row in rows:
        plat = row[0]
        sentiment = row[1]
        count = row[2]
        
        if plat not in breakdown:
            breakdown[plat] = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        if sentiment in breakdown[plat]:
            breakdown[plat][sentiment] = count
    
    return breakdown
