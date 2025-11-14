from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid

class RedditPostBase(BaseModel):
    post_id: str
    subreddit: str
    title: str
    url: str
    score: Optional[int] = None
    num_comments: Optional[int] = None
    created_utc: Optional[datetime] = None
    extracted_keywords: Optional[List[str]] = None

class RedditPostCreate(RedditPostBase):
    pass

class RedditPost(RedditPostBase):
    id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True

