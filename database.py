import sqlite3
from sqlite3 import Error

def get_db_connection(db_path='habits.db'):
    """Creates a database connection."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        # Enforce Foreign Key support
        conn.execute("PRAGMA foreign_keys = ON") 
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_tables(conn):
    """Creates the habits and check_offs tables."""
    sql_create_habits = """
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        periodicity TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL
    );
    """
    sql_create_checkoffs = """
    CREATE TABLE IF NOT EXISTS check_offs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_habits)
        c.execute(sql_create_checkoffs)
    except Error as e:
        print(f"Error creating tables: {e}")

def save_new_habit(conn, name, periodicity, created_at):
    """Inserts a new habit and returns its ID."""
    sql = 'INSERT INTO habits(name, periodicity, created_at) VALUES(?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, (name, periodicity, created_at))
    conn.commit()
    return cur.lastrowid

def save_new_checkoff(conn, habit_id, timestamp):
    """Inserts a new check-off."""
    sql = 'INSERT INTO check_offs(habit_id, timestamp) VALUES(?,?)'
    cur = conn.cursor()
    cur.execute(sql, (habit_id, timestamp))
    conn.commit()

def fetch_all_habits_and_checkoffs(conn):
    """Retrieves all raw data."""
    cur = conn.cursor()
    cur.execute("SELECT id, name, periodicity, created_at FROM habits")
    habits = cur.fetchall()
    
    cur.execute("SELECT habit_id, timestamp FROM check_offs")
    checkoffs = cur.fetchall()
    return habits, checkoffs

def delete_habit_by_id(conn, habit_id):
    """Deletes a habit and its check-offs."""
    sql = 'DELETE FROM habits WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (habit_id,))
    conn.commit()