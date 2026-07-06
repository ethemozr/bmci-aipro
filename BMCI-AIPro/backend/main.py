from fastapi import FastAPI
from .data_provider import get_history
from .indicators import calculate_rsi, calculate_macd, calculate_obv, calculate_ema, fibonacci_levels
from .cycle_engine import analyze_cycle
from .bmci_score import calculate_bmci_score
from .risk_engine import calculate_risk
from .ai_commentary import generate_ai_comment

app = FastAPI(title="BMCI AIPro - BIST Master Cycle Intelligence")

WATCHLIST = ["THYAO", "ASELS", "BIMAS", "KONYA", "KCHOL", "SISE", "EREGL", "TUPRS", "GARAN", "AKBNK"]

@app.get("/")
def root():
    return {
        "status": "ok",
        "project": "BMCI AIPro",
        "version": "v4-cycle-engine"
    }

@app.get("/api/analyze/{symbol}")
def analyze(symbol: str):
    symbol = symbol.upper()
    candles = get_history(symbol)
    prices = [c["close"] for c in candles]
    volumes = [c["volume"] for c in candles]

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
    cycle = analyze_cycle(prices)
    risk = calculate_risk(prices, rsi, cycle)

    volume_avg = sum(volumes[-20:]) / 20
    volume_strength = round(min(100, (volumes[-1] / volume_avg) * 50)) if volume_avg else 50

    score = calculate_bmci_score(
        rsi=rsi,
        macd_signal=macd_signal,
        obv=obv,
        price=price,
        ema20=ema20,
        ema50=ema50,
        cycle=cycle,
        ath_distance_percent=ath_distance_percent,
        volume_strength=volume_strength,
        risk_score=risk["risk_score"]
    )

    if score >= 75:
        signal = "BUY"
    elif score >= 50:
        signal = "WATCH"
    else:
        signal = "SELL"

    ai_comment = generate_ai_comment(symbol, score, rsi, macd_signal, cycle, risk)

    return {
        "symbol": symbol,
        "price": price,
        "signal": signal,
        "bmci_score": score,
        "indicators": {
            "rsi": rsi,
            "macd": macd_value,
            "macd_signal": macd_signal,
            "obv": obv,
            "ema20": ema20,
            "ema50": ema50
        },
        "fibonacci": fib,
        "ath": {
            "ath": ath,
            "distance_percent": ath_distance_percent
        },
        "cycle": cycle,
        "risk": risk,
        "volume_strength": volume_strength,
        "ai_comment": ai_comment,
        "disclaimer": "Yatırım tavsiyesi değildir."
    }

@app.get("/api/scanner")
def scanner():
    results = []

    for symbol in WATCHLIST:
        analysis = analyze(symbol)
        tags = []

        if analysis["bmci_score"] >= 90:
            tags.append("BMCI > 90")
        if analysis["indicators"]["macd_signal"] == "positive":
            tags.append("MACD AL")
        else:
            tags.append("MACD SAT")
        if analysis["indicators"]["obv"] > 0:
            tags.append("Para Girişi")
        if analysis["cycle"]["phase"] == "early_accumulation":
            tags.append("Yeni Döngü")
        if analysis["ath"]["distance_percent"] < 5:
            tags.append("Yeni ATH Yakını")
        if analysis["volume_strength"] > 70:
            tags.append("Hacim Patlaması")

        results.append({
            "symbol": symbol,
            "score": analysis["bmci_score"],
            "signal": analysis["signal"],
            "tags": tags,
            "cycle_phase": analysis["cycle"]["phase"],
            "days_left": analysis["cycle"]["estimated_days_left"]
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
