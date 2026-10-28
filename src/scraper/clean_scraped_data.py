
import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_FILE = BASE_DIR / "data" / "raw" / "scraped_items.json"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "scraped_items_clean.csv"


def clean_scraped_data():
    with open(RAW_FILE, "r", encoding="utf-8") as file:
        items = json.load(file)

    df = pd.DataFrame(items)
    before = len(df)

    required = ["title", "price", "availability", "source_url"]
    df = df.dropna(subset=required)
    df["title"] = df["title"].astype(str).str.strip()
    df["price"] = df["price"].astype(str).str.strip()
    df["availability"] = df["availability"].astype(str).str.strip()
    df = df[df["title"] != ""]
    df = df.drop_duplicates(subset=["title", "source_url"])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Rows before cleaning: {before}")
    print(f"Rows after cleaning: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_scraped_data()
