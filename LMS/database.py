import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect("lms.db")

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            book TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

def issue_book(student_id, name, email, phone, book):
    conn = connect_db()
    cur = conn.cursor()

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    cur.execute("""
        INSERT INTO issued_books
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
    """, (student_id, name, email, phone, book, date, time))

    conn.commit()
    conn.close()

def get_books(student_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, book, date, time
        FROM issued_books
        WHERE student_id = ?
    """, (student_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_book(book_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM issued_books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()