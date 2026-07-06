"use client";

import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

type AnalysisData = {
  symbol: string;
  price: number;
  source: string;
  signal: string;
  bmci_score: number;
  indicators: {
    rsi: number;
    macd: number;
    macd_signal: string;
    obv: number;
    ema20: number;
    ema50: number;
  };
  fibonacci: Record<string, number>;
  support_resistance: {
    support: number;
    resistance: number;
  };
  ath: {
    ath: number;
    distance_percent: number;
  };
  cycle: {
    phase: string;
    cycle_length: number;
    cycle_completion: number;
    estimated_days_left: number;
    comment: string;
  };
  risk: {
    risk_score: number;
    risk_level: string;
  };
  volume_strength: number;
  ai_comment: string;
};

export default function Page() {
  const [query, setQuery] = useState("THYAO");
  const [data, setData] = useState<AnalysisData | null>(null);
  const [scanner, setScanner] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadData(symbol: string) {
    try {
      setLoading(true);
      setError("");

      const clean = symbol.trim().toUpperCase();

      const analysisRes = await fetch(`${API_URL}/api/analyze/${clean}`);
      if (!analysisRes.ok) {
        throw new Error("Backend analiz cevabı alınamadı.");
      }

      const analysis = await analysisRes.json();

      let scannerData: any[] = [];
      try {
        const scannerRes = await fetch(`${API_URL}/api/scanner`);
        scannerData = await scannerRes.json();
      } catch {
        scannerData = [];
      }

      setData(analysis);
      setScanner(Array.isArray(scannerData) ? scannerData : []);
    } catch (err) {
      setError(
        "Backend bağlantısı yok. Önce run_backend.bat çalıştır veya şu komutu aç: py -3.12 -m uvicorn backend.main:app --reload"
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData("THYAO");
  }, []);

  function submitSearch(e: React.FormEvent) {
    e.preventDefault();
    loadData(query);
  }

  return (
    <main className="page">
      <header className="topbar">
        <div>
          <div className="brandMark">BMCI</div>
          <h1>BMCI AIPro</h1>
          <p>BIST Master Cycle Intelligence</p>
        </div>

        <form className="searchPanel" onSubmit={submitSearch}>
          <label>Hisse Ara</label>
          <div className="searchLine">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="THYAO, KONYA, ASELS..."
            />
            <button type="submit">{loading ? "Analiz..." : "Analiz Et"}</button>
          </div>
        </form>
      </header>

      {error && (
        <section className="errorBox">
          <strong>Bağlantı Hatası</strong>
          <p>{error}</p>
        </section>
      )}

      {!data && !error && (
        <section className="loadingBox">BMCI AIPro yükleniyor...</section>
      )}

      {data && (
        <>
          <nav className="tabs">
            <span className="active">Genel Bakış</span>
            <span>Teknik Analiz</span>
            <span>Döngü</span>
            <span>Scanner</span>
            <span>Portföy</span>
            <span>Alarm</span>
          </nav>

          <section className="summaryGrid">
            <div className="scoreCard">
              <span className="miniTitle">Seçili Hisse</span>
              <h2>{data.symbol}</h2>
              <div className="gauge">
                <div className="gaugeInner">
                  <span>{data.bmci_score}</span>
                  <small>BMCI</small>
                </div>
              </div>
              <span className={`signal ${data.signal?.toLowerCase()}`}>
                {translateSignal(data.signal)}
              </span>
              <p className="muted">Son fiyat: {data.price}</p>
            </div>

            <InfoCard title="Teknik Göstergeler">
              <Row label="RSI" value={data.indicators.rsi} />
              <Row label="MACD" value={data.indicators.macd_signal === "positive" ? "Pozitif" : "Negatif"} />
              <Row label="EMA 20" value={data.indicators.ema20} />
              <Row label="EMA 50" value={data.indicators.ema50} />
              <Row label="OBV" value={formatNumber(data.indicators.obv)} />
            </InfoCard>

            <InfoCard title="Döngü Analizi">
              <Row label="Faz" value={translatePhase(data.cycle.phase)} />
              <Row label="Tamamlanma" value={`%${data.cycle.cycle_completion}`} />
              <Row label="Tahmini Kalan" value={`${data.cycle.estimated_days_left} gün`} />
              <Row label="Ortalama Döngü" value={`${data.cycle.cycle_length} gün`} />
              <p className="note">{data.cycle.comment}</p>
            </InfoCard>

            <InfoCard title="Risk ve ATH">
              <Row label="Risk Seviyesi" value={translateRisk(data.risk.risk_level)} />
              <Row label="Risk Skoru" value={data.risk.risk_score} />
              <Row label="ATH Uzaklık" value={`%${data.ath.distance_percent}`} />
              <Row label="Veri Kaynağı" value={data.source} />
            </InfoCard>
          </section>

          <section className="analysisGrid">
            <div className="panel aiPanel">
              <div className="panelHeader">
                <h3>Yapay Zekâ Yorumu</h3>
                <span>Model Yorumu</span>
              </div>
              <p>{turkishComment(data.ai_comment)}</p>
            </div>

            <div className="panel">
              <h3>Destek / Direnç</h3>
              <Row label="Destek" value={data.support_resistance?.support ?? "-"} />
              <Row label="Direnç" value={data.support_resistance?.resistance ?? "-"} />
              <Row label="ATH" value={data.ath.ath} />
            </div>

            <div className="panel">
              <h3>Fibonacci</h3>
              {Object.entries(data.fibonacci || {}).map(([key, value]) => (
                <Row key={key} label={key} value={value} />
              ))}
            </div>
          </section>

          <section className="panel scannerPanel">
            <div className="panelHeader">
              <h3>Akıllı Scanner</h3>
              <span>BMCI sıralı izleme listesi</span>
            </div>

            <div className="scannerTable">
              <div className="scannerHead">
                <span>Hisse</span>
                <span>BMCI</span>
                <span>Sinyal</span>
                <span>Fiyat</span>
                <span>Etiketler</span>
              </div>

              {scanner.map((item) => (
                <div className="scannerRow" key={item.symbol}>
                  <strong>{item.symbol}</strong>
                  <span>{item.score}</span>
                  <span>{translateSignal(item.signal)}</span>
                  <span>{item.price}</span>
                  <small>{item.tags?.join(", ") || "-"}</small>
                </div>
              ))}
            </div>
          </section>
        </>
      )}
    </main>
  );
}

function InfoCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      {children}
    </div>
  );
}

