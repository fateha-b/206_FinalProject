### code to make sure there are overlapping dates between reddit & weather data ###
# import sqlite3

# conn = sqlite3.connect('final_project.db')
# cur = conn.cursor()

# print("RedditPosts sample dates:")
# cur.execute('SELECT DISTINCT date FROM RedditPosts ORDER BY date DESC LIMIT 10')
# print(cur.fetchall())

# print("\nWeather2025 sample dates:")
# cur.execute('SELECT DISTINCT date FROM Weather2025 ORDER BY date DESC LIMIT 10')
# print(cur.fetchall())

# conn.close() 

import sqlite3

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()


### code to add in data from 4/10-4/14 bc i didnt manually scrape data on those dates
cur.execute("""
    SELECT * FROM RedditPosts
    WHERE date BETWEEN '2025-04-10' AND '2025-04-14'
""")
posts = cur.fetchall()
print(f"Total Reddit posts between April 10 and April 14: {len(posts)}")


### code to make sure there is overlapping data between reddit & weather ###
cur.execute('''
SELECT COUNT(*)
FROM RedditPosts
WHERE date IN (SELECT date FROM Weather2025)
''')

print("Reddit posts with matching weather data:", cur.fetchone()[0])

# conn.close()

# import sqlite3

# conn = sqlite3.connect('final_project.db')
# cur = conn.cursor()

cur.execute('''
    SELECT 
        W.weather_type,
        COUNT(*) AS total_posts,
        ROUND(AVG(post_counts.daily_count), 2) AS avg_posts_per_day
    FROM (
        SELECT 
            date,
            COUNT(*) AS daily_count
        FROM RedditPosts
        GROUP BY date
    ) AS post_counts
    JOIN (
        SELECT 
            date,
            CASE 
                WHEN CAST(SUBSTR(precipitation, 1, INSTR(precipitation, ' ') - 1) AS FLOAT) > 0.0 THEN 'Rainy'
                ELSE 'Sunny'
            END AS weather_type
        FROM Weather2025
    ) AS W
    ON post_counts.date = W.date
    GROUP BY W.weather_type
''')

results = cur.fetchall()

for row in results:
    print(f"Weather: {row[0]} | Total Posts: {row[1]} | Avg Posts/Day: {row[2]}")

conn.close()