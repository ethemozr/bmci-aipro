async function getAnalysis(symbol: string) {
  const res = await fetch(`http://localhost:8000/api/analyze/${symbol}`, {
    cache: "no-store",
  });
  return res.json();
}

async function getScanner() {
  const res = await fetch("http://localhost:8000/api/scanner", {
    cache: "no-store",
  });
  return res.json();
}

export default async function Page() {
  const data = await getAnalysis("THYAO");
  const scanner = await getScanner();

  return (
    <main style={{ padding: 24, maxWidth: 1180, margin: "0 auto" }}>
      <section style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 38, marginBottom: 6 }}>BMCI AIPro</h1>
        <p style={{ color: "#aaa" }}>BIST Master Cycle Intelligence</p>
      </section>

      <section className="grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))" }}>
        <div className="card">
          <h2>{data.symbol}</h2>
          <p style={{ fontSize: 42, margin: 0 }}>{data.bmci_score}</p>
          <span className="badge">{data.signal}</span>
        </div>

        <div className="card">
          <h3>İndikatörler</h3>
          <p>RSI: {data.indicators.rsi}</p>
          <p>MACD: {data.indicators.macd_signal}</p>
          <p>EMA20: {data.indicators.ema20}</p>
          <p>EMA50: {data.indicators.ema50}</p>
        </div>

        <div className="card">
          <h3>Döngü</h3>
          <p>Faz: {data.cycle.phase}</p>
          <p>Tamamlanma: %{data.cycle.cycle_completion}</p>
          <p>Kalan: {data.cycle.estimated_days_left} gün</p>
        </div>

        <div className="card">
          <h3>Risk</h3>
          <p>Seviye: {data.risk.risk_level}</p>
          <p>Skor: {data.risk.risk_score}</p>
          <p>ATH Uzaklık: %{data.ath.distance_percent}</p>
        </div>
      </section>

      <section className="card" style={{ marginTop: 18 }}>
        <h3>AI Yorumu</h3>
        <p>{data.ai_comment}</p>
      </section>

      <section className="card" style={{ marginTop: 18 }}>
        <h3>Scanner</h3>
        <div className="grid">
          {scanner.map((item: any) => (
            <div key={item.symbol} style={{ borderBottom: "1px solid #222", padding: "10px 0" }}>
              <strong>{item.symbol}</strong> — BMCI: {item.score} — {item.signal}
              <br />
              <small>{item.tags.join(", ")}</small>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
