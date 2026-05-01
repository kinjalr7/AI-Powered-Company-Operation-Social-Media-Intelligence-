from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import and_, desc, select, func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.social_data import SocialPost, SocialAccount
from app.services.auth import get_user_by_email, verify_token

router = APIRouter()
security_optional = HTTPBearer(auto_error=False)


async def _get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
):
    """
    Single source of truth for the entire dashboard UI:
    - cards
    - charts
    - active platforms count (platforms.length)
    - report PDF snapshots
    """
    if current_user_opt is None:
        return {"data": [], "message": "No data available. Add posts to begin."}

    current_user = current_user_opt
    try:
        from datetime import timezone
        # Use naive datetimes (UTC) to match how data is likely stored and queried in other modules
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        posts_result = db.execute(
            select(SocialPost)
            .where(
                and_(
                    SocialPost.user_id == current_user.id,
                    SocialPost.posted_at >= start_date,
                    SocialPost.posted_at <= end_date,
                )
            )
            .order_by(desc(SocialPost.posted_at))
        )
        posts = posts_result.scalars().all()

        # REQUIRED DEBUG LOGS
        print("TOTAL POSTS FOUND:", len(posts))
        print("CURRENT USER ID:", current_user.id)

        accounts_result = db.execute(
            select(SocialAccount).where(
                and_(SocialAccount.user_id == current_user.id, SocialAccount.is_active == True)
            )
        )
        accounts = accounts_result.scalars().all()
        print("ACCOUNTS FOUND:", len(accounts))

        # 1. Fallback Logic: If no recent data is found, show demo data
        # This prevents the "0 values" issue for new users or during demos.
        # We fallback if:
        # - NO posts AND NO accounts are found
        # - OR if it's the demo user and they have no recent posts
        if len(posts) == 0:
            return {"data": [], "message": "No data available. Add posts to begin."}

        # 2. Primary Stats - Derived directly from the fetched posts (Single Source of Truth)
        # We calculate an average sentiment score (0-10) for the main stats card
        all_sentiment_scores = [float(p.sentiment_score or 0) for p in posts]
        avg_raw_sentiment = sum(all_sentiment_scores) / len(all_sentiment_scores) if all_sentiment_scores else 0.0
        # Map raw sentiment (-1 to 1) to a 0-10 scale for the UI card
        avg_sentiment_10 = round((avg_raw_sentiment + 1) * 5, 1)
        stats_posts = len(posts)
        stats_likes = sum(int(p.likes or 0) for p in posts)
        stats_comments = sum(int(p.comments or 0) for p in posts)
        stats_shares = sum(int(p.shares or 0) for p in posts)
        stats_engagement = stats_likes + stats_comments + stats_shares

        # 2. Per-platform aggregation
        platform_agg: Dict[str, Dict[str, Any]] = {}
        for p in posts:
            p_name = (p.platform or "unknown").lower()
            if p_name not in platform_agg:
                platform_agg[p_name] = {
                    "platform": p_name,
                    "total_posts": 0,
                    "likes": 0,
                    "comments": 0,
                    "shares": 0,
                    "total_engagement": 0,
                    "sentiment": {"positive": 0, "neutral": 0, "negative": 0},
                    "avg_sentiment": avg_sentiment_10,
                }
            item = platform_agg[p_name]
            item["total_posts"] += 1
            item["likes"] += int(p.likes or 0)
            item["comments"] += int(p.comments or 0)
            item["shares"] += int(p.shares or 0)
            item["total_engagement"] += int((p.likes or 0) + (p.comments or 0) + (p.shares or 0))

        # 3. Unified "platforms" array for UI
        unified_platforms: List[Dict[str, Any]] = []
        account_platforms = set()
        
        for account in accounts:
            p_name = account.platform.lower()
            account_platforms.add(p_name)
            
            # Note: We associate platform-level stats with the account. 
            # If multiple accounts for one platform, they share the platform stats 
            # unless SocialPost has an account_id (not in current schema).
            agg = platform_agg.get(p_name, {
                "total_posts": 0, "likes": 0, "comments": 0, "shares": 0, "total_engagement": 0
            })
            
            unified_platforms.append({
                "name": p_name,
                "posts": int(agg["total_posts"]),
                "likes": int(agg["likes"]),
                "comments": int(agg["comments"]),
                "shares": int(agg["shares"]),
                "engagement": int(agg["total_engagement"]),
                "username": account.username,
                "is_active": True
            })

        # Add posts from platforms that don't have a connected account (e.g. legacy data)
        for p_name, agg in platform_agg.items():
            if p_name not in account_platforms:
                unified_platforms.append({
                    "name": p_name,
                    "posts": int(agg["total_posts"]),
                    "likes": int(agg["likes"]),
                    "comments": int(agg["comments"]),
                    "shares": int(agg["shares"]),
                    "engagement": int(agg["total_engagement"]),
                    "username": "System",
                    "is_active": True
                })

        # 4. Timeseries (Daily charts) - Include today!
        timeseries: List[Dict[str, Any]] = []
        engagement_chart: List[Dict[str, Any]] = []
        
        # Determine unique dates from start_date to today
        current_day = start_date.date()
        today = end_date.date()
        date_list = []
        while current_day <= today:
            date_list.append(current_day)
            current_day += timedelta(days=1)

        for d0 in date_list:
            day_posts = [p for p in posts if p.posted_at and p.posted_at.date() == d0]
            day_likes = sum(int(p.likes or 0) for p in day_posts)
            day_comments = sum(int(p.comments or 0) for p in day_posts)
            day_shares = sum(int(p.shares or 0) for p in day_posts)
            day_engagement = day_likes + day_comments + day_shares
            
            scores = [float(p.sentiment_score) for p in day_posts if p.sentiment_score is not None]
            avg_score = round(sum(scores) / len(scores), 4) if scores else 0.0

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
                "posts": int(stats_posts),
                "total_posts": int(stats_posts),
                "likes": int(stats_likes),
                "total_likes": int(stats_likes),
                "comments": int(stats_comments),
                "total_comments": int(stats_comments),
                "shares": int(stats_shares),
                "total_shares": int(stats_shares),
                "engagement": int(stats_engagement),
                "total_engagement": int(stats_engagement),
                "avg_sentiment": avg_sentiment_10,
                "sentiment_score": avg_sentiment_10,
            },
            "platforms": unified_platforms,
            "charts": {
                "engagement": engagement_chart,
            },
            # Legacy fields kept for backward compatibility with existing UI components.
            "period": {
                "start_date": start_date.strftime("%d %b %Y"),
                "end_date": end_date.strftime("%d %b %Y"),
                "days": days,
            },
            "metrics": {
                "total_posts": int(stats_posts),
                "total_likes": int(stats_likes),
                "total_comments": int(stats_comments),
                "total_shares": int(stats_shares),
                "total_engagement": int(stats_engagement),
                "avg_engagement_per_post": round(stats_engagement / stats_posts, 2) if stats_posts else 0,
            },
            # Preserve account-level data for any existing consumers.
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
                {**v, "avg_sentiment": avg_sentiment_10} for v in platform_agg.values()
            ], key=lambda x: x["total_posts"], reverse=True),
            "timeseries": timeseries,
            "top_topics": [],
            "recent_posts": [
                {
                    "id": p.id,
                    "platform": p.platform,
                    "content": p.content,
                    "posted_at": p.posted_at.isoformat() if p.posted_at else None,
                    "sentiment": p.sentiment or "neutral",
                    "likes": int(p.likes or 0),
                    "comments": int(p.comments or 0),
                    "shares": int(p.shares or 0),
                    "sentimentScore": float(p.sentiment_score or 0.0),
                    "engagement": int((p.likes or 0) + (p.comments or 0) + (p.shares or 0)),
                }
                for p in posts[:8]
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build dashboard-data: {str(e)}")

