from fastapi import FastAPI
from data_provider import get_bist_price, get_volume, get_history

app = FastAPI()

@app.get("/api/bist/{symbol}")
def bist(symbol: str):

    # ✅ DATA LAYER (V2)
    price = get_bist_price(symbol)
    volume = get_volume()
    history = get_history(symbol)

    # örnek response (şimdilik)
    return {
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "candles": history
    }
