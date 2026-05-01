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
from app.models.user import User
from app.models.social_data import SocialPost, AnalyticsData, Report, NotificationSettings

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
            print("✓ Database tables created successfully")
            print("\n🎉 Database initialization completed successfully!")
            print("\nNext steps:")
            print("1. Start the backend server: python -m app.main")
            print("2. Start the frontend: cd frontend && npm run dev")
            print("3. Visit http://localhost:3000 to access the application")

        finally:
            db.close()

    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    init_database()