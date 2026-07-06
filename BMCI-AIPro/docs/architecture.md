# BMCI AIPro Architecture

## Flow
User -> Next.js Dashboard -> FastAPI -> Data Provider -> Indicator Engine -> Cycle Engine -> BMCI Score -> AI Commentary

## Modules
- data_provider.py: veri katmanı
- indicators.py: RSI, MACD, EMA, OBV, Fibonacci
- cycle_engine.py: dip/tepe ve döngü analizi
- bmci_score.py: 100 puanlık BMCI hesaplama
- risk_engine.py: risk analizi
- ai_commentary.py: yapay zekâ yorumu
- scanner endpoint: otomatik tarama

## Next Phase
Gerçek BIST veri sağlayıcı entegrasyonu.
