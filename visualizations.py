import sqlite3
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

DB_NAME = "final_project.db"
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

### part 4: reddit word cloud ###
cur.execute('''
    SELECT r.title
    FROM RedditPosts r
    JOIN Weather2025 w ON DATE(r.date) = w.date
    WHERE r.keyword IN ('college', 'student', 'campus')
''')
titles = cur.fetchall()
text = " ".join([t[0] for t in titles if t[0] is not None])

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color='white',
    colormap='plasma',
    max_words=100
).generate(text)

# displaying word cloud
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Common Words in Reddit Posts (Keywords: student, college, campus)", fontsize=14)
plt.tight_layout()
plt.show()
