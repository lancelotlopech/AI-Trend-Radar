import sys
import os
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'crawlers')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'services')))

from crawlers.google_trends_crawler import run_google_trends_crawler
from crawlers.app_store_crawler import run_app_store_crawler
from crawlers.reddit_crawler import run_reddit_crawler
from crawlers.news_rss_crawler import run_news_rss_crawler
from services.trend_calculator import run_trend_calculator

def run_all_tasks():
    print(f"[{datetime.now()}] Starting all scheduled tasks...")

    print(f"[{datetime.now()}] --- Running crawlers ---")
    run_google_trends_crawler()
    run_app_store_crawler()
    run_reddit_crawler()
    run_news_rss_crawler()

    print(f"[{datetime.now()}] --- Running trend calculator ---")
    run_trend_calculator()

    print(f"[{datetime.now()}] All scheduled tasks finished.")

if __name__ == "__main__":
    run_all_tasks()

