def generate_ai_comment(symbol, score, rsi, macd_signal, cycle, risk):
    signal_text = "AL bölgesine yakın" if score >= 70 else "BEKLE bölgesinde" if score >= 50 else "ZAYIF bölgede"
    return (
        f"{symbol.upper()} için BMCI skoru {score}. "
        f"Sistem {signal_text} görünüm veriyor. "
        f"RSI {rsi}, MACD {macd_signal}. "
        f"Döngü fazı: {cycle.get('phase')}, tamamlanma: %{cycle.get('cycle_completion')}. "
        f"Tahmini kalan süre: {cycle.get('estimated_days_left')} gün. "
        f"Risk seviyesi: {risk.get('risk_level')}. "
        f"Bu yorum yatırım tavsiyesi değildir."
    )
