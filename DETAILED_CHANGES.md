# Detailed Line-by-Line Changes

## File 1: backend/app/services/social_collector.py

### Change 1.1: Twitter Collection - Remove Mock Data Call
**Location**: Line 25  
**Before**:
```python
if not getattr(settings, 'TWITTER_BEARER_TOKEN', None):
    logger.info("Twitter API token not configured, using mock data")
    return self._generate_mock_twitter_data(keywords, days_back, max_results)
```
**After**:
```python
if not getattr(settings, 'TWITTER_BEARER_TOKEN', None):
    logger.info("Twitter API token not configured")
    return []
```

### Change 1.2: Twitter Collection - Remove Mock Data Fallback
**Location**: Line 87-89  
**Before**:
```python
except tweepy.TweepyException as e:
    logger.error(f"Twitter API error: {e}")
    return self._generate_mock_twitter_data(keywords, days_back, max_results)

except Exception as e:
    logger.error(f"Twitter data collection failed: {e}")
    return self._generate_mock_twitter_data(keywords, days_back, max_results)
```
**After**:
```python
except tweepy.TweepyException as e:
    logger.error(f"Twitter API error: {e}")
    return []

except Exception as e:
    logger.error(f"Twitter data collection failed: {e}")
    return []
```

### Change 1.3: LinkedIn Collection - Remove Mock Data
**Location**: Line 92-100  
**Before**:
```python
async def collect_linkedin_data(...) -> List[Dict[str, Any]]:
    """Collect data from LinkedIn API"""
    try:
        if not settings.LINKEDIN_ACCESS_TOKEN:
            return self._generate_mock_linkedin_data(keywords, days_back, max_results)

        # LinkedIn API implementation would go here
        return self._generate_mock_linkedin_data(keywords, days_back, max_results)
```
**After**:
```python
async def collect_linkedin_data(...) -> List[Dict[str, Any]]:
    """Collect data from LinkedIn API"""
    try:
        if not settings.LINKEDIN_ACCESS_TOKEN:
            return []

        # LinkedIn API implementation would go here
        return []
```

### Change 1.4: Facebook Collection - Remove Mock Data
**Location**: Line 110-118  
**Before**:
```python
async def collect_facebook_data(...) -> List[Dict[str, Any]]:
    """Collect data from Facebook Graph API"""
    try:
        if not settings.FACEBOOK_ACCESS_TOKEN:
            return self._generate_mock_facebook_data(keywords, days_back, max_results)

        # Facebook API implementation would go here
        return self._generate_mock_facebook_data(keywords, days_back, max_results)
```
**After**:
```python
async def collect_facebook_data(...) -> List[Dict[str, Any]]:
    """Collect data from Facebook Graph API"""
    try:
        if not settings.FACEBOOK_ACCESS_TOKEN:
            return []

        # Facebook API implementation would go here
        return []
```

### Change 1.5: Instagram Collection - Remove Mock Data
**Location**: Line 128-135  
**Before**:
```python
async def collect_instagram_data(...) -> List[Dict[str, Any]]:
    """Collect data from Instagram Basic Display API"""
    try:
        # Instagram API implementation would go here
        return self._generate_mock_instagram_data(keywords, days_back, max_results)
```
**After**:
```python
async def collect_instagram_data(...) -> List[Dict[str, Any]]:
    """Collect data from Instagram Basic Display API"""
    try:
        # Instagram API implementation would go here
        return []
```

### Change 1.6: Delete Mock Data Generation Functions
**Location**: Lines 244-406  
**Deleted Functions**:
- `_generate_mock_twitter_data()` (40 lines)
- `_generate_mock_linkedin_data()` (40 lines)
- `_generate_mock_facebook_data()` (40 lines)
- `_generate_mock_instagram_data()` (40 lines)

---

## File 2: backend/app/services/ai_analytics.py

### Change 2.1: Delete Keyword Counting Fallback
**Location**: Lines 135-147  
**Before**:
```python
# Very basic keyword-based fallback
if not self.sentiment_analyzer:
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'best', 'awesome']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointed', 'poor', 'sad', 'angry']

    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    if pos_count > neg_count:
        sentiment = 'positive'
        confidence = 0.6
    elif neg_count > pos_count:
        sentiment = 'negative'
        confidence = 0.6
    else:
        sentiment = 'neutral'
        confidence = 0.5
```
**After**:
```python
# Very basic keyword-based fallback
if not self.sentiment_analyzer:
    return {"label": "neutral", "score": 0.0, "error": "analyzer_unavailable"}
```

### Change 2.2: Delete First-3-Sentences Summarizer
**Location**: Lines 186-205  
**Before**:
```python
# Fallback: extract first few sentences
sentences = re.split(r'[.!?]+', text)
summary_sentences = sentences[:3]  # Take first 3 sentences
summary = '. '.join([s.strip() for s in summary_sentences if s.strip()])
return summary + ('.' if summary and not summary.endswith('.') else '')
```
**After**:
```python
# Fallback: return empty string
return ""
```

---

## File 3: backend/app/services/social_poster.py

### Change 3.1-3.6: Delete Mock Account Verification Functions
**Location**: Lines 172-291  

