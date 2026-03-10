import sqlite3

DATABASE_NAME = "pulse.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   email TEXT NOT NULL UNIQUE,
                   name TEXT NOT NULL
                   )
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS projects (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   description TEXT
                   )
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   description TEXT,
                   project_id INTEGER NOT NULL,
                   is_done INTEGER NOT NULL DEFAULT 0,
                   FOREIGN KEY (project_id) REFERENCES projects (id)
                   )
                   """)
    
    conn.commit()
    conn.close()