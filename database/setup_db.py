#!/usr/bin/env python3
"""
Database setup script for AI Social Intelligence platform.
This script creates the PostgreSQL database and initializes the schema.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'ai_social_db')
    }

def create_database(db_config):
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()

        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                      (db_config['database'],))
        exists = cursor.fetchone()

        if not exists:
            print(f"Creating database '{db_config['database']}'...")
            cursor.execute(f"CREATE DATABASE {db_config['database']}")
            print(f"✓ Database '{db_config['database']}' created successfully")
        else:
            print(f"✓ Database '{db_config['database']}' already exists")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"✗ Error creating database: {e}")
        return False

def initialize_schema(db_config):
    """Initialize the database schema"""
    try:
        # Connect to the specific database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Read and execute the schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas', 'init.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        print("Initializing database schema...")
        cursor.execute(schema_sql)
        conn.commit()

        print("✓ Database schema initialized successfully")

        # Verify tables were created
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        print(f"✓ Created tables: {', '.join(table_names)}")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"✗ Error initializing schema: {e}")
        return False
    except FileNotFoundError:
        print("✗ Schema file not found. Make sure 'schemas/init.sql' exists.")
        return False

def insert_sample_data(db_config):
    """Insert sample data for testing"""
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        print("Inserting sample data...")

        # Sample users
        cursor.execute("""
            INSERT INTO users (email, hashed_password, full_name, plan)
            VALUES
                ('demo@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeA5DoEW5qKhFSr.', 'Demo User', 'pro'),
                ('admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeA5DoEW5qKhFSr.', 'Admin User', 'enterprise')
            ON CONFLICT (email) DO NOTHING;
        """)

        # Sample notification settings
        cursor.execute("""
            INSERT INTO notification_settings (user_id, email_reports, keywords)
            SELECT id, true, '["AI", "machine learning", "technology"]'::jsonb
            FROM users
            WHERE email IN ('demo@example.com', 'admin@example.com')
            ON CONFLICT (user_id) DO NOTHING;
        """)

        conn.commit()
        print("✓ Sample data inserted successfully")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"✗ Error inserting sample data: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Setup AI Social Intelligence database')
    parser.add_argument('--create-db', action='store_true',
                       help='Create the database if it doesn\'t exist')
    parser.add_argument('--init-schema', action='store_true',
                       help='Initialize the database schema')
    parser.add_argument('--sample-data', action='store_true',
                       help='Insert sample data for testing')
    parser.add_argument('--all', action='store_true',
                       help='Do everything (create DB, init schema, insert sample data)')

    args = parser.parse_args()

    # If no specific args, do everything
    if not any([args.create_db, args.init_schema, args.sample_data]):
        args.all = True

    db_config = get_db_config()
    print(f"Database configuration: {db_config['host']}:{db_config['port']}/{db_config['database']}")

    success = True

    if args.all or args.create_db:
        success &= create_database(db_config)

    if args.all or args.init_schema:
        success &= initialize_schema(db_config)

    if args.all or args.sample_data:
        success &= insert_sample_data(db_config)

    if success:
        print("\n🎉 Database setup completed successfully!")
        print("\nNext steps:")
        print("1. Start the backend server: cd backend && python -m app.main")
        print("2. Start the frontend: cd frontend && npm run dev")
        print("3. Visit http://localhost:3000 to access the application")
    else:
        print("\n❌ Database setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()