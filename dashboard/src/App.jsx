
import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState(null);
  const [marketData, setMarketData] = useState([]);
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const responses = await Promise.all([
          fetch(`${API}/api/summary`),
          fetch(`${API}/api/market-data`),
          fetch(`${API}/api/scraped-items`),
        ]);

        if (responses.some((response) => !response.ok)) {
          throw new Error("API request failed");
        }

        const [summaryData, prices, scraped] = await Promise.all(
          responses.map((response) => response.json())
        );

        setSummary(summaryData);
        setMarketData(prices);
        setItems(scraped);
      } catch (err) {
        setError("Backend connect nahi ho raha. Check karo ke FastAPI running hai.");
      }
    }

    loadData();
  }, []);

  const latestPrices = summary?.stocks ?? [];

  const chartData = marketData
    .filter((row) => row.symbol === "AAPL")
    .slice()
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .map((row) => ({
      date: row.date.slice(0, 10),
      price: Number(row.price.toFixed(2)),
    }));

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>FinPulse<span>.</span></h2>
        <p className="side-label">WORKSPACE</p>
        <a className="active" href="#overview">▦ Overview</a>
        <a href="#markets">↗ Market Data</a>
        <a href="#scraped">▤ Scraped Items</a>
        <div className="side-footer">Financial ETL Pipeline<br />Local Dashboard</div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <p className="eyebrow">FINANCIAL DATA PLATFORM</p>
            <h1>Market Overview</h1>
            <p className="muted">Your collected and processed data in one place.</p>
          </div>
          <span className="status">● API Connected</span>
        </header>

        {error && <div className="error">{error}</div>}

        <section className="stats" id="overview">
          <article className="stat-card">
            <p>Database Records</p>
            <h2>{summary?.total_records ?? "—"}</h2>
            <span>Stored market records</span>
          </article>
          <article className="stat-card">
            <p>Tracked Stocks</p>
            <h2>{latestPrices.length || "—"}</h2>
            <span>AAPL · MSFT · GOOGL</span>
          </article>
          <article className="stat-card">
            <p>Scraped Items</p>
            <h2>{items.length || "—"}</h2>
            <span>Preview loaded from CSV</span>
          </article>
        </section>

        <section className="panel chart-panel">
          <div className="panel-heading">
            <div>
              <h2>Apple (AAPL) Price History</h2>
              <p className="muted">Historical closing prices · USD</p>
            </div>
            <span className="pill">5-day dataset</span>
          </div>
          <div className="chart">
            {chartData.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis domain={["auto", "auto"]} />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="price"
                    name="Closing Price ($)"
                    stroke="#6c63ff"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="muted">Loading chart data...</p>
            )}
          </div>
        </section>

        <section className="panel" id="markets">
          <div className="panel-heading">
            <div>
              <h2>Latest Market Prices</h2>
              <p className="muted">Latest available record for each stock</p>
            </div>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Symbol</th><th>Closing Price</th><th>Currency</th><th>Date</th></tr>
              </thead>
              <tbody>
                {latestPrices.map((stock) => (
                  <tr key={stock.symbol}>
                    <td><strong>{stock.symbol}</strong></td>
                    <td>${Number(stock.price).toFixed(2)}</td>
                    <td>{stock.currency}</td>
                    <td>{stock.date.slice(0, 10)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="panel" id="scraped">
          <div className="panel-heading">
            <div>
              <h2>Scraped Items</h2>
              <p className="muted">First 100 items returned by the API</p>
            </div>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Title</th><th>Price</th><th>Availability</th></tr>
              </thead>
              <tbody>
                {items.slice(0, 10).map((item, index) => (
                  <tr key={`${item.title}-${index}`}>
                    <td>{item.title}</td>
                    <td>{item.price}</td>
                    <td>{item.availability}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <footer>FinPulse · Built with React, FastAPI, Pandas and SQLite</footer>
      </main>
    </div>
  );
}

export default App;
