import { useState, useEffect } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
} from "recharts";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [strategies, setStrategies] = useState([]);   // dropdown options
  const [ticker, setTicker] = useState("AAPL");       // form input
  const [strategy, setStrategy] = useState("momentum");// form input
  const [result, setResult] = useState(null);         // API response
  const [loading, setLoading] = useState(false);

  // On first load, fetch the list of strategies for the dropdown.
  useEffect(() => {
    fetch(`${API}/strategies`)
      .then((r) => r.json())
      .then((d) => setStrategies(d.strategies));
  }, []);

  // Called when user clicks "Run backtest".
  async function runBacktest() {
    setLoading(true);
    const r = await fetch(`${API}/backtest?ticker=${ticker}&strategy=${strategy}`);
    const data = await r.json();
    setResult(data);
    setLoading(false);
  }

  // Reshape the three parallel arrays into what recharts wants:
  // [{ date, equity, benchmark }, ...]
  const chartData =
    result?.dates?.map((date, i) => ({
      date,
      equity: result.equity[i],
      benchmark: result.benchmark[i],
    })) ?? [];

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Backtesting Framework</h1>

      {/* --- Controls --- */}
      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <input
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          placeholder="Ticker (e.g. AAPL)"
        />
        <select value={strategy} onChange={(e) => setStrategy(e.target.value)}>
          {strategies.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <button onClick={runBacktest} disabled={loading}>
          {loading ? "Running..." : "Run backtest"}
        </button>
      </div>

      {/* --- Metrics --- */}
      {result?.metrics && (
        <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 20 }}>
          <Metric label="Total return" value={pct(result.metrics.total_return)} />
          <Metric label="CAGR" value={pct(result.metrics.cagr)} />
          <Metric label="Sharpe" value={result.metrics.sharpe?.toFixed(2)} />
          <Metric label="Max drawdown" value={pct(result.metrics.max_drawdown)} />
          <Metric label="Win rate" value={pct(result.metrics.win_rate)} />
          <Metric label="Profit factor" value={result.metrics.profit_factor?.toFixed(2)} />
        </div>
      )}

      {/* --- Chart --- */}
      {chartData.length > 0 && (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <XAxis dataKey="date" minTickGap={60} />
            <YAxis domain={["auto", "auto"]} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="equity" stroke="#2563eb" dot={false} name="Strategy" />
            <Line type="monotone" dataKey="benchmark" stroke="#f59e0b" dot={false} name="Buy & hold" />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

// Small helper component for a metric card.
function Metric({ label, value }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: "10px 16px" }}>
      <div style={{ fontSize: 12, color: "#666" }}>{label}</div>
      <div style={{ fontSize: 20, fontWeight: 600 }}>{value ?? "—"}</div>
    </div>
  );
}

// Format a fraction as a percent, e.g. 0.354 -> "35.40%".
function pct(x) {
  return x == null ? "—" : (x * 100).toFixed(2) + "%";
}