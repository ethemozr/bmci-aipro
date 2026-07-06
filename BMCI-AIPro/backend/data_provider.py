import random
from datetime import datetime, timedelta

def get_bist_price(symbol: str) -> float:
    candles = get_history(symbol)
    return round(candles[-1]["close"], 2)

def get_volume() -> int:
    return random.randint(100_000, 5_000_000)

def get_history(symbol: str, days: int = 160):
    """
    V4 demo data provider.
    Sonraki aşamada buraya gerçek BIST veri sağlayıcısı bağlanacak.
    """
    random.seed(symbol.upper())
    base = random.uniform(20, 500)
    trend = random.uniform(-0.4, 0.7)

    candles = []
    price = base
    start = datetime.now() - timedelta(days=days)

    for i in range(days):
        cycle = 8 * random.uniform(-1, 1) + 12 * __import__("math").sin(i / 11)
        noise = random.uniform(-3, 3)
        price = max(1, price + trend + cycle * 0.04 + noise * 0.35)

        open_price = price + random.uniform(-2, 2)
        close = price
        high = max(open_price, close) + random.uniform(0, 4)
        low = min(open_price, close) - random.uniform(0, 4)
        volume = random.randint(100_000, 5_000_000)

        candles.append({
            "date": (start + timedelta(days=i)).strftime("%Y-%m-%d"),
            "open": round(open_price, 2),
            "high": round(high, 2),
            "low": round(max(0.1, low), 2),
            "close": round(close, 2),
            "volume": volume
        })

    return candles
