# nyt_books.py
import requests
import sqlite3
import os
from datetime import datetime

# set up file paths so it works no matter where we run it from
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

DB_NAME = "final_project.db"
API_KEY = open("nyt_api.txt").read().strip()
LIST_NAME = "advice-how-to-and-miscellaneous"
'''Genres: 
advice-how-to-and-miscellaneous
hardcover-fiction
hardcover-nonfiction
young-adult-hardcover
graphic-books-and-manga
series-books
education
business-books
'''
DATE = "2025-04-20"  # update this weekly if pulling a different date's list

def drop_books_table():
    # only use this if you need to fully reset the Books table
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Books")
    conn.commit()
    conn.close()
    print("Books table dropped.")

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create Genres table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Genres (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Authors table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Books table with split date and foreign keys
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
    cur.execute("INSERT INTO Genres (name) VALUES (?)", (genre_name,))
    conn.commit()
    return cur.lastrowid

def insert_books():
    url = f"https://api.nytimes.com/svc/books/v3/lists/{DATE}/{LIST_NAME}.json?api-key={API_KEY}"
    resp = requests.get(url)
    data = resp.json()

    if "results" not in data or "books" not in data["results"]:
        print("No books found for this list or date.")
        return

    books = data["results"]["books"]
    published_date = data["results"]["published_date"]
    genre_name = data["results"]["list_name"]

    # Convert published_date to year, month, day
    try:
        pub_dt = datetime.strptime(published_date, "%Y-%m-%d")
        year = pub_dt.year
        month = pub_dt.month
        day = pub_dt.day
    except Exception as e:
        print(f"Invalid published_date: {published_date}")
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    new_books = 0

    genre_id = get_or_create_genre_id(conn, cur, genre_name)

    for book in books:
        book_id = book["primary_isbn13"]   # unique key
        title = book["title"]
        author_name = book["author"]
        rank = book["rank"]

        # skip if book is already in the database
        cur.execute("SELECT book_id FROM Books WHERE book_id = ?", (book_id,))
        if cur.fetchone():
            continue

        author_id = get_or_create_author_id(conn, cur, author_name)

        cur.execute('''
            INSERT INTO Books (book_id, title, rank, year, month, day, genre_id, author_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (book_id, title, rank, year, month, day, genre_id, author_id))
        new_books += 1

        if new_books >= 25:  # limit per execution
            break

    conn.commit()
    conn.close()
    print(f"{new_books} books inserted from NYT list.")

def main():
    # drop_books_table()  # uncomment only if you want to reset the Books table
    create_tables()
    insert_books()

if __name__ == "__main__":
    main()
