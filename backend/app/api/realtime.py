from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from typing import Dict, List, Any
import json
import asyncio
import logging
from datetime import datetime

# WebSocket authentication dependency
from app.services.ai_analytics import AIAnalyticsService
from app.core.database import get_db
from app.models.social_data import SocialPost, AnalyticsData

logger = logging.getLogger(__name__)

router = APIRouter()

# Global connection manager for WebSocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"User {user_id} disconnected. Remaining connections: {len(self.active_connections.get(user_id, []))}")

    async def send_personal_message(self, message: Dict[str, Any], user_id: int):
        """Send message to all connections for a specific user"""
        if user_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to send message to user {user_id}: {e}")
                    disconnected.append(connection)

            # Clean up disconnected clients
            for conn in disconnected:
                self.disconnect(conn, user_id)

    async def broadcast_to_user(self, message: Dict[str, Any], user_id: int):
        """Alias for send_personal_message"""
        await self.send_personal_message(message, user_id)

    async def send_user_stats(self, user_id: int, stats: Dict[str, Any]):
        """Send user statistics update"""
        message = {
            "type": "stats_update",
            "data": stats,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_personal_message(message, user_id)

    async def send_new_post_alert(self, user_id: int, post_data: Dict[str, Any]):
        """Send alert for new post detected"""
        message = {
            "type": "new_post",
            "data": post_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_personal_message(message, user_id)

    async def send_sentiment_alert(self, user_id: int, alert_data: Dict[str, Any]):
        """Send sentiment analysis alert"""
        message = {
            "type": "sentiment_alert",
            "data": alert_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_personal_message(message, user_id)

# Global manager instance
manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for real-time dashboard updates"""
    # Simple authentication - in production, you'd validate tokens
    await manager.connect(websocket, user_id)

    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                # Handle client messages if needed
                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong", "timestamp": datetime.now().isoformat()})
                elif message.get("type") == "request_stats":
                    # Trigger stats update
                    await send_realtime_stats(user_id)

            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON message"})

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(websocket, user_id)

@router.websocket("/ws/dashboard/{user_id}")
async def dashboard_websocket_endpoint(websocket: WebSocket, user_id: int):
    """Dedicated WebSocket for dashboard real-time updates"""
    # Simple authentication - in production, you'd validate tokens
    await manager.connect(websocket, user_id)

    # Send initial stats on connection
    await send_realtime_stats(user_id)

    try:
        # Start background task to periodically send updates
        background_task = asyncio.create_task(send_periodic_updates(user_id))

        while True:
            try:
                # Listen for client messages
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                message = json.loads(data)

                if message.get("type") == "request_update":
                    await send_realtime_stats(user_id)
                elif message.get("type") == "stop_updates":
                    background_task.cancel()
                    break

            except asyncio.TimeoutError:
                # Send keepalive ping
                await websocket.send_json({"type": "ping", "timestamp": datetime.now().isoformat()})
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid message format"})

    except WebSocketDisconnect:
        if 'background_task' in locals():
            background_task.cancel()
        manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"Dashboard WebSocket error for user {user_id}: {e}")
        if 'background_task' in locals():
            background_task.cancel()
        manager.disconnect(websocket, user_id)

async def send_realtime_stats(user_id: int):
    """Send current statistics to user"""
    try:
        from app.core.database import get_db_sync
        from sqlalchemy import func, desc

        # Get database session
        db = next(get_db_sync())

        # Get recent posts (last 24 hours)
        yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        posts = db.query(SocialPost).filter(
            SocialPost.user_id == user_id,
            SocialPost.posted_at >= yesterday
        ).all()

        # Calculate basic stats
        total_posts = len(posts)
        total_engagement = sum((p.likes + p.shares + p.comments) for p in posts)

        # Sentiment distribution
        sentiment_counts = {}
        for post in posts:
            sent = post.sentiment or 'neutral'
            sentiment_counts[sent] = sentiment_counts.get(sent, 0) + 1

        # Platform distribution
        platform_counts = {}
        for post in posts:
            platform_counts[post.platform] = platform_counts.get(post.platform, 0) + 1

        # Get latest analytics
        latest_analytics = db.query(AnalyticsData).filter(
            AnalyticsData.user_id == user_id
        ).order_by(desc(AnalyticsData.date)).first()

        stats = {
            "total_posts_today": total_posts,
            "total_engagement_today": total_engagement,
            "sentiment_distribution": sentiment_counts,
            "platform_distribution": platform_counts,
            "latest_analytics": {
                "total_posts": latest_analytics.total_posts if latest_analytics else 0,
                "sentiment_positive": latest_analytics.sentiment_positive if latest_analytics else 0,
                "sentiment_negative": latest_analytics.sentiment_negative if latest_analytics else 0,
                "sentiment_neutral": latest_analytics.sentiment_neutral if latest_analytics else 0,
                "total_engagement": latest_analytics.total_engagement if latest_analytics else 0,
            } if latest_analytics else None
        }

        await manager.send_user_stats(user_id, stats)

    except Exception as e:
        logger.error(f"Error sending real-time stats to user {user_id}: {e}")
    finally:
        if 'db' in locals():
            db.close()

async def send_periodic_updates(user_id: int):
    """Send periodic updates every 30 seconds"""
    while True:
        try:
            await asyncio.sleep(30)  # Update every 30 seconds
            await send_realtime_stats(user_id)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in periodic updates for user {user_id}: {e}")
            break

# Utility functions for external use
async def notify_new_post(user_id: int, post_data: Dict[str, Any]):
    """Notify user of new post (called from other services)"""
    await manager.send_new_post_alert(user_id, post_data)

async def notify_sentiment_alert(user_id: int, alert_data: Dict[str, Any]):
    """Notify user of sentiment alert"""
    await manager.send_sentiment_alert(user_id, alert_data)

async def broadcast_stats_update(user_id: int):
    """Broadcast statistics update to user"""
    await send_realtime_stats(user_id)