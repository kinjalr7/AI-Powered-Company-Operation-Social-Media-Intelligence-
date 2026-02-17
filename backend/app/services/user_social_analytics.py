import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re
import json

from app.core.config import settings
from app.services.ai_analytics import AIAnalyticsService

class UserSocialAnalyticsService:
    def __init__(self):
        self.ai_service = AIAnalyticsService()
        self.twitter_api_key = getattr(settings, 'TWITTER_API_KEY', None)
        self.twitter_api_secret = getattr(settings, 'TWITTER_API_SECRET', None)
        self.linkedin_access_token = getattr(settings, 'LINKEDIN_ACCESS_TOKEN', None)
        self.facebook_access_token = getattr(settings, 'FACEBOOK_ACCESS_TOKEN', None)
        self.instagram_access_token = getattr(settings, 'INSTAGRAM_ACCESS_TOKEN', None)

    def analyze_user_social_presence(self, user_profiles: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze user's social media presence across all platforms
        Returns comprehensive analysis report
        """
        analysis_results = {}

        # Analyze each platform
        if user_profiles.get('twitter_handle'):
            analysis_results['twitter'] = self._analyze_twitter_profile(user_profiles['twitter_handle'])

        if user_profiles.get('linkedin_profile'):
            analysis_results['linkedin'] = self._analyze_linkedin_profile(user_profiles['linkedin_profile'])

        if user_profiles.get('facebook_profile'):
            analysis_results['facebook'] = self._analyze_facebook_profile(user_profiles['facebook_profile'])

        if user_profiles.get('instagram_handle'):
            analysis_results['instagram'] = self._analyze_instagram_profile(user_profiles['instagram_handle'])

        if user_profiles.get('youtube_channel'):
            analysis_results['youtube'] = self._analyze_youtube_channel(user_profiles['youtube_channel'])

        if user_profiles.get('tiktok_handle'):
            analysis_results['tiktok'] = self._analyze_tiktok_profile(user_profiles['tiktok_handle'])

        # Generate overall analysis
        overall_analysis = self._generate_overall_analysis(analysis_results)

        return {
            'platform_analyses': analysis_results,
            'overall_analysis': overall_analysis,
            'generated_at': datetime.utcnow().isoformat(),
            'recommendations': self._generate_personal_recommendations(overall_analysis)
        }

    def _analyze_twitter_profile(self, handle: str) -> Dict[str, Any]:
        """Analyze Twitter profile (mock implementation - would use Twitter API)"""
        try:
            # In a real implementation, this would call Twitter API
            # For now, return mock data based on handle analysis
            return {
                'handle': handle,
                'follower_estimate': self._estimate_followers(handle, 'twitter'),
                'activity_level': 'high' if len(handle) > 10 else 'medium',
                'content_focus': self._analyze_handle_content(handle),
                'engagement_rate': 0.05,  # 5%
                'recent_posts': 25,
                'sentiment_score': 0.7,
                'topics': ['technology', 'social media', 'AI'],
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}

    def _analyze_linkedin_profile(self, profile_url: str) -> Dict[str, Any]:
        """Analyze LinkedIn profile (mock implementation)"""
        try:
            handle = self._extract_handle_from_url(profile_url, 'linkedin')
            return {
                'profile_url': profile_url,
                'handle': handle,
                'connections_estimate': 500,
                'profile_completeness': 85,  # percentage
                'industry': 'Technology',
                'experience_level': 'Senior',
                'content_frequency': 'weekly',
                'network_strength': 'strong',
                'endorsements': 45,
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}

    def _analyze_facebook_profile(self, profile_url: str) -> Dict[str, Any]:
        """Analyze Facebook profile (mock implementation)"""
        try:
            handle = self._extract_handle_from_url(profile_url, 'facebook')
            return {
                'profile_url': profile_url,
                'handle': handle,
                'friends_count': 350,
                'posts_frequency': 'daily',
                'engagement_rate': 0.08,
                'content_type': 'mixed',
                'privacy_settings': 'moderate',
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}

    def _analyze_instagram_profile(self, handle: str) -> Dict[str, Any]:
        """Analyze Instagram profile (mock implementation)"""
        try:
            return {
                'handle': handle,
                'follower_count': self._estimate_followers(handle, 'instagram'),
                'following_count': 200,
                'posts_count': 150,
                'engagement_rate': 0.06,
                'content_style': 'visual',
                'hashtags_used': ['tech', 'ai', 'socialmedia'],
                'story_frequency': 'daily',
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}

    def _analyze_youtube_channel(self, channel_url: str) -> Dict[str, Any]:
        """Analyze YouTube channel (mock implementation)"""
        try:
            channel_name = self._extract_channel_name(channel_url)
            return {
                'channel_url': channel_url,
                'channel_name': channel_name,
                'subscriber_count': self._estimate_subscribers(channel_name),
                'video_count': 45,
                'total_views': 150000,
                'avg_views_per_video': 3333,
                'upload_frequency': 'weekly',
                'content_category': 'Technology',
                'engagement_rate': 0.04,
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}

    def _analyze_tiktok_profile(self, handle: str) -> Dict[str, Any]:
        """Analyze TikTok profile (mock implementation)"""
        try:
            return {
                'handle': handle,
                'follower_count': self._estimate_followers(handle, 'tiktok'),
                'following_count': 150,
                'video_count': 80,
                'total_likes': 25000,
                'avg_likes_per_video': 312,
                'content_style': 'short_form',
                'trending_score': 7.5,  # out of 10
                'viral_potential': 'high',
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}

    def _estimate_followers(self, handle: str, platform: str) -> int:
        """Estimate follower count based on handle characteristics"""
        base_score = len(handle) * 10  # Simple heuristic

        # Platform multipliers
        multipliers = {
            'twitter': 1.2,
            'instagram': 1.5,
            'tiktok': 0.8,
            'facebook': 1.0
        }

        return int(base_score * multipliers.get(platform, 1.0))

    def _estimate_subscribers(self, channel_name: str) -> int:
        """Estimate YouTube subscribers"""
        return len(channel_name) * 50  # Simple heuristic

    def _extract_handle_from_url(self, url: str, platform: str) -> str:
        """Extract handle/username from social media URL"""
        if platform == 'linkedin':
            match = re.search(r'linkedin\.com/in/([^/]+)', url)
            return match.group(1) if match else 'unknown'
        elif platform == 'facebook':
            match = re.search(r'facebook\.com/([^/]+)', url)
            return match.group(1) if match else 'unknown'
        return 'unknown'

    def _extract_channel_name(self, url: str) -> str:
        """Extract YouTube channel name from URL"""
        match = re.search(r'youtube\.com/(?:c|channel|user)/([^/?]+)', url)
        return match.group(1) if match else 'unknown'

    def _analyze_handle_content(self, handle: str) -> str:
        """Analyze what type of content the handle suggests"""
        tech_keywords = ['tech', 'ai', 'dev', 'code', 'data', 'digital']
        business_keywords = ['biz', 'corp', 'enter', 'ventures', 'group']
        creative_keywords = ['art', 'design', 'photo', 'video', 'music']

        handle_lower = handle.lower()

        if any(keyword in handle_lower for keyword in tech_keywords):
            return 'technology'
        elif any(keyword in handle_lower for keyword in business_keywords):
            return 'business'
        elif any(keyword in handle_lower for keyword in creative_keywords):
            return 'creative'
        else:
            return 'general'

    def _generate_overall_analysis(self, platform_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall analysis across all platforms"""
        successful_analyses = [result for result in platform_results.values() if result.get('status') == 'success']

        if not successful_analyses:
            return {'error': 'No successful platform analyses'}

        total_followers = 0
        total_engagement = 0
        platforms_active = len(successful_analyses)
        content_categories = []
        engagement_rates = []

        for result in successful_analyses:
            # Sum up followers/subscribers
            if 'follower_count' in result:
                total_followers += result['follower_count']
            elif 'subscriber_count' in result:
                total_followers += result['subscriber_count']
            elif 'friends_count' in result:
                total_followers += result['friends_count']

            # Collect engagement rates
            if 'engagement_rate' in result:
                engagement_rates.append(result['engagement_rate'])

            # Collect content categories
            if 'content_focus' in result:
                content_categories.append(result['content_focus'])
            elif 'content_category' in result:
                content_categories.append(result['content_category'])
            elif 'content_style' in result:
                content_categories.append(result['content_style'])

        avg_engagement_rate = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0
        primary_category = max(set(content_categories), key=content_categories.count) if content_categories else 'mixed'

        return {
            'total_followers': total_followers,
            'platforms_active': platforms_active,
            'avg_engagement_rate': avg_engagement_rate,
            'primary_content_category': primary_category,
            'social_presence_score': self._calculate_presence_score(total_followers, platforms_active, avg_engagement_rate),
            'engagement_level': self._categorize_engagement(avg_engagement_rate),
            'content_consistency': self._analyze_content_consistency(content_categories)
        }

    def _calculate_presence_score(self, followers: int, platforms: int, engagement: float) -> float:
        """Calculate overall social presence score (0-100)"""
        follower_score = min(followers / 1000, 1.0) * 40  # Max 40 points
        platform_score = min(platforms / 6, 1.0) * 30      # Max 30 points
        engagement_score = engagement * 30                  # Max 30 points

        return follower_score + platform_score + engagement_score

    def _categorize_engagement(self, rate: float) -> str:
        """Categorize engagement level"""
        if rate >= 0.08:
            return 'high'
        elif rate >= 0.04:
            return 'medium'
        else:
            return 'low'

    def _analyze_content_consistency(self, categories: List[str]) -> str:
        """Analyze how consistent content is across platforms"""
        if len(set(categories)) == 1:
            return 'highly_consistent'
        elif len(set(categories)) <= 2:
            return 'moderately_consistent'
        else:
            return 'diverse'

    def _generate_personal_recommendations(self, overall_analysis: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations based on analysis"""
        recommendations = []

        presence_score = overall_analysis.get('social_presence_score', 0)
        engagement_level = overall_analysis.get('engagement_level', 'low')
        platforms_active = overall_analysis.get('platforms_active', 0)
        content_consistency = overall_analysis.get('content_consistency', 'diverse')

        # Presence score recommendations
        if presence_score < 30:
            recommendations.append("Build your social media presence by consistently posting quality content")
        elif presence_score < 70:
            recommendations.append("Your social presence is growing - focus on engagement to accelerate growth")

        # Engagement recommendations
        if engagement_level == 'low':
            recommendations.append("Increase engagement by asking questions and responding to comments promptly")
        elif engagement_level == 'high':
            recommendations.append("Maintain your high engagement levels - they're working well for you!")

        # Platform recommendations
        if platforms_active < 3:
            recommendations.append("Consider expanding to more social platforms to reach different audiences")
        elif platforms_active >= 5:
            recommendations.append("You're active on many platforms - ensure you have enough time to engage meaningfully on each")

        # Content consistency recommendations
        if content_consistency == 'diverse':
            recommendations.append("Consider creating more consistent branding across your social platforms")
        elif content_consistency == 'highly_consistent':
            recommendations.append("Your consistent branding is strong - keep it up!")

        return recommendations

    def generate_personal_report(self, user_analysis: Dict[str, Any], user_name: str = "User") -> str:
        """Generate a comprehensive personal social media analysis report"""
        platform_analyses = user_analysis.get('platform_analyses', {})
        overall_analysis = user_analysis.get('overall_analysis', {})

        report = f"""
# Personal Social Media Analysis Report

**Generated for: {user_name}**
**Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}**

## Executive Summary

Your social media presence spans {overall_analysis.get('platforms_active', 0)} platforms with a total reach of approximately {overall_analysis.get('total_followers', 0):,} followers/subscribers.

**Social Presence Score: {overall_analysis.get('social_presence_score', 0):.1f}/100**
**Engagement Level: {overall_analysis.get('engagement_level', 'unknown').title()}**
**Content Focus: {overall_analysis.get('primary_content_category', 'mixed').title()}**

## Platform-by-Platform Analysis

"""

        for platform, analysis in platform_analyses.items():
            if analysis.get('status') == 'success':
                report += self._format_platform_report(platform, analysis)

        report += f"""
## Overall Performance Metrics

- **Total Reach**: {overall_analysis.get('total_followers', 0):,} followers/subscribers
- **Platforms Active**: {overall_analysis.get('platforms_active', 0)}
- **Average Engagement Rate**: {overall_analysis.get('avg_engagement_rate', 0):.1%}
- **Content Consistency**: {overall_analysis.get('content_consistency', 'unknown').replace('_', ' ').title()}

## Personalized Recommendations

"""

        recommendations = user_analysis.get('recommendations', [])
        if recommendations:
            for rec in recommendations:
                report += f"- {rec}\n"
        else:
            report += "- Continue building your social media presence with consistent, quality content\n"

        report += """

## Next Steps

1. **Review your content strategy** - Ensure it aligns with your goals
2. **Focus on engagement** - Respond to comments and build relationships
3. **Track your progress** - Monitor these metrics monthly
4. **Stay consistent** - Regular posting builds stronger connections

---
*This report was generated automatically by AI Social Intelligence System*
"""

        return report.strip()

    def _format_platform_report(self, platform: str, analysis: Dict[str, Any]) -> str:
        """Format individual platform analysis for report"""
        platform_name = platform.title()

        if platform == 'twitter':
            return f"""
### {platform_name} (@{analysis.get('handle', 'unknown')})
- **Followers**: ~{analysis.get('follower_estimate', 0)}
- **Activity Level**: {analysis.get('activity_level', 'unknown').title()}
- **Content Focus**: {analysis.get('content_focus', 'unknown').title()}
- **Engagement Rate**: {analysis.get('engagement_rate', 0):.1%}
- **Recent Posts**: {analysis.get('recent_posts', 0)}

"""
        elif platform == 'linkedin':
            return f"""
### {platform_name} ({analysis.get('handle', 'unknown')})
- **Profile Completeness**: {analysis.get('profile_completeness', 0)}%
- **Industry**: {analysis.get('industry', 'unknown')}
- **Experience Level**: {analysis.get('experience_level', 'unknown')}
- **Content Frequency**: {analysis.get('content_frequency', 'unknown')}
- **Network Strength**: {analysis.get('network_strength', 'unknown').title()}

"""
        elif platform == 'instagram':
            return f"""
### {platform_name} (@{analysis.get('handle', 'unknown')})
- **Followers**: {analysis.get('follower_count', 0)}
- **Following**: {analysis.get('following_count', 0)}
- **Total Posts**: {analysis.get('posts_count', 0)}
- **Engagement Rate**: {analysis.get('engagement_rate', 0):.1%}
- **Content Style**: {analysis.get('content_style', 'unknown').title()}

"""
        elif platform == 'youtube':
            return f"""
### {platform_name} ({analysis.get('channel_name', 'unknown')})
- **Subscribers**: {analysis.get('subscriber_count', 0)}
- **Total Videos**: {analysis.get('video_count', 0)}
- **Total Views**: {analysis.get('total_views', 0):,}
- **Average Views/Video**: {analysis.get('avg_views_per_video', 0):,}
- **Upload Frequency**: {analysis.get('upload_frequency', 'unknown')}

"""
        elif platform == 'tiktok':
            return f"""
### {platform_name} (@{analysis.get('handle', 'unknown')})
- **Followers**: {analysis.get('follower_count', 0)}
- **Total Videos**: {analysis.get('video_count', 0)}
- **Total Likes**: {analysis.get('total_likes', 0):,}
- **Average Likes/Video**: {analysis.get('avg_likes_per_video', 0)}
- **Viral Potential**: {analysis.get('viral_potential', 'unknown').title()}

"""
        else:
            return f"""
### {platform_name}
- Analysis data available but formatting not implemented

"""