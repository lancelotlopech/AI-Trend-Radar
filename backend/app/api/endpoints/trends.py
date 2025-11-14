from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.services.crud import trend_data
from app.schemas.trend import TrendScore, Keyword

router = APIRouter()

@router.get("/latest", response_model=List[TrendScore], summary="获取最新的AI趋势榜单")
def get_latest_ai_trends(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    获取最新的AI热点趋势榜单，包含综合趋势指数及各项分值。
    """
    return trend_data.get_latest_trend_scores(db, limit=limit)

@router.get("/{keyword_id}/history", response_model=List[TrendScore], summary="获取关键词历史趋势数据")
def get_keyword_trend_history(
    keyword_id: str,
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """
    获取指定关键词在过去一段时间内的历史趋势分数，用于绘制折线图。
    """
    return trend_data.get_trend_scores_for_keyword(db, keyword_id, days=days)

@router.get("/keywords", response_model=List[Keyword], summary="获取所有追踪的关键词")
def get_all_keywords(db: Session = Depends(get_db)):
    """
    获取所有已追踪的AI关键词列表。
    """
    return db.query(Keyword).all()

