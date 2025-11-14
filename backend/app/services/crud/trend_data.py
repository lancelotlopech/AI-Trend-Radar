from sqlalchemy.orm import Session
from app.models.trend import Keyword, TrendScore
from app.schemas.trend import KeywordCreate, TrendScoreCreate
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import func

def get_keyword_by_name(db: Session, keyword: str):
    return db.query(Keyword).filter(Keyword.keyword == keyword).first()

def create_keyword(db: Session, keyword: KeywordCreate):
    db_keyword = Keyword(keyword=keyword.keyword)
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

def get_latest_trend_scores(db: Session, limit: int = 10) -> List[TrendScore]:
    subquery = db.query(TrendScore.keyword_id, func.max(TrendScore.timestamp).label("max_timestamp")) \
                  .group_by(TrendScore.keyword_id).subquery()

    latest_scores = db.query(TrendScore).join(subquery,
        (TrendScore.keyword_id == subquery.c.keyword_id) &
        (TrendScore.timestamp == subquery.c.max_timestamp)
    ).order_by(TrendScore.trend_score.desc()).limit(limit).all()
    return latest_scores


def get_trend_scores_for_keyword(db: Session, keyword_id: str, days: int = 7) -> List[TrendScore]:
    seven_days_ago = datetime.now() - timedelta(days=days)
    return db.query(TrendScore).filter(
        TrendScore.keyword_id == keyword_id,
        TrendScore.timestamp >= seven_days_ago
    ).order_by(TrendScore.timestamp.asc()).all()

def create_trend_score(db: Session, trend_score: TrendScoreCreate):
    db_trend_score = TrendScore(**trend_score.dict())
    db.add(db_trend_score)
    db.commit()
    db.refresh(db_trend_score)
    return db_trend_score

