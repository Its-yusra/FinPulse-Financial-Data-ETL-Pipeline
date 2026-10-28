
import json
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]


def test_financial_raw_data_exists():
    path = BASE_DIR / "data/raw/financial_data.csv"
    assert path.exists()

    df = pd.read_csv(path)
    assert not df.empty
    assert {"symbol", "date", "price"}.issubset(df.columns)


def test_cleaned_financial_data():
    path = BASE_DIR / "data/processed/financial_data_clean.csv"
    assert path.exists()

    df = pd.read_csv(path)
    assert not df.empty
    assert df["price"].notna().all()
    assert (df["price"] > 0).all()


def test_database_has_market_records():
    path = BASE_DIR / "data/finpulse.db"
    assert path.exists()

    with sqlite3.connect(path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM market_prices"
        ).fetchone()[0]

        symbols = {
            row[0]
            for row in connection.execute(
                "SELECT DISTINCT symbol FROM market_prices"
            ).fetchall()
        }

    assert count >= 3
    assert {"AAPL", "MSFT", "GOOGL"}.issubset(symbols)


def test_scraped_json_has_items():
    path = BASE_DIR / "data/raw/scraped_items.json"
    assert path.exists()

    with open(path, encoding="utf-8") as file:
        items = json.load(file)

    assert len(items) > 0
    assert {"title", "price", "availability"}.issubset(items[0])


def test_cleaned_scraped_csv_exists():
    path = BASE_DIR / "data/processed/scraped_items_clean.csv"
    assert path.exists()

    df = pd.read_csv(path)
    assert not df.empty
    assert {"title", "price", "availability"}.issubset(df.columns)
