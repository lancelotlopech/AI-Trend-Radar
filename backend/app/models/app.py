from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db import Base

class AppTrend(Base):
    __tablename__ = "app_trends"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_name = Column(String, nullable=False)
    store_platform = Column(String, nullable=False) # 'App Store', 'Play Store'
    category = Column(String)
    current_rank = Column(Integer)
    download_change = Column(Integer)
    icon_url = Column(String)
    app_url = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

