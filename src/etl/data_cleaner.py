
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_FILE = BASE_DIR / "data" / "raw" / "financial_data.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_FILE = PROCESSED_DIR / "financial_data_clean.csv"


def clean_financial_data():
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {RAW_FILE}"
        )

    # Load raw financial data
    df = pd.read_csv(RAW_FILE)

    initial_rows = len(df)
    print(f"Rows loaded: {initial_rows}")

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    required_columns = [
        "symbol",
        "price",
        "currency",
        "source",
        "collected_at",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns missing: {missing_columns}"
        )

    # Normalize text fields
    df["symbol"] = df["symbol"].astype("string").str.strip().str.upper()
    df["currency"] = df["currency"].astype("string").str.strip().str.upper()

    # Convert prices to numeric values
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Remove incomplete and invalid records
    df = df.dropna(
        subset=["symbol", "price", "currency", "collected_at"]
    )

    df = df[
        (df["symbol"] != "")
        & (df["currency"] != "")
        & (df["price"] > 0)
    ]

    # Remove duplicate records
    df = df.drop_duplicates(
        subset=["symbol", "currency", "collected_at"]
    )

    # Save cleaned data
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_FILE, index=False)

    print(f"Rows before cleaning: {initial_rows}")
    print(f"Rows after cleaning: {len(df)}")
    print(f"Rows removed: {initial_rows - len(df)}")
    print(f"Saved cleaned data to: {PROCESSED_FILE}")

    if df.empty:
        raise ValueError("No valid financial records remain after cleaning.")

    return df


if __name__ == "__main__":
    cleaned_df = clean_financial_data()
    print("\nCleaned data preview:")
    print(cleaned_df.to_string(index=False))
