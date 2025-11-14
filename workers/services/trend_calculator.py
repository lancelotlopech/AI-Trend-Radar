import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from backend.app.models.trend import Keyword, TrendScore
from backend.app.models.app import AppTrend
from backend.app.models.reddit import RedditPost
from backend.app.models.news import NewsArticle
from workers.services.db_updater import get_db_session, get_or_create_keyword

TREND_WEIGHTS = {
    "google_trends": 0.40,
    "reddit": 0.30,
    "news": 0.20,
    "app_downloads": 0.10
}

def normalize_score(value, min_val, max_val):
    if max_val == min_val:
        return 0
    return ((value - min_val) / (max_val - min_val)) * 100

def calculate_reddit_score(db: Session, keyword_id: str, keyword_text: str, lookback_hours: int = 24):
    time_threshold = datetime.now() - timedelta(hours=lookback_hours)
    
    relevant_posts = db.query(RedditPost).filter(
        RedditPost.timestamp >= time_threshold,
        (RedditPost.title.ilike(f"%{keyword_text}%")) |
        (RedditPost.extracted_keywords.contains([keyword_text.lower()]))
    ).all()

    total_score = sum(post.score or 0 for post in relevant_posts)
    total_comments = sum(post.num_comments or 0 for post in relevant_posts)

    reddit_raw_score = len(relevant_posts) * 5 + total_score / 10 + total_comments

    all_reddit_raw_scores = [
        (p.score or 0) / 10 + (p.num_comments or 0) + len([1 for rp in db.query(RedditPost).filter(
            RedditPost.timestamp >= time_threshold,
            (RedditPost.title.ilike(f"%{k.keyword}%")) |
            (RedditPost.extracted_keywords.contains([k.keyword.lower()]))
        ).all() if k.keyword.lower() in rp.title.lower() or (rp.extracted_keywords and k.keyword.lower() in rp.extracted_keywords)]) * 5
        for k in db.query(Keyword).all() for p in db.query(RedditPost).filter(
            RedditPost.timestamp >= time_threshold,
            (RedditPost.title.ilike(f"%{k.keyword}%")) |
            (RedditPost.extracted_keywords.contains([k.keyword.lower()]))
        ).all()
    ]
    
    if not all_reddit_raw_scores:
        return 0
    
    min_reddit_score = min(all_reddit_raw_scores)
    max_reddit_score = max(all_reddit_raw_scores)

    return normalize_score(reddit_raw_score, min_reddit_score, max_reddit_score)


def calculate_news_score(db: Session, keyword_id: str, keyword_text: str, lookback_hours: int = 24):
    time_threshold = datetime.now() - timedelta(hours=lookback_hours)

    relevant_articles = db.query(NewsArticle).filter(
        NewsArticle.timestamp >= time_threshold,
        (NewsArticle.title.ilike(f"%{keyword_text}%")) |
        (NewsArticle.summary.ilike(f"%{keyword_text}%")) |
        (NewsArticle.extracted_keywords.contains([keyword_text.lower()]))
    ).all()

    news_raw_score = len(relevant_articles) * 10

    all_news_raw_scores = [
        len(db.query(NewsArticle).filter(
            NewsArticle.timestamp >= time_threshold,
            (NewsArticle.title.ilike(f"%{k.keyword}%")) |
            (NewsArticle.summary.ilike(f"%{k.keyword}%")) |
            (NewsArticle.extracted_keywords.contains([k.keyword.lower()]))
        ).all()) * 10
        for k in db.query(Keyword).all()
    ]

    if not all_news_raw_scores:
        return 0

    min_news_score = min(all_news_raw_scores)
    max_news_score = max(all_news_raw_scores)

    return normalize_score(news_raw_score, min_news_score, max_news_score)

def calculate_app_score(db: Session, keyword_id: str, keyword_text: str, lookback_hours: int = 24):
    time_threshold = datetime.now() - timedelta(hours=lookback_hours)
    
    relevant_apps = db.query(AppTrend).filter(
        AppTrend.timestamp >= time_threshold,
        (AppTrend.app_name.ilike(f"%{keyword_text}%")) |
        (AppTrend.category.ilike("%AI%"))
    ).all()

    app_raw_score = sum((app.download_change or 0) * 0.1 for app in relevant_apps) + len(relevant_apps) * 5

    all_app_raw_scores = [
        sum((app.download_change or 0) * 0.1 for app in db.query(AppTrend).filter(
            AppTrend.timestamp >= time_threshold,
            (AppTrend.app_name.ilike(f"%{k.keyword}%")) | (AppTrend.category.ilike("%AI%"))
        ).all()) + len(db.query(AppTrend).filter(
            AppTrend.timestamp >= time_threshold,
            (AppTrend.app_name.ilike(f"%{k.keyword}%")) | (AppTrend.category.ilike("%AI%"))
        ).all()) * 5
        for k in db.query(Keyword).all()
    ]

    if not all_app_raw_scores:
        return 0
    
    min_app_score = min(all_app_raw_scores)
    max_app_score = max(all_app_raw_scores)

    return normalize_score(app_raw_score, min_app_score, max_app_score)


def run_trend_calculator():
    db = get_db_session()
    print(f"[{datetime.now()}] Starting Trend Score Calculation...")

    keywords = db.query(Keyword).all()
    
    for keyword_obj in keywords:
        keyword_id = keyword_obj.id
        keyword_text = keyword_obj.keyword

        print(f"  Calculating scores for keyword: {keyword_text}")

        latest_google_trend = db.query(TrendScore).filter(
            TrendScore.keyword_id == keyword_id
        ).order_by(TrendScore.timestamp.desc()).first()
        
        google_score = latest_google_trend.google_trends_score if latest_google_trend else 0

        reddit_score = calculate_reddit_score(db, keyword_id, keyword_text)
        news_score = calculate_news_score(db, keyword_id, keyword_text)
        app_score = calculate_app_score(db, keyword_id, keyword_text)

        final_trend_score = (
            google_score * TREND_WEIGHTS["google_trends"] +
            reddit_score * TREND_WEIGHTS["reddit"] +
            news_score * TREND_WEIGHTS["news"] +
            app_score * TREND_WEIGHTS["app_downloads"]
        )

        new_trend_score_entry = TrendScore(
            keyword_id=keyword_id,
            trend_score=round(final_trend_score, 2),
            google_trends_score=round(google_score, 2),
            reddit_score=round(reddit_score, 2),
            news_score=round(news_score, 2),
            app_score=round(app_score, 2)
        )
        db.add(new_trend_score_entry)
        db.commit()
        db.refresh(new_trend_score_entry)
        print(f"    Saved Trend Score for {keyword_text}: {final_trend_score:.2f}")

    db.close()
    print(f"[{datetime.now()}] Trend Score Calculation Finished.")

if __name__ == "__main__":
    run_trend_calculator()

