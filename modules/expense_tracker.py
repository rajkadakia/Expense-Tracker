import sqlite3

def add_expense(user_id, amount, category, date, description=""):
    """Adds a new expense to the database."""
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, amount, category, date, description))
    
    conn.commit()
    conn.close()
    print("✅ Expense added successfully!")

def get_expenses(user_id):
    """Retrieves all expenses from the database."""
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))

    expenses = cursor.fetchall()
    
    conn.close()
    return expenses

def update_expense(expense_id, amount=None, category=None, date=None, description=None):
    """Updates an existing expense based on its ID."""
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()
    
    update_fields = []
    update_values = []
    
    if amount:
        update_fields.append("amount = ?")
        update_values.append(amount)
    if category:
        update_fields.append("category = ?")
        update_values.append(category)
    if date:
        update_fields.append("date = ?")
        update_values.append(date)
    if description:
        update_fields.append("description = ?")
        update_values.append(description)
    
    update_values.append(expense_id)
    
    cursor.execute(f'''
        UPDATE expenses
        SET {', '.join(update_fields)}
        WHERE id = ?
    ''', update_values)
    
    conn.commit()
    conn.close()
    print("✅ Expense updated successfully!")

def delete_expense(expense_id):
    """Deletes an expense by ID."""
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    
    
    conn.commit()
    conn.close()
    print("✅ Expense deleted successfully!")
