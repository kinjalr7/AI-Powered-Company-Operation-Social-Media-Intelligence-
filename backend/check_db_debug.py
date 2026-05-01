from app.core.database import SessionLocal
from app.models.social_data import SocialPost
from app.models.user import User
from sqlalchemy import select

def check_db():
    db = SessionLocal()
    try:
        users = db.execute(select(User)).scalars().all()
        print(f"Total Users: {len(users)}")
        for u in users:
            posts = db.execute(select(SocialPost).where(SocialPost.user_id == u.id)).scalars().all()
            print(f"User {u.email} (ID: {u.id}) has {len(posts)} posts.")
        
        all_posts = db.execute(select(SocialPost)).scalars().all()
        print(f"Total Posts in DB: {len(all_posts)}")
        for p in all_posts:
            print(f"Post ID: {p.id}, User ID: {p.user_id}, Platform: {p.platform}, Date: {p.posted_at}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
