import praw
import sqlite3
import os
from datetime import datetime, timezone

# Reddit API credentials
REDDIT_CLIENT_ID = '5PNl2SuITto3biTpbqHxnw'
REDDIT_CLIENT_SECRET = 'nA1WqTLuuxTxnSMEWctiHK31gsdybQ'
REDDIT_USERNAME = 'crunchcrunchgrape'
REDDIT_PASSWORD = 'Reddituser25'
REDDIT_USER_AGENT = 'SI206FinalProjectScript by u/crunchcrunchgrape'

# Keywords to look for & limit on amount of posts found
KEYWORDS = ['college', 'student', 'campus']
LIMIT_PER_RUN = 25

def fetch_and_store(KEYWORDS):

    # Initializing API
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        user_agent=REDDIT_USER_AGENT
    )

    # Connect to project database
    conn = sqlite3.connect('final_project2.db')
    cur = conn.cursor()

    # Creating table if it doesn't exist
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


    totaladded = 0
    for kw in KEYWORDS:
        if totaladded >= LIMIT_PER_RUN:
            break
        
        # Limit is greater to account for duplicates
        for post in reddit.subreddit('all').search(kw, sort='new', limit=LIMIT_PER_RUN*2):
            if totaladded >= LIMIT_PER_RUN:
                break

            post_id = post.id
            title = post.title
            subreddit = post.subreddit.display_name
            date = datetime.fromtimestamp(post.created_utc, tz=timezone.utc).isoformat()
            upvotes = post.score
            num_comments = post.num_comments

            # Inserting posts into database, skips if ID already exists
            try:
                cur.execute('''
                    INSERT INTO RedditPosts (post_id, title, subreddit, date, keyword, upvotes, num_comments)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (post_id, title, subreddit, date, kw, upvotes, num_comments))
                conn.commit()
                totaladded += 1
            except sqlite3.IntegrityError:
                continue

    print(f"{totaladded} total new posts added across all keywords.")
    conn.close()

fetch_and_store(KEYWORDS)