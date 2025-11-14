from sqlalchemy.orm import Session
from app.models.reddit import RedditPost
from app.schemas.reddit import RedditPostCreate
from datetime import datetime, timedelta
from typing import List, Optional

def get_latest_reddit_posts(db: Session, limit: int = 10) -> List[RedditPost]:
    return db.query(RedditPost).order_by(RedditPost.created_utc.desc()).limit(limit).all()

def create_reddit_post(db: Session, reddit_post: RedditPostCreate):
    db_reddit_post = RedditPost(**reddit_post.dict())
    db.add(db_reddit_post)
    db.commit()
    db.refresh(db_reddit_post)
    return db_reddit_post

