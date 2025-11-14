from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.services.crud import reddit_data
from app.schemas.reddit import RedditPost

router = APIRouter()

@router.get("/latest", response_model=List[RedditPost], summary="获取最新的Reddit热门AI帖子")
def get_latest_reddit_ai_posts(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    获取Reddit r/ArtificialIntelligence, r/ChatGPT 等子版块的最新热门帖子。
    """
    return reddit_data.get_latest_reddit_posts(db, limit=limit)

