from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.services.auth import verify_token, get_user_by_email
from app.services.ai_analytics import AIAnalyticsService
from app.services.query_service import (
    get_post_count,
    get_sentiment_distribution,
    get_recent_posts,
    get_platform_breakdown,
    get_sentiment_by_platform
)
from app.models.social_data import SocialPost, AnalyticsData
from app.schemas.social_data import AnalyticsData as AnalyticsDataSchema, SocialPost as SocialPostSchema

router = APIRouter()
security = HTTPBearer()
ai_service = AIAnalyticsService()

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

@router.get("/dashboard", response_model=dict)
async def get_dashboard_data(
    days: int = Query(7, description="Number of days to analyze"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive dashboard analytics data"""
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Fetch social posts for the period
        result = await db.execute(
            select(SocialPost).where(
                and_(
                    SocialPost.user_id == current_user.id,
                    SocialPost.posted_at >= start_date,
                    SocialPost.posted_at <= end_date
                )
            ).order_by(desc(SocialPost.posted_at))
        )
        posts = result.scalars().all()

        # Convert to dict format for AI analysis
        posts_data = [
            {
                'content': post.content,
                'platform': post.platform,
                'likes': post.likes,
                'shares': post.shares,
                'comments': post.comments,
                'sentiment': post.sentiment
            }
            for post in posts
        ]

        # Generate AI insights
        insights = ai_service.generate_insights(posts_data)

        # Get aggregated analytics data
        analytics_result = await db.execute(
            select(AnalyticsData).where(
                and_(
                    AnalyticsData.user_id == current_user.id,
                    AnalyticsData.date >= start_date,
                    AnalyticsData.date <= end_date
                )
            ).order_by(desc(AnalyticsData.date))
        )
        analytics_records = analytics_result.scalars().all()

        # Format response
        response = {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': days
            },
            'insights': insights,
            'analytics_history': [
                {
                    'date': record.date.isoformat(),
                    'total_posts': record.total_posts,
                    'sentiment_positive': record.sentiment_positive,
                    'sentiment_negative': record.sentiment_negative,
                    'sentiment_neutral': record.sentiment_neutral,
                    'total_engagement': record.total_engagement,
                    'top_topics': record.top_topics
                }
                for record in analytics_records
            ],
            'recent_posts': [
                {
                    'id': post.id,
                    'platform': post.platform,
                    'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
                    'author': post.author,
                    'posted_at': post.posted_at.isoformat(),
                    'engagement': post.likes + post.shares + post.comments,
                    'sentiment': post.sentiment
                }
                for post in posts[:10]  # Last 10 posts
            ]
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics generation failed: {str(e)}")

@router.get("/sentiment-analysis", response_model=dict)
async def get_sentiment_analysis(
    platform: Optional[str] = None,
    days: int = Query(30, description="Number of days to analyze"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed sentiment analysis - uses centralized query service"""
    try:
        # Use centralized query service for sentiment distribution
        sentiment_dist = await get_sentiment_distribution(
            db,
            current_user.id,
            platform=platform,
            days=days
        )
        
        # Get total post count
        total_posts = await get_post_count(
            db,
            current_user.id,
            platform=platform,
            days=days
        )
        
        # Get sentiment by platform if no specific platform filter
        platform_breakdown = {}
        if not platform:
            platform_breakdown = await get_sentiment_by_platform(
                db,
                current_user.id,
                days=days
            )

        return {
            'period': f"{days} days",
            'total_posts': total_posts,
            'sentiment_distribution': sentiment_dist,
            'platform_breakdown': platform_breakdown
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")

@router.get("/topic-analysis", response_model=dict)
async def get_topic_analysis(
    days: int = Query(30, description="Number of days to analyze"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get topic analysis and trending keywords"""
    try:
        # Get recent posts from centralized query service
        recent_posts = await get_recent_posts(
            db,
            current_user.id,
            limit=1000,
            days=days
        )

        if not recent_posts:
            return {
                'period': f"{days} days",
                'total_posts_analyzed': 0,
                'topics': []
            }

        # Extract topics from all posts
        all_content = " ".join([post['content'] for post in recent_posts])
        topics = ai_service.extract_topics(all_content, max_topics=20)

        # Analyze topic frequency and sentiment
        topic_analysis = {}
        for post in recent_posts:
            post_topics = ai_service.extract_topics(post['content'], max_topics=5)
            sentiment = post['sentiment_label'] or 'neutral'

            for topic in post_topics:
                if topic not in topic_analysis:
                    topic_analysis[topic] = {
                        'count': 0,
                        'sentiment_scores': {'positive': 0, 'negative': 0, 'neutral': 0},
                        'avg_sentiment_score': 0
                    }

                topic_analysis[topic]['count'] += 1
                if sentiment in topic_analysis[topic]['sentiment_scores']:
                    topic_analysis[topic]['sentiment_scores'][sentiment] += 1

        # Calculate sentiment distribution for each topic
        for topic_data in topic_analysis.values():
            total = topic_data['count']
            if total > 0:
                # Calculate weighted sentiment score
                pos_score = topic_data['sentiment_scores']['positive'] / total
                neg_score = topic_data['sentiment_scores']['negative'] / total
                topic_data['avg_sentiment_score'] = pos_score - neg_score

        # Sort by frequency
        sorted_topics = sorted(
            topic_analysis.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        return {
            'period': f"{days} days",
            'total_posts_analyzed': len(recent_posts),
            'topics': [
                {
                    'topic': topic,
                    'frequency': data['count'],
                    'sentiment_distribution': data['sentiment_scores'],
                    'sentiment_score': data['avg_sentiment_score']
                }
                for topic, data in sorted_topics[:15]  # Top 15 topics
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Topic analysis failed: {str(e)}")

@router.post("/analyze-post")
async def analyze_single_post(
    content: str,
    current_user = Depends(get_current_user)
):
    """Analyze a single post's sentiment and topics"""
    try:
        sentiment = ai_service.analyze_sentiment(content)
        topics = ai_service.extract_topics(content)
        summary = ai_service.summarize_text(content)

        return {
            'content': content,
            'sentiment': sentiment,
            'topics': topics,
            'summary': summary,
            'analyzed_at': datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Post analysis failed: {str(e)}")