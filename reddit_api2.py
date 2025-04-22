import praw
import sqlite3
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

    # Step 1: Rename old table if exists
    try:
        cur.execute('ALTER TABLE RedditPosts RENAME TO RedditPosts_old')
        conn.commit()
    except sqlite3.OperationalError:
        print("Old table not found, proceeding with new table creation.")

    # Step 2: Create new table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS RedditPosts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id TEXT UNIQUE,
        title TEXT,
        subreddit TEXT,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        mentioned_college INTEGER,
        mentioned_student INTEGER,
        mentioned_campus INTEGER,
        upvotes INTEGER,
        num_comments INTEGER
    )
    ''')
    conn.commit()

    # Step 3: Migrate data from old table if exists
    cur.execute('SELECT post_id, title, subreddit, date, upvotes, num_comments FROM RedditPosts_old')
    rows = cur.fetchall()

    for row in rows:
        post_id, title, subreddit, date_str, upvotes, num_comments = row

        # Convert string date to datetime
        try:
            post_datetime = datetime.fromisoformat(date_str)
        except Exception as e:
            print(f"Skipping invalid date: {date_str}")
            continue

        year = post_datetime.year
        month = post_datetime.month
        day = post_datetime.day

        mentioned_college = 1 if 'college' in title.lower() else 0
        mentioned_student = 1 if 'student' in title.lower() else 0
        mentioned_campus = 1 if 'campus' in title.lower() else 0

        # Add only if at least one keyword is present
        if mentioned_college or mentioned_student or mentioned_campus:
            try:
                cur.execute('''
                    INSERT INTO RedditPosts (
                        post_id, title, subreddit, year, month, day,
                        mentioned_college, mentioned_student, mentioned_campus,
                        upvotes, num_comments
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    post_id, title, subreddit, year, month, day,
                    mentioned_college, mentioned_student, mentioned_campus,
                    upvotes, num_comments
                ))
            except sqlite3.IntegrityError:
                continue
    conn.commit()
    print("Old data successfully migrated to new table.")

    # Fetch and store new posts from Reddit
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
            post_datetime = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)

            year = post_datetime.year
            month = post_datetime.month
            day = post_datetime.day
            upvotes = post.score
            num_comments = post.num_comments

            # Checking if keywords are mentioned
            mentioned_college = 1 if 'college' in title.lower() else 0
            mentioned_student = 1 if 'student' in title.lower() else 0
            mentioned_campus = 1 if 'campus' in title.lower() else 0

            # Add only if at least one keyword is present
            if mentioned_college or mentioned_student or mentioned_campus:
                try:
                    cur.execute('''
                        INSERT INTO RedditPosts (
                            post_id, title, subreddit, year, month, day,
                            mentioned_college, mentioned_student, mentioned_campus,
                            upvotes, num_comments
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        post_id, title, subreddit, year, month, day,
                        mentioned_college, mentioned_student, mentioned_campus,
                        upvotes, num_comments
                    ))
                    conn.commit()
                    totaladded += 1
                except sqlite3.IntegrityError:
                    continue

    print(f"{totaladded} total new posts added across all keywords.")
    conn.close()

fetch_and_store(KEYWORDS)