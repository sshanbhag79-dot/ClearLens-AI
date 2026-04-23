import sqlite3
import datetime

DB_NAME = "daily_logs.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Explicitly creating the 'logs' table as requested by user
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT,            -- product_name
            calories INTEGER,     -- total calories
            grade TEXT,           -- Red, Yellow, Green
            barcode TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_meal(username, barcode, product_name, calories_per_100g, quantity, status, total_calories=None):
    """
    Logs a meal to the database.
    """
    if total_calories is not None:
        calories_total = total_calories
    else:
        calories_total = (calories_per_100g or 0) * quantity
    
    return log_food(username, product_name, int(calories_total), status, barcode)

def log_food(username, name, calories, grade, barcode=None):
    """
    Requested function to log food details directly.
    """
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO logs (username, barcode, name, calories, grade) 
            VALUES (?, ?, ?, ?, ?)
        ''', (username, barcode, name, calories, grade))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error logging food: {e}")
        return False
def delete_log(log_id):
    """
    Deletes a specific log record from the database.
    """
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('DELETE FROM logs WHERE id = ?', (log_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting log: {e}")
        return False
    finally:
        conn.close()

def get_daily_summary(username):
    """
    Retrieves the daily summary for the current day.
    Returns: { 'total_calories': int, 'upf_index': int (0-100% Red) }
    """
    today = datetime.date.today().isoformat()
    
    conn = get_connection()
    c = conn.cursor()
    
    # Get all logs for today
    c.execute('''
        SELECT calories, grade 
        FROM logs 
        WHERE username = ? AND date(timestamp) = ?
    ''', (username, today))
    
    rows = c.fetchall()
    conn.close()
    
    total_calories = 0
    red_calories = 0
    green_calories = 0
    
    for row in rows:
        cal = row['calories'] or 0
        grade = row['grade']
        
        total_calories += cal
        if grade == 'Red':
            red_calories += cal
        elif grade == 'Green':
            green_calories += cal
            
    # Calculate UPF Ratio (Percentage of calories from Red foods)
    upf_ratio = 0
    if total_calories > 0:
        upf_ratio = int((red_calories / total_calories) * 100)
        
    return {
        "total_calories": int(total_calories),
        "red_calories": int(red_calories),
        "clean_calories": int(green_calories),
        "upf_ratio": upf_ratio # % Red
    }

def get_daily_logs(username):
    """
    Retrieves the list of meal logs for the current day.
    """
    today = datetime.date.today().isoformat()
    
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT id, name, calories, grade, timestamp
        FROM logs 
        WHERE username = ? AND date(timestamp) = ?
        ORDER BY timestamp DESC
    ''', (username, today))
    
    rows = c.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
