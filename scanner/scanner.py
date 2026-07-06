def scan_signal(score: int):
    if score >= 90:
        return "STRONG_BUY"
    if score >= 75:
        return "BUY"
    if score >= 50:
        return "WATCH"
    return "SELL"
