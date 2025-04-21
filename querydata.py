import sqlite3
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

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

cur.execute('''
SELECT date, temp_max,temp_min, precipitation, humidity
FROM Weather2025
ORDER BY date DESC
LIMIT 5
''')
weather_results = cur.fetchall()

print("Recent 5 Days of Weather Data:")
for row in weather_results:
    print(f"Date: {row[0]}, Temp (°F): {row[1]}, Humidity: {row[2]}%, Weather: {row[3]}, Precipitation: {row[4]}mm")

conn.close()