from fastapi import FastAPI

app = FastAPI(title="BMCI AIPro - BIST")

@app.get("/")
def home():
    return {"status": "ok", "market": "BIST AI System"}

@app.get("/api/signal/{symbol}")
def signal(symbol: str):

    # basit demo logic (sonra gerçek analiz ekleyeceğiz)
    return {
        "symbol": symbol,
        "signal": "BUY",
        "strategy": "EMA + RSI + Supertrend",
        "confidence": 0.72
    }