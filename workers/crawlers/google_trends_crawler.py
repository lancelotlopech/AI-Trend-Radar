import os
from pytrends.request import TrendReq
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.app.models.trend import TrendScore # 假设backend/app/models/trend 可以访问
from backend.app.models.trend import Keyword # 假设backend/app/models/trend 可以访问
from workers.services.db_updater import get_db_session, get_or_create_keyword
import time

def get_google_trends_data(keywords: list, timeframe='today 1-m'):
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
        data = pytrends.interest_over_time()
        return data
    except Exception as e:
        print(f"Error fetching Google Trends for {keywords}: {e}")
        return None

def run_google_trends_crawler():
    db = get_db_session()
    tracked_keywords = ["AI", "ChatGPT", "Generative AI", "Large Language Model", "AI Agent"]

    print(f"[{datetime.now()}] Starting Google Trends crawler...")

    for kw_text in tracked_keywords:
        keyword_obj = get_or_create_keyword(db, kw_text)
        data = get_google_trends_data([kw_text], timeframe='now 1-H')
        if data is not None and not data.empty:
            latest_score = data[kw_text].iloc[-1]
            print(f"Keyword: {kw_text}, Latest Google Trends Score: {latest_score}")

            new_trend_score = TrendScore(
                keyword_id=keyword_obj.id,
                google_trends_score=latest_score,
                trend_score=0
            )
            db.add(new_trend_score)
            db.commit()
            db.refresh(new_trend_score)
            print(f"Saved Google Trends score for {kw_text}")
        time.sleep(5)

    db.close()
    print(f"[{datetime.now()}] Google Trends crawler finished.")

if __name__ == "__main__":
    run_google_trends_crawler()

