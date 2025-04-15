# nyt_books.py
import requests
import sqlite3
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

DB_NAME = "final_project.db"
API_KEY = open("nyt_api.txt").read().strip()
LIST_NAME = "graphic-books-and-manga" # genres students might be interested in
DATE = "2025-04-10" # dates

def drop_books_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Books")
    conn.commit()
    conn.close()
    print("Books table dropped.")


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Authors table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # NYTBooks table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            book_id TEXT PRIMARY KEY,
            title TEXT,
            rank INTEGER,
            published_date TEXT,
            list_name TEXT,
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

def insert_books():
    url = f"https://api.nytimes.com/svc/books/v3/lists/{DATE}/{LIST_NAME}.json?api-key={API_KEY}"
    resp = requests.get(url)
    data = resp.json()
    
    books = data["results"]["books"]
    published_date = data["results"]["published_date"]

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    new_books = 0

    for book in books:
        book_id = book["primary_isbn13"]  # unique identifier
        title = book["title"]
        author_name = book["author"]
        rank = book["rank"]
        list_name = data["results"]["list_name"]

        # check for duplicates
        cur.execute("SELECT book_id FROM Books WHERE book_id = ?", (book_id,))
        if cur.fetchone():
            continue

        author_id = get_or_create_author_id(conn, cur, author_name)

        cur.execute('''
            INSERT INTO Books (book_id, title, rank, published_date, list_name, author_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (book_id, title, rank, published_date, list_name, author_id))
        new_books += 1

        if new_books >= 25:  # limit per execution
            break

    conn.commit()
    conn.close()
    print(f"{new_books} books inserted from NYT list.")

def main():
    # drop_books_table()
    create_tables()
    insert_books()

if __name__ == "__main__":
    main()
