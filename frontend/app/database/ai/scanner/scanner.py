def scan(score: int):
    if score >= 90:
        return "STRONG BUY"
    elif score >= 70:
        return "BUY"
    elif score >= 50:
        return "NEUTRAL"
    else:
        return "SELL"