**Before** (6 functions with mock data):
```python
async def _verify_twitter_account(self, account: SocialAccount) -> Dict[str, Any]:
    """Verify Twitter account connection"""
    try:
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {account.access_token}",
            "Content-Type": "application/json"
        }
        return {
            "verified": True,
            "message": "Twitter account verified successfully",
            "account_id": account.account_id or "1234567890",
            "username": account.username or "demo_user",
            "display_name": account.display_name or "Demo User",
            "follower_count": 15420,
            "following_count": 892
        }
    except Exception as e:
        return {
            "verified": False,
            "message": f"Twitter verification failed: {str(e)}"
        }

async def _verify_instagram_account(self, account: SocialAccount) -> Dict[str, Any]:
    """Verify Instagram account connection"""
    try:
        return {
            "verified": True,
            "message": "Instagram account verified successfully",
            "account_id": account.account_id or "1234567890",
            "username": account.username or "demo_user",
            "display_name": account.display_name or "Demo User",
            "follower_count": 25680,
            "following_count": 1240
        }
    except Exception as e:
        return {
            "verified": False,
            "message": f"Instagram verification failed: {str(e)}"
        }

# ... 4 more similar functions for Facebook, LinkedIn, YouTube, TikTok
```

**After** (6 functions replaced):
```python
async def _verify_twitter_account(self, account: SocialAccount) -> Dict[str, Any]:
    """Verify Twitter account connection"""
    return {"verified": False, "error": "not_implemented"}

async def _verify_instagram_account(self, account: SocialAccount) -> Dict[str, Any]:
    """Verify Instagram account connection"""
    return {"verified": False, "error": "not_implemented"}

async def _verify_facebook_account(self, account: SocialAccount) -> Dict[str, Any]:
    """Verify Facebook account connection"""
    return {"verified": False, "error": "not_implemented"}

async def _verify_linkedin_account(self, account: SocialAccount) -> Dict[str, Any]:
    """Verify LinkedIn account connection"""
    return {"verified": False, "error": "not_implemented"}

async def _verify_youtube_account(self, account: SocialAccount) -> Dict[str, Any]:
    """Verify YouTube account connection"""
    return {"verified": False, "error": "not_implemented"}

async def _verify_tiktok_account(self, account: SocialAccount) -> Dict[str, Any]:
    """Verify TikTok account connection"""
    return {"verified": False, "error": "not_implemented"}
```

### Change 3.7: Delete Hardcoded Account Stats
**Location**: Lines 430-445  
**Before**:
```python
async def get_account_stats(self, account: SocialAccount) -> Dict[str, Any]:
    """Get account statistics"""
    try:
        base_stats = {
            "follower_count": account.follower_count,
            "following_count": account.following_count,
            "total_posts": 0,
            "recent_engagement": 0,
            "last_updated": datetime.utcnow().isoformat()
        }

        if account.platform == "twitter":
            base_stats.update({
                "total_tweets": 1250,
                "recent_likes": 450,
                "recent_retweets": 89
            })
        elif account.platform == "instagram":
            base_stats.update({
                "total_posts": 890,
                "recent_likes": 1250,
                "recent_comments": 234
            })
        elif account.platform == "facebook":
            base_stats.update({
                "total_posts": 567,
                "recent_likes": 890,
                "recent_shares": 45
            })

        return base_stats

    except Exception as e:
        return {
            "error": f"Failed to get account stats: {str(e)}"
        }
```
**After**:
```python
async def get_account_stats(self, account: SocialAccount) -> Dict[str, Any]:
    """Get account statistics"""
    return {"error": "not_implemented"}
```

---

## File 4: backend/app/services/user_social_analytics.py

### Change 4.1-4.8: Delete Mock Platform Analysis Functions
**Location**: Lines 59-191  

**Before** (8 functions with mock data):
```python
def _analyze_twitter_profile(self, handle: str) -> Dict[str, Any]:
    """Analyze Twitter profile (mock implementation - would use Twitter API)"""
    try:
        return {
            'handle': handle,
            'follower_estimate': self._estimate_followers(handle, 'twitter'),
            'activity_level': 'high' if len(handle) > 10 else 'medium',
            'content_focus': self._analyze_handle_content(handle),
            'engagement_rate': 0.05,
            'recent_posts': 25,
            'sentiment_score': 0.7,
            'topics': ['technology', 'social media', 'AI'],
            'status': 'success'
        }
    except Exception as e:
        return {'error': str(e), 'status': 'failed'}

# ... 7 more similar functions
```

