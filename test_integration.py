#!/usr/bin/env python3
"""
Simple integration test to verify frontend-backend connectivity
"""

import requests
import json
import time

def test_backend_endpoints():
    """Test basic backend endpoints"""
    base_url = "http://localhost:8000"

    print("Testing backend endpoints...")

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Health endpoint working")
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")
        return False

    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✓ Root endpoint working")
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Root endpoint error: {e}")
        return False

    # Test API docs
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✓ API docs working")
        else:
            print(f"✗ API docs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ API docs error: {e}")
        return False

    return True

def test_frontend():
    """Test that frontend is serving"""
    frontend_url = "http://localhost:3000"

    print("Testing frontend...")

    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("✓ Frontend serving successfully")
            return True
        else:
            print(f"✗ Frontend failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Frontend error: {e}")
        return False

def test_database_has_data():
    """Test that sample data was created"""
    print("Testing database has sample data...")

    try:
        import sqlite3
        import os

        # Check if database file exists
        db_path = os.path.join(os.path.dirname(__file__), 'backend', 'ai_social_dev.db')
        if not os.path.exists(db_path):
            print("✗ Database file not found")
            return False

        # Connect to database and count posts
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM social_posts")
        count = cursor.fetchone()[0]
        conn.close()

        if count > 0:
            print(f"✓ Database has {count} sample posts")
            return True
        else:
            print("✗ No sample data found")
            return False
    except Exception as e:
        print(f"✗ Database test error: {e}")
        return False

def main():
    print("🚀 AI Social Intelligence Integration Test")
    print("=" * 50)

    # Wait a moment for services to be ready
    time.sleep(2)

    results = []

    # Test backend
    results.append(test_backend_endpoints())

    # Test frontend
    results.append(test_frontend())

    # Test database
    results.append(test_database_has_data())

    print("\n" + "=" * 50)
    if all(results):
        print("🎉 All tests passed! Integration successful.")
        return True
    else:
        print("❌ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)