function Row({ label, value }: { label: string; value: any }) {
  return (
    <div className="row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function translateSignal(signal: string) {
  if (signal === "BUY") return "AL";
  if (signal === "SELL") return "SAT";
  if (signal === "WATCH") return "İZLE";
  return signal;
}

function translateRisk(risk: string) {
  if (risk === "low") return "Düşük";
  if (risk === "medium") return "Orta";
  if (risk === "high") return "Yüksek";
  return risk;
}

function translatePhase(phase: string) {
  const map: Record<string, string> = {
    early_accumulation: "Erken Birikim",
    trend_expansion: "Trend Genişleme",
    late_cycle: "Döngü Sonu",
    weak_cycle: "Zayıf Döngü",
    unknown: "Bilinmiyor",
  };
  return map[phase] || phase;
}

function formatNumber(value: number) {
  return new Intl.NumberFormat("tr-TR").format(value);
}

function turkishComment(text: string) {
  return text
    ?.replaceAll("positive", "pozitif")
    .replaceAll("negative", "negatif")
    .replaceAll("late_cycle", "döngü sonu")
    .replaceAll("trend_expansion", "trend genişleme")
    .replaceAll("early_accumulation", "erken birikim")
    .replaceAll("weak_cycle", "zayıf döngü")
    .replaceAll("medium", "orta")
    .replaceAll("low", "düşük")
    .replaceAll("high", "yüksek");
}
