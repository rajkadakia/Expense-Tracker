import sqlite3

def add_user(name, email):
    """Adds a new user to the database."""
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO users (name, email)
        VALUES (?, ?)
    ''', (name, email))
    
    conn.commit()
    conn.close()
    print(f"✅ User '{name}' added successfully!")

def get_user(name):
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()  # 👈 fetchone(), not fetchall()

    conn.close()
    return user


