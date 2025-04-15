
import praw
import sqlite3
import os
from datetime import datetime, timedelta, timezone
REDDIT_CLIENT_ID = '5PNl2SuITto3biTpbqHxnw'
REDDIT_CLIENT_SECRET = 'nA1WqTLuuxTxnSMEWctiHK31gsdybQ'
REDDIT_USERNAME = 'crunchcrunchgrape'
REDDIT_PASSWORD = 'Reddituser25'
REDDIT_USER_AGENT = 'SI206FinalProjectScript by u/crunchcrunchgrape'

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent=REDDIT_USER_AGENT
)

KEYWORDS = ['college', 'student', 'campus']
LIMIT_PER_RUN = 25

# Connect to project database
conn = sqlite3.connect('final_project.db')
cur = conn.cursor()
# DB_NAME = "final_project.db"
# # print(os.path.abspath("final_project.db"))

cur.execute('''
CREATE TABLE IF NOT EXISTS RedditPosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id TEXT UNIQUE,
    title TEXT,
    subreddit TEXT,
    date TEXT,
    keyword TEXT,
    upvotes INTEGER,
    num_comments INTEGER
)
''')
conn.commit()

# SPECIFIC_DATES = ['2025-04-11', '2025-04-12', '2025-04-13']

def fetch_and_store(keyword, target_date=None):
    count = 0

### attempting to search for old dates for more data, didnt work
    # if target_date:
    #     start_date = datetime.strptime(target_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    #     end_date = start_date + timedelta(days=1)
    # else:
    #     start_date = datetime.utcnow()
    #     end_date = start_date + timedelta(days=1)
    
    for post in reddit.subreddit('all').search(keyword, sort='new', limit=LIMIT_PER_RUN*2):
        post_datetime = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)

        # print(f"{post.title} - {post_datetime.year}")

        # storing only from 2024
        # if post_datetime.year != 2024:
        #     continue

        post_id = post.id
        title = post.title
        subreddit = post.subreddit.display_name
        date = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
        upvotes = post.score
        num_comments = post.num_comments

        try:
            cur.execute('''
                INSERT INTO RedditPosts (post_id, title, subreddit, date, keyword, upvotes, num_comments)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (post_id, title, subreddit, date, keyword, upvotes, num_comments))
            conn.commit()
            count += 1
        except sqlite3.IntegrityError:
            continue

        if count >= LIMIT_PER_RUN:
            break

    print(f"{count} new posts added for keyword: {keyword}")

### attempting to search for old dates for more data, didnt work
# for target_date in SPECIFIC_DATES:
#     for kw in KEYWORDS:
#         fetch_and_store(kw, target_date)

for kw in KEYWORDS:
    fetch_and_store(kw)


# def test_entries_for_specific_dates():
#     for target_date in SPECIFIC_DATES:
#         cur.execute('''
#             SELECT COUNT(*) FROM RedditPosts WHERE date = ?
#         ''', (target_date,))
#         count = cur.fetchone()[0]
#         print(f"Number of posts on {target_date}: {count}")

# Run the test function
# test_entries_for_specific_dates()

conn.close()