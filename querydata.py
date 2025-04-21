import sqlite3

conn = sqlite3.connect("/Users/fbushra/Documents/SI 206/206_FinalProject/final_project.db")
cur = conn.cursor()

cur.execute("SELECT title, author_id, published_date FROM Books ORDER BY published_date DESC LIMIT 5")
results = cur.fetchall()

for row in results:
    print(row)

conn.close()
