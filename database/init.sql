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
);

CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    lot REAL NOT NULL,
    cost REAL NOT NULL,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS alarms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    condition_text TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TEXT
);
