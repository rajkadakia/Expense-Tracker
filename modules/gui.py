import customtkinter as ctk
from tkinter import messagebox
from modules.expense_tracker import get_expenses, add_expense
from modules.budget_manager import get_budget, set_budget
from modules.user_manager import get_user, add_user
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import defaultdict

# Global variable to track logged-in user
current_user = None

# Function to handle user login
def login():
    global current_user
    name = name_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Please enter your name!")
        return

    user = get_user(name)
    if not user:
        messagebox.showinfo("New User", "User not found. Creating new account...")
        add_user(name, name + "@gmail.com")
        user = get_user(name)

    current_user = user[0]
    print("✅ Logged in user ID:", current_user)
    show_dashboard()

# Function to display the dashboard
def show_dashboard():
    login_frame.pack_forget()
    dashboard_frame.pack(fill='both', expand=True)

# Function to display expenses
def show_expenses():
    expenses_listbox.delete("1.0", "end")
    expenses = get_expenses(current_user)
    if not expenses:
        expenses_listbox.insert("end", "No expenses found.\n")
    else:
        expenses_listbox.insert("end", f"{'Date':<12} {'Category':<15} {'Amount':<10} Description\n")
        expenses_listbox.insert("end", "-" * 50 + "\n")
        for exp in expenses:
            expenses_listbox.insert("end", f"{exp[3]:<12} {exp[2]:<15} ₹{exp[1]:<10} {exp[4]}\n")

# Function to add a new expense
def add_expense_gui():
    amount = expense_amount_entry.get().strip()
    category = expense_category_entry.get().strip()

    if not amount or not category:
        messagebox.showerror("Error", "Please fill all fields!")
        return

    date = datetime.now().strftime("%Y-%m-%d")
    add_expense(current_user, float(amount), category, date, "Added via GUI")
    messagebox.showinfo("Success", "Expense added successfully!")
    show_expenses()

# Function to show budgets
def show_budget():
    budget_listbox.delete("1.0", "end")
    budgets = get_budget(current_user)
    if not budgets:
        budget_listbox.insert("end", "No budgets found.\n")
    else:
        budget_listbox.insert("end", f"{'Category':<15} {'Amount':<10} {'Start':<12} {'End':<12}\n")
        budget_listbox.insert("end", "-" * 60 + "\n")
        for b in budgets:
            budget_listbox.insert("end", f"{b[2]:<15} ₹{b[3]:<10} {b[4]:<12} {b[5]:<12}\n")

# Function to set a new budget
def set_budget_gui():
    category = budget_category_entry.get().strip()
    amount = budget_amount_entry.get().strip()

    if not category or not amount:
        messagebox.showerror("Error", "Please fill all fields!")
        return

    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    set_budget(current_user, category, float(amount), start_date, end_date)
    messagebox.showinfo("Success", "Budget set successfully!")
    show_budget()

# Insights Window (Embedded charts inside the window)
def open_insights_window():
    insights_window = ctk.CTkToplevel(root)
    insights_window.title("Insights Dashboard")
    insights_window.geometry("1000x800")

    ctk.CTkLabel(insights_window, text="📊 Insights & Analytics", font=("Arial", 20, "bold")).pack(pady=10)

    # Get data
    expenses = get_expenses(current_user)
    budgets = get_budget(current_user)

    # Calculate stats
    total_expense = sum(exp[1] for exp in expenses)
    total_budget = sum(b[3] for b in budgets)
    remaining_budget = total_budget - total_expense

    stats_text = f"Total Expense: ₹{total_expense}\nTotal Budget: ₹{total_budget}\nRemaining Budget: ₹{remaining_budget}"
    ctk.CTkLabel(insights_window, text=stats_text, font=("Arial", 14)).pack(pady=10)

    if not expenses:
        ctk.CTkLabel(insights_window, text="No expense data to show charts.", font=("Arial", 12)).pack(pady=5)
        return

    # Prepare data
    expense_totals = defaultdict(float)
    for exp in expenses:
        expense_totals[exp[2]] += exp[1]

    budget_totals = defaultdict(float)
    for b in budgets:
        budget_totals[b[2]] += b[3]

    all_categories = list(set(list(expense_totals.keys()) + list(budget_totals.keys())))
    expense_values = [expense_totals.get(cat, 0) for cat in all_categories]
    budget_values = [budget_totals.get(cat, 0) for cat in all_categories]

    # Matplotlib Figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Pie chart
    ax1.pie(expense_values, labels=all_categories, autopct='%1.1f%%', startangle=90)
    ax1.set_title("Expenses by Category")
    ax1.axis('equal')

    # Bar chart
    x = range(len(all_categories))
    ax2.bar(x, budget_values, width=0.4, label='Budget', align='center', color='green')
    ax2.bar(x, expense_values, width=0.4, label='Expenses', align='edge', color='orange')
    ax2.set_xlabel('Category')
    ax2.set_ylabel('Amount (₹)')
    ax2.set_title('Budget vs Expenses by Category')
    ax2.set_xticks(list(x))
    ax2.set_xticklabels(all_categories, rotation=45)
    ax2.legend()

    plt.tight_layout()

    # Embed the plot in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=insights_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

    plt.close(fig)  # Close to prevent external window

