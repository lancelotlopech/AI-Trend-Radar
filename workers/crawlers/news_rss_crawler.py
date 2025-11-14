import feedparser
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.models.news import NewsArticle # 假设backend/app/models/news 可以访问
from workers.services.db_updater import get_db_session
import time

RSS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
}

def run_news_rss_crawler():
    db = get_db_session()
    print(f"[{datetime.now()}] Starting News RSS crawler...")

    for source_name, rss_url in RSS_FEEDS.items():
        print(f"  Fetching RSS from {source_name}...")
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published_at = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else None
            summary = entry.summary if hasattr(entry, 'summary') else None

            extracted_keywords = [word.lower() for word in title.split() if len(word) > 3 and word.lower() not in ["the", "a", "an", "is", "of"]]
            
            new_article = NewsArticle(
                source=source_name,
                title=title,
                url=link,
                published_at=published_at,
                summary=summary,
                extracted_keywords=extracted_keywords
            )
            existing_article = db.query(NewsArticle).filter_by(url=new_article.url).first()
            if not existing_article:
                db.add(new_article)
                db.commit()
                db.refresh(new_article)
                print(f"    Saved News article: {new_article.title}")
            time.sleep(0.5)

    db.close()
    print(f"[{datetime.now()}] News RSS crawler finished.")

if __name__ == "__main__":
    run_news_rss_crawler()

