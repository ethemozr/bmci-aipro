import random

def get_bist_price(symbol: str):
    return round(random.uniform(50, 500), 2)

def get_volume():
    return random.randint(10000, 500000)

def get_history(symbol: str):
    return [{'close': random.uniform(50, 500)} for _ in range(30)]
