from fastapi import FastAPI
import random

app = FastAPI(title="BMCI BIST Data Engine")

# --- MOCK DATA (şimdilik gerçek API bağlamıyoruz) ---
def get_price(symbol: str):
    return round(random.uniform(50, 500), 2)

def calculate_indicators(price: float):
    rsi = random.randint(30, 80)
    macd = random.choice(["positive", "negative"])
    obv = random.choice(["strong", "weak"])
    return rsi, macd, obv

def bmci_score(rsi, macd, obv):
    score = 0

    # RSI katkı
    if 40 <= rsi <= 60:
        score += 15
    elif rsi > 60:
        score += 10
    else:
        score += 5

    # MACD
    score += 10 if macd == "positive" else 5

    # OBV
    score += 10 if obv == "strong" else 5

    # trend fake (v1)
    score += random.randint(20, 50)

    return min(score, 100)

@app.get("/")
def root():
    return {"system": "BMCI BIST Engine v1"}

@app.get("/api/bist/{symbol}")
def bist(symbol: str):

    price = get_price(symbol)
    rsi, macd, obv = calculate_indicators(price)
    score = bmci_score(rsi, macd, obv)

    signal = "BUY" if score > 70 else "NEUTRAL" if score > 50 else "SELL"

    return {
        "symbol": symbol,
        "price": price,
        "bmci_score": score,
        "signal": signal,
        "indicators": {
            "rsi": rsi,
            "macd": macd,
            "obv": obv
        }
    }
