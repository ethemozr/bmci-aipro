import random

def get_bist_price(symbol: str):
    # V1: mock data (sonra gerçek API bağlanacak)
    return round(random.uniform(50, 500), 2)

def get_volume():
    return random.randint(10000, 500000)

def get_history(symbol: str):
    # fake candle data (şimdilik)
    return [
        {"close": random.uniform(50, 500)} for _ in range(20)
    ]
