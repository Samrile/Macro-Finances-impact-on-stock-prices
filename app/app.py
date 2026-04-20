import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="OMEGA Dashboard", layout="wide")

# ─────────────────────────────────────────────
# CUSTOM UI (PREMIUM LOOK)
# ─────────────────────────────────────────────
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #00ffcc;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────────
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

# Stock return
df["stock_return"] = df["close"].pct_change()
df = df.dropna()

# ─────────────────────────────────────────────
# STANDARDIZATION (Z-SCORE)
# ─────────────────────────────────────────────
scaler = StandardScaler()

cols_to_scale = [
    "close", "stock_return",
    "interest_rate", "inflation",
    "unemployment", "gdp"
]

df_scaled = df.copy()
df_scaled[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])

# ─────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────
st.title("🚀 OMEGA Dashboard")
st.markdown("### 📈 Standardized Macro-Financial Analysis")

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.header("Controls")

indicator = st.sidebar.selectbox(
    "Select Indicator",
    ["interest_rate", "inflation", "unemployment", "gdp"]
)

lag = st.sidebar.slider("Lag (months)", 0, 6, 0)

# Apply lag
df_scaled[f"{indicator}_lag"] = df_scaled[indicator].shift(lag)

# ─────────────────────────────────────────────
# KPI SECTION
# ─────────────────────────────────────────────
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Latest Price", round(df["close"].iloc[-1], 2))
col2.metric("Volatility", round(df["volatility"].mean(), 4))
col3.metric("Avg Volume", int(df["volume"].mean()))
col4.metric("Avg Return", round(df["stock_return"].mean(), 4))

st.markdown("---")

# ─────────────────────────────────────────────
# STANDARDIZED COMPARISON PLOT
# ─────────────────────────────────────────────
st.subheader(f"📊 Stock vs {indicator} (Standardized)")

fig1 = px.line(
    df_scaled,
    x="date",
    y=["close", indicator],
    labels={"value": "Z-Score"},
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# LAG ANALYSIS
# ─────────────────────────────────────────────
st.subheader(f"📉 Lag Analysis (Lag = {lag})")

fig2 = px.line(
    df_scaled,
    x="date",
    y=["stock_return", f"{indicator}_lag"],
    labels={"value": "Z-Score"}
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# ROLLING CORRELATION
# ─────────────────────────────────────────────
st.subheader("📈 Rolling Correlation")

rolling_corr = df_scaled["stock_return"].rolling(6).corr(df_scaled[f"{indicator}_lag"])

fig3 = px.line(
    x=df_scaled["date"],
    y=rolling_corr,
    labels={"x": "Date", "y": "Correlation"}
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# HEATMAP
# ─────────────────────────────────────────────
st.subheader("🔥 Correlation Heatmap")

corr = df_scaled[
    ["stock_return", "interest_rate", "inflation", "unemployment", "gdp"]
].corr()

fig4 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r")

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# MACHINE LEARNING MODEL
# ─────────────────────────────────────────────
st.subheader("🤖 Prediction Model")

features = ["interest_rate", "inflation", "unemployment", "gdp"]
target = "stock_return"

df_model = df_scaled.dropna()

X = df_model[features]
y = df_model[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

model = LinearRegression()
model.fit(X_train, y_train)

df_model["prediction"] = model.predict(X)

# Plot prediction
fig5 = px.line(
    df_model,
    x="date",
    y=["stock_return", "prediction"],
    title="Actual vs Predicted Returns"
)

st.plotly_chart(fig5, use_container_width=True)

# Model score
r2 = r2_score(y_test, model.predict(X_test))
st.metric("Model R² Score", round(r2, 3))

st.markdown("---")

# ─────────────────────────────────────────────
# AI INSIGHTS
# ─────────────────────────────────────────────
st.subheader("🧠 AI Insights")

corr_value = df_scaled["stock_return"].corr(df_scaled[f"{indicator}_lag"])

if corr_value > 0.3:
    st.success("📈 Positive relationship detected")
elif corr_value < -0.3:
    st.error("📉 Negative relationship detected")
else:
    st.warning("⚖️ Weak relationship")

st.write(f"Correlation: {round(corr_value, 3)}")