from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db import Base

class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keyword = Column(Text, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TrendScore(Base):
    __tablename__ = "trend_scores"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keyword_id = Column(UUID(as_uuid=True), ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False)
    trend_score = Column(Numeric(5, 2), nullable=False)
    google_trends_score = Column(Numeric(5, 2))
    reddit_score = Column(Numeric(5, 2))
    news_score = Column(Numeric(5, 2))
    app_score = Column(Numeric(5, 2))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

