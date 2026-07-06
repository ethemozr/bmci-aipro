def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50.0

    gains = 0.0
    losses = 0.0

    for i in range(-period, 0):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains += change
        else:
            losses += abs(change)

    if losses == 0:
        return 100.0

    rs = gains / losses
    return round(100 - (100 / (1 + rs)), 2)

def calculate_ema(prices, period=14):
    if not prices:
        return 0.0

    if len(prices) < period:
        return round(sum(prices) / len(prices), 2)

    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period

    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema

    return round(ema, 2)

def calculate_macd(prices):
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)
    macd_line = round(ema12 - ema26, 2)
    signal = "positive" if macd_line > 0 else "negative"
    return macd_line, signal

def calculate_obv(prices, volumes):
    obv = 0
    for i in range(1, min(len(prices), len(volumes))):
        if prices[i] > prices[i - 1]:
            obv += volumes[i]
        elif prices[i] < prices[i - 1]:
            obv -= volumes[i]
    return obv

def fibonacci_levels(high, low):
    diff = high - low
    return {
        "0.236": round(high - diff * 0.236, 2),
        "0.382": round(high - diff * 0.382, 2),
        "0.500": round(high - diff * 0.500, 2),
        "0.618": round(high - diff * 0.618, 2),
        "0.786": round(high - diff * 0.786, 2),
    }
