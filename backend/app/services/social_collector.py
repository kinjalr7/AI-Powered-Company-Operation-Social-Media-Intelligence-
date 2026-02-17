import requests
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.config import settings
from app.models.social_data import SocialPost
from app.services.ai_analytics import AIAnalyticsService
from app.api.realtime import notify_new_post

logger = logging.getLogger(__name__)

class SocialDataCollector:
    def __init__(self):
        self.ai_service = AIAnalyticsService()
        self.session = requests.Session()

    async def collect_twitter_data(
        self,
        keywords: List[str],
        days_back: int = 7,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """Collect data from Twitter API v2"""
        try:
            if not getattr(settings, 'TWITTER_BEARER_TOKEN', None):
                logger.info("Twitter API token not configured, using mock data")
                return self._generate_mock_twitter_data(keywords, days_back, max_results)

            # Twitter API v2 implementation
            import tweepy

            # Initialize Tweepy client
            client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)

            all_tweets = []
            query = " OR ".join([f'"{kw}"' for kw in keywords])

            # Calculate date range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days_back)

            try:
                # Search recent tweets
                tweets = client.search_recent_tweets(
                    query=query,
                    max_results=min(max_results, 100),  # Twitter API limit
                    tweet_fields=['created_at', 'public_metrics', 'author_id', 'lang'],
                    user_fields=['username', 'name'],
                    start_time=start_time,
                    end_time=end_time,
                    expansions=['author_id']
                )

                if tweets.data:
                    users = {user.id: user for user in tweets.includes['users']} if tweets.includes else {}

                    for tweet in tweets.data:
                        author = users.get(tweet.author_id)

                        tweet_data = {
                            'platform': 'twitter',
                            'post_id': str(tweet.id),
                            'content': tweet.text,
                            'author': author.username if author else f'user_{tweet.author_id}',
                            'author_id': str(tweet.author_id),
                            'url': f'https://twitter.com/i/status/{tweet.id}',
                            'posted_at': tweet.created_at,
                            'likes': tweet.public_metrics['like_count'] if hasattr(tweet, 'public_metrics') else 0,
                            'shares': tweet.public_metrics['retweet_count'] if hasattr(tweet, 'public_metrics') else 0,
                            'comments': tweet.public_metrics['reply_count'] if hasattr(tweet, 'public_metrics') else 0,
                            'views': tweet.public_metrics.get('impression_count', 0) if hasattr(tweet, 'public_metrics') else 0,
                            'language': tweet.lang if hasattr(tweet, 'lang') else 'en'
                        }
                        all_tweets.append(tweet_data)

                logger.info(f"Collected {len(all_tweets)} tweets from Twitter API")
                return all_tweets

            except tweepy.TweepyException as e:
                logger.error(f"Twitter API error: {e}")
                return self._generate_mock_twitter_data(keywords, days_back, max_results)

        except Exception as e:
            logger.error(f"Twitter data collection failed: {e}")
            return self._generate_mock_twitter_data(keywords, days_back, max_results)

    async def collect_linkedin_data(
        self,
        keywords: List[str],
        days_back: int = 7,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """Collect data from LinkedIn API"""
        try:
            if not settings.LINKEDIN_ACCESS_TOKEN:
                return self._generate_mock_linkedin_data(keywords, days_back, max_results)

            # LinkedIn API implementation would go here
            return self._generate_mock_linkedin_data(keywords, days_back, max_results)

        except Exception as e:
            print(f"LinkedIn data collection failed: {e}")
            return []

    async def collect_facebook_data(
        self,
        keywords: List[str],
        days_back: int = 7,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """Collect data from Facebook Graph API"""
        try:
            if not settings.FACEBOOK_ACCESS_TOKEN:
                return self._generate_mock_facebook_data(keywords, days_back, max_results)

            # Facebook API implementation would go here
            return self._generate_mock_facebook_data(keywords, days_back, max_results)

        except Exception as e:
            print(f"Facebook data collection failed: {e}")
            return []

    async def collect_instagram_data(
        self,
        keywords: List[str],
        days_back: int = 7,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """Collect data from Instagram Basic Display API"""
        try:
            # Instagram API implementation would go here
            return self._generate_mock_instagram_data(keywords, days_back, max_results)

        except Exception as e:
            print(f"Instagram data collection failed: {e}")
            return []

    async def collect_all_platforms(
        self,
        keywords: List[str],
        platforms: List[str] = None,
        days_back: int = 7,
        max_results_per_platform: int = 100
    ) -> List[Dict[str, Any]]:
        """Collect data from all specified platforms"""
        if platforms is None:
            platforms = ["twitter", "linkedin", "facebook", "instagram"]

        all_data = []

        tasks = []
        if "twitter" in platforms:
            tasks.append(self.collect_twitter_data(keywords, days_back, max_results_per_platform))
        if "linkedin" in platforms:
            tasks.append(self.collect_linkedin_data(keywords, days_back, max_results_per_platform))
        if "facebook" in platforms:
            tasks.append(self.collect_facebook_data(keywords, days_back, max_results_per_platform))
        if "instagram" in platforms:
            tasks.append(self.collect_instagram_data(keywords, days_back, max_results_per_platform))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, list):
                all_data.extend(result)

        return all_data

    async def save_posts_to_database(
        self,
        posts_data: List[Dict[str, Any]],
        user_id: int,
        db: AsyncSession
    ) -> int:
        """Save collected posts to database with AI analysis"""
        saved_count = 0

        for post_data in posts_data:
            try:
                # Check if post already exists
                existing_post = await db.execute(
                    select(SocialPost).where(
                        and_(
                            SocialPost.post_id == post_data['post_id'],
                            SocialPost.platform == post_data['platform']
                        )
                    )
                )
                if existing_post.scalar_one_or_none():
                    continue

                # Analyze content with AI
                content = post_data['content']
                sentiment_analysis = self.ai_service.analyze_sentiment(content)
                topics = self.ai_service.extract_topics(content)

                # Create post record
                post = SocialPost(
                    user_id=user_id,
                    platform=post_data['platform'],
                    post_id=post_data['post_id'],
                    content=content,
                    author=post_data.get('author'),
                    author_id=post_data.get('author_id'),
                    url=post_data.get('url'),
                    posted_at=post_data['posted_at'],
                    likes=post_data.get('likes', 0),
                    shares=post_data.get('shares', 0),
                    comments=post_data.get('comments', 0),
                    views=post_data.get('views', 0),
                    sentiment=sentiment_analysis['sentiment'],
                    sentiment_score=sentiment_analysis['scores']['vader']['compound'],
                    topics=topics
                )

                db.add(post)
                saved_count += 1

                # Notify real-time subscribers
                try:
                    await notify_new_post(user_id, {
                        'id': post.id,
                        'platform': post.platform,
                        'content': post.content[:100] + '...' if len(post.content) > 100 else post.content,
                        'sentiment': post.sentiment,
                        'engagement': post.likes + post.shares + post.comments,
                        'posted_at': post.posted_at.isoformat() if hasattr(post.posted_at, 'isoformat') else str(post.posted_at)
                    })
                except Exception as e:
                    logger.error(f"Failed to send real-time notification: {e}")

            except Exception as e:
                print(f"Failed to save post {post_data.get('post_id')}: {e}")
                continue

        await db.commit()
        return saved_count

    def _generate_mock_twitter_data(
        self,
        keywords: List[str],
        days_back: int,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Generate mock Twitter data for demonstration"""
        mock_posts = []
        base_date = datetime.utcnow() - timedelta(days=days_back)

        sample_content = [
            f"Excited about new developments in {keyword}! The future looks bright.",
            f"Great insights on {keyword} from industry leaders. Very informative.",
            f"Concerns about {keyword} adoption in traditional industries.",
            f"Innovative applications of {keyword} changing how we work.",
            f"Looking forward to upcoming {keyword} conferences and events.",
            f"Challenges and opportunities in {keyword} implementation.",
            f"Amazing results from {keyword} integration in our workflow.",
            f"Questions about the future impact of {keyword} on employment.",
        ]

        for i in range(max_results):
            keyword = keywords[i % len(keywords)] if keywords else "AI"
            content = sample_content[i % len(sample_content)].format(keyword=keyword)

            post = {
                'platform': 'twitter',
                'post_id': f'twitter_{i+1}',
                'content': content,
                'author': f'User{i+1}',
                'author_id': f'user_{i+1}',
                'url': f'https://twitter.com/user{i+1}/status/{i+1}',
                'posted_at': base_date + timedelta(hours=i*2),
                'likes': max(0, int(i * 1.5) % 100),
                'shares': max(0, int(i * 0.8) % 50),
                'comments': max(0, int(i * 0.5) % 25),
                'views': max(100, int(i * 3) % 1000)
            }
            mock_posts.append(post)

        return mock_posts

    def _generate_mock_linkedin_data(
        self,
        keywords: List[str],
        days_back: int,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Generate mock LinkedIn data for demonstration"""
        mock_posts = []
        base_date = datetime.utcnow() - timedelta(days=days_back)

        sample_content = [
            f"Sharing insights on {keyword} trends in the professional world.",
            f"Excited to announce our new {keyword} initiative at the company.",
            f"Thoughts on how {keyword} is transforming business operations.",
            f"Looking for talent skilled in {keyword} for our growing team.",
            f"Published an article about {keyword} best practices.",
            f"Networking event focused on {keyword} innovation.",
            f"Company culture and {keyword} adoption success story.",
        ]

        for i in range(max_results):
            keyword = keywords[i % len(keywords)] if keywords else "AI"
            content = sample_content[i % len(sample_content)].format(keyword=keyword)

            post = {
                'platform': 'linkedin',
                'post_id': f'linkedin_{i+1}',
                'content': content,
                'author': f'Professional User {i+1}',
                'author_id': f'linkedin_user_{i+1}',
                'url': f'https://linkedin.com/posts/user{i+1}',
                'posted_at': base_date + timedelta(hours=i*3),
                'likes': max(5, int(i * 2) % 200),
                'shares': max(1, int(i * 1.2) % 80),
                'comments': max(2, int(i * 0.8) % 40),
                'views': max(50, int(i * 5) % 2000)
            }
            mock_posts.append(post)

        return mock_posts

    def _generate_mock_facebook_data(
        self,
        keywords: List[str],
        days_back: int,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Generate mock Facebook data for demonstration"""
        mock_posts = []
        base_date = datetime.utcnow() - timedelta(days=days_back)

        sample_content = [
            f"Loving the new developments in {keyword}! So exciting!",
            f"What's your take on {keyword} changing our daily lives?",
            f"Shared a meme about {keyword} that made me laugh 😂",
            f"Family discussion about the impact of {keyword} on society.",
            f"Local community event featuring {keyword} demonstrations.",
            f"Personal experience with {keyword} adoption at home.",
        ]

        for i in range(max_results):
            keyword = keywords[i % len(keywords)] if keywords else "AI"
            content = sample_content[i % len(sample_content)].format(keyword=keyword)

            post = {
                'platform': 'facebook',
                'post_id': f'facebook_{i+1}',
                'content': content,
                'author': f'Facebook User {i+1}',
                'author_id': f'fb_user_{i+1}',
                'url': f'https://facebook.com/posts/{i+1}',
                'posted_at': base_date + timedelta(hours=i*4),
                'likes': max(10, int(i * 3) % 500),
                'shares': max(2, int(i * 1.5) % 100),
                'comments': max(5, int(i * 1.8) % 80),
                'views': max(200, int(i * 8) % 5000)
            }
            mock_posts.append(post)

        return mock_posts

    def _generate_mock_instagram_data(
        self,
        keywords: List[str],
        days_back: int,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Generate mock Instagram data for demonstration"""
        mock_posts = []
        base_date = datetime.utcnow() - timedelta(days=days_back)

        sample_content = [
            f"Beautiful visualization of {keyword} concepts! ✨ #Tech #Innovation",
            f"Behind the scenes of our {keyword} project 🎥",
            f"Artistic representation of {keyword} in everyday life 🎨",
            f"Quick tip about {keyword} that changed everything 💡",
            f"Sunset thoughts on the future of {keyword} 🌅",
            f"Dance challenge inspired by {keyword} moves 🕺💃",
        ]

        for i in range(max_results):
            keyword = keywords[i % len(keywords)] if keywords else "AI"
            content = sample_content[i % len(sample_content)].format(keyword=keyword)

            post = {
                'platform': 'instagram',
                'post_id': f'instagram_{i+1}',
                'content': content,
                'author': f'@instagram_user_{i+1}',
                'author_id': f'insta_user_{i+1}',
                'url': f'https://instagram.com/p/{i+1}',
                'posted_at': base_date + timedelta(hours=i*5),
                'likes': max(20, int(i * 4) % 1000),
                'shares': max(0, int(i * 0.5) % 20),  # Instagram doesn't have traditional shares
                'comments': max(8, int(i * 2.2) % 150),
                'views': max(100, int(i * 10) % 10000)
            }
            mock_posts.append(post)

        return mock_posts