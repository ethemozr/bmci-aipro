def scan(score):
    if score > 90:
        return 'STRONG BUY'
    if score > 70:
        return 'BUY'
    if score > 50:
        return 'NEUTRAL'
    return 'SELL'
