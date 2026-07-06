async function getData(symbol: string) {
  const res = await fetch(`http://localhost:8000/api/bist/${symbol}`, {
    cache: "no-store"
  });

  return res.json();
}

export default async function Page() {
  const data = await getData("THYAO");

  return (
    <main style={{ padding: 20, background: "#0a0a0a", color: "white" }}>
      <h1>BMCI BIST Engine</h1>

      <h2>{data.symbol}</h2>

      <p>Price: {data.price}</p>
      <p>BMCI Score: {data.bmci_score}</p>
      <p>Signal: {data.signal}</p>

      <pre>{JSON.stringify(data.indicators, null, 2)}</pre>
    </main>
  );
}
