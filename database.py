import os, sqlite3
import pandas as pd
from datetime import date, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "trackr.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('Expense','Income')),
            amount REAL NOT NULL CHECK(amount > 0),
            payment_method TEXT DEFAULT 'Other',
            notes TEXT DEFAULT '',
            is_demo INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL CHECK(amount > 0),
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target REAL NOT NULL CHECK(target > 0),
            saved REAL NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")

def add_transaction(d, desc, category, typ, amount, method="Other", notes="", is_demo=0):
    with get_connection() as conn:
        conn.execute("INSERT INTO transactions(date,description,category,type,amount,payment_method,notes,is_demo) VALUES(?,?,?,?,?,?,?,?)",
                     (str(d), str(desc), str(category), str(typ), float(amount), str(method), str(notes), int(is_demo)))

def update_transaction(txid, d, desc, category, typ, amount, method, notes):
    with get_connection() as conn:
        conn.execute("UPDATE transactions SET date=?,description=?,category=?,type=?,amount=?,payment_method=?,notes=? WHERE id=?",
                     (str(d), str(desc), str(category), str(typ), float(amount), str(method), str(notes), int(txid)))

def delete_transaction(txid):
    with get_connection() as conn:
        conn.execute("DELETE FROM transactions WHERE id=?", (int(txid),))

def get_transactions():
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT id,date,description,category,type,amount,payment_method,notes,is_demo FROM transactions ORDER BY date DESC, id DESC", conn)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        df["month"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m")
    else:
        df["month"] = pd.Series(dtype=str)
    return df

def set_budget(category, amount):
    with get_connection() as conn:
        conn.execute("INSERT INTO budgets(category,amount) VALUES(?,?) ON CONFLICT(category) DO UPDATE SET amount=excluded.amount, updated_at=CURRENT_TIMESTAMP",
                     (str(category), float(amount)))

def get_budgets():
    with get_connection() as conn:
        return pd.read_sql_query("SELECT id,category,amount FROM budgets ORDER BY category", conn)

def add_goal(name, target):
    with get_connection() as conn:
        conn.execute("INSERT INTO goals(name,target,saved) VALUES(?,?,0)", (str(name), float(target)))

def get_goals():
    with get_connection() as conn:
        return pd.read_sql_query("SELECT id,name,target,saved FROM goals ORDER BY id DESC", conn)

def update_goal(goal_id, saved):
    with get_connection() as conn:
        conn.execute("UPDATE goals SET saved=? WHERE id=?", (float(saved), int(goal_id)))

def seed_demo_data():
    existing = get_transactions()
    if not existing.empty and int(existing["is_demo"].sum()) > 0:
        return
    today = date.today()
    examples = [
        (-1,"Weekly groceries","Food & Dining","Expense",1450,"UPI","Groceries"),
        (-2,"Metro and cab","Transport","Expense",480,"UPI","Commute"),
        (-3,"Monthly salary","Salary","Income",42000,"Bank transfer","Monthly income"),
        (-4,"Electricity bill","Bills & Utilities","Expense",1250,"UPI","Utility bill"),
        (-5,"Coffee with friends","Food & Dining","Expense",390,"Card","Cafe"),
        (-7,"Online course","Education","Expense",999,"Card","Learning"),
        (-8,"Freelance design","Freelance","Income",4500,"Bank transfer","Side income"),
        (-10,"Gym membership","Health","Expense",1800,"UPI","Fitness"),
        (-12,"Movie night","Entertainment","Expense",720,"Card","Weekend"),
        (-15,"New backpack","Shopping","Expense",2200,"Card","Personal"),
        (-20,"Rent","Rent","Expense",10000,"Bank transfer","Monthly rent"),
        (-24,"Fuel","Transport","Expense",1100,"UPI","Travel"),
    ]
    with get_connection() as conn:
        for days, desc, cat, typ, amount, method, notes in examples:
            d = (today + timedelta(days=days)).isoformat()
            conn.execute("INSERT INTO transactions(date,description,category,type,amount,payment_method,notes,is_demo) VALUES(?,?,?,?,?,?,?,1)",
                         (d,desc,cat,typ,amount,method,notes))
        conn.execute("INSERT OR IGNORE INTO budgets(category,amount) VALUES('Food & Dining',6000)")
        conn.execute("INSERT OR IGNORE INTO budgets(category,amount) VALUES('Transport',2500)")
        conn.execute("INSERT OR IGNORE INTO budgets(category,amount) VALUES('Shopping',3000)")

def clear_demo_data():
    with get_connection() as conn:
        conn.execute("DELETE FROM transactions WHERE is_demo=1")
