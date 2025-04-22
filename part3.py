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
# ----------------------------------------------------
cur.execute('''
    SELECT 
        ROUND(AVG(CAST(REPLACE(precipitation, ' mm', '') AS REAL)), 2),
        ROUND(AVG(CAST(REPLACE(temp_max, ' °F', '') AS REAL)), 1),
        ROUND(AVG(CAST(REPLACE(temp_min, ' °F', '') AS REAL)), 1)
    FROM Weather2025
    WHERE date BETWEEN '2025-04-06' AND '2025-04-13'
''')
avg_precip, avg_temp_max, avg_temp_min = cur.fetchone()

cur.execute('''
    SELECT g.name, COUNT(*) AS genre_count, AVG(b.rank)
    FROM Books b
    JOIN Genres g ON b.genre_id = g.genre_id
    WHERE b.year = 2025 AND b.month = 4 AND b.day = 13
    GROUP BY g.name
''')
books_results = cur.fetchall()

fateha_summary = ["--- Book Genre Trends with Weekly Weather Averages (Fateha) ---"]
fateha_summary.append(
    f"Avg Precipitation: {avg_precip} mm | Avg High: {avg_temp_max} °F | Avg Low: {avg_temp_min} °F\n"
)

for genre_name, count, avg_rank in books_results:
    fateha_summary.append(
        f"Genre/List: {genre_name}, Count: {count}, Avg Rank: {round(avg_rank, 2)}"
    )

# ----------------------------------------------------
# SARINA'S SECTION: Reddit + Weather Analysis (4/10, 4/14, 4/15, 4/17)
# ----------------------------------------------------
cur.execute('''
    SELECT r.year, r.month, r.day,
           w.precipitation,
           COUNT(r.post_id),
           AVG(r.upvotes),
           AVG(r.num_comments)
    FROM RedditPosts r
    LEFT JOIN Weather2025 w 
        ON DATE(r.year || '-' || printf('%02d', r.month) || '-' || printf('%02d', r.day)) = w.date
    WHERE DATE(r.year || '-' || printf('%02d', r.month) || '-' || printf('%02d', r.day)) 
          IN ('2025-04-10', '2025-04-14', '2025-04-15', '2025-04-17')
    GROUP BY r.year, r.month, r.day, w.precipitation
''')
reddit_weather_results = cur.fetchall()

sarina_summary = ["--- Reddit Engagement by Weather (Sarina) ---"]
for row in reddit_weather_results:
    date_str = f"{row[0]:04d}-{row[1]:02d}-{row[2]:02d}"
    weather = row[3] if row[3] is not None else "No weather data"
    sarina_summary.append(
        f"Date: {date_str}, Weather: {weather}, Posts: {row[4]}, "
        f"Avg Upvotes: {round(row[5], 2)}, Avg Comments: {round(row[6], 2)}"
    )

# ----------------------------------------------------
# NAJMUL'S SECTION: Weekly Weather Summary (4/6–4/13)
# ----------------------------------------------------
cur.execute('''
    SELECT 
        SUM(CASE WHEN CAST(REPLACE(precipitation, ' mm', '') AS REAL) = 0 THEN 1 ELSE 0 END),
        SUM(CASE WHEN CAST(REPLACE(precipitation, ' mm', '') AS REAL) > 0 AND CAST(REPLACE(precipitation, ' mm', '') AS REAL) <= 2 THEN 1 ELSE 0 END),
        SUM(CASE WHEN CAST(REPLACE(precipitation, ' mm', '') AS REAL) > 2 THEN 1 ELSE 0 END)
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
# WRITE TO TEXT FILE
# ----------------------------------------------------
with open("weekly_analysis.txt", "w") as f:
    f.write("\n".join(fateha_summary) + "\n\n")
    f.write("\n".join(sarina_summary) + "\n\n")
    f.write("\n".join(najmul_summary) + "\n")

print("✅ weekly_analysis.txt has been generated.")
