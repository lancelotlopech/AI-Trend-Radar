import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.models.app import AppTrend # 假设backend/app/models/app 可以访问
from workers.services.db_updater import get_db_session
import time

APP_STORE_FREE_APPS_URL = "https://apps.apple.com/us/charts/top-free-apps"
PLAY_STORE_FREE_APPS_URL = "https://play.google.com/store/apps/top/free"

def fetch_app_store_data(url: str, platform: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = httpx.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        apps_data = []

        if platform == 'App Store':
            app_elements = soup.select('div.l-row.product-row a.product-item')

            for rank, app_element in enumerate(app_elements[:20]):
                app_name = app_element.select_one('h3.product-name')
                if app_name: # 检查 app_name 是否为 None
                    app_name_text = app_name.text.strip()
                    app_url = "https://apps.apple.com" + app_element['href']
                    icon_url_element = app_element.select_one('img.artwork-item')
                    icon_url = icon_url_element['src'] if icon_url_element else None # 检查 icon_url_element 是否为 None

                    apps_data.append({
                        "app_name": app_name_text,
                        "store_platform": platform,
                        "current_rank": rank + 1,
                        "app_url": app_url,
                        "icon_url": icon_url,
                        "download_change": None
                    })
        elif platform == 'Play Store':
            app_elements = soup.select('.ImZGtf.mpDcBf')
            for rank, app_element in enumerate(app_elements[:20]):
                app_name_element = app_element.select_one('.DdYX5')
                if app_name_element: # 检查 app_name_element 是否为 None
                    app_name = app_name_element.text.strip()
                    app_url = "https://play.google.com" + app_element.select_one('a')['href']
                    icon_url_element = app_element.select_one('img.T75of.E5L5rc')
                    icon_url = icon_url_element['src'] if icon_url_element else None # 检查 icon_url_element 是否为 None
                    
                    apps_data.append({
                        "app_name": app_name,
                        "store_platform": platform,
                        "current_rank": rank + 1,
                        "app_url": app_url,
                        "icon_url": icon_url,
                        "download_change": None
                    })
        return apps_data
    except httpx.HTTPStatusError as e:
        print(f"HTTP error for {url}: {e}")
    except Exception as e:
        print(f"Error fetching {platform} data: {e}")
    return None

def run_app_store_crawler():
    db = get_db_session()
    print(f"[{datetime.now()}] Starting App Store / Play Store crawler...")

    app_store_apps = fetch_app_store_data(APP_STORE_FREE_APPS_URL, 'App Store')
    if app_store_apps:
        for app_data in app_store_apps:
            new_app_trend = AppTrend(**app_data)
            db.add(new_app_trend)
        db.commit()
        print(f"Saved {len(app_store_apps)} App Store app trends.")
    time.sleep(10)

    play_store_apps = fetch_app_store_data(PLAY_STORE_FREE_APPS_URL, 'Play Store')
    if play_store_apps:
        for app_data in play_store_apps:
            new_app_trend = AppTrend(**app_data)
            db.add(new_app_trend)
        db.commit()
        print(f"Saved {len(play_store_apps)} Play Store app trends.")

    db.close()
    print(f"[{datetime.now()}] App Store / Play Store crawler finished.")

if __name__ == "__main__":
    run_app_store_crawler()

