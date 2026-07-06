export default async function Home() {
  const res = await fetch("http://localhost:8000/api/signal", {
    cache: "no-store"
  });

  const data = await res.json();

  return (
    <main style={{ padding: 20 }}>
      <h1>BMCI AIPro</h1>
      <p>Asset: {data.asset}</p>
      <p>Signal: {data.signal}</p>
      <p>Confidence: {data.confidence}</p>
    </main>
  );
}