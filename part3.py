import sqlite3
import os

# Ensure script runs from correct directory
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# Connect to the database
DB_NAME = "final_project.db"
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# ----------------------------------------------------
# FATEHA'S SECTION: Books + Weekly Average Weather (4/6–4/13)
# Use NYT list dated 2025-04-13 (reflects week)
# Use average weather from 2025-04-06 to 2025-04-13
# ----------------------------------------------------
cur.execute('''
    SELECT 
        ROUND(AVG(CAST(REPLACE(precipitation, ' mm', '') AS REAL)), 2) AS avg_precip,
        ROUND(AVG(CAST(REPLACE(temp_max, ' °F', '') AS REAL)), 1) AS avg_temp_max,
        ROUND(AVG(CAST(REPLACE(temp_min, ' °F', '') AS REAL)), 1) AS avg_temp_min
    FROM Weather2025
    WHERE date BETWEEN '2025-04-06' AND '2025-04-13'
''')
avg_precip, avg_temp_max, avg_temp_min = cur.fetchone()

cur.execute('''
    SELECT list_name, COUNT(*) AS genre_count, AVG(rank) AS avg_rank
    FROM Books
    WHERE published_date = '2025-04-13'
    GROUP BY list_name
''')
books_results = cur.fetchall()

fateha_summary = ["--- Book Genre Trends with Weekly Weather Average (Fateha) ---"]
fateha_summary = ["--- Book Genre Trends with Weekly Weather Averages (Fateha) ---"]
fateha_summary.append(
    f"Avg Precipitation: {avg_precip} mm | Avg High: {avg_temp_max} °F | Avg Low: {avg_temp_min} °F\n"
)

for row in books_results:
    fateha_summary.append(
        f"Genre/List: {row[0]}, Count: {row[1]}, Avg Rank: {round(row[2], 2)}"
    )

# ----------------------------------------------------
# 🔹 SARINA'S SECTION: Reddit + Weather Analysis (4/10, 4/14, 4/15, 4/17)
# ----------------------------------------------------
cur.execute('''
    SELECT DATE(r.date) AS date_only,
           w.precipitation,
           COUNT(r.post_id) AS post_count,
           AVG(r.upvotes) AS avg_upvotes,
           AVG(r.num_comments) AS avg_comments
    FROM RedditPosts r
    LEFT JOIN Weather2025 w ON DATE(r.date) = w.date
    WHERE DATE(r.date) IN ('2025-04-10', '2025-04-14', '2025-04-15', '2025-04-17')
      AND r.keyword IN ('college', 'student', 'campus')
    GROUP BY DATE(r.date), w.precipitation
''')
reddit_weather_results = cur.fetchall()

sarina_summary = ["--- Reddit Engagement by Weather (Sarina) ---"]
for row in reddit_weather_results:
    weather = row[1] if row[1] is not None else "No weather data"
    sarina_summary.append(
        f"Date: {row[0]}, Weather: {weather}, Posts: {row[2]}, "
        f"Avg Upvotes: {round(row[3], 2)}, Avg Comments: {round(row[4], 2)}"
    )

# ----------------------------------------------------
# 🔹 NAJMUL'S SECTION: Weekly Weather Summary (4/6–4/13)
# ----------------------------------------------------
cur.execute('''
    SELECT 
        SUM(CASE WHEN CAST(REPLACE(precipitation, ' mm', '') AS REAL) = 0 THEN 1 ELSE 0 END) AS clear_days,
        SUM(CASE WHEN CAST(REPLACE(precipitation, ' mm', '') AS REAL) > 0 AND CAST(REPLACE(precipitation, ' mm', '') AS REAL) <= 2 THEN 1 ELSE 0 END) AS light_rain_days,
        SUM(CASE WHEN CAST(REPLACE(precipitation, ' mm', '') AS REAL) > 2 THEN 1 ELSE 0 END) AS rainy_days
    FROM Weather2025
    WHERE date BETWEEN '2025-04-06' AND '2025-04-13'
''')
clear_days, light_rain_days, rainy_days = cur.fetchone()

cur.execute('''
    SELECT 
        ROUND(AVG(CAST(REPLACE(temp_max, ' °F', '') AS REAL)), 1),
        ROUND(AVG(CAST(REPLACE(temp_min, ' °F', '') AS REAL)), 1),
        ROUND(AVG(CAST(REPLACE(humidity, ' %', '') AS REAL)), 1)
    FROM Weather2025
    WHERE date BETWEEN '2025-04-06' AND '2025-04-13'
''')
avg_high, avg_low, avg_humidity = cur.fetchone()

najmul_summary = ["--- Weekly Weather Summary (Najmul) ---"]
najmul_summary.append(f"Clear days: {clear_days}")
najmul_summary.append(f"Light rain days (0–2 mm): {light_rain_days}")
najmul_summary.append(f"Rainy days (>2 mm): {rainy_days}\n")
najmul_summary.append(f"Avg High Temp: {avg_high} °F")
najmul_summary.append(f"Avg Low Temp: {avg_low} °F")
najmul_summary.append(f"Avg Humidity: {avg_humidity} %")

# ----------------------------------------------------
# 🔸 WRITE TO TEXT FILE (ALL MEMBERS CONTRIBUTE)
# ----------------------------------------------------
with open("weekly_analysis.txt", "w") as f:
    f.write("\n".join(fateha_summary) + "\n\n")
    f.write("\n".join(sarina_summary) + "\n\n")
    f.write("\n".join(najmul_summary) + "\n")

print("✅ weekly_analysis.txt has been generated.")
