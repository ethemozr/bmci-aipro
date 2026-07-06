export default async function Page(){
  const res = await fetch('http://localhost:8000/api/bist/THYAO',{cache:'no-store'})
  const data = await res.json()

  return (
    <main style={{padding:20,background:'#000',color:'#fff'}}>
      <h1>BMCI AIPro</h1>
      <p>{data.symbol}</p>
      <p>Score: {data.bmci_score}</p>
      <p>Signal: {data.signal}</p>
    </main>
  )
}
