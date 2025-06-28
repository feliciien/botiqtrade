"use client";
import { useState } from "react";

export default function Home() {
  const [symbol, setSymbol] = useState("BTCUSD");
  const [result, setResult] = useState("");
  const [rsi, setRsi] = useState("");
  const [advice, setAdvice] = useState("");
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState("What is your advice for the current market?");

  const apiBase = "http://127.0.0.1:5000";

  async function fetchPrice() {
    setLoading(true);
    setResult("");
    setRsi("");
    setAdvice("");
    try {
      const res = await fetch(`${apiBase}/price?symbol=${symbol}`);
      const data = await res.json();
      if (data.price) {
        setResult(`Current price for ${symbol}: ${data.price}`);
      } else {
        setResult(data.error || "Error fetching price.");
      }
    } catch (e) {
      setResult("Error connecting to backend.");
    }
    setLoading(false);
  }

  async function fetchRSI() {
    setLoading(true);
    setRsi("");
    setAdvice("");
    try {
      const res = await fetch(`${apiBase}/rsi?symbol=${symbol}`);
      const data = await res.json();
      if (data.rsi) {
        setRsi(`Current RSI for ${symbol}: ${data.rsi.toFixed(2)}`);
      } else {
        setRsi(data.error || "Error fetching RSI.");
      }
    } catch (e) {
      setRsi("Error connecting to backend.");
    }
    setLoading(false);
  }

  async function fetchAdvice() {
    setLoading(true);
    setAdvice("");
    try {
      const res = await fetch(`${apiBase}/advice`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol, question }),
      });
      const data = await res.json();
      if (data.advice) {
        setAdvice(data.advice);
      } else {
        setAdvice(data.error || "Error fetching advice.");
      }
    } catch (e) {
      setAdvice("Error connecting to backend.");
    }
    setLoading(false);
  }

  return (
    <main style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Trading Assistant Web</h1>
      <div style={{ marginBottom: 16 }}>
        <label>
          Symbol:{" "}
          <select value={symbol} onChange={e => setSymbol(e.target.value)}>
            <option value="BTCUSD">BTC/USD</option>
            <option value="EURUSD">EUR/USD</option>
          </select>
        </label>
      </div>
      <div style={{ marginBottom: 16 }}>
        <label>
          Question:{" "}
          <input
            type="text"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            style={{ width: 350, maxWidth: "90%" }}
          />
        </label>
      </div>
      <div style={{ margin: "1rem 0" }}>
        <button onClick={fetchPrice} disabled={loading} style={{ marginRight: 8 }}>
          Get Price
        </button>
        <button onClick={fetchRSI} disabled={loading} style={{ marginRight: 8 }}>
          Get RSI
        </button>
        <button onClick={fetchAdvice} disabled={loading}>
          Get AI Advice
        </button>
      </div>
      {loading && <div>Loading...</div>}
      {result && <div style={{ marginTop: 16, padding: 12, background: "#f0f0f0" }}>{result}</div>}
      {rsi && <div style={{ marginTop: 8, padding: 12, background: "#e0f7fa" }}>{rsi}</div>}
      {advice && <div style={{ marginTop: 8, padding: 12, background: "#fffde7" }}>{advice}</div>}
      <div style={{ marginTop: 32, fontSize: 14, color: "#888" }}>
        <p>
          <b>Indicator Breakdown (sample):</b>
          <br />
          RSI: 55.23 (Neutral)
          <br />
          MACD: 0.12 (Bullish)
          <br />
          Support: 64000.00
          <br />
          Resistance: 67000.00
        </p>
        <p>
          <i>More features coming soon: AI advice, news, and trade history.</i>
        </p>
      </div>
    </main>
  );
}