# FinPulse — Financial Data ETL Pipeline

FinPulse is a financial data collection and ETL project built with Python. It collects historical stock market data, cleans and validates records, stores them in SQLite, and provides a dashboard through a FastAPI backend and React frontend.

## Features

- **Financial Data Collection:** Collects historical stock data for AAPL, MSFT, and GOOGL using `yfinance`.
- **Web Scraping:** Uses Scrapy to extract product information from Books to Scrape.
- **Data Cleaning:** Processes CSV data using Pandas.
- **Database:** Stores market records in SQLite.
- **REST API:** Exposes data through FastAPI endpoints.
- **Dashboard:** Displays stock prices, a historical price chart, and scraped products using React and Recharts.
- **Automation:** Includes a Python scheduler script and Windows Task Scheduler integration.
- **Testing:** Includes pytest tests for saved data and database records.

## Tech Stack

- Python
- Pandas
- yfinance
- Scrapy
- SQLite
- FastAPI
- Uvicorn
- React
- Vite
- Recharts
- Pytest

## Project Structure

```text
FinPulse/
├── data/
│   ├── raw/
│   ├── processed/
│   └── finpulse.db
├── dashboard/
│   └── src/
├── docs/
├── logs/
├── src/
│   ├── api.py
│   ├── database.py
│   ├── data_collector.py
│   ├── main.py
│   ├── scheduler.py
│   ├── etl/
│   │   └── data_cleaner.py
│   └── scraper/
│       ├── financial_spider.py
│       └── clean_scraped_data.py
└── tests/
    └── test_pipeline.py
```

## Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FinPulse
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
python -m pip install pandas yfinance scrapy fastapi uvicorn pytest
```

Install any additional database or project dependencies required by your environment.

### 4. Run the ETL pipeline

```powershell
python src/main.py
```

The pipeline collects market data, cleans it, and loads it into SQLite.

### 5. Run the web scraper

```powershell
scrapy runspider src/scraper/financial_spider.py -O data/raw/scraped_items.json
python src/scraper/clean_scraped_data.py
```

### 6. Start the API

From the project root:

```powershell
python -m uvicorn src.api:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### 7. Start the React dashboard

Open a second terminal:

```powershell
cd dashboard
npm install
npm install recharts
npm run dev
```

Open the local URL displayed by Vite, usually http://localhost:5173.

## Run Tests

From the project root:

```powershell
python -m pytest tests/test_pipeline.py -v
```

## API Endpoints

| Endpoint | Description |
|---|---|
| `/` | API status |
| `/api/summary` | Total records and latest stock prices |
| `/api/market-data` | Historical market records |
| `/api/scraped-items` | Scraped product records |
| `/docs` | Interactive API documentation |

## Automation

The script `src/scheduler.py` runs the ETL pipeline and writes execution details to `logs/scheduler.log`. Windows Task Scheduler can execute this script daily.

## Notes

- Market data is historical and may be delayed; this project does not provide guaranteed real-time quotes.
- The Scrapy spider uses Books to Scrape, a practice website, to demonstrate web scraping.
- Data availability depends on internet access and third-party source availability.
- This project is intended for learning and portfolio demonstration, not financial advice.

## Author

Yusra Komal

GitHub: https://github.com/Its-yusra
