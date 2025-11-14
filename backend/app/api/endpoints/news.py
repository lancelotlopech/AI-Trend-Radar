from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.services.crud import news_data
from app.schemas.news import NewsArticle

router = APIRouter()

@router.get("/latest", response_model=List[NewsArticle], summary="获取最新的AI新闻和新品")
def get_latest_ai_news(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    获取最新的AI相关新闻和新品发布文章。
    """
    return news_data.get_latest_news_articles(db, limit=limit)

