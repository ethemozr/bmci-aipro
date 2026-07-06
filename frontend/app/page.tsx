export default async function Page() {
  const res = await fetch("http://localhost:8000/api/analyze/THYAO", {
    cache: "no-store"
  });

  const data = await res.json();

  return (
    <main style={{ padding: 20, background: "#0a0a0a", color: "white" }}>
      <h1>BMCI AIPro Dashboard</h1>

      <h2>{data.symbol}</h2>

      <p>BMCI Score: {data.bmci_score}</p>
      <p>Signal: {data.signal}</p>
      <p>Risk: {data.risk}</p>

      <p>AI: {data.ai_comment}</p>
    </main>
  );
}
