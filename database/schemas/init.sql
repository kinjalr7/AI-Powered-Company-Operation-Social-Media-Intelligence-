-- AI Social Intelligence Database Schema
-- PostgreSQL 13+ compatible

-- Create database (run this manually or adjust connection string)
-- CREATE DATABASE ai_social_db;
-- \c ai_social_db;

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For text search

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    plan VARCHAR(50) DEFAULT 'free',
    avatar_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,

    -- Social media profiles
    twitter_handle VARCHAR(255),
    linkedin_profile VARCHAR(500),
    facebook_profile VARCHAR(500),
    instagram_handle VARCHAR(255),
    youtube_channel VARCHAR(500),
    tiktok_handle VARCHAR(255)
);

-- User plans table
CREATE TABLE user_plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    features JSONB, -- Array of feature descriptions
    limits JSONB,   -- Usage limits (social_accounts, reports, api_calls, storage)
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Social posts table
CREATE TABLE social_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- twitter, linkedin, facebook, instagram
    post_id VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(255),
    author_id VARCHAR(255),
    url VARCHAR(500),
    posted_at TIMESTAMP WITH TIME ZONE NOT NULL,
    collected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Engagement metrics
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,

    -- AI Analysis results
    sentiment VARCHAR(20), -- positive, negative, neutral
    sentiment_score DECIMAL(3,2), -- -1.0 to 1.0
    topics JSONB, -- Array of extracted topics
    entities JSONB, -- Named entities
    language VARCHAR(10) DEFAULT 'en',

    -- Full-text search
    search_vector TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('english', content)
    ) STORED
);

-- Analytics data table (aggregated daily metrics)
CREATE TABLE analytics_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    total_posts INTEGER DEFAULT 0,

    -- Sentiment distribution
    sentiment_positive DECIMAL(5,2) DEFAULT 0,
    sentiment_negative DECIMAL(5,2) DEFAULT 0,
    sentiment_neutral DECIMAL(5,2) DEFAULT 0,

    -- Platform breakdown (JSON)
    platform_stats JSONB,

    -- Engagement metrics
    total_engagement INTEGER DEFAULT 0,
    avg_engagement DECIMAL(8,2) DEFAULT 0,

    -- Topics and keywords
    top_topics JSONB,
    trending_keywords JSONB,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id, date)
);

-- Reports table
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL, -- daily, weekly, monthly
    date_range_start TIMESTAMP WITH TIME ZONE,
    date_range_end TIMESTAMP WITH TIME ZONE,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Report content
    summary TEXT,
    insights JSONB, -- Array of insights
    recommendations JSONB, -- Array of recommendations
    data_snapshot JSONB, -- Snapshot of analytics data

    -- Status
    status VARCHAR(50) DEFAULT 'generated', -- generated, sent, failed
    sent_at TIMESTAMP WITH TIME ZONE,

    -- Full-text search on content
    search_vector TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('english', COALESCE(summary, '') || ' ' || COALESCE(title, ''))
    ) STORED
);

-- Notification settings table
CREATE TABLE notification_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    email_reports BOOLEAN DEFAULT TRUE,
    real_time_alerts BOOLEAN DEFAULT FALSE,

    -- Alert thresholds
    sentiment_threshold DECIMAL(3,2) DEFAULT 0.7, -- Alert when sentiment drops below
    engagement_threshold INTEGER DEFAULT 1000,

    -- Keywords to monitor
    keywords JSONB, -- Array of keywords

    -- Schedule
    report_frequency VARCHAR(20) DEFAULT 'daily', -- daily, weekly, monthly
    timezone VARCHAR(50) DEFAULT 'UTC',

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_social_posts_user_id ON social_posts(user_id);
CREATE INDEX idx_social_posts_platform ON social_posts(platform);
CREATE INDEX idx_social_posts_posted_at ON social_posts(posted_at);
CREATE INDEX idx_social_posts_sentiment ON social_posts(sentiment);
CREATE INDEX idx_social_posts_search_vector ON social_posts USING GIN(search_vector);

CREATE INDEX idx_analytics_data_user_id ON analytics_data(user_id);
CREATE INDEX idx_analytics_data_date ON analytics_data(date);

CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_generated_at ON reports(generated_at);
CREATE INDEX idx_reports_search_vector ON reports USING GIN(search_vector);

