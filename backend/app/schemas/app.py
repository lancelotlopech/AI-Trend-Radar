from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class AppTrendBase(BaseModel):
    app_name: str
    store_platform: str
    category: Optional[str] = None
    current_rank: Optional[int] = None
    download_change: Optional[int] = None
    icon_url: Optional[str] = None
    app_url: Optional[str] = None

class AppTrendCreate(AppTrendBase):
    pass

class AppTrend(AppTrendBase):
    id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True