# GUI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Personalized Expense Tracker")
root.geometry("1000x700")

# Login Frame
login_frame = ctk.CTkFrame(root)
login_frame.pack(pady=40)

ctk.CTkLabel(login_frame, text="Personalized Expense Tracker", font=("Arial", 22, "bold")).pack(pady=15)
ctk.CTkLabel(login_frame, text="Enter your name to access your dashboard.", font=("Arial", 14)).pack(pady=5)

name_entry = ctk.CTkEntry(login_frame, width=300, placeholder_text="Enter your name")
name_entry.pack(pady=8)

ctk.CTkButton(login_frame, text="Login", width=120, command=login).pack(pady=15)

# Dashboard Frame
dashboard_frame = ctk.CTkFrame(root)

ctk.CTkLabel(dashboard_frame, text="Welcome to Your Expense Dashboard", font=("Arial", 20, "bold")).pack(pady=15)
ctk.CTkLabel(dashboard_frame, text="Manage your expenses and budgets easily.", font=("Arial", 14)).pack()

# Horizontal Layout Frame
horizontal_frame = ctk.CTkFrame(dashboard_frame)
horizontal_frame.pack(pady=15, fill='both', expand=True, padx=20)

# Expense Section
expense_frame = ctk.CTkFrame(horizontal_frame)
expense_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

ctk.CTkLabel(expense_frame, text="💸 Expense Management", font=("Arial", 16, "bold")).pack(pady=8)
ctk.CTkLabel(expense_frame, text="Add your expenses below:", font=("Arial", 12)).pack(pady=2)

expense_amount_entry = ctk.CTkEntry(expense_frame, width=250, placeholder_text="Amount (e.g., 50.00)")
expense_amount_entry.pack(pady=5)

expense_category_entry = ctk.CTkEntry(expense_frame, width=250, placeholder_text="Category (e.g., Food, Transport)")
expense_category_entry.pack(pady=5)

ctk.CTkButton(expense_frame, text="Add Expense", width=150, command=add_expense_gui).pack(pady=8)

ctk.CTkLabel(expense_frame, text="Your Expenses", font=("Arial", 14, "bold")).pack(pady=5)
expenses_listbox = ctk.CTkTextbox(expense_frame, height=300, width=400)
expenses_listbox.pack(pady=5, fill='both', expand=True)

ctk.CTkButton(expense_frame, text="Show Expenses", width=150, command=show_expenses).pack(pady=5)
ctk.CTkButton(expense_frame, text="Open Insights", width=150, command=open_insights_window).pack(pady=8)

# Budget Section
budget_frame = ctk.CTkFrame(horizontal_frame)
budget_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

ctk.CTkLabel(budget_frame, text="💰 Budget Management", font=("Arial", 16, "bold")).pack(pady=8)
ctk.CTkLabel(budget_frame, text="Set your budget below:", font=("Arial", 12)).pack(pady=2)

budget_category_entry = ctk.CTkEntry(budget_frame, width=250, placeholder_text="Category (e.g., Groceries)")
budget_category_entry.pack(pady=5)

budget_amount_entry = ctk.CTkEntry(budget_frame, width=250, placeholder_text="Budget Amount (e.g., 500.00)")
budget_amount_entry.pack(pady=5)

ctk.CTkButton(budget_frame, text="Set Budget", width=150, command=set_budget_gui).pack(pady=8)

ctk.CTkLabel(budget_frame, text="Your Budgets", font=("Arial", 14, "bold")).pack(pady=5)
budget_listbox = ctk.CTkTextbox(budget_frame, height=300, width=400)
budget_listbox.pack(pady=5, fill='both', expand=True)

ctk.CTkButton(budget_frame, text="Show Budgets", width=150, command=show_budget).pack(pady=5)
ctk.CTkButton(budget_frame, text="Open Insights", width=150, command=open_insights_window).pack(pady=8)

def run_app():
    root.mainloop()

if __name__ == "__main__":
    run_app()


