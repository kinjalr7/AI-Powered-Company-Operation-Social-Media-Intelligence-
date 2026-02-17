import os
from typing import List, Dict, Any, Optional
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

from app.core.config import settings

# Try to import NLTK components, fall back gracefully
try:
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    HAS_NLTK = True
    try:
        # Disable SSL verification for NLTK downloads (common in corporate environments)
        import ssl
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    except Exception as e:
        print(f"Warning: NLTK download failed: {e}. Sentiment analysis will use fallback methods.")
        pass
except ImportError:
    HAS_NLTK = False

class AIAnalyticsService:
    def __init__(self):
        # Lazy loading - models will be loaded when first needed
        self._sentiment_analyzer = None
        self._sentiment_pipeline = None
        self._summarizer = None

    @property
    def sentiment_analyzer(self):
        if self._sentiment_analyzer is None and HAS_NLTK:
            try:
                self._sentiment_analyzer = SentimentIntensityAnalyzer()
            except Exception as e:
                print(f"Warning: Could not load NLTK sentiment analyzer: {e}")
                self._sentiment_analyzer = False  # Mark as tried and failed
        return self._sentiment_analyzer if self._sentiment_analyzer else None

    @property
    def sentiment_pipeline(self):
        if self._sentiment_pipeline is None:
            try:
                self._sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    top_k=None  # Updated parameter
                )
            except Exception as e:
                print(f"Warning: Could not load transformer sentiment model: {e}")
                self._sentiment_pipeline = False  # Mark as tried and failed
        return self._sentiment_pipeline if self._sentiment_pipeline else None

    @property
    def summarizer(self):
        if self._summarizer is None:
            try:
                self._summarizer = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    tokenizer="facebook/bart-large-cnn"
                )
            except Exception as e:
                print(f"Warning: Could not load summarization model: {e}")
                self._summarizer = False  # Mark as tried and failed
        return self._summarizer if self._summarizer else None

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text using available methods"""
        transformer_scores = None
        vader_scores = {'compound': 0.0, 'pos': 0.0, 'neu': 0.5, 'neg': 0.0}

        # Transformer-based sentiment (if available)
        if self.sentiment_pipeline:
            try:
                # Truncate text if too long for the model
                truncated_text = text[:512] if len(text) > 512 else text
                transformer_scores = self.sentiment_pipeline(truncated_text)
            except Exception as e:
                print(f"Transformer sentiment analysis failed: {e}")

        # VADER sentiment (if available)
        if self.sentiment_analyzer:
            try:
                vader_scores = self.sentiment_analyzer.polarity_scores(text)
            except Exception as e:
                print(f"VADER sentiment analysis failed: {e}")

        # Determine overall sentiment
        sentiment = 'neutral'
        confidence = 0.5

        # Use transformer results if available
        if transformer_scores and len(transformer_scores[0]) >= 3:
            # Map transformer labels to our sentiment categories
            scores_dict = {item['label'].lower(): item['score'] for item in transformer_scores[0]}
            transformer_sentiment = max(scores_dict, key=scores_dict.get)
            transformer_confidence = max(scores_dict.values())

            sentiment = transformer_sentiment
            confidence = transformer_confidence
        else:
            # Fall back to VADER or simple keyword analysis
            compound_score = vader_scores['compound']
            if compound_score >= 0.05:
                sentiment = 'positive'
            elif compound_score <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            confidence = abs(compound_score)

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

        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'scores': {
                'vader': vader_scores,
                'transformer': transformer_scores
            }
        }

    def extract_topics(self, text: str, max_topics: int = 5) -> List[str]:
        """Extract key topics/themes from text"""
        # Simple word frequency analysis
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her'
        ])

        filtered_words = [word for word in words if len(word) > 3 and word.isalnum() and word not in stop_words]

        # Count word frequency
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Return top topics
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_topics]]

    def summarize_text(self, text: str, max_length: int = 150) -> str:
        """Summarize text using transformer model or fallback method"""
        if self.summarizer and len(text) > 100:
            try:
                # Truncate input if too long
                max_input_length = 1024
                if len(text) > max_input_length:
                    text = text[:max_input_length]

                summary_result = self.summarizer(
                    text,
                    max_length=max_length,
                    min_length=max(30, max_length // 4),
                    do_sample=False
                )
                return summary_result[0]['summary_text'].strip()
            except Exception as e:
                print(f"Transformer summarization failed: {e}")

        # Fallback: extract first few sentences
        sentences = re.split(r'[.!?]+', text)
        summary_sentences = sentences[:3]  # Take first 3 sentences
        summary = '. '.join([s.strip() for s in summary_sentences if s.strip()])
        return summary + ('.' if summary and not summary.endswith('.') else '')

    def generate_insights(self, posts_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive insights from social media posts"""
        if not posts_data:
            return {"error": "No data provided"}

        # Analyze all posts
        sentiments = []
        topics = []
        platforms = {}
        engagement_total = 0

        for post in posts_data:
            # Sentiment analysis
            content = post.get('content', '')
            sentiment_result = self.analyze_sentiment(content)
            sentiments.append(sentiment_result)

            # Topic extraction
            post_topics = self.extract_topics(content)
            topics.extend(post_topics)

            # Platform stats
            platform = post.get('platform', 'unknown')
            platforms[platform] = platforms.get(platform, 0) + 1

            # Engagement
            engagement_total += post.get('likes', 0) + post.get('shares', 0) + post.get('comments', 0)

        # Aggregate results
        sentiment_counts = {}
        for s in sentiments:
            sent = s['sentiment']
            sentiment_counts[sent] = sentiment_counts.get(sent, 0) + 1

        # Find top topics
        topic_freq = {}
        for topic in topics:
            topic_freq[topic] = topic_freq.get(topic, 0) + 1

        top_topics = sorted(topic_freq.items(), key=lambda x: x[1], reverse=True)[:10]

        insights = {
            'total_posts': len(posts_data),
            'sentiment_distribution': sentiment_counts,
            'platform_breakdown': platforms,
            'total_engagement': engagement_total,
            'avg_engagement_per_post': engagement_total / len(posts_data) if posts_data else 0,
            'top_topics': top_topics,
            'sentiment_trend': self._calculate_sentiment_trend(sentiments),
            'recommendations': self._generate_recommendations(sentiment_counts, platforms, top_topics)
        }

        return insights

    def _calculate_sentiment_trend(self, sentiments: List[Dict[str, Any]]) -> str:
        """Calculate sentiment trend"""
        if len(sentiments) < 2:
            return "insufficient_data"

        recent_sentiments = sentiments[-10:]  # Last 10 posts
        avg_sentiment = sum(s['scores']['vader']['compound'] for s in recent_sentiments) / len(recent_sentiments)

        if avg_sentiment > 0.1:
            return "improving"
        elif avg_sentiment < -0.1:
            return "declining"
        else:
            return "stable"

    def _generate_recommendations(self, sentiment_counts: Dict[str, int],
                                platforms: Dict[str, int],
                                top_topics: List[tuple]) -> List[str]:
        """Generate AI-powered recommendations"""
        recommendations = []

        total_posts = sum(sentiment_counts.values())

        if total_posts > 0:
            positive_pct = (sentiment_counts.get('positive', 0) / total_posts) * 100
            negative_pct = (sentiment_counts.get('negative', 0) / total_posts) * 100

            if positive_pct > 70:
                recommendations.append("Maintain current positive engagement strategies")
            elif negative_pct > 30:
                recommendations.append("Address customer concerns and improve service quality")

            # Platform recommendations
            top_platform = max(platforms.items(), key=lambda x: x[1])[0]
            recommendations.append(f"Focus content strategy on {top_platform} for maximum reach")

            # Topic recommendations
            if top_topics:
                top_topic = top_topics[0][0]
                recommendations.append(f"Create more content around '{top_topic}' as it's trending")

        return recommendations

    def generate_business_report(self, insights: Dict[str, Any], time_period: str = "daily") -> str:
        """Generate a comprehensive business report"""
        # Use template-based report generation
        return self._generate_template_report(insights, time_period)

    def _generate_template_report(self, insights: Dict[str, Any], time_period: str) -> str:
        """Generate a basic report when LLM is not available"""
        report = f"""
# AI Social Intelligence {time_period.title()} Report

## Executive Summary
This report provides insights from {insights.get('total_posts', 0)} social media posts analyzed during the {time_period} period.

## Key Metrics
- Total Posts Analyzed: {insights.get('total_posts', 0)}
- Total Engagement: {insights.get('total_engagement', 0)}
- Average Engagement per Post: {insights.get('avg_engagement_per_post', 0):.1f}

## Sentiment Analysis
{self._format_sentiment_section(insights.get('sentiment_distribution', {}))}

## Platform Performance
{self._format_platform_section(insights.get('platform_breakdown', {}))}

## Top Topics
{self._format_topics_section(insights.get('top_topics', []))}

## Recommendations
{chr(10).join(f"- {rec}" for rec in insights.get('recommendations', []))}

---
*Generated automatically by AI Social Intelligence System*
        """.strip()

        return report

    def _format_sentiment_section(self, sentiment_dist: Dict[str, int]) -> str:
        """Format sentiment distribution for report"""
        total = sum(sentiment_dist.values())
        if total == 0:
            return "No sentiment data available."

        lines = []
        for sentiment, count in sentiment_dist.items():
            percentage = (count / total) * 100
            lines.append(f"- {sentiment.title()}: {count} posts ({percentage:.1f}%)")

        return "\n".join(lines)

    def _format_platform_section(self, platform_dist: Dict[str, int]) -> str:
        """Format platform breakdown for report"""
        if not platform_dist:
            return "No platform data available."

        lines = []
        for platform, count in platform_dist.items():
            lines.append(f"- {platform.title()}: {count} posts")

        return "\n".join(lines)

    def _format_topics_section(self, topics: List[tuple]) -> str:
        """Format top topics for report"""
        if not topics:
            return "No topic data available."

        lines = []
        for topic, count in topics[:5]:  # Top 5 topics
            lines.append(f"- {topic}: {count} mentions")

        return "\n".join(lines)