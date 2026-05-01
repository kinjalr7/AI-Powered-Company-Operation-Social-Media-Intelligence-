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

conn.commit()
conn.close()

print("✅ Database setup complete!")