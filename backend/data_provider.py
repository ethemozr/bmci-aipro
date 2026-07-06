import math
import random
from datetime import datetime, timedelta
from .config import USE_REAL_DATA

def normalize_symbol(symbol: str) -> str:
    return symbol.upper().replace(".IS", "")

def demo_history(symbol: str, days: int = 220):
    random.seed(symbol.upper())
    price = random.uniform(20, 500)
    trend = random.uniform(-0.35, 0.65)
    start = datetime.now() - timedelta(days=days)
    candles = []

    for i in range(days):
        wave = 12 * math.sin(i / 11)
        noise = random.uniform(-3, 3)
        price = max(1, price + trend + wave * 0.04 + noise * 0.35)
        open_price = price + random.uniform(-2, 2)
        high = max(open_price, price) + random.uniform(0, 4)
        low = min(open_price, price) - random.uniform(0, 4)

        candles.append({
            "date": (start + timedelta(days=i)).strftime("%Y-%m-%d"),
            "open": round(open_price, 2),
            "high": round(high, 2),
            "low": round(max(0.1, low), 2),
            "close": round(price, 2),
            "volume": random.randint(100000, 5000000),
            "source": "demo"
        })

    return candles

def yfinance_history(symbol: str, period: str = "1y"):
    try:
        import yfinance as yf
        ticker = normalize_symbol(symbol) + ".IS"
        df = yf.Ticker(ticker).history(period=period, interval="1d", auto_adjust=False)
        if df is None or df.empty:
            return []

        candles = []
        for index, row in df.iterrows():
            close = row.get("Close")
            if close is None:
                continue
            candles.append({
                "date": index.strftime("%Y-%m-%d"),
                "open": round(float(row.get("Open", close)), 2),
                "high": round(float(row.get("High", close)), 2),
                "low": round(float(row.get("Low", close)), 2),
                "close": round(float(close), 2),
                "volume": int(row.get("Volume", 0) or 0),
                "source": "yfinance"
            })
        return candles
    except Exception:
        return []

def get_history(symbol: str, days: int = 220):
    symbol = normalize_symbol(symbol)
    if USE_REAL_DATA:
        real = yfinance_history(symbol)
        if len(real) >= 60:
            return real[-days:]
    return demo_history(symbol, days)
