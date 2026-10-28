
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = RAW_DIR / "financial_data.csv"

SYMBOLS = ["AAPL", "MSFT", "GOOGL"]


def collect_financial_data():
    records = []

    for symbol in SYMBOLS:
        print(f"Fetching {symbol}...")

        try:
            history = yf.Ticker(symbol).history(
                period="5d",
                interval="1d"
            )

            if history.empty:
                print(f"No data returned for {symbol}")
                continue

            for date, row in history.iterrows():
                if pd.isna(row["Close"]):
                    continue

                records.append({
                    "symbol": symbol,
                    "date": date.isoformat(),
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "price": row["Close"],
                    "volume": row["Volume"],
                    "currency": "USD",
                    "source": "Yahoo Finance via yfinance",
                    "collected_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                })

        except Exception as error:
            print(f"Could not fetch {symbol}: {error}")

    if not records:
        raise RuntimeError(
            "No market data collected. Check internet access "
            "or data source availability."
        )

    df = pd.DataFrame(records)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nTotal records collected: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")
    print(df.head().to_string(index=False))

    return df


if __name__ == "__main__":
    collect_financial_data()
