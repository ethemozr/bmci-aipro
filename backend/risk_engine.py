def calculate_risk(prices, rsi, cycle):
    if len(prices) < 20:
        return {"risk_score": 50, "risk_level": "medium"}
    last = prices[-1]
    high_20 = max(prices[-20:])
    low_20 = min(prices[-20:])
    drawdown = ((high_20 - last) / high_20) * 100 if high_20 else 0
    volatility = ((high_20 - low_20) / low_20) * 100 if low_20 else 0

    risk = 30
    if rsi > 75: risk += 20
    if cycle.get("phase") == "late_cycle": risk += 20
    if volatility > 25: risk += 15
    if drawdown > 15: risk += 10
    risk = min(100, round(risk))
    level = "low" if risk < 40 else "medium" if risk < 70 else "high"
    return {"risk_score": risk, "risk_level": level, "drawdown_from_20_high": round(drawdown, 2), "volatility_20": round(volatility, 2)}
