import math

# -------------------------
# RSI CALCULATION
# -------------------------
def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50

    gains = 0
    losses = 0

    for i in range(-period, -1):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains += change
        else:
            losses += abs(change)

    if losses == 0:
        return 100

    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))

    return round(rsi, 2)


# -------------------------
# EMA CALCULATION
# -------------------------
def calculate_ema(prices, period=14):
    if len(prices) < period:
        return prices[-1]

    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period

    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema

    return round(ema, 2)


# -------------------------
# MACD CALCULATION
# -------------------------
def calculate_macd(prices):
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)

    macd_line = ema12 - ema26

    signal = "positive" if macd_line > 0 else "negative"

    return round(macd_line, 2), signal


# -------------------------
# OBV (Volume trend)
# -------------------------
def calculate_obv(prices, volumes):
    obv = 0

    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            obv += volumes[i]
        elif prices[i] < prices[i - 1]:
            obv -= volumes[i]

    return obv
