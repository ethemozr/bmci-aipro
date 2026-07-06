def scan_signal(score):
    if score >= 90:
        return "STRONG BUY"
    if score >= 75:
        return "BUY"
    if score >= 50:
        return "WATCH"
    return "SELL"
