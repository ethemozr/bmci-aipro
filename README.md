# BMCI AIPro
## BIST Master Cycle Intelligence

BMCI AIPro; BIST hisseleri için yapay zekâ destekli analiz, döngü analizi, BMCI skoru, scanner, portföy ve alarm altyapısı sunan profesyonel analiz platformudur.

## İçerik
- FastAPI backend
- Next.js frontend
- SQLite database
- BMCI Score Engine
- RSI, MACD, EMA, OBV
- Fibonacci
- ATH analizi
- Döngü analizi
- Risk motoru
- AI yorum motoru
- Scanner
- Portföy
- Alarm

## Backend Çalıştırma

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Test:
```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/api/analyze/THYAO
http://127.0.0.1:8000/api/scanner
```

## Frontend Çalıştırma

```bash
cd frontend
npm install
npm run dev
```

Frontend:
```text
http://localhost:3000
```

## Uyarı
Bu proje yatırım tavsiyesi değildir. Teknik analiz ve model çıktısı üretir.
