# BMCI AIPro v5
BIST Master Cycle Intelligence

Bu paket SQLite veritabanı, portföy ve alarm altyapısı eklenmiş V5 sürümüdür.

## Backend çalıştırma
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

## Test
http://127.0.0.1:8000/
http://127.0.0.1:8000/api/analyze/THYAO
http://127.0.0.1:8000/api/scanner
http://127.0.0.1:8000/api/last-analyses
http://127.0.0.1:8000/api/portfolio
http://127.0.0.1:8000/api/alarms
