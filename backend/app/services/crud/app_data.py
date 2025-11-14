from sqlalchemy.orm import Session
from app.models.app import AppTrend
from app.schemas.app import AppTrendCreate
from datetime import datetime, timedelta
from typing import List, Optional

def get_latest_app_trends(db: Session, limit: int = 10) -> List[AppTrend]:
    return db.query(AppTrend).order_by(AppTrend.timestamp.desc()).limit(limit).all()

def create_app_trend(db: Session, app_trend: AppTrendCreate):
    db_app_trend = AppTrend(**app_trend.dict())
    db.add(db_app_trend)
    db.commit()
    db.refresh(db_app_trend)
    return db_app_trend

