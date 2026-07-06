def calculate_bmci_score(rsi, macd_signal, obv, price, ema20, ema50, cycle, ath_distance_percent, volume_strength=50, risk_score=50):
    score = 0
    score += 15 if price > ema20 > ema50 else 10 if price > ema20 else 4

    completion = cycle.get("cycle_completion", 0)
    phase = cycle.get("phase", "")
    score += 15 if phase in ["early_accumulation", "trend_expansion"] and completion < 75 else 9 if completion < 90 else 4

    score += 10 if ath_distance_percent < 10 else 7 if ath_distance_percent < 25 else 4
    score += 10 if 45 <= rsi <= 65 else 7 if 35 <= rsi <= 75 else 3
    score += 10 if macd_signal == "positive" else 4
    score += 10 if obv > 0 else 4
    score += 7
    score += 10 if volume_strength > 70 else 7 if volume_strength > 45 else 4
    score += 3
    score += 5 if risk_score < 35 else 3 if risk_score < 65 else 1
    return min(100, round(score))
