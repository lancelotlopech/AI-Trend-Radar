from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class KeywordBase(BaseModel):
    keyword: str

class KeywordCreate(KeywordBase):
    pass

class Keyword(KeywordBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class TrendScoreBase(BaseModel):
    keyword_id: uuid.UUID
    trend_score: float
    google_trends_score: Optional[float] = None
    reddit_score: Optional[float] = None
    news_score: Optional[float] = None
    app_score: Optional[float] = None

class TrendScoreCreate(TrendScoreBase):
    pass

class TrendScore(TrendScoreBase):
    id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True

