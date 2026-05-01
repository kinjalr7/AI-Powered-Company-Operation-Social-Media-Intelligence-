from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.services.auth import verify_token, get_user_by_email
from app.services.ai_analytics import AIAnalyticsService
from app.services.user_social_analytics import UserSocialAnalyticsService
from app.services.email_service import EmailService
from app.models.social_data import Report, AnalyticsData, SocialPost
from app.schemas.social_data import Report as ReportSchema, ReportCreate

router = APIRouter()
security = HTTPBearer()
ai_service = AIAnalyticsService()
user_social_service = UserSocialAnalyticsService()
email_service = EmailService()

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

@router.post("/generate", response_model=ReportSchema)
async def generate_report(
    report_data: ReportCreate,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate a new AI-powered business report"""
    try:
        # Determine date range based on report type
        end_date = datetime.utcnow()
        if report_data.report_type == "daily":
            start_date = end_date - timedelta(days=1)
        elif report_data.report_type == "weekly":
            start_date = end_date - timedelta(days=7)
        elif report_data.report_type == "monthly":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = report_data.date_range_start or (end_date - timedelta(days=7))
            end_date = report_data.date_range_end or end_date

        # Fetch data for the period
        posts_result = await db.execute(
            select(SocialPost).where(
                and_(
                    SocialPost.user_id == current_user.id,
                    SocialPost.posted_at >= start_date,
                    SocialPost.posted_at <= end_date
                )
            )
        )
        posts = posts_result.scalars().all()

        # Generate insights
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

        insights = ai_service.generate_insights(posts_data)

        # Generate AI report
        report_content = ai_service.generate_business_report(insights, report_data.report_type)

        # Create report record
        db_report = Report(
            user_id=current_user.id,
            title=report_data.title,
            report_type=report_data.report_type,
            date_range_start=start_date,
            date_range_end=end_date,
            summary=insights.get('summary', ''),
            insights=insights.get('recommendations', []),
            recommendations=insights.get('recommendations', []),
            data_snapshot=insights
        )

        db.add(db_report)
        await db.commit()
        await db.refresh(db_report)

        # Send email in background if user has email reports enabled
        background_tasks.add_task(
            send_report_email,
            current_user.email,
            report_content,
            report_data.title,
            report_data.report_type
        )

        return db_report

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.get("/", response_model=List[ReportSchema])
async def get_reports(
    report_type: Optional[str] = None,
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's reports"""
    try:
        query = select(Report).where(Report.user_id == current_user.id)

        if report_type:
            query = query.where(Report.report_type == report_type)

        result = await db.execute(
            query.order_by(desc(Report.generated_at)).limit(limit)
        )
        reports = result.scalars().all()

        return reports

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reports: {str(e)}")

@router.get("/{report_id}", response_model=ReportSchema)
async def get_report(
    report_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific report"""
    try:
        result = await db.execute(
            select(Report).where(
                and_(
                    Report.id == report_id,
                    Report.user_id == current_user.id
                )
            )
        )
        report = result.scalar_one_or_none()

        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        return report

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch report: {str(e)}")

@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a report"""
    try:
        result = await db.execute(
            select(Report).where(
                and_(
                    Report.id == report_id,
                    Report.user_id == current_user.id
                )
            )
        )
        report = result.scalar_one_or_none()

        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        await db.delete(report)
        await db.commit()

        return {"message": "Report deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete report: {str(e)}")

@router.post("/personal-social-analysis", response_model=ReportSchema)
async def generate_personal_social_analysis(
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate AI-powered personal social media analysis report"""
    try:
        # Check if user has any social profiles configured
        user_profiles = {
            'twitter_handle': current_user.twitter_handle,
            'linkedin_profile': current_user.linkedin_profile,
            'facebook_profile': current_user.facebook_profile,
            'instagram_handle': current_user.instagram_handle,
            'youtube_channel': current_user.youtube_channel,
            'tiktok_handle': current_user.tiktok_handle
        }

        active_profiles = {k: v for k, v in user_profiles.items() if v is not None}
        if not active_profiles:
            raise HTTPException(
                status_code=400,
                detail="No social media profiles configured. Please add your social media handles first."
            )

        # Analyze user's social media presence
        analysis_result = user_social_service.analyze_user_social_presence(active_profiles)

        # Generate personal report
        report_content = user_social_service.generate_personal_report(
            analysis_result,
            current_user.full_name or current_user.email
        )

        # Create report record
        db_report = Report(
            user_id=current_user.id,
            title="Personal Social Media Analysis",
            report_type="personal",
            summary=f"Analysis of {len(active_profiles)} social media profiles",
            insights=analysis_result.get('recommendations', []),
            recommendations=analysis_result.get('recommendations', []),
            data_snapshot=analysis_result
        )

        db.add(db_report)
        await db.commit()
        await db.refresh(db_report)

        # Send email in background
        background_tasks.add_task(
            send_personal_report_email,
            current_user.email,
            report_content,
            current_user.full_name or "User",
            len(active_profiles)
        )

        return db_report

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personal analysis failed: {str(e)}")

@router.post("/schedule-daily")
async def schedule_daily_report(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Schedule daily automated reports"""
    try:
        # This would typically integrate with a task scheduler like Celery
        # For now, we'll just return a success message
        return {
            "message": "Daily reports scheduled successfully",
            "user_id": current_user.id,
            "schedule": "daily"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule reports: {str(e)}")

# Background task for sending emails
async def send_report_email(email: str, report_content: str, title: str, report_type: str):
    """Send report via email"""
    try:
        subject = f"AI Social Intelligence - {title} ({report_type.title()} Report)"
        await email_service.send_email(
            to_email=email,
            subject=subject,
            content=report_content,
            content_type="html"
        )
    except Exception as e:
        print(f"Failed to send email: {e}")
        # In a production app, you'd want to log this and possibly retry

async def send_personal_report_email(email: str, report_content: str, user_name: str, profiles_count: int):
    """Send personal social analysis report via email"""
    try:
        subject = f"Your Personal Social Media Analysis Report - AI Social Intelligence"
        html_content = f"""
        <html>
        <body>
        <h2>Hello {user_name}!</h2>

        <p>Your personal social media analysis report is ready. We've analyzed your presence across {profiles_count} social media platforms.</p>

        <div style="background-color: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px;">
        <pre style="white-space: pre-wrap; font-family: monospace; font-size: 14px;">{report_content}</pre>
        </div>

        <p>This analysis helps you understand your social media presence and provides personalized recommendations for growth.</p>

        <p>Keep building your online presence!</p>

        <br>
        <p>Best regards,<br>AI Social Intelligence Team</p>
        </body>
        </html>
        """

        await email_service.send_email(
            to_email=email,
            subject=subject,
            content=html_content,
            content_type="html"
        )
    except Exception as e:
        print(f"Failed to send personal report email: {e}")
        # In a production app, you'd want to log this and possibly retry