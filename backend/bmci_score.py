def calculate_bmci_score(rsi, macd_signal, obv, price, ema20, ema50, cycle, ath_distance_percent, volume_strength=50, risk_score=50):
    score = 0

    # Trend 15
    if price > ema20 > ema50:
        score += 15
    elif price > ema20:
        score += 10
    else:
        score += 4

    # Cycle 15
    completion = cycle.get("cycle_completion", 0)
    phase = cycle.get("phase", "")
    if phase in ["early_accumulation", "trend_expansion"] and completion < 75:
        score += 15
    elif completion < 90:
        score += 9
    else:
        score += 4

    # ATH 10
    if ath_distance_percent < 10:
        score += 10
    elif ath_distance_percent < 25:
        score += 7
    else:
        score += 4

    # RSI 10
    if 45 <= rsi <= 65:
        score += 10
    elif 35 <= rsi < 45 or 65 < rsi <= 75:
        score += 7
    else:
        score += 3

    # MACD 10
    score += 10 if macd_signal == "positive" else 4

    # OBV 10
    score += 10 if obv > 0 else 4

    # Fibonacci 10
    score += 7

    # Hacim 10
    if volume_strength > 70:
        score += 10
    elif volume_strength > 45:
        score += 7
    else:
        score += 4

    # Temel Analiz 5
    score += 3

    # Risk 5
    if risk_score < 35:
        score += 5
    elif risk_score < 65:
        score += 3
    else:
        score += 1

    return min(100, round(score))
