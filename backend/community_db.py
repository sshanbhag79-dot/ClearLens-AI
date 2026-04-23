import sqlite3
import os
from datetime import datetime

# Build path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "biofilter_community.db")

def get_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database by creating the flags table if it doesn't exist."""
    print(f"Initializing database at: {DB_NAME}")
    conn = get_connection()
    c = conn.cursor()
    
    # Create table with username column
    c.execute('''
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT NOT NULL,
            vote_type TEXT CHECK(vote_type IN ('vouch', 'flag')),
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            username TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Migration: Check if username column exists, if not add it
    try:
        c.execute("SELECT username FROM flags LIMIT 1")
    except sqlite3.OperationalError:
        print("Migrating database: Adding username column...")
        c.execute("ALTER TABLE flags ADD COLUMN username TEXT")

    # Migration: Check if rating column exists
    try:
        c.execute("SELECT rating FROM flags LIMIT 1")
    except sqlite3.OperationalError:
        print("Migrating database: Adding rating column...")
        c.execute("ALTER TABLE flags ADD COLUMN rating INTEGER")
    
    conn.commit()
    conn.close()

def save_vote(barcode, rating, comment, username="Anonymous"):
    """
    Saves a new review with rating.
    
    Args:
        barcode (str): The product barcode.
        rating (int): Star rating (1-5).
        comment (str): User comment.
        username (str): The username of the voter.
    """
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5")

    conn = get_connection()
    c = conn.cursor()
    try:
        # Map rating to vote_type to satisfy legacy CHECK constraint
        # 4-5 stars = vouch, 1-3 stars = flag
        vote_type = 'vouch' if rating >= 4 else 'flag'
        
        c.execute('''
            INSERT INTO flags (barcode, vote_type, rating, comment, username) 
            VALUES (?, ?, ?, ?, ?)
        ''', (barcode, vote_type, rating, comment, username))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving review: {e}")
    finally:
        conn.close()

def get_vote_counts(barcode):
    """
    Retrieves the total count and average rating for a specific barcode.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT 
            COUNT(*) as total_reviews,
            AVG(rating) as average_rating
        FROM flags
        WHERE barcode = ? AND rating IS NOT NULL
    ''', (barcode,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {
            'total_reviews': result['total_reviews'],
            'average_rating': round(result['average_rating'], 1) if result['average_rating'] else 0.0
        }
    return {'total_reviews': 0, 'average_rating': 0.0}

def get_product_activity(barcode, limit=50):
    """
    Retrieves recent usage activity (reviews) for a barcode.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT rating, comment, username, timestamp
        FROM flags
        WHERE barcode = ? AND comment IS NOT NULL AND comment != ""
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (barcode, limit))
    
    rows = c.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
    # Example usage
    test_barcode = "123456789"
    save_vote(test_barcode, "vouch", "Great product!")
    save_vote(test_barcode, "flag", "Contains peanuts not listed.")
    
    counts = get_vote_counts(test_barcode)
    print(f"Barcode {test_barcode}: Vouches={counts['vouch_count']}, Flags={counts['flag_count']}")
