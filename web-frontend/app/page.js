"use client";
import { useState } from "react";
import "./globals.css";

function Badge({ text, color }) {
  return (
    <span
      style={{
        display: "inline-block",
        background: color,
        color: "#fff",
        borderRadius: "6px",
        padding: "2px 10px",
        fontSize: "0.95em",
        marginLeft: 8,
        fontWeight: 600,
        verticalAlign: "middle",
      }}
    >
      {text}
    </span>
  );
}

export default function Home() {
  const [symbol, setSymbol] = useState("BTCUSD");
  const [result, setResult] = useState("");
  const [rsi, setRsi] = useState("");
  const [advice, setAdvice] = useState("");
  const [indicators, setIndicators] = useState(null);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState("What is your advice for the current market?");
  const [error, setError] = useState("");
  const [showIndicators, setShowIndicators] = useState(true);

  const apiBase = "http://127.0.0.1:5000";

  function getRsiBadge(val) {
    if (val > 70) return <Badge text="Overbought" color="#e53935" />;
    if (val < 30) return <Badge text="Oversold" color="#1e88e5" />;
    return <Badge text="Neutral" color="#43a047" />;
  }
  function getMacdBadge(val) {
    if (val > 0) return <Badge text="Bullish" color="#43a047" />;
    if (val < 0) return <Badge text="Bearish" color="#e53935" />;
    return <Badge text="Neutral" color="#757575" />;
  }

  async function fetchPrice() {
    setLoading(true);
    setResult("");
    setRsi("");
    setAdvice("");
    setIndicators(null);
    setError("");
    try {
      const res = await fetch(`${apiBase}/price?symbol=${symbol}`);
      const data = await res.json();
      if (data.price) {
        setResult(`Current price for ${symbol}: ${data.price}`);
      } else {
        setError(data.error || "Error fetching price.");
      }
    } catch (e) {
      setError("Error connecting to backend.");
    }
    setLoading(false);
  }

  async function fetchRSI() {
    setLoading(true);
    setRsi("");
    setAdvice("");
    setIndicators(null);
    setError("");
    try {
      const res = await fetch(`${apiBase}/rsi?symbol=${symbol}`);
      const data = await res.json();
      if (data.rsi) {
        setRsi(`Current RSI for ${symbol}: ${data.rsi.toFixed(2)}`);
      } else {
        setError(data.error || "Error fetching RSI.");
      }
    } catch (e) {
      setError("Error connecting to backend.");
    }
    setLoading(false);
  }

  async function fetchAdvice() {
    setLoading(true);
    setAdvice("");
    setIndicators(null);
    setError("");
    try {
      const res = await fetch(`${apiBase}/advice`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol, question }),
      });
      const data = await res.json();
      if (data.advice) {
        setAdvice(data.advice);
        setIndicators(data.indicators || null);
      } else {
        setError(data.error || "Error fetching advice.");
      }
    } catch (e) {
      setError("Error connecting to backend.");
    }
    setLoading(false);
  }

  return (
    <div className="boltiq-container" style={{ maxWidth: 520, margin: "2.5rem auto" }}>
      <div className="boltiq-header" style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 12 }}>
        <img src="/vercel.svg" alt="BoltiqTrade" style={{ width: 38, height: 38, marginBottom: 0 }} />
        <div>
          <h1 style={{ marginBottom: 0 }}>BoltiqTrade</h1>
          <p style={{ marginTop: 2 }}>Your AI-powered trading assistant for BTC/USD & EUR/USD</p>
        </div>
      </div>
      <div className="boltiq-section" style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
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
        <label className="boltiq-label" style={{ flex: 1 }}>
          Question:
          <input
            className="boltiq-input"
            type="text"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            style={{ width: "100%", minWidth: 180, maxWidth: 320 }}
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
      {loading && (
        <div className="boltiq-card" style={{ textAlign: "center" }}>
          <span className="spinner" style={{
            display: "inline-block",
            width: 24,
            height: 24,
            border: "3px solid #90caf9",
            borderTop: "3px solid #1976d2",
            borderRadius: "50%",
            animation: "spin 1s linear infinite",
            marginRight: 10,
            verticalAlign: "middle"
          }} />
          Loading...
          <style>{`
            @keyframes spin {
              0% { transform: rotate(0deg);}
              100% { transform: rotate(360deg);}
            }
          `}</style>
        </div>
      )}
      {error && (
        <div className="boltiq-card" style={{ background: "#ffebee", color: "#b71c1c", fontWeight: 500 }}>
          {error}
        </div>
      )}
      {result && <div className="boltiq-card">{result}</div>}
      {rsi && <div className="boltiq-card">{rsi}</div>}
      {advice && <div className="boltiq-card" style={{ background: "#fffde7" }}>{advice}</div>}
      {indicators && (
        <div className="boltiq-card" style={{ background: "#e3f2fd", marginTop: 24 }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", cursor: "pointer" }}
            onClick={() => setShowIndicators(v => !v)}>
            <b>Indicator Breakdown</b>
            <span style={{
              fontSize: 18,
              color: "#1976d2",
              fontWeight: 700,
              marginLeft: 8,
              userSelect: "none"
            }}>{showIndicators ? "▼" : "▲"}</span>
          </div>
          {showIndicators && (
            <div style={{ marginTop: 10 }}>
              <div>
                RSI: {indicators.rsi?.toFixed(2)} {getRsiBadge(indicators.rsi)}
              </div>
              <div>
                MACD: {indicators.macd?.toFixed(2)} {getMacdBadge(indicators.macd)}
              </div>
              <div>
                Support: <span style={{ color: "#388e3c", fontWeight: 600 }}>{indicators.support?.toFixed(2)}</span>
              </div>
              <div>
                Resistance: <span style={{ color: "#d32f2f", fontWeight: 600 }}>{indicators.resistance?.toFixed(2)}</span>
              </div>
              <div>
                Price: <span style={{ color: "#1976d2", fontWeight: 600 }}>{indicators.price?.toFixed(2)}</span>
              </div>
            </div>
          )}
        </div>
      )}
      <div className="boltiq-footer">
        &copy; {new Date().getFullYear()} BoltiqTrade &mdash; Powered by Python, Next.js, and OpenAI
      </div>
    </div>
  );
}