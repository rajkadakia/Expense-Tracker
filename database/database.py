import sqlite3

# Connect to the database
conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

# Function to check if a table exists
def table_exists(table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    return cursor.fetchone() is not None

#  Create Tables (Only if They Don't Exist)
if not table_exists("users"):
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )''')

if not table_exists("income"):
    cursor.execute('''CREATE TABLE income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount FLOAT NOT NULL,
        source TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

if not table_exists("expenses"):
    cursor.execute('''CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount FLOAT NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

if not table_exists("recurring_expenses"):
    cursor.execute('''CREATE TABLE recurring_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount FLOAT NOT NULL,
        category TEXT NOT NULL,
        frequency TEXT NOT NULL,
        start_date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

if not table_exists("budgets"):
    cursor.execute('''CREATE TABLE budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        budget_limit FLOAT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

if not table_exists("savings"):
    cursor.execute('''CREATE TABLE savings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        goal_name TEXT NOT NULL,
        target_amount FLOAT NOT NULL,
        saved_amount FLOAT NOT NULL DEFAULT 0,
        deadline TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

if not table_exists("transactions"):
    cursor.execute('''CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        amount FLOAT NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

conn.commit()
print("Tables checked and created if not existing.")

# Function to check if data exists in a table
def is_table_empty(table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    return cursor.fetchone()[0] == 0

# Insert sample data only if the users table is empty
if is_table_empty("users"):
    print(" Inserting sample data...")
    
    # Sample Users
    cursor.execute("INSERT INTO users (name, email) VALUES ('Alice Johnson', 'alice@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Bob Smith', 'bob@example.com')")

    # Sample Income
    cursor.execute("INSERT INTO income (user_id, amount, source, date) VALUES (1, 5000, 'Salary', '2024-03-01')")
    cursor.execute("INSERT INTO income (user_id, amount, source, date) VALUES (2, 6000, 'Freelancing', '2024-03-05')")

    # Sample Expenses
    cursor.execute("INSERT INTO expenses (user_id, amount, category, date, description) VALUES (1, 100, 'Groceries', '2024-03-02', 'Bought fruits and veggies')")
    cursor.execute("INSERT INTO expenses (user_id, amount, category, date, description) VALUES (1, 50, 'Transport', '2024-03-03', 'Bus fare')")
    cursor.execute("INSERT INTO expenses (user_id, amount, category, date, description) VALUES (2, 200, 'Dining Out', '2024-03-06', 'Dinner at a restaurant')")

    # Sample Recurring Expenses
    cursor.execute("INSERT INTO recurring_expenses (user_id, amount, category, frequency, start_date) VALUES (1, 100, 'Internet', 'monthly', '2024-03-01')")
    cursor.execute("INSERT INTO recurring_expenses (user_id, amount, category, frequency, start_date) VALUES (2, 50, 'Netflix', 'monthly', '2024-03-01')")

    # Sample Budgets
    cursor.execute("INSERT INTO budgets (user_id, category, budget_limit, start_date, end_date) VALUES (1, 'Groceries', 500, '2024-03-01', '2024-03-31')")
    cursor.execute("INSERT INTO budgets (user_id, category, budget_limit, start_date, end_date) VALUES (2, 'Dining Out', 300, '2024-03-01', '2024-03-31')")

    # Sample Savings Goals
    cursor.execute("INSERT INTO savings (user_id, goal_name, target_amount, saved_amount, deadline) VALUES (1, 'Emergency Fund', 2000, 500, '2024-12-31')")
    cursor.execute("INSERT INTO savings (user_id, goal_name, target_amount, saved_amount, deadline) VALUES (2, 'Vacation', 3000, 1000, '2024-08-01')")

    # Sample Transactions (General Log)
    cursor.execute("INSERT INTO transactions (user_id, type, amount, category, date) VALUES (1, 'income', 5000, 'Salary', '2024-03-01')")
    cursor.execute("INSERT INTO transactions (user_id, type, amount, category, date) VALUES (2, 'expense', 200, 'Dining Out', '2024-03-06')")

    conn.commit()
    print(" Sample data inserted successfully!")
else:
    print(" Sample data already exists. Skipping insertion.")

# Close connection
conn.close()
