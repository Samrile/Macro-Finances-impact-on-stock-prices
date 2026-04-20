import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Omega Dashboard", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "final_dataset.csv"

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
if not DATA_PATH.exists():
    st.error("Dataset not found!")
    st.stop()

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

df["stock_return"] = df["close"].pct_change()
df = df.dropna()

# ─────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────
st.title("📊 Omega: Stock vs Macroeconomic Analysis")
st.markdown("Interactive dashboard for analyzing macro-financial relationships")

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.header("Controls")

start_date = st.sidebar.date_input("Start Date", df["date"].min())
end_date = st.sidebar.date_input("End Date", df["date"].max())

indicator = st.sidebar.selectbox(
    "Select Indicator",
    ["interest_rate", "inflation", "unemployment", "gdp"]
)

lag = st.sidebar.slider("Lag (months)", 0, 6, 0)

rolling_window = st.sidebar.slider("Rolling Window", 3, 24, 6)

# Filter
df = df[(df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))]

# Apply lag
df[f"{indicator}_lag"] = df[indicator].shift(lag)

# ─────────────────────────────────────────────
# KPI
# ─────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

col1.metric("Avg Price", round(df["close"].mean(), 2))
col2.metric("Volatility", round(df["volatility"].mean(), 4))
col3.metric("Volume", int(df["volume"].mean()))

# ─────────────────────────────────────────────
# STOCK PRICE
# ─────────────────────────────────────────────
st.subheader("📈 Stock Price")

fig1 = px.line(df, x="date", y="close")
st.plotly_chart(fig1, use_container_width=True)

# ─────────────────────────────────────────────
# LAG ANALYSIS PLOT
# ─────────────────────────────────────────────
st.subheader(f"📊 Stock Return vs {indicator} (Lag = {lag})")

fig2 = px.line(
    df,
    x="date",
    y=["stock_return", f"{indicator}_lag"]
)

st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# ROLLING CORRELATION
# ─────────────────────────────────────────────
st.subheader("📉 Rolling Correlation")

rolling_corr = df["stock_return"].rolling(rolling_window).corr(df[f"{indicator}_lag"])

fig3 = px.line(
    x=df["date"],
    y=rolling_corr,
    labels={"x": "Date", "y": "Correlation"}
)

st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────
# HEATMAP
# ─────────────────────────────────────────────
st.subheader("🔥 Correlation Heatmap")

corr = df[["stock_return", "interest_rate", "inflation", "unemployment", "gdp"]].corr()

fig4 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r")
st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────
# AUTO INSIGHTS
# ─────────────────────────────────────────────
st.subheader("🧠 Auto Insights")

current_corr = df["stock_return"].corr(df[f"{indicator}_lag"])

if current_corr > 0.3:
    insight = "Positive relationship detected"
elif current_corr < -0.3:
    insight = "Negative relationship detected"
else:
    insight = "Weak or no clear relationship"

st.markdown(f"""
- Selected Indicator: **{indicator}**
- Lag Applied: **{lag} months**
- Correlation: **{round(current_corr, 3)}**

👉 Insight: **{insight}**
""")