import requests
import pandas as pd
import time
from pathlib import Path
import yfinance as yf

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

FRED_API_KEY = "2b02f73b2a365004a3857ecec30306f9"

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# STOCK DATA — Yahoo Finance (yfinance)
# ─────────────────────────────────────────────

def fetch_stock_data(symbol="AAPL"):
    print(f"\n[Stock] Fetching data for {symbol}...")

    try:
        df = yf.download(symbol, start="2015-01-01", progress=False)
    except Exception as e:
        print(f"[Stock] ERROR — Failed to fetch data: {e}")
        return

    if df.empty:
        print("[Stock] ERROR — No data fetched.")
        return

    # Sort (safety)
    df = df.sort_index()

    # Keep required columns
    df = df[["Close", "Volume"]]

    # Reset index
    df.reset_index(inplace=True)

    # Rename columns
    df.rename(columns={
        "Date": "date",
        "Close": "close",
        "Volume": "volume"
    }, inplace=True)

    # Save
    output_path = RAW_DIR / "stock_data.csv"
    df.to_csv(output_path, index=False)

    print(f"[Stock] OK — {len(df)} rows saved to {output_path}")


# ─────────────────────────────────────────────
# MACRO DATA — FRED
# ─────────────────────────────────────────────

def fetch_fred_series(series_id: str, filename: str):
    print(f"\n[FRED] Fetching '{series_id}'...")

    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}"
        f"&api_key={FRED_API_KEY}"
        f"&file_type=json"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[FRED] ERROR — {series_id}: {e}")
        return

    data = response.json()

    if "observations" not in data:
        print(f"[FRED] ERROR — Invalid response for {series_id}")
        return

    rows = []
    for obs in data["observations"]:
        raw_value = obs.get("value", ".")
        rows.append({
            "date": obs.get("date"),
            "value": float(raw_value) if raw_value != "." else None
        })

    if not rows:
        print(f"[FRED] WARNING — No data for {series_id}")
        return

    df = pd.DataFrame(rows)

    output_path = RAW_DIR / f"{filename}.csv"
    df.to_csv(output_path, index=False)

    print(f"[FRED] OK — {len(df)} rows saved to {output_path}")


def fetch_all_fred_series():
    series_map = {
        "FEDFUNDS": "interest_rate",
        "CPIAUCSL": "inflation",
        "UNRATE": "unemployment",
        "GDP": "gdp"
    }

    for series_id, filename in series_map.items():
        fetch_fred_series(series_id, filename)
        time.sleep(0.5)  # polite delay


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("Starting data fetch pipeline")
    print("=" * 50)

    fetch_stock_data("AAPL")

    time.sleep(1)

    fetch_all_fred_series()

    print("\n" + "=" * 50)
    print("Pipeline complete. Files saved to:", RAW_DIR)
    print("=" * 50)