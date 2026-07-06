from fastapi import FastAPI

app = FastAPI(title="BMCI AIPro")

@app.get("/")
def root():
    return {"status": "ok", "system": "BMCI AIPro"}

@app.get("/api/analyze/{symbol}")
def analyze(symbol: str):

    score = 78

    return {
        "symbol": symbol,
        "bmci_score": score,
        "signal": "BUY" if score > 70 else "NEUTRAL",
        "indicators": {
            "rsi": 52,
            "macd": "positive",
            "obv": "strong"
        },
        "risk": "medium",
        "ai_comment": f"{symbol} güçlü yapı gösteriyor, trend yukarı yönlü."
    }