-- Insert default user plans
INSERT INTO user_plans (name, price, features, limits) VALUES
('Free', 0.00,
 '["5 social accounts monitoring", "Basic sentiment analysis", "Weekly reports", "Community support"]',
 '{"social_accounts": 5, "reports": 1, "api_calls": 1000, "storage": "1GB"}'),

('Pro', 29.00,
 '["25 social accounts monitoring", "Advanced NLP analysis", "Daily AI reports", "Priority support", "Real-time alerts", "Custom dashboards"]',
 '{"social_accounts": 25, "reports": 7, "api_calls": 10000, "storage": "10GB"}'),

('Enterprise', 99.00,
 '["Unlimited social accounts", "Enterprise NLP models", "Real-time AI insights", "24/7 premium support", "Custom integrations", "Advanced security", "Multi-user access"]',
 '{"social_accounts": -1, "reports": -1, "api_calls": -1, "storage": "Unlimited"}');

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notification_settings_updated_at BEFORE UPDATE ON notification_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function for sentiment trend analysis
CREATE OR REPLACE FUNCTION calculate_sentiment_trend(user_id_param INTEGER, days INTEGER DEFAULT 7)
RETURNS TABLE (
    date DATE,
    avg_sentiment DECIMAL,
    trend VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    WITH daily_sentiment AS (
        SELECT
            DATE(posted_at) as post_date,
            AVG(sentiment_score) as avg_score,
            COUNT(*) as post_count
        FROM social_posts
        WHERE user_id = user_id_param
          AND posted_at >= CURRENT_DATE - INTERVAL '1 day' * days
        GROUP BY DATE(posted_at)
        ORDER BY post_date
    ),
    trend_calc AS (
        SELECT
            post_date,
            avg_score,
            LAG(avg_score) OVER (ORDER BY post_date) as prev_score,
            CASE
                WHEN avg_score > LAG(avg_score) OVER (ORDER BY post_date) THEN 'improving'
                WHEN avg_score < LAG(avg_score) OVER (ORDER BY post_date) THEN 'declining'
                ELSE 'stable'
            END as daily_trend
        FROM daily_sentiment
    )
    SELECT
        post_date,
        ROUND(avg_score::numeric, 3),
        daily_trend
    FROM trend_calc
    WHERE post_date >= CURRENT_DATE - INTERVAL '1 day' * (days - 1);
END;
$$ LANGUAGE plpgsql;

-- Function for topic frequency analysis
CREATE OR REPLACE FUNCTION get_topic_frequency(user_id_param INTEGER, days INTEGER DEFAULT 30)
RETURNS TABLE (
    topic VARCHAR,
    frequency INTEGER,
    avg_sentiment DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        jsonb_array_elements_text(topics) as topic,
        COUNT(*)::INTEGER as frequency,
        ROUND(AVG(sentiment_score)::numeric, 3) as avg_sentiment
    FROM social_posts
    WHERE user_id = user_id_param
      AND posted_at >= CURRENT_DATE - INTERVAL '1 day' * days
      AND topics IS NOT NULL
    GROUP BY jsonb_array_elements_text(topics)
    ORDER BY frequency DESC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- Row Level Security (optional, for multi-tenant setup)
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE social_posts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE analytics_data ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE notification_settings ENABLE ROW LEVEL SECURITY;

-- Create policies (uncomment if using RLS)
-- CREATE POLICY user_posts_policy ON social_posts
--     FOR ALL USING (user_id = current_user_id());
-- (Note: current_user_id() would need to be implemented)

-- Comments for documentation
COMMENT ON TABLE users IS 'User accounts and authentication data';
COMMENT ON TABLE user_plans IS 'Available subscription plans and features';
COMMENT ON TABLE social_posts IS 'Collected social media posts with AI analysis';
COMMENT ON TABLE analytics_data IS 'Aggregated analytics data for dashboards';
COMMENT ON TABLE reports IS 'Generated AI reports and insights';
COMMENT ON TABLE notification_settings IS 'User notification preferences and thresholds';

COMMENT ON COLUMN social_posts.sentiment_score IS 'Sentiment score from -1 (negative) to 1 (positive)';
COMMENT ON COLUMN analytics_data.sentiment_positive IS 'Percentage of positive sentiment posts';
COMMENT ON COLUMN notification_settings.sentiment_threshold IS 'Threshold for sentiment alerts (0-1)';