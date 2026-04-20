import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────

df_stock = pd.read_csv(RAW_DIR / "stock_data.csv")
df_stock["close"] = pd.to_numeric(df_stock["close"], errors="coerce")
df_stock["volume"] = pd.to_numeric(df_stock["volume"], errors="coerce")

df_interest = pd.read_csv(RAW_DIR / "interest_rate.csv")
df_inflation = pd.read_csv(RAW_DIR / "inflation.csv")
df_unemployment = pd.read_csv(RAW_DIR / "unemployment.csv")
df_gdp = pd.read_csv(RAW_DIR / "gdp.csv")

# ─────────────────────────────────────────────
# STOCK PROCESSING
# ─────────────────────────────────────────────

df_stock["date"] = pd.to_datetime(df_stock["date"])
df_stock = df_stock.sort_values("date")

df_stock["return"] = df_stock["close"].pct_change()

df_stock.set_index("date", inplace=True)

# Daily → Monthly (Month Start)
monthly_stock = df_stock.resample("MS").agg({
    "close": "last",
    "volume": "sum",
    "return": "mean"
})

# Volatility
monthly_stock["volatility"] = df_stock["return"].resample("MS").std()

# Reset index for merge
monthly_stock = monthly_stock.reset_index()

# ─────────────────────────────────────────────
# MACRO PROCESSING
# ─────────────────────────────────────────────

def clean_macro(df):
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    return df

df_interest = clean_macro(df_interest)
df_inflation = clean_macro(df_inflation)
df_unemployment = clean_macro(df_unemployment)
df_gdp = clean_macro(df_gdp)

# Fix GDP (quarterly → monthly)
df_gdp = df_gdp.resample("MS").ffill()

# Rename columns
df_interest.rename(columns={"value": "interest_rate"}, inplace=True)
df_inflation.rename(columns={"value": "inflation"}, inplace=True)
df_unemployment.rename(columns={"value": "unemployment"}, inplace=True)
df_gdp.rename(columns={"value": "gdp"}, inplace=True)

# Reset index (so we can merge on date)
df_interest = df_interest.reset_index()
df_inflation = df_inflation.reset_index()
df_unemployment = df_unemployment.reset_index()
df_gdp = df_gdp.reset_index()

# ─────────────────────────────────────────────
# 🔥 FINAL MERGE (SIMPLE & ROBUST)
# ─────────────────────────────────────────────

df_final = monthly_stock.merge(df_interest, on="date", how="left")
df_final = df_final.merge(df_inflation, on="date", how="left")
df_final = df_final.merge(df_unemployment, on="date", how="left")
df_final = df_final.merge(df_gdp, on="date", how="left")

# Handle missing values
df_final = df_final.ffill()

# Drop rows where stock is missing (safety)
df_final.dropna(subset=["close"], inplace=True)

# ─────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────

output_path = PROCESSED_DIR / "final_dataset.csv"
df_final.to_csv(output_path, index=False)

print("=" * 50)
print(f"Final dataset saved to: {output_path}")
print(f"Shape of dataset: {df_final.shape}")
print("=" * 50)
