import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 导入所有可能用到的模型
from app.models.trend import Keyword, TrendScore
from app.models.app import AppTrend
from app.models.reddit import RedditPost
from app.models.news import NewsArticle
from sqlalchemy.ext.declarative import declarative_base # 需要导入Base以创建engine

Base = declarative_base() # 在worker中也需要一个Base实例，或者从backend导入

def get_db_session():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def save_to_db(data_object, db_session):
    db_session.add(data_object)
    db_session.commit()
    db_session.refresh(data_object)
    return data_object

def get_or_create_keyword(db_session, keyword_text: str):
    keyword = db_session.query(Keyword).filter_by(keyword=keyword_text).first()
    if not keyword:
        keyword = Keyword(keyword=keyword_text)
        db_session.add(keyword)
        db_session.commit()
        db_session.refresh(keyword)
    return keyword

