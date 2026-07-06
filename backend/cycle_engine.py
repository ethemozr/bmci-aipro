def find_local_extremes(prices, window=3):
    peaks, troughs = [], []
    for i in range(window, len(prices) - window):
        current = prices[i]
        left = prices[i-window:i]
        right = prices[i+1:i+1+window]
        if current >= max(left) and current >= max(right):
            peaks.append(i)
        if current <= min(left) and current <= min(right):
            troughs.append(i)
    return peaks, troughs

def analyze_cycle(prices):
    if len(prices) < 30:
        return {"phase": "unknown", "cycle_length": None, "cycle_completion": 0, "estimated_days_left": None, "comment": "Yeterli veri yok."}

    peaks, troughs = find_local_extremes(prices)
    if len(troughs) >= 2:
        lengths = [troughs[i] - troughs[i-1] for i in range(1, len(troughs))]
        avg_cycle = round(sum(lengths) / len(lengths), 1)
        last_trough = troughs[-1]
    else:
        avg_cycle = 34
        last_trough = max(0, len(prices) - avg_cycle)

    bars_since = len(prices) - 1 - last_trough
    completion = min(100, round((bars_since / avg_cycle) * 100, 1))
    days_left = max(0, round(avg_cycle - bars_since))
    last_price = prices[-1]
    prev_price = prices[-8] if len(prices) >= 8 else prices[0]

    if completion < 35 and last_price >= prev_price:
        phase = "early_accumulation"
        comment = "Döngü yeni başlamış olabilir."
    elif 35 <= completion < 75 and last_price >= prev_price:
        phase = "trend_expansion"
        comment = "Döngü orta bölgede."
    elif completion >= 75:
        phase = "late_cycle"
        comment = "Döngü son bölgeye yaklaşmış olabilir."
    else:
        phase = "weak_cycle"
        comment = "Döngü zayıf ilerliyor."

    return {
        "phase": phase,
        "cycle_length": avg_cycle,
        "cycle_completion": completion,
        "estimated_days_left": days_left,
        "last_trough_index": last_trough,
        "peak_count": len(peaks),
        "trough_count": len(troughs),
        "comment": comment
    }
