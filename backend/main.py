from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import APP_NAME, APP_VERSION, DEFAULT_WATCHLIST
from .data_provider import get_history
from .indicators import calculate_rsi, calculate_macd, calculate_obv, calculate_ema, fibonacci_levels, support_resistance
from .cycle_engine import analyze_cycle
from .bmci_score import calculate_bmci_score
from .risk_engine import calculate_risk
from .ai_commentary import generate_ai_comment
from .database import init_db, save_analysis, get_last_analyses, get_portfolio, add_portfolio_item, get_alarms, add_alarm
from .schemas import PortfolioCreate, AlarmCreate

app = FastAPI(title="bmci-aipro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"status": "ok", "project": APP_NAME, "version": APP_VERSION}

@app.get("/api/symbols")
def symbols():
    return DEFAULT_WATCHLIST

@app.get("/api/analyze/{symbol}")
def analyze(symbol: str):
    symbol = symbol.upper()
    candles = get_history(symbol)
    prices = [c["close"] for c in candles]
    volumes = [c["volume"] for c in candles]
    source = candles[-1].get("source", "unknown") if candles else "unknown"

    price = prices[-1]
    high = max(prices)
    low = min(prices)
    ath = high
    ath_distance_percent = round(((ath - price) / ath) * 100, 2) if ath else 0

    rsi = calculate_rsi(prices)
    macd_value, macd_signal = calculate_macd(prices)
    obv = calculate_obv(prices, volumes)
    ema20 = calculate_ema(prices, 20)
    ema50 = calculate_ema(prices, 50)
    fib = fibonacci_levels(high, low)
    sr = support_resistance(prices)
    cycle = analyze_cycle(prices)
    risk = calculate_risk(prices, rsi, cycle)

    volume_avg = sum(volumes[-20:]) / 20 if len(volumes) >= 20 else max(sum(volumes) / len(volumes), 1)
    volume_strength = round(min(100, (volumes[-1] / volume_avg) * 50)) if volume_avg else 50

    score = calculate_bmci_score(rsi, macd_signal, obv, price, ema20, ema50, cycle, ath_distance_percent, volume_strength, risk["risk_score"])
    signal = "BUY" if score >= 75 else "WATCH" if score >= 50 else "SELL"
    ai_comment = generate_ai_comment(symbol, score, rsi, macd_signal, cycle, risk, source)

    payload = {
        "symbol": symbol,
        "price": price,
        "source": source,
        "signal": signal,
        "bmci_score": score,
        "indicators": {"rsi": rsi, "macd": macd_value, "macd_signal": macd_signal, "obv": obv, "ema20": ema20, "ema50": ema50},
        "fibonacci": fib,
        "support_resistance": sr,
        "ath": {"ath": ath, "distance_percent": ath_distance_percent},
        "cycle": cycle,
        "risk": risk,
        "volume_strength": volume_strength,
        "ai_comment": ai_comment,
        "candles": candles[-120:],
        "disclaimer": "Yatırım tavsiyesi değildir."
    }

    save_analysis(payload)
    return payload

@app.get("/api/scanner")
def scanner():
    results = []
    for symbol in DEFAULT_WATCHLIST:
        analysis = analyze(symbol)
        tags = []
        if analysis["bmci_score"] >= 90:
            tags.append("BMCI > 90")
        tags.append("MACD AL" if analysis["indicators"]["macd_signal"] == "positive" else "MACD SAT")
        if analysis["indicators"]["obv"] > 0:
            tags.append("Para Girişi")
        if analysis["cycle"]["phase"] == "early_accumulation":
            tags.append("Yeni Döngü")
        if analysis["ath"]["distance_percent"] < 5:
            tags.append("ATH Yakını")
        if analysis["volume_strength"] > 70:
            tags.append("Hacim Patlaması")
        results.append({
            "symbol": symbol,
            "score": analysis["bmci_score"],
            "signal": analysis["signal"],
            "price": analysis["price"],
            "source": analysis["source"],
            "tags": tags,
            "cycle_phase": analysis["cycle"]["phase"],
            "days_left": analysis["cycle"]["estimated_days_left"]
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)

@app.get("/api/last-analyses")
def last_analyses():
    return get_last_analyses()

@app.get("/api/portfolio")
def portfolio():
    return get_portfolio()

@app.post("/api/portfolio")
def create_portfolio_item(item: PortfolioCreate):
    add_portfolio_item(item.symbol, item.lot, item.cost)
    return {"status": "ok", "message": "portfolio item added"}

@app.get("/api/alarms")
def alarms():
    return get_alarms()

@app.post("/api/alarms")
def create_alarm(item: AlarmCreate):
    add_alarm(item.symbol, item.condition_text)
    return {"status": "ok", "message": "alarm added"}
