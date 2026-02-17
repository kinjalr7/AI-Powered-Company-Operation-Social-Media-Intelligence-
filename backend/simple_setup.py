#!/usr/bin/env python3
"""
Simple database setup script
"""

import sqlite3
import os

# Database file path
db_path = "ai_social_dev.db"

# Remove existing database if it exists
if os.path.exists(db_path):
    os.remove(db_path)

# Create database and tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT 1,
    is_superuser BOOLEAN DEFAULT 0,
    plan VARCHAR(50) DEFAULT 'free',
    avatar_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    last_login DATETIME
)
''')

# Create social_posts table
cursor.execute('''
CREATE TABLE social_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    platform VARCHAR(50) NOT NULL,
    post_id VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(255),
    author_id VARCHAR(255),
    url VARCHAR(500),
    posted_at DATETIME NOT NULL,
    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    sentiment VARCHAR(20),
    sentiment_score DECIMAL(3,2),
    topics TEXT,
    entities TEXT,
    language VARCHAR(10) DEFAULT 'en'
)
''')

# Insert sample user
cursor.execute('''
INSERT INTO users (email, hashed_password, full_name, plan)
VALUES (?, ?, ?, ?)
''', ('demo@example.com', '$2b$12$demo', 'Demo User', 'pro'))

# Insert sample posts
posts = [
    ('twitter', 'sample_1', 'Excited about AI developments! #AI', 'TechUser', 'tech1', 'https://twitter.com/tech1/status/1', '2024-01-01 10:00:00', 45, 12, 8, 234, 'positive', 0.8, '["AI", "technology"]'),
    ('linkedin', 'sample_2', 'Great insights on machine learning today.', 'DataScientist', 'data1', 'https://linkedin.com/posts/data1', '2024-01-01 08:00:00', 23, 5, 3, 156, 'positive', 0.7, '["machine learning"]'),
    ('twitter', 'sample_3', 'Privacy concerns with new regulations.', 'PrivacyAdvocate', 'privacy1', 'https://twitter.com/privacy1/status/3', '2024-01-01 06:00:00', 67, 23, 15, 445, 'negative', -0.3, '["privacy", "regulations"]')
]

for post in posts:
    cursor.execute('''
    INSERT INTO social_posts (platform, post_id, content, author, author_id, url, posted_at, likes, shares, comments, views, sentiment, sentiment_score, topics, user_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    ''', post)

conn.commit()
conn.close()

print("✅ Database setup complete!")
print("Demo login: demo@example.com / demo123")