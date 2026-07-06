def generate_ai_comment(symbol: str, score: int):
    if score > 80:
        return f"{symbol} güçlü yükseliş trendinde."
    elif score > 60:
        return f"{symbol} birikim bölgesinde."
    else:
        return f"{symbol} zayıf yapı, dikkat edilmeli."
