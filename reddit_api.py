
import praw
import sqlite3
from datetime import datetime

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

def fetch_and_store(keyword):
    count = 0
    for post in reddit.subreddit('all').search(keyword, sort='new', limit=LIMIT_PER_RUN*2):
        post_id = post.id
        title = post.title
        subreddit = post.subreddit.display_name
        date = datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d')
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

for kw in KEYWORDS:
    fetch_and_store(kw)

conn.close()