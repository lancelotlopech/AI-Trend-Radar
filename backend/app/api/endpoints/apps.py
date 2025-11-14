from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.services.crud import app_data
from app.schemas.app import AppTrend

router = APIRouter()

@router.get("/latest", response_model=List[AppTrend], summary="获取最新的AI应用榜单")
def get_latest_ai_apps(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    获取最新的AI应用下载趋势榜单。
    """
    return app_data.get_latest_app_trends(db, limit=limit)

