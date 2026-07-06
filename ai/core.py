def explain_score(score: int):
    if score >= 90:
        return "Çok güçlü BMCI bölgesi"
    if score >= 75:
        return "Güçlü izleme bölgesi"
    if score >= 50:
        return "Nötr izleme bölgesi"
    return "Zayıf bölge"
