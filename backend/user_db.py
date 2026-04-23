import sqlite3
import json
import datetime

DB_NAME = "biofilter_community.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            allergies TEXT,
            diets TEXT,
            strictness TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_user_profile(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            "username": row["username"],
            "allergies": json.loads(row["allergies"]) if row["allergies"] else [],
            "diets": json.loads(row["diets"]) if row["diets"] else [],
            "strictness": row["strictness"]
        }
    return None

def update_user_profile(username, profile_data):
    conn = get_connection()
    c = conn.cursor()
    
    allergies_json = json.dumps(profile_data.get("allergies", []))
    diets_json = json.dumps(profile_data.get("diets", []))
    strictness = profile_data.get("strictness", "Strict")
    
    # Check if user exists
    c.execute('SELECT username FROM users WHERE username = ?', (username,))
    exists = c.fetchone()
    
    if exists:
        c.execute('''
            UPDATE users 
            SET allergies = ?, diets = ?, strictness = ?, updated_at = CURRENT_TIMESTAMP
            WHERE username = ?
        ''', (allergies_json, diets_json, strictness, username))
    else:
        c.execute('''
            INSERT INTO users (username, allergies, diets, strictness)
            VALUES (?, ?, ?, ?)
        ''', (username, allergies_json, diets_json, strictness))
        
    conn.commit()
    conn.close()
    return True
