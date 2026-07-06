import random
import math
from datetime import datetime, timedelta

BIST_SYMBOLS = [
    "THYAO", "ASELS", "BIMAS", "KONYA", "KCHOL",
    "SISE", "EREGL", "TUPRS", "GARAN", "AKBNK",
    "YKBNK", "ISCTR", "FROTO", "TOASO", "SASA"
]

def get_history(symbol: str, days: int = 180):
    # Demo veri üretir. Gerçek veri sağlayıcı daha sonra buraya bağlanacak.
    random.seed(symbol.upper())
    base = random.uniform(20, 500)
    trend = random.uniform(-0.35, 0.65)

    candles = []
    price = base
    start = datetime.now() - timedelta(days=days)

    for i in range(days):
        cycle_wave = 12 * math.sin(i / 11)
        noise = random.uniform(-3, 3)
        price = max(1, price + trend + cycle_wave * 0.04 + noise * 0.35)

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
