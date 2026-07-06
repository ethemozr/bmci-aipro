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
