# BMCI AIPro
## BIST Master Cycle Intelligence

BMCI AIPro, BIST hisseleri için yapay zekâ destekli teknik analiz, döngü analizi, scanner ve portföy altyapısı sunan profesyonel analiz platformudur.

## Özellikler
- BIST hisse analiz API
- BMCI Score Engine (0-100)
- RSI, EMA, MACD, OBV hesaplama
- Döngü analizi
- ATH analizi
- Risk analizi
- AI yorum motoru
- Scanner altyapısı
- Next.js dashboard başlangıcı
- FastAPI backend

## Klasör Yapısı

```text
BMCI-AIPro/
├── backend/
├── frontend/
├── ai/
├── scanner/
├── database/
├── docs/
├── render.yaml
├── README.md
└── .gitignore
```

## Backend Çalıştırma

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Test:
```text
http://127.0.0.1:8000/api/analyze/THYAO
http://127.0.0.1:8000/api/scanner
```

## Frontend Çalıştırma

```bash
cd frontend
npm install
npm run dev
```

## Not
Bu sürüm gerçek veri bağlantısı için hazırlanmış modüler altyapıdır. Şu an demo candle üretir; sonraki aşamada gerçek BIST veri sağlayıcısı bağlanır.
