import sqlite3

# Connect to the database
conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

# Fetch all users
cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()
print("\n📌 Users:")
for user in users:
    print(user)

# Fetch all expenses
cursor.execute("SELECT * FROM expenses;")
expenses = cursor.fetchall()
print("\n📌 Expenses:")
for expense in expenses:
    print(expense)

# Fetch all budgets
cursor.execute("SELECT * FROM budgets;")
budgets = cursor.fetchall()
print("\n📌 Budgets:")
for budget in budgets:
    print(budget)

conn.close()
