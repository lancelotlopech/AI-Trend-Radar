from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid

class NewsArticleBase(BaseModel):
    source: str
    title: str
    url: str
    published_at: Optional[datetime] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    extracted_keywords: Optional[List[str]] = None

class NewsArticleCreate(NewsArticleBase):
    pass

class NewsArticle(NewsArticleBase):
    id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True

