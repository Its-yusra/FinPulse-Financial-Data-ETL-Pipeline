
import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "data" / "finpulse.db"
SCRAPED_FILE = BASE_DIR / "data" / "processed" / "scraped_items_clean.csv"

app = FastAPI(title="FinPulse API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FinPulse API is running"}


@app.get("/api/market-data")
def market_data():
    with sqlite3.connect(DB_FILE) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("""
            SELECT symbol, date, open, high, low, price,
                   volume, currency
            FROM market_prices
            ORDER BY date DESC, symbol
        """).fetchall()

    return [dict(row) for row in rows]



@app.get("/api/summary")
def summary():
    with sqlite3.connect(DB_FILE) as connection:
        connection.row_factory = sqlite3.Row

        total = connection.execute(
            "SELECT COUNT(*) FROM market_prices"
        ).fetchone()[0]

        latest = connection.execute("""
            SELECT symbol, price, date
            FROM market_prices
            WHERE date IN (
                SELECT MAX(date)
                FROM market_prices
                GROUP BY symbol
            )
            ORDER BY symbol
        """).fetchall()

    return {
        "total_records": total,
        "stocks": [dict(row) for row in latest],
    }


@app.get("/api/scraped-items")
def scraped_items():
    if not SCRAPED_FILE.exists():
        return []

    df = pd.read_csv(SCRAPED_FILE).fillna("")
    return df.head(100).to_dict(orient="records")
