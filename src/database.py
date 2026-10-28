
import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "processed" / "financial_data_clean.csv"
DB_FILE = BASE_DIR / "data" / "finpulse.db"


def load_to_database():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Cleaned CSV not found: {CSV_FILE}")

    df = pd.read_csv(CSV_FILE)

    if df.empty:
        raise ValueError("No cleaned financial data to load.")

    required = [
        "symbol", "date", "open", "high", "low", "price",
        "volume", "currency", "source", "collected_at"
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_FILE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS market_prices (
                symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                price REAL NOT NULL,
                volume REAL,
                currency TEXT NOT NULL,
                source TEXT,
                collected_at TEXT,
                PRIMARY KEY (symbol, date)
            )
        """)

        records = df[required].where(pd.notna(df[required]), None)
        records = records.astype(object)

        connection.executemany("""
            INSERT INTO market_prices (
                symbol, date, open, high, low, price,
                volume, currency, source, collected_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(symbol, date) DO UPDATE SET
                open = excluded.open,
                high = excluded.high,
                low = excluded.low,
                price = excluded.price,
                volume = excluded.volume,
                currency = excluded.currency,
                source = excluded.source,
                collected_at = excluded.collected_at
        """, records.itertuples(index=False, name=None))

        count = connection.execute(
            "SELECT COUNT(*) FROM market_prices"
        ).fetchone()[0]

    print(f"Database updated: {DB_FILE}")
    print(f"Total records in database: {count}")


if __name__ == "__main__":
    load_to_database()
