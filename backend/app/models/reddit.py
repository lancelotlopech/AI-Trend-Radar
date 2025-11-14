from sqlalchemy import Column, String, Integer, DateTime, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db import Base

class RedditPost(Base):
    __tablename__ = "reddit_posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(String, unique=True, nullable=False)
    subreddit = Column(String, nullable=False)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    score = Column(Integer)
    num_comments = Column(Integer)
    created_utc = Column(DateTime(timezone=True))
    extracted_keywords = Column(ARRAY(Text))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

