#!/usr/bin/env python3
"""
Script to create sample social media data for demonstration
"""

import random
import datetime
from app.core.database import get_db
from app.models.social_data import SocialPost
from app.services.ai_analytics import AIAnalyticsService

def generate_sample_posts(count: int = 100):
    """Generate sample social media posts"""

    # Sample post templates
    positive_templates = [
        "Just launched our new product! So excited about the future! #innovation #success",
        "Amazing customer feedback today! Love helping businesses grow! 🚀",
        "Team celebration - we hit our quarterly goals! Grateful for such an awesome team!",
        "New partnership announcement! Can't wait to collaborate on amazing projects! 🤝",
        "Product update: Users are loving the new features! Thank you for the support! ❤️"
    ]

    negative_templates = [
        "Disappointed with the recent update. Features I need are missing now.",
        "Customer service response time is terrible. Been waiting for hours.",
        "Product quality has declined significantly. Not happy with this purchase.",
        "Pricing is way too high for the features provided. Overpriced.",
        "App keeps crashing. Very frustrating user experience."
    ]

    neutral_templates = [
        "Here's our latest blog post about industry trends. Check it out!",
        "New office location opening next month. Come visit us!",
        "Team meeting today to discuss Q4 strategy and goals.",
        "Updated our privacy policy. Please review the changes.",
        "New team member joined today. Welcome to the family!"
    ]

    platforms = ['twitter', 'linkedin', 'facebook', 'instagram']
    sentiments = ['positive', 'negative', 'neutral']

    posts = []

    for i in range(count):
        sentiment = random.choice(sentiments)

        if sentiment == 'positive':
            content = random.choice(positive_templates)
            sentiment_score = random.uniform(0.6, 1.0)
        elif sentiment == 'negative':
            content = random.choice(negative_templates)
            sentiment_score = random.uniform(-1.0, -0.4)
        else:
            content = random.choice(neutral_templates)
            sentiment_score = random.uniform(-0.3, 0.3)

        # Generate realistic engagement metrics based on sentiment
        base_likes = random.randint(10, 1000)
        if sentiment == 'positive':
            likes = int(base_likes * random.uniform(1.5, 3.0))
            shares = int(likes * random.uniform(0.1, 0.3))
        elif sentiment == 'negative':
            likes = int(base_likes * random.uniform(0.3, 0.8))
            shares = int(likes * random.uniform(0.05, 0.15))
        else:
            likes = base_likes
            shares = int(likes * random.uniform(0.05, 0.2))

        comments = int(likes * random.uniform(0.1, 0.4))
        views = likes * random.randint(5, 20)

        # Generate post data
        post_id = f"sample_{i+1}"
        platform = random.choice(platforms)
        author = f"User{random.randint(1, 1000)}"
        author_id = f"user_{random.randint(1000, 9999)}"

        # Generate URL based on platform
        if platform == 'twitter':
            url = f"https://twitter.com/{author}/status/{post_id}"
        elif platform == 'linkedin':
            url = f"https://linkedin.com/posts/{author}_{post_id}"
        elif platform == 'facebook':
            url = f"https://facebook.com/{author}/posts/{post_id}"
        else:  # instagram
            url = f"https://instagram.com/p/{post_id}"

        # Generate posted_at (last 30 days)
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        posted_at = datetime.datetime.now() - datetime.timedelta(days=days_ago, hours=hours_ago)

        post_data = {
            'platform': platform,
            'post_id': post_id,
            'content': content,
            'author': author,
            'author_id': author_id,
            'url': url,
            'posted_at': posted_at,
            'collected_at': datetime.datetime.now(),
            'likes': likes,
            'shares': shares,
            'comments': comments,
            'views': views,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'topics': ['business', 'technology', 'social-media'],  # Simplified for demo
            'entities': [],
            'language': 'en',
            'user_id': 1  # Default user
        }

        posts.append(post_data)

    return posts

def save_sample_data_to_db(posts):
    """Save generated posts to database"""
    db = next(get_db())

    try:
        imported_count = 0
        for post_data in posts:
            # Check if post already exists
            existing = db.query(SocialPost).filter(
                SocialPost.post_id == post_data['post_id']
            ).first()

            if not existing:
                post = SocialPost(**post_data)
                db.add(post)
                imported_count += 1

        db.commit()
        print(f"Successfully imported {imported_count} sample posts to database")
        return imported_count

    except Exception as e:
        db.rollback()
        print(f"Error saving to database: {e}")
        return 0
    finally:
        db.close()

def main():
    print("Generating sample social media data...")

    # Generate 200 sample posts
    sample_posts = generate_sample_posts(200)

    print(f"Generated {len(sample_posts)} sample posts")

    # Save to database
    imported_count = save_sample_data_to_db(sample_posts)

    print(f"Demo data creation complete! Imported {imported_count} posts.")

    # Show some statistics
    platforms = {}
    sentiments = {}

    for post in sample_posts:
        platforms[post['platform']] = platforms.get(post['platform'], 0) + 1
        sentiments[post['sentiment']] = sentiments.get(post['sentiment'], 0) + 1

    print("\nStatistics:")
    print("Platforms:", platforms)
    print("Sentiments:", sentiments)

if __name__ == "__main__":
    main()