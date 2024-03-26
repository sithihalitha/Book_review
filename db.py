import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
        return conn
    except Error as e:
        print(e)
    return conn


def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication_year INTEGER NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            text_review TEXT,
            rating INTEGER,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
        """)
        conn.commit()
    except Error as e:
        print(e)

# CRUD Operations for Books
def add_book(conn, title, author, publication_year):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)", (title, author, publication_year))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None

def get_all_books(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []

def get_book_by_id(conn, book_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
        return cursor.fetchone()
    except Error as e:
        print(e)
        return None

def update_book(conn, book_id, title, author, publication_year):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET title=?, author=?, publication_year=? WHERE id=?", (title, author, publication_year, book_id))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def delete_book(conn, book_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

# CRUD Operations for Reviews
def add_review(conn, book_id, text_review, rating):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reviews (book_id, text_review, rating) VALUES (?, ?, ?)", (book_id, text_review, rating))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None

def get_reviews_for_book(conn, book_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reviews WHERE book_id=?", (book_id,))
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []

if __name__ == '__main__':
    db_file = 'book_review_system.db'
    conn = create_connection(db_file)
    if conn is not None:
        create_tables(conn)
    else:
        print("Error: Unable to connect to the database.")
