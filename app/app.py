import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Omega Dashboard", layout="wide")

# ─────────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "final_dataset.csv"

# ─────────────────────────────────────────────
# DEBUG CHECK (VERY IMPORTANT)
# ─────────────────────────────────────────────
st.write("📂 Looking for dataset at:", DATA_PATH)

if not DATA_PATH.exists():
    st.error("❌ Dataset not found! Make sure final_dataset.csv is uploaded to GitHub.")
    st.stop()

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Create stock return
df["stock_return"] = df["close"].pct_change()
df = df.dropna()

# ─────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────
st.title("📊 Omega: Stock vs Macroeconomic Analysis")
st.markdown("Analyzing AAPL stock performance against macro indicators")

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", df["date"].min())
end_date = st.sidebar.date_input("End Date", df["date"].max())

df = df[(df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))]

indicator = st.sidebar.selectbox(
    "Select Macro Indicator",
    ["interest_rate", "inflation", "unemployment", "gdp"]
)

# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

col1.metric("Avg Stock Price", round(df["close"].mean(), 2))
col2.metric("Avg Volatility", round(df["volatility"].mean(), 4))
col3.metric("Avg Volume", int(df["volume"].mean()))

# ─────────────────────────────────────────────
# STOCK PRICE CHART
# ─────────────────────────────────────────────
st.subheader("📈 Stock Price Over Time")

fig1 = px.line(df, x="date", y="close", title="AAPL Stock Price")
st.plotly_chart(fig1, use_container_width=True)

# ─────────────────────────────────────────────
# STOCK RETURN VS MACRO
# ─────────────────────────────────────────────
st.subheader(f"📊 Stock Return vs {indicator}")

fig2 = px.line(
    df,
    x="date",
    y=["stock_return", indicator],
    title=f"Stock Return vs {indicator}"
)

st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# CORRELATION HEATMAP
# ─────────────────────────────────────────────
st.subheader("🔥 Correlation Heatmap")

corr = df[["stock_return", "interest_rate", "inflation", "unemployment", "gdp"]].corr()

fig3 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Correlation Matrix"
)

st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────
# INSIGHTS SECTION
# ─────────────────────────────────────────────
st.subheader("🧠 Key Insights")

st.markdown("""
- 📌 Strong relationship between trading volume and volatility  
- 📌 Interest rates show weak inverse relation with stock returns  
- 📌 Inflation impact is moderate and lag-dependent  
- 📌 GDP correlation is trend-driven, not immediate causation  
""")