from sqlalchemy.orm import Session
from app.models.news import NewsArticle
from app.schemas.news import NewsArticleCreate
from datetime import datetime, timedelta
from typing import List, Optional

def get_latest_news_articles(db: Session, limit: int = 10) -> List[NewsArticle]:
    return db.query(NewsArticle).order_by(NewsArticle.published_at.desc()).limit(limit).all()

def create_news_article(db: Session, news_article: NewsArticleCreate):
    db_news_article = NewsArticle(**news_article.dict())
    db.add(db_news_article)
    db.commit()
    db.refresh(db_news_article)
    return db_news_article

