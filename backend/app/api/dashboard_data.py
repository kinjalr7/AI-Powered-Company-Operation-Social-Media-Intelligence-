from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import and_, desc, select, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.social_data import SocialPost, SocialAccount
from app.services.auth import get_user_by_email, verify_token
from app.services.query_service import (
    get_post_count,
    get_sentiment_distribution,
    get_recent_posts,
    get_platform_breakdown
)

router = APIRouter()
security_optional = HTTPBearer(auto_error=False)


async def _get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    db: AsyncSession = Depends(get_db),
):
    if not credentials:
        return None
    email = verify_token(credentials.credentials)
    if email is None:
        return None
    return get_user_by_email(db, email)


@router.get("/dashboard-data", response_model=dict)
async def get_dashboard_data(
    days: int = Query(7, description="Number of days to analyze"),
    current_user_opt: Optional[object] = Depends(_get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """
    Single source of truth for the entire dashboard UI using centralized query service.
    All metrics are derived from social_posts table only.
    """
    if current_user_opt is None:
        return {"data": [], "message": "No data available. Add posts to begin."}

    current_user = current_user_opt
    try:
        # Get total post count using centralized query service
        total_posts = await get_post_count(db, current_user.id, days=days)
        
        if total_posts == 0:
            return {"data": [], "message": "No data available. Add posts to begin."}
        
        # Get sentiment distribution using centralized query service
        sentiment_dist = await get_sentiment_distribution(db, current_user.id, days=days)
        
        # Get platform breakdown using centralized query service
        platform_breakdown = await get_platform_breakdown(db, current_user.id, days=days)
        
        # Get recent posts using centralized query service
        recent_posts_data = await get_recent_posts(db, current_user.id, limit=8, days=days)
        
        # Fetch accounts for platform info
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        accounts_result = await db.execute(
            select(SocialAccount).where(
                and_(SocialAccount.user_id == current_user.id, SocialAccount.is_active == True)
            )
        )
        accounts = accounts_result.scalars().all()

        # Build unified platforms array
        unified_platforms: List[Dict[str, Any]] = []
        account_platforms = set()
        
        for account in accounts:
            p_name = account.platform.lower()
            account_platforms.add(p_name)
            
            plat_data = platform_breakdown.get(p_name, {
                'total_posts': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_shares': 0,
                'total_engagement': 0,
                'avg_sentiment_score': 0.0
            })
            
            unified_platforms.append({
                "name": p_name,
                "posts": int(plat_data['total_posts']),
                "likes": int(plat_data['total_likes']),
                "comments": int(plat_data['total_comments']),
                "shares": int(plat_data['total_shares']),
                "engagement": int(plat_data['total_engagement']),
                "username": account.username,
                "is_active": True
            })

        # Add posts from platforms without connected accounts
        for p_name, plat_data in platform_breakdown.items():
            if p_name not in account_platforms:
                unified_platforms.append({
                    "name": p_name,
                    "posts": int(plat_data['total_posts']),
                    "likes": int(plat_data['total_likes']),
                    "comments": int(plat_data['total_comments']),
                    "shares": int(plat_data['total_shares']),
                    "engagement": int(plat_data['total_engagement']),
                    "username": "System",
                    "is_active": True
                })

        # Calculate aggregated stats
        total_likes = sum(p['total_likes'] for p in platform_breakdown.values())
        total_comments = sum(p['total_comments'] for p in platform_breakdown.values())
        total_shares = sum(p['total_shares'] for p in platform_breakdown.values())
        total_engagement = total_likes + total_comments + total_shares
        
        # Calculate average sentiment (0-10 scale)
        avg_sentiment_scores = [p['avg_sentiment_score'] for p in platform_breakdown.values() if p['avg_sentiment_score']]
        avg_raw_sentiment = sum(avg_sentiment_scores) / len(avg_sentiment_scores) if avg_sentiment_scores else 0.0
        avg_sentiment_10 = round((avg_raw_sentiment + 1) * 5, 1)

        # Build timeseries data
        timeseries: List[Dict[str, Any]] = []
        engagement_chart: List[Dict[str, Any]] = []
        
        current_day = start_date.date()
        today = end_date.date()
        date_list = []
        while current_day <= today:
            date_list.append(current_day)
            current_day += timedelta(days=1)

        # Fetch all posts for the period to build timeseries
        posts_result = await db.execute(
            select(SocialPost).where(
                and_(
                    SocialPost.user_id == current_user.id,
                    SocialPost.posted_at >= start_date,
                    SocialPost.posted_at <= end_date,
                )
            ).order_by(desc(SocialPost.posted_at))
        )
        all_posts = posts_result.scalars().all()

        for d0 in date_list:
            day_posts = [p for p in all_posts if p.posted_at and p.posted_at.date() == d0]
            day_likes = sum(int(p.likes or 0) for p in day_posts)
            day_comments = sum(int(p.comments or 0) for p in day_posts)
            day_shares = sum(int(p.shares or 0) for p in day_posts)
            day_engagement = day_likes + day_comments + day_shares
            
            day_iso = d0.isoformat()
            timeseries.append({
                "date": day_iso,
                "posts": len(day_posts),
                "likes": int(day_likes),
                "comments": int(day_comments),
                "shares": int(day_shares),
                "engagement": int(day_engagement),
                "sentiment_score_avg": round(avg_raw_sentiment, 4),
            })
            engagement_chart.append({
                "date": day_iso,
                "likes": int(day_likes),
                "comments": int(day_comments),
            })

        return {
            "stats": {
                "posts": int(total_posts),
                "total_posts": int(total_posts),
                "likes": int(total_likes),
                "total_likes": int(total_likes),
                "comments": int(total_comments),
                "total_comments": int(total_comments),
                "shares": int(total_shares),
                "total_shares": int(total_shares),
                "engagement": int(total_engagement),
                "total_engagement": int(total_engagement),
                "avg_sentiment": avg_sentiment_10,
                "sentiment_score": avg_sentiment_10,
            },
            "platforms": unified_platforms,
            "charts": {
                "engagement": engagement_chart,
            },
            "period": {
                "start_date": start_date.strftime("%d %b %Y"),
                "end_date": end_date.strftime("%d %b %Y"),
                "days": days,
            },
            "metrics": {
                "total_posts": int(total_posts),
                "total_likes": int(total_likes),
                "total_comments": int(total_comments),
                "total_shares": int(total_shares),
                "total_engagement": int(total_engagement),
                "avg_engagement_per_post": round(total_engagement / total_posts, 2) if total_posts else 0,
            },
            "accounts": [
                {
                    "id": a.id,
                    "platform": a.platform,
                    "username": a.username,
                    "display_name": a.display_name,
                    "is_active": bool(a.is_active),
                    "is_verified": bool(a.is_verified),
                    "follower_count": int(a.follower_count or 0),
                }
                for a in accounts
            ],
            "platform_metrics": sorted([
                {
                    "platform": k,
                    "total_posts": v['total_posts'],
                    "likes": v['total_likes'],
                    "comments": v['total_comments'],
                    "shares": v['total_shares'],
                    "total_engagement": v['total_engagement'],
                    "avg_sentiment": avg_sentiment_10
                }
                for k, v in platform_breakdown.items()
            ], key=lambda x: x["total_posts"], reverse=True),
            "timeseries": timeseries,
            "top_topics": [],
            "recent_posts": [
                {
                    "id": p['id'],
                    "platform": p['platform'],
                    "content": p['content'],
                    "posted_at": p['posted_at'],
                    "sentiment": p['sentiment_label'] or "neutral",
                    "likes": int(p['likes']),
                    "comments": int(p['comments']),
                    "shares": int(p['shares']),
                    "sentimentScore": float(p['sentiment_score'] or 0.0),
                    "engagement": int(p['likes'] + p['comments'] + p['shares']),
                }
                for p in recent_posts_data
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build dashboard-data: {str(e)}")

