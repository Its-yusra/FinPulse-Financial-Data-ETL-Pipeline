
from datetime import datetime

from data_collector import collect_financial_data
from etl.data_cleaner import clean_financial_data
from database import load_to_database


def main():
    print("=" * 45)
    print("FinPulse - Financial Data ETL Pipeline")
    print("=" * 45)
    print(f"Pipeline started at: {datetime.now()}")

    try:
        print("\n[1/3] Collecting market data...")
        collect_financial_data()

        print("\n[2/3] Cleaning and validating data...")
        clean_financial_data()

        print("\n[3/3] Loading data into database...")
        load_to_database()

        print("\nPipeline completed successfully!")

    except Exception as error:
        print(f"\nPipeline failed: {error}")
        raise


if __name__ == "__main__":
    main()
