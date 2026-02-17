#!/usr/bin/env python3
"""
Database initialization script for AI Social Intelligence platform.
This script creates the SQLite database and initializes the schema.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.core.database import create_tables, SessionLocal
from app.core.config import settings

def init_database():
    """Initialize the database"""
    try:
        print("Creating database tables...")

        # Create tables
        create_tables()

        print("✓ Database tables created successfully")

        # Import and create sample data
        from app.models.user import User
        from app.models.social_data import SocialPost
        from passlib.context import CryptContext
        from datetime import datetime, timedelta

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        db = SessionLocal()

        try:
            # Create sample users
            users_data = [
                {
                    "email": "demo@example.com",
                    "hashed_password": pwd_context.hash("demo123"),
                    "full_name": "Demo User",
                    "plan": "pro"
                },
                {
                    "email": "admin@example.com",
                    "hashed_password": pwd_context.hash("admin123"),
                    "full_name": "Admin User",
                    "plan": "enterprise"
                }
            ]

            for user_data in users_data:
                user = User(**user_data)
                db.add(user)

            db.commit()

            # Create sample social posts
            sample_posts = [
                {
                    "platform": "twitter",
                    "post_id": "sample_1",
                    "content": "Excited about the new AI developments in our industry! The future looks bright. #AI #Tech",
                    "author": "TechInnovator",
                    "author_id": "tech_user_1",
                    "url": "https://twitter.com/tech_user_1/status/sample_1",
                    "posted_at": datetime.utcnow() - timedelta(hours=2),
                    "likes": 45,
                    "shares": 12,
                    "comments": 8,
                    "views": 234,
                    "sentiment": "positive",
                    "sentiment_score": 0.8,
                    "topics": ["AI", "technology", "innovation"],
                    "language": "en",
                    "user_id": 1
                },
                {
                    "platform": "linkedin",
                    "post_id": "sample_2",
                    "content": "Great insights on machine learning applications in business intelligence. Very informative session today.",
                    "author": "DataScientist",
                    "author_id": "data_user_1",
                    "url": "https://linkedin.com/posts/data_user_1",
                    "posted_at": datetime.utcnow() - timedelta(hours=4),
                    "likes": 23,
                    "shares": 5,
                    "comments": 3,
                    "views": 156,
                    "sentiment": "positive",
                    "sentiment_score": 0.7,
                    "topics": ["machine learning", "business intelligence"],
                    "language": "en",
                    "user_id": 1
                },
                {
                    "platform": "twitter",
                    "post_id": "sample_3",
                    "content": "Concerned about data privacy issues with new regulations. Need better compliance frameworks.",
                    "author": "PrivacyAdvocate",
                    "author_id": "privacy_user_1",
                    "url": "https://twitter.com/privacy_user_1/status/sample_3",
                    "posted_at": datetime.utcnow() - timedelta(hours=6),
                    "likes": 67,
                    "shares": 23,
                    "comments": 15,
                    "views": 445,
                    "sentiment": "negative",
                    "sentiment_score": -0.3,
                    "topics": ["data privacy", "regulations", "compliance"],
                    "language": "en",
                    "user_id": 1
                }
            ]

            for post_data in sample_posts:
                post = SocialPost(**post_data)
                db.add(post)

            db.commit()

            print("✓ Sample data created successfully")
            print("\n🎉 Database initialization completed successfully!")
            print("\nNext steps:")
            print("1. Start the backend server: python -m app.main")
            print("2. Start the frontend: cd frontend && npm run dev")
            print("3. Visit http://localhost:3000 to access the application")
            print("\nDemo accounts:")
            print("- demo@example.com / demo123")
            print("- admin@example.com / admin123")

        finally:
            db.close()

    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    init_database()