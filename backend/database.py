import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "bmci.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        price REAL,
        bmci_score INTEGER,
        signal TEXT,
        rsi REAL,
        macd TEXT,
        cycle_phase TEXT,
        risk_level TEXT,
        ai_comment TEXT,
        created_at TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        lot REAL NOT NULL,
        cost REAL NOT NULL,
        created_at TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS alarms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        condition_text TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT
    )
    ''')

    conn.commit()
    conn.close()

def save_analysis(payload: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO analyses
    (symbol, price, bmci_score, signal, rsi, macd, cycle_phase, risk_level, ai_comment, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        payload.get("symbol"),
        payload.get("price"),
        payload.get("bmci_score"),
        payload.get("signal"),
        payload.get("indicators", {}).get("rsi"),
        payload.get("indicators", {}).get("macd_signal"),
        payload.get("cycle", {}).get("phase"),
        payload.get("risk", {}).get("risk_level"),
        payload.get("ai_comment"),
        datetime.now().isoformat(timespec="seconds")
    ))
    conn.commit()
    conn.close()

def get_last_analyses(limit: int = 20):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

def get_portfolio():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM portfolio ORDER BY id DESC")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

def add_portfolio_item(symbol: str, lot: float, cost: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO portfolio (symbol, lot, cost, created_at) VALUES (?, ?, ?, ?)",
        (symbol.upper(), lot, cost, datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

def get_alarms():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM alarms ORDER BY id DESC")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

def add_alarm(symbol: str, condition_text: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alarms (symbol, condition_text, is_active, created_at) VALUES (?, ?, 1, ?)",
        (symbol.upper(), condition_text, datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()
