# google_books_api.py
import requests
import os
import sqlite3
import time

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

DB_NAME = "final_project.db"
API_URL = "https://www.googleapis.com/books/v1/volumes"
QUERY = "bestseller fiction OR young adult OR mystery OR self-help"

def load_api_key(filename="books_api.txt"):
    with open(filename, "r") as file:
        return file.read().strip()

def create_books_and_authors_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Authors table (author_id is PRIMARY KEY)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Books table with foreign key
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            book_id TEXT PRIMARY KEY,
            title TEXT,
            genre TEXT,
            release_date TEXT,
            average_rating REAL,
            ratings_count INTEGER,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES Authors(author_id)
        )
    ''')

    conn.commit()
    conn.close()

def get_or_create_author_id(conn, cur, author_name):
    cur.execute("SELECT author_id FROM Authors WHERE name = ?", (author_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        cur.execute("INSERT INTO Authors (name) VALUES (?)", (author_name,))
        conn.commit()
        return cur.lastrowid

def get_existing_ids():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT book_id FROM Books")
    existing_ids = {row[0] for row in cur.fetchall()}
    conn.close()
    return existing_ids


def get_books_data(api_key, start_index=0):
    params = {
        'q': QUERY,
        'startIndex': start_index,
        'maxResults': 25,
        'key': api_key,
        'printType': 'books'
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("items", [])

def insert_books_to_db(books):
    existing_ids = get_existing_ids()
    new_books = 0

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for book in books:
        volume_info = book.get("volumeInfo", {})
        book_id = book.get("id")
        if not book_id or book_id in existing_ids:
            continue

        title = volume_info.get("title", "Unknown Title")
        authors_list = volume_info.get("authors", ["Unknown"])
        author_name = authors_list[0]  
        genre = ", ".join(volume_info.get("categories", ["Unknown"]))
        release_date = volume_info.get("publishedDate", "Unknown")
        avg_rating = volume_info.get("averageRating", None)
        ratings_count = volume_info.get("ratingsCount", None)

        # Get author ID
        author_id = get_or_create_author_id(conn, cur, author_name)

        cur.execute('''
            INSERT INTO Books (book_id, title, genre, release_date, average_rating, ratings_count, author_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (book_id, title, genre, release_date, avg_rating, ratings_count, author_id))

        new_books += 1
        if new_books >= 25:
            break

    conn.commit()
    conn.close()
    print(f"{new_books} new books added.")

def main():
    api_key = load_api_key()
    create_books_and_authors_tables()
    start_index = len(get_existing_ids())
    books = get_books_data(api_key, start_index)
    insert_books_to_db(books)


if __name__ == "__main__":
    main()
