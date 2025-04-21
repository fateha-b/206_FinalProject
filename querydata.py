import sqlite3
import os

<<<<<<< Updated upstream
# conn = sqlite3.connect("/Users/fbushra/Documents/SI 206/206_FinalProject/final_project.db")
=======
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

>>>>>>> Stashed changes
conn = sqlite3.connect("final_project.db")
cur = conn.cursor()

cur.execute("SELECT title, author_id, published_date FROM Books ORDER BY published_date DESC LIMIT 5")
results = cur.fetchall()

for row in results:
    print(row)

# Select from Reddit top 5 posts
cur.execute('''
SELECT title, subreddit, upvotes, keyword, date
FROM RedditPosts
ORDER BY upvotes DESC
LIMIT 5
''')

results = cur.fetchall()

# Display the results
print("Top 5 Reddit Posts:")
for row in results:
    print(f"Title: {row[0]}\nSubreddit: {row[1]}\nUpvotes: {row[2]}\nKeyword: {row[3]}\nDate: {row[4]}\n")

conn.close()