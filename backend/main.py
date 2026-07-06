from fastapi import FastAPI

app = FastAPI(title="BMCI AIPro")

@app.get("/")
def home():
    return {"status": "ok", "project": "BMCI AIPro"}

@app.get("/api/signal")
def signal():
    return {
        "asset": "BTC",
        "signal": "NEUTRAL",
        "confidence": 0.55
    }