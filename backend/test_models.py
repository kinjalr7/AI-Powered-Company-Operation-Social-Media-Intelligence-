from app.services.ai_analytics import AIAnalyticsService
import asyncio

def test():
    service = AIAnalyticsService()
    print("Testing sentiment analysis...")
    text = "I love this product, it's amazing!"
    result = service.analyze_sentiment(text)
    print(f"Sentiment: {result['sentiment']}, confidence: {result['confidence']}")
    
    print("\nTesting topic extraction...")
    text = "AI and machine learning are transforming the world of technology and business intelligence."
    topics = service.extract_topics(text)
    print(f"Topics: {topics}")
    
    print("\nTesting summarization...")
    text = "The quick brown fox jumps over the lazy dog. " * 10
    summary = service.summarize_text(text)
    print(f"Summary: {summary}")

if __name__ == "__main__":
    test()
