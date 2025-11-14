from sqlalchemy import Column, String, DateTime, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String, nullable=False)
    title = Column(Text, nullable=False)
    url = Column(Text, unique=True, nullable=False)
    published_at = Column(DateTime(timezone=True))
    summary = Column(Text)
    image_url = Column(String)
    extracted_keywords = Column(ARRAY(Text))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

