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
LIST_NAME = "series-books" 
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
DATE = "2025-04-13" # update this weekly if pulling a different date's list

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

    # make the Authors table if it doesn’t exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # NYTBooks table
    # make the Books table — book_id is primary to avoid duplicates
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
    # if the author already exists, grab their id
    cur.execute("SELECT author_id FROM Authors WHERE name = ?", (author_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        # otherwise, add them to the Authors table and return new id
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
        book_id = book["primary_isbn13"]   # this will be our unique key
        title = book["title"]
        author_name = book["author"]
        rank = book["rank"]
        list_name = data["results"]["list_name"]

        # skip if book is already in the database
        cur.execute("SELECT book_id FROM Books WHERE book_id = ?", (book_id,))
        if cur.fetchone():
            continue

        author_id = get_or_create_author_id(conn, cur, author_name)

        # insert the new book entry
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
    # drop_books_table() # only uncomment this if you want to reset the Books table
    create_tables()
    insert_books()

if __name__ == "__main__":
    main()
