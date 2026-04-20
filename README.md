# 🚀 OMEGA: Macro-Financial Impact Analysis Dashboard

## 📌 Overview

OMEGA is an end-to-end data science project that analyzes the relationship between macroeconomic indicators and stock performance.
The project focuses on Apple (AAPL) and explores how factors like interest rates, inflation, unemployment, and GDP influence stock returns.

It combines **data engineering, time-series analysis, and machine learning** into an interactive dashboard built with Streamlit.

---

## 🎯 Problem Statement

Financial markets are influenced by macroeconomic conditions, but these relationships are often unclear and delayed.
This project aims to:

* Identify correlations between macro indicators and stock returns
* Analyze delayed (lagged) effects
* Build a predictive model for stock returns

---

## 📊 Data Sources

* Stock Data: Apple (AAPL) via yfinance
* Macroeconomic Data: FRED (Federal Reserve Economic Data)

  * Interest Rate
  * Inflation
  * Unemployment
  * GDP

---

## ⚙️ Project Pipeline

1. Data fetched using APIs
2. Stored in raw format (CSV)
3. Cleaned and transformed into monthly frequency
4. Merged into a unified dataset
5. Used for analysis, visualization, and modeling

---

## 📈 Key Features

* 📊 **Z-score Standardization** for fair comparison across variables
* 🔁 **Lag Analysis** to capture delayed macroeconomic effects
* 📉 **Rolling Correlation** to analyze dynamic relationships
* 🤖 **Linear Regression Model** for stock return prediction
* 📊 Interactive **Streamlit Dashboard**

---

## 🧠 Key Insights

* Strong relationship between **trading volume and volatility**
* Moderate relationship between **interest rates and stock returns**
* Weak correlation with **inflation**
* Strong trend-based relationship between **GDP and stock price**
* Macroeconomic indicators often impact stock returns **with delay**

---

## 🤖 Machine Learning

* Model: Linear Regression
* Features: Interest Rate, Inflation, Unemployment, GDP
* Target: Stock Return
* Performance: Moderate predictive power (R² score varies)

---

## 📊 Dashboard Features

* Interactive filters
* Standardized comparison plots
* Lag-based analysis
* Rolling correlation visualization
* Prediction vs actual comparison

---

## 🛠️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* Plotly
* Streamlit

---

## 📸 Dashboard Preview

![image alt](https://github.com/Samrile/Macro-Finances-impact-on-stock-prices/blob/9ad3be6631763c3c47b3ae2c854e7221a0f02238/Screenshot%202026-04-20%20192316.png)

---

## ⚠️ Limitations

* Single stock analysis (AAPL only)
* Macro data frequency mismatch
* External factors (news, sentiment) not included
* Correlation does not imply causation

---

## 🚀 Future Improvements

* Multi-stock analysis (S&P 500)
* Advanced models (XGBoost, LSTM)
* Real-time data pipeline
* Sentiment analysis integration

---

## 🧠 Conclusion

This project demonstrates how macroeconomic indicators influence stock performance, often with delayed effects.
It highlights the importance of time-series analysis, feature engineering, and data normalization in financial analytics.

---

## 👤 Author

Sam Khair
Aspiring Data Scientist
