import os
import praw
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.models.reddit import RedditPost # 假设backend/app/models/reddit 可以访问
from workers.services.db_updater import get_db_session
import time

def run_reddit_crawler():
    db = get_db_session()

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    subreddits = ["ArtificialIntelligence", "ChatGPT"]
    print(f"[{datetime.now()}] Starting Reddit crawler...")

    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=20):
            print(f"  Fetching Reddit post: {submission.title}")
            extracted_keywords = [word.lower() for word in submission.title.split() if len(word) > 3 and word.lower() not in ["the", "a", "an", "is", "of", "in", "for", "with"]]

            new_post = RedditPost(
                post_id=submission.id,
                subreddit=subreddit_name,
                title=submission.title,
                url=f"https://www.reddit.com{submission.permalink}",
                score=submission.score,
                num_comments=submission.num_comments,
                created_utc=datetime.fromtimestamp(submission.created_utc),
                extracted_keywords=extracted_keywords
            )
            existing_post = db.query(RedditPost).filter_by(post_id=new_post.post_id).first()
            if not existing_post:
                db.add(new_post)
                db.commit()
                db.refresh(new_post)
                print(f"    Saved Reddit post: {new_post.title}")
            else:
                print(f"    Reddit post already exists: {existing_post.title}")
            time.sleep(1)

    db.close()
    print(f"[{datetime.now()}] Reddit crawler finished.")

if __name__ == "__main__":
    run_reddit_crawler()

