def calculate_rsi(prices, period=14):
    if len(prices) < period+1:
        return 50
    gains = losses = 0
    for i in range(-period, -1):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            gains += diff
        else:
            losses += abs(diff)
    if losses == 0:
        return 100
    rs = gains / losses
    return round(100 - (100 / (1 + rs)), 2)

def calculate_ema(prices, period=14):
    ema = sum(prices[:period]) / period
    k = 2/(period+1)
    for p in prices[period:]:
        ema = p*k + ema*(1-k)
    return round(ema, 2)

def calculate_macd(prices):
    ema12 = sum(prices[-12:]) / 12
    ema26 = sum(prices[-26:]) / 26 if len(prices) >= 26 else ema12
    macd = ema12 - ema26
    return round(macd, 2), 'positive' if macd > 0 else 'negative'

def calculate_obv(prices, volumes):
    obv = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            obv += volumes[i]
        else:
            obv -= volumes[i]
    return obv
