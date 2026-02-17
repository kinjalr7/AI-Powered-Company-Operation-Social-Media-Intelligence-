import asyncio
from datetime import datetime, time
import schedule
import threading
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import get_db
from app.services.ai_analytics import AIAnalyticsService
from app.services.email_service import EmailService
from app.services.social_collector import SocialDataCollector
from app.models.user import User
from app.models.social_data import NotificationSettings
from app.schemas.social_data import ReportCreate

ai_service = AIAnalyticsService()
email_service = EmailService()
social_collector = SocialDataCollector()

# Global database session for scheduler
engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class TaskScheduler:
    def __init__(self):
        self.running = False
        self.thread = None

    def start_scheduler(self):
        """Start the background scheduler"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        print("Task scheduler started")

    def stop_scheduler(self):
        """Stop the background scheduler"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("Task scheduler stopped")

    def _run_scheduler(self):
        """Run the scheduler loop"""
        # Schedule daily tasks
        schedule.every().day.at("09:00").do(self._send_daily_reports)
        schedule.every().day.at("02:00").do(self._collect_social_data)
        schedule.every().hour.do(self._check_alerts)

        while self.running:
            schedule.run_pending()
            asyncio.run(asyncio.sleep(60))  # Check every minute

    async def _send_daily_reports(self):
        """Send daily reports to all users who have them enabled"""
        try:
            async with AsyncSessionLocal() as db:
                # Get all users with email reports enabled
                result = await db.execute(
                    """
                    SELECT u.*, ns.report_frequency, ns.email_reports
                    FROM users u
                    JOIN notification_settings ns ON u.id = ns.user_id
                    WHERE ns.email_reports = true AND ns.report_frequency = 'daily'
                    """
                )
                users = result.fetchall()

                for user_row in users:
                    user_dict = dict(user_row)
                    await self._generate_and_send_report(
                        user_dict['id'],
                        user_dict['email'],
                        user_dict['full_name'] or user_dict['email'],
                        "daily"
                    )

        except Exception as e:
            print(f"Daily reports task failed: {e}")

    async def _collect_social_data(self):
        """Collect fresh social media data"""
        try:
            async with AsyncSessionLocal() as db:
                # Get all active users
                result = await db.execute("SELECT id FROM users WHERE is_active = true")
                user_ids = [row[0] for row in result.fetchall()]

                for user_id in user_ids:
                    # Collect data for common keywords
                    keywords = ["AI", "machine learning", "technology", "business intelligence"]
                    posts_data = await social_collector.collect_all_platforms(
                        keywords=keywords,
                        days_back=1,  # Collect last 24 hours
                        max_results_per_platform=50
                    )

                    if posts_data:
                        saved_count = await social_collector.save_posts_to_database(
                            posts_data, user_id, db
                        )
                        print(f"Saved {saved_count} posts for user {user_id}")

        except Exception as e:
            print(f"Social data collection task failed: {e}")

    async def _check_alerts(self):
        """Check for alerts and send notifications"""
        try:
            async with AsyncSessionLocal() as db:
                # Get users with real-time alerts enabled
                result = await db.execute(
                    """
                    SELECT u.*, ns.sentiment_threshold, ns.engagement_threshold, ns.real_time_alerts
                    FROM users u
                    JOIN notification_settings ns ON u.id = ns.user_id
                    WHERE ns.real_time_alerts = true
                    """
                )
                users = result.fetchall()

                for user_row in users:
                    user_dict = dict(user_row)
                    await self._check_user_alerts(user_dict, db)

        except Exception as e:
            print(f"Alert checking task failed: {e}")

    async def _generate_and_send_report(
        self,
        user_id: int,
        email: str,
        user_name: str,
        report_type: str
    ):
        """Generate and send a report for a specific user"""
        try:
            async with AsyncSessionLocal() as db:
                # Generate report logic here (simplified)
                report_title = f"Daily Business Intelligence Report - {datetime.now().strftime('%Y-%m-%d')}"

                # Create report record
                report_data = ReportCreate(
                    title=report_title,
                    report_type=report_type
                )

                # This would call the actual report generation logic
                # For now, just send a simple email
                await email_service.send_report_email(
                    email=email,
                    report_title=report_title,
                    report_content=f"Daily report for {user_name}",
                    report_type=report_type
                )

                print(f"Sent {report_type} report to {email}")

        except Exception as e:
            print(f"Failed to send report to {email}: {e}")

    async def _check_user_alerts(self, user_dict: Dict[str, Any], db: AsyncSession):
        """Check alerts for a specific user"""
        try:
            user_id = user_dict['id']
            email = user_dict['email']
            sentiment_threshold = user_dict['sentiment_threshold']
            engagement_threshold = user_dict['engagement_threshold']

            # Check recent posts for alerts
            # This is a simplified version - in reality, you'd check recent analytics
            # and compare against thresholds

            # Example: Check if sentiment dropped significantly
            # Example: Check if engagement spiked

            # For demo purposes, we'll skip actual alert logic
            # In production, this would analyze recent data and send alerts

        except Exception as e:
            print(f"Alert check failed for user {user_dict['id']}: {e}")

# Global scheduler instance
scheduler = TaskScheduler()

def start_scheduler():
    """Start the global scheduler"""
    scheduler.start_scheduler()

def stop_scheduler():
    """Stop the global scheduler"""
    scheduler.stop_scheduler()

# Manual trigger functions for testing/admin
async def trigger_daily_reports():
    """Manually trigger daily reports"""
    await scheduler._send_daily_reports()

async def trigger_data_collection():
    """Manually trigger data collection"""
    await scheduler._collect_social_data()

async def trigger_alert_check():
    """Manually trigger alert checking"""
    await scheduler._check_alerts()