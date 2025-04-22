import sqlite3
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime

# Setup
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

DB_NAME = "final_project.db"
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

### PART 4: Reddit Word Cloud ###
cur.execute('''
    SELECT title
    FROM RedditPosts
    WHERE mentioned_college = 1 OR mentioned_student = 1 OR mentioned_campus = 1
''')
titles = cur.fetchall()
text = " ".join([t[0] for t in titles if t[0]])

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color='white',
    colormap='plasma',
    max_words=100
).generate(text)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Common Words in Reddit Posts (Keywords: student, college, campus)", fontsize=14)
plt.tight_layout()
plt.show()

### PART 5: Precipitation Line Chart ###
cur.execute('''
    SELECT date, CAST(REPLACE(precipitation, ' mm', '') AS REAL)
    FROM Weather2025
    WHERE date BETWEEN '2025-04-10' AND '2025-04-16'
    ORDER BY date ASC
''')
rows = cur.fetchall()
dates = [datetime.strptime(row[0], "%Y-%m-%d").strftime("%b %d") for row in rows]
precip = [row[1] for row in rows]

plt.figure(figsize=(10, 5))
plt.plot(dates, precip, marker='o', color='royalblue', linewidth=2)
plt.title("Daily Precipitation in Ann Arbor (Apr 10–16)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Precipitation (mm)")
plt.grid(True, linestyle='--', alpha=0.6)

if "Apr 10" in dates:
    i = dates.index("Apr 10")
    plt.annotate("📌 April 10", xy=(dates[i], precip[i]), xytext=(dates[i], precip[i]+1),
                 ha='center', arrowprops=dict(arrowstyle='->', color='gray'))

plt.tight_layout()
plt.show()

### PART 6: Bar Chart of Genre Frequency + Weather Summary (Fateha) ###
cur.execute('''
    SELECT g.name, COUNT(*) AS genre_count
    FROM Books b
    JOIN Genres g ON b.genre_id = g.genre_id
    WHERE b.year = 2025 AND b.month = 4 AND b.day = 13
    GROUP BY g.name
''')
book_rows = cur.fetchall()
genres = [row[0] for row in book_rows]
counts = [row[1] for row in book_rows]

cur.execute('''
    SELECT 
        ROUND(AVG(CAST(REPLACE(precipitation, ' mm', '') AS REAL)), 2),
        ROUND(AVG(CAST(REPLACE(temp_max, ' °F', '') AS REAL)), 1),
        ROUND(AVG(CAST(REPLACE(temp_min, ' °F', '') AS REAL)), 1)
    FROM Weather2025
    WHERE date BETWEEN '2025-04-06' AND '2025-04-13'
''')
avg_precip, avg_high, avg_low = cur.fetchone()

plt.figure(figsize=(10, 6))
plt.barh(genres, counts, color='mediumpurple')
plt.xlabel("Number of Books")
plt.ylabel("Genre/List Name")
plt.title(
    f"NYT Bestseller Genres (Week of Apr 6–13)\n"
    f"Avg Weather: {avg_high}°F / {avg_low}°F | Precipitation: {avg_precip} mm",
    fontsize=14
)
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.show()
