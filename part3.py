import sqlite3
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# Connect to the database
DB_NAME = "final_project.db"
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# ----------------------------------------------------
# 🔹 FATEHA'S SECTION: Books + Weather Analysis
# ----------------------------------------------------
# Tasks:
# - Join NYT books and weather data based on published_date
# - Calculate genre frequency by weather condition
# - Calculate average rank per weather condition
# - Prepare summary strings for output

cur.execute('''
    SELECT w.date, w.precipitation, b.list_name, COUNT(*) AS genre_count, AVG(b.rank) AS avg_rank
    FROM Books b
    JOIN Weather2025 w ON b.published_date = w.date
    GROUP BY w.date, w.precipitation, b.list_name
''')
books_weather_results = cur.fetchall()

fateha_summary = ["--- Book Genre Trends by Weather (Fateha) ---"]
for row in books_weather_results:
    fateha_summary.append(
        f"Date: {row[0]}, Weather: {row[1]}, Genre/List: {row[2]}, Count: {row[3]}, Avg Rank: {round(row[4], 2)}"
    )


# ----------------------------------------------------
# 🔹 SARINA'S SECTION: Reddit + Weather Analysis
# ----------------------------------------------------
# Tasks:
# - Join Reddit and weather data by date
# - Count posts with "student", "college", "campus" keywords
# - Calculate average upvotes/comments by weather condition
# - Prepare summary strings for output

cur.execute('''
    SELECT w.date, w.precipitation, COUNT(r.post_id) AS post_count, 
           AVG(r.upvotes) AS avg_upvotes, AVG(r.num_comments) AS avg_comments
    FROM RedditPosts r
    JOIN Weather2025 w ON DATE(r.date) = w.date
    WHERE r.keyword IN ('college', 'student', 'campus')
    GROUP BY w.date, w.precipitation
''')
reddit_weather_results = cur.fetchall()

sarina_summary = ["--- Reddit Engagement by Weather (Sarina) ---"]
for row in reddit_weather_results:
    sarina_summary.append(
        f"Date: {row[0]}, Weather: {row[1]}, Posts: {row[2]}, "
        f"Avg Upvotes: {round(row[3], 2)}, Avg Comments: {round(row[4], 2)}"
    )


# ----------------------------------------------------
# 🔹 NAJMUL'S SECTION: Weather Summary + Integration
# ----------------------------------------------------
# Tasks:
# - Summarize daily weather conditions from 4/6 to 4/13
# - Enable clean joins with Reddit and Books via date
# - Optionally prepare summary of total rainy/sunny/cloudy days

cur.execute('''
    SELECT precipitation, COUNT(*) AS day_count
    FROM Weather2025
    WHERE date BETWEEN '2025-04-06' AND '2025-04-13'
    GROUP BY precipitation
''')
weather_summary = cur.fetchall()

najmul_summary = ["--- Weekly Weather Summary (Najmul) ---"]
for row in weather_summary:
    najmul_summary.append(f"Weather: {row[0]}, Days: {row[1]}")


# ----------------------------------------------------
# 🔸 WRITE TO TEXT FILE (ALL MEMBERS CONTRIBUTE)
# ----------------------------------------------------
# Tasks:
# - Combine summary outputs from all three sections
# - Write final combined summary to "weekly_analysis.txt"

with open("weekly_analysis.txt", "w") as f:
    f.write("\n".join(fateha_summary) + "\n\n")
    f.write("\n".join(sarina_summary) + "\n\n")
    f.write("\n".join(najmul_summary) + "\n")

print("✅ weekly_analysis.txt has been generated.")