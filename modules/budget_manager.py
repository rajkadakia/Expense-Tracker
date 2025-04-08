import sqlite3
from datetime import datetime, timedelta

def set_budget(user_id, category, amount,start_date,end_date):
    """Sets a budget for a specific category."""
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    # Auto-generate dates
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")  # 30 days from now

    cursor.execute('''
        INSERT INTO budgets (user_id, category, budget_limit, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, category, amount, start_date, end_date))

    conn.commit()
    conn.close()
    print(f"✅ Budget set for {category}: {amount}")


def get_budget(user_id):
    """Retrieves all budgets."""
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM budgets")
    budgets = cursor.fetchall()
    
    conn.close()
    return budgets

def update_budget(budget_id, amount):
    """Updates an existing budget."""
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE budgets
        SET amount = ?
        WHERE id = ?
    ''', (amount, budget_id))
    
    conn.commit()
    conn.close()
    print(f"✅ Budget {budget_id} updated!")

def delete_budget(budget_id):
    """Deletes a budget by ID."""
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
    
    conn.commit()
    conn.close()
    print(f"✅ Budget {budget_id} deleted!")