**After** (8 functions replaced):
```python
def _analyze_twitter_profile(self, handle: str) -> Dict[str, Any]:
    """Analyze Twitter profile (mock implementation - would use Twitter API)"""
    return {"error": "not_implemented"}

def _analyze_linkedin_profile(self, profile_url: str) -> Dict[str, Any]:
    """Analyze LinkedIn profile (mock implementation)"""
    return {"error": "not_implemented"}

def _analyze_facebook_profile(self, profile_url: str) -> Dict[str, Any]:
    """Analyze Facebook profile (mock implementation)"""
    return {"error": "not_implemented"}

def _analyze_instagram_profile(self, handle: str) -> Dict[str, Any]:
    """Analyze Instagram profile (mock implementation)"""
    return {"error": "not_implemented"}

def _analyze_youtube_channel(self, channel_url: str) -> Dict[str, Any]:
    """Analyze YouTube channel (mock implementation)"""
    return {"error": "not_implemented"}

def _analyze_tiktok_profile(self, handle: str) -> Dict[str, Any]:
    """Analyze TikTok profile (mock implementation)"""
    return {"error": "not_implemented"}

def _estimate_followers(self, handle: str, platform: str) -> int:
    """Estimate follower count based on handle characteristics"""
    return 0

def _estimate_subscribers(self, channel_name: str) -> int:
    """Estimate YouTube subscribers"""
    return 0
```

---

## File 5: backend/app/api/social_data.py

### Change 5.1: Delete Hardcoded Monitoring Status
**Location**: Lines 272-277  
**Before**:
```python
@router.get("/monitoring/status")
async def get_monitoring_status(current_user = Depends(get_current_user)):
    """Get the status of social media monitoring"""
    return {
        "monitoring_active": True,  # This would check actual monitoring status
        "last_collection": datetime.utcnow() - timedelta(hours=2),  # Mock last collection time
        "platforms_monitored": ["twitter", "linkedin", "facebook", "instagram"],
        "keywords_tracked": ["AI", "machine learning", "technology", "business intelligence"],
        "total_posts_collected": 15432  # Mock number
    }
```
**After**:
```python
@router.get("/monitoring/status")
async def get_monitoring_status(current_user = Depends(get_current_user)):
    """Get the status of social media monitoring"""
    return {
        "data": [],
        "message": "No data available."
    }
```

---

## File 6: backend/app/services/scheduler.py

### Change 6.1: Delete Skipped Alert Logic
**Location**: Lines 182-184  
**Before**:
```python
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
```
**After**:
```python
async def _check_user_alerts(self, user_dict: Dict[str, Any], db: AsyncSession):
    """Check alerts for a specific user"""
    try:
        pass

    except Exception as e:
        print(f"Alert check failed for user {user_dict['id']}: {e}")
```

---

## File 7: backend/app/main_demo.py

### Change 7.1: Delete Entire File
**Status**: DELETED  
**Lines Removed**: 300+  
**Content**: Complete demo API server with mock endpoints

---

## File 8: backend/app/demo_social_data.py

### Change 8.1: Delete Entire File
**Status**: DELETED  
**Lines Removed**: 400+  
**Content**: Deterministic demo dataset generation module

---

## File 9: backend/init_db.py

### Change 9.1: Delete Demo User Insertion
**Location**: Lines 35-50  
**Before**:
```python
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
```
**After**: DELETED

### Change 9.2: Delete Sample Posts Insertion
**Location**: Lines 52-95  
**Before**:
```python
# Create sample social posts
sample_posts = [
    {
        "platform": "twitter",
        "post_id": "sample_1",
        "content": "Excited about the new AI developments...",
        ...
    },
    ...
]

for post_data in sample_posts:
    post = SocialPost(**post_data)
    db.add(post)

db.commit()
```
**After**: DELETED

### Change 9.3: Update Success Message
**Location**: Line 97  
**Before**:
```python
print("✓ Sample data created successfully")
print("\n🎉 Database initialization completed successfully!")
print("\nNext steps:")
print("1. Start the backend server: python -m app.main")
print("2. Start the frontend: cd frontend && npm run dev")
print("3. Visit http://localhost:3000 to access the application")
print("\nDemo accounts:")
print("- demo@example.com / demo123")
print("- admin@example.com / admin123")
```
**After**:
```python
print("✓ Database tables created successfully")
print("\n🎉 Database initialization completed successfully!")
print("\nNext steps:")
print("1. Start the backend server: python -m app.main")
print("2. Start the frontend: cd frontend && npm run dev")
print("3. Visit http://localhost:3000 to access the application")
```

---

## File 10: backend/create_sample_data.py

### Change 10.1: Replace Entire File Content
**Before**: 150+ lines of sample post generation logic  
**After**:
```python
#!/usr/bin/env python3
"""
Script to create sample social media data for demonstration
This file is deprecated - no demo data should be created.
"""

def main():
    print("Demo data creation is disabled. Use real data collection instead.")

if __name__ == "__main__":
    main()
```

---

## Summary of Changes

| File | Changes | Type |
|------|---------|------|
| social_collector.py | 5 replacements + 4 function deletions | Deletion |
| ai_analytics.py | 2 replacements | Deletion |
| social_poster.py | 7 replacements | Deletion |
| user_social_analytics.py | 8 replacements | Deletion |
| social_data.py | 1 replacement | Deletion |
| scheduler.py | 1 replacement | Deletion |
| main_demo.py | File deleted | Deletion |
| demo_social_data.py | File deleted | Deletion |
| init_db.py | 2 deletions + 1 update | Deletion |
| create_sample_data.py | Complete rewrite | Deprecation |

**Total**: 10 files modified, 2 files deleted, 1,200+ lines removed
