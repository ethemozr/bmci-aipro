from fastapi import FastAPI
from data_provider import get_bist_price, get_volume, get_history
from indicators import calculate_rsi, calculate_macd, calculate_obv, calculate_ema

app = FastAPI(title='BMCI AIPro')

@app.get('/api/bist/{symbol}')
def bist(symbol: str):

    history = get_history(symbol)
    prices = [c['close'] for c in history]
    volumes = [get_volume() for _ in history]

    rsi = calculate_rsi(prices)
    macd, macd_signal = calculate_macd(prices)
    obv = calculate_obv(prices, volumes)
    ema = calculate_ema(prices)

    score = 0
    score += 25 if 40 < rsi < 60 else 10
    score += 25 if macd_signal == 'positive' else 10
    score += 25 if prices[-1] > ema else 10
    score = min(score, 100)

    signal = 'BUY' if score > 70 else 'NEUTRAL' if score > 50 else 'SELL'

    return {
        'symbol': symbol,
        'bmci_score': score,
        'signal': signal,
        'rsi': rsi,
        'macd': macd_signal,
        'ema': ema,
        'obv': obv
    }
