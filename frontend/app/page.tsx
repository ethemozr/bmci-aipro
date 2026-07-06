"use client";

import { useEffect, useState } from "react";

export default function Page() {
  const [symbol, setSymbol] = useState("THYAO");
  const [query, setQuery] = useState("THYAO");
  const [data, setData] = useState<any>(null);
  const [scanner, setScanner] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function loadData(target: string) {
    setLoading(true);

    const analysisRes = await fetch(`http://127.0.0.1:8000/api/analyze/${target}`);
    const analysis = await analysisRes.json();

    const scannerRes = await fetch("http://127.0.0.1:8000/api/scanner");
    const scannerData = await scannerRes.json();

    setData(analysis);
    setScanner(scannerData);
    setLoading(false);
  }

  useEffect(() => {
    loadData(symbol);
  }, []);

  function searchStock() {
    const clean = query.trim().toUpperCase();
    if (!clean) return;
    setSymbol(clean);
    loadData(clean);
  }

  if (!data) {
    return <main className="page">Yükleniyor...</main>;
  }

  return (
    <main className="page">
      <header className="header">
        <div>
          <h1>BMCI AIPro</h1>
          <p>BIST Master Cycle Intelligence</p>
        </div>

        <div className="searchBox">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Hisse ara: THYAO, KONYA, ASELS..."
          />
          <button onClick={searchStock}>
            {loading ? "Analiz ediliyor..." : "Analiz Et"}
          </button>
        </div>
      </header>

      <section className="tabs">
        <span className="activeTab">Genel Analiz</span>
        <span>Teknik</span>
        <span>Döngü</span>
        <span>Scanner</span>
        <span>Portföy</span>
      </section>

      <section className="hero">
        <div className="scoreCard">
          <span className="label">Hisse</span>
          <h2>{data.symbol}</h2>
          <div className="score">{data.bmci_score}</div>
          <span className={`signal ${data.signal?.toLowerCase()}`}>
            {data.signal === "BUY" ? "AL" : data.signal === "SELL" ? "SAT" : "İZLE"}
          </span>
        </div>

        <div className="card">
          <h3>Teknik Göstergeler</h3>
          <div className="row"><span>RSI</span><strong>{data.indicators.rsi}</strong></div>
          <div className="row"><span>MACD</span><strong>{data.indicators.macd_signal === "positive" ? "Pozitif" : "Negatif"}</strong></div>
          <div className="row"><span>EMA 20</span><strong>{data.indicators.ema20}</strong></div>
          <div className="row"><span>EMA 50</span><strong>{data.indicators.ema50}</strong></div>
        </div>

        <div className="card">
          <h3>Döngü Analizi</h3>
          <div className="row"><span>Faz</span><strong>{translatePhase(data.cycle.phase)}</strong></div>
          <div className="row"><span>Tamamlanma</span><strong>%{data.cycle.cycle_completion}</strong></div>
          <div className="row"><span>Tahmini Kalan</span><strong>{data.cycle.estimated_days_left} gün</strong></div>
          <div className="row"><span>Ortalama Döngü</span><strong>{data.cycle.cycle_length} gün</strong></div>
        </div>

        <div className="card">
          <h3>Risk & ATH</h3>
          <div className="row"><span>Risk Seviyesi</span><strong>{translateRisk(data.risk.risk_level)}</strong></div>
          <div className="row"><span>Risk Skoru</span><strong>{data.risk.risk_score}</strong></div>
          <div className="row"><span>ATH Uzaklık</span><strong>%{data.ath.distance_percent}</strong></div>
          <div className="row"><span>Veri Kaynağı</span><strong>{data.source}</strong></div>
        </div>
      </section>

      <section className="contentGrid">
        <div className="panel wide">
          <h3>Yapay Zekâ Yorumu</h3>
          <p>{data.ai_comment}</p>
        </div>

        <div className="panel">
          <h3>Destek / Direnç</h3>
          <div className="row"><span>Destek</span><strong>{data.support_resistance?.support}</strong></div>
          <div className="row"><span>Direnç</span><strong>{data.support_resistance?.resistance}</strong></div>
        </div>

        <div className="panel">
          <h3>Fibonacci</h3>
          {Object.entries(data.fibonacci || {}).map(([key, value]: any) => (
            <div className="row" key={key}>
              <span>{key}</span>
              <strong>{value}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3>Akıllı Scanner</h3>
        <div className="scannerTable">
          {scanner.map((item) => (
            <div className="scannerRow" key={item.symbol}>
              <strong>{item.symbol}</strong>
              <span>BMCI: {item.score}</span>
              <span>{item.signal === "BUY" ? "AL" : item.signal === "SELL" ? "SAT" : "İZLE"}</span>
              <small>{item.tags.join(", ")}</small>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}

function translateRisk(risk: string) {
  if (risk === "low") return "Düşük";
  if (risk === "medium") return "Orta";
  if (risk === "high") return "Yüksek";
  return risk;
}

function translatePhase(phase: string) {
  const map: any = {
    early_accumulation: "Erken Birikim",
    trend_expansion: "Trend Genişleme",
    late_cycle: "Döngü Sonu",
    weak_cycle: "Zayıf Döngü",
    unknown: "Bilinmiyor",
  };

  return map[phase] || phase;
}
