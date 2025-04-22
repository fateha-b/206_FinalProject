import requests
import sqlite3
import os
from datetime import datetime

# Set up file paths so it works no matter where we run it from
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

DB_NAME = "final_project.db"
API_KEY = open("nyt_api.txt").read().strip()

LIST_NAME = "advice-how-to-and-miscellaneous"   #change this manually
DATE = "2025-04-13"                             #change this manually

'''Genres: 
advice-how-to-and-miscellaneous
hardcover-fiction
hardcover-nonfictiona
young-adult-hardcover
graphic-books-and-manga
series-books
education
business-books
'''

def drop_books_and_genres_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Books")
    cur.execute("DROP TABLE IF EXISTS Genres")
    conn.commit()
    conn.close()
    print("Books and Genres tables dropped.")

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Genres (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            book_count INTEGER DEFAULT 0
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            book_id TEXT PRIMARY KEY,
            title TEXT,
            rank INTEGER,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            genre_id INTEGER,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES Authors(author_id),
            FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
        )
    ''')

    conn.commit()
    conn.close()

def get_or_create_author_id(conn, cur, author_name):
    cur.execute("SELECT author_id FROM Authors WHERE name = ?", (author_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO Authors (name) VALUES (?)", (author_name,))
    conn.commit()
    return cur.lastrowid

def get_or_create_genre_id(conn, cur, genre_name):
    cur.execute("SELECT genre_id FROM Genres WHERE name = ?", (genre_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO Genres (name, book_count) VALUES (?, 0)", (genre_name,))
    conn.commit()
    return cur.lastrowid

def insert_books(date_str, list_name):
    url = f"https://api.nytimes.com/svc/books/v3/lists/{date_str}/{list_name}.json?api-key={API_KEY}"
    resp = requests.get(url)
    data = resp.json()

    if "results" not in data or "books" not in data["results"]:
        print(f"No books found for {list_name} on {date_str}.")
        return

    books = data["results"]["books"]
    published_date = data["results"]["published_date"]
    genre_name = data["results"]["list_name"]

    try:
        pub_dt = datetime.strptime(published_date, "%Y-%m-%d")
        year, month, day = pub_dt.year, pub_dt.month, pub_dt.day
    except Exception:
        print(f"Invalid date format: {published_date}")
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    new_books = 0

    genre_id = get_or_create_genre_id(conn, cur, genre_name)

    for book in books:
        book_id = book["primary_isbn13"]
        title = book["title"]
        author_name = book["author"]
        rank = book["rank"]

        cur.execute("SELECT book_id FROM Books WHERE book_id = ?", (book_id,))
        if cur.fetchone():
            continue

        author_id = get_or_create_author_id(conn, cur, author_name)

        cur.execute('''
            INSERT INTO Books (book_id, title, rank, year, month, day, genre_id, author_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (book_id, title, rank, year, month, day, genre_id, author_id))

        cur.execute('''
            UPDATE Genres
            SET book_count = book_count + 1
            WHERE genre_id = ?
        ''', (genre_id,))

        new_books += 1

    conn.commit()
    conn.close()
    print(f"{new_books} books inserted from {list_name} on {date_str}.")

def main():
    # drop_books_and_genres_tables()  #uncomment if you want to reset both tables
    create_tables()
    insert_books(DATE, LIST_NAME)

if __name__ == "__main__":
    main()
