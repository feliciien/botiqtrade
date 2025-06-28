"use client";
import { useState } from "react";
import "./globals.css";

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
    <div className="boltiq-container">
      <div className="boltiq-header">
        <h1>BoltiqTrade</h1>
        <p>Your AI-powered trading assistant for BTC/USD & EUR/USD</p>
      </div>
      <div className="boltiq-section">
        <label className="boltiq-label">
          Symbol:
          <select
            className="boltiq-select"
            value={symbol}
            onChange={e => setSymbol(e.target.value)}
          >
            <option value="BTCUSD">BTC/USD</option>
            <option value="EURUSD">EUR/USD</option>
          </select>
        </label>
      </div>
      <div className="boltiq-section">
        <label className="boltiq-label">
          Question:
          <input
            className="boltiq-input"
            type="text"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            style={{ width: 320, maxWidth: "90%" }}
          />
        </label>
      </div>
      <div className="boltiq-section" style={{ marginBottom: 0 }}>
        <button className="boltiq-btn" onClick={fetchPrice} disabled={loading}>
          Get Price
        </button>
        <button className="boltiq-btn" onClick={fetchRSI} disabled={loading}>
          Get RSI
        </button>
        <button className="boltiq-btn" onClick={fetchAdvice} disabled={loading}>
          Get AI Advice
        </button>
      </div>
      {loading && <div className="boltiq-card">Loading...</div>}
      {result && <div className="boltiq-card">{result}</div>}
      {rsi && <div className="boltiq-card">{rsi}</div>}
      {advice && <div className="boltiq-card">{advice}</div>}
      <div className="boltiq-card" style={{ background: "#e3f2fd", marginTop: 24 }}>
        <b>Indicator Breakdown (sample):</b>
        <br />
        RSI: 55.23 (Neutral)
        <br />
        MACD: 0.12 (Bullish)
        <br />
        Support: 64000.00
        <br />
        Resistance: 67000.00
      </div>
      <div className="boltiq-footer">
        &copy; {new Date().getFullYear()} BoltiqTrade &mdash; Powered by Python, Next.js, and OpenAI
      </div>
    </div>
  );
}