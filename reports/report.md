# 📊 OMEGA: Macro-Financial Impact Analysis

## 1. 📌 Problem Statement

The objective of this project is to analyze how macroeconomic indicators such as interest rates, inflation, unemployment, and GDP impact stock performance, specifically focusing on Apple (AAPL).

The goal is to understand whether macroeconomic factors influence stock returns directly or with a lag, and to explore if these relationships can be used for predictive modeling.

---

## 2. 📊 Data Sources

The project uses multiple real-world financial data sources:

* Stock Data: Apple (AAPL) historical data via yfinance
* Macroeconomic Data: Federal Reserve Economic Data (FRED)

  * Interest Rate (FEDFUNDS)
  * Inflation (CPIAUCSL)
  * Unemployment (UNRATE)
  * GDP

---

## 3. ⚙️ Data Pipeline

An end-to-end data pipeline was built:

* Data fetched using APIs
* Stored in raw format (CSV)
* Cleaned and converted to consistent datetime format
* Stock data resampled from daily to monthly
* Macroeconomic data aligned to monthly frequency
* All datasets merged into a single unified dataset

This ensured consistency for time-series analysis.

---

## 4. 📈 Feature Engineering

Several key features were created:

* Monthly stock returns (percentage change)
* Volatility (standard deviation of returns)
* Lagged macroeconomic variables
* Standardized (Z-score) values for comparison across scales

Standardization was critical because macro indicators and stock prices operate on different scales.

---

## 5. 📊 Exploratory Data Analysis (EDA)

### Key Observations:

* 📌 Strong relationship between **trading volume and volatility**
* 📌 Moderate correlation between **interest rates and stock returns**
* 📌 Weak relationship between **inflation and stock returns**
* 📌 Strong trend-based relationship between **GDP and stock price**

---

## 6. 🔁 Lag Analysis

Lag analysis was performed to understand delayed effects of macroeconomic indicators.

### Findings:

* Macroeconomic variables do not impact stock returns immediately
* Some indicators show stronger correlation when lagged by 1–3 months
* This suggests delayed market reaction to economic changes

---

## 7. 📉 Rolling Correlation

Rolling correlation was used to analyze how relationships change over time.

### Insights:

* Correlations are not stable and vary across time periods
* Certain economic phases show stronger dependencies
* Reinforces that financial markets are dynamic

---

## 8. 🤖 Predictive Modeling

A Linear Regression model was built to predict stock returns using macroeconomic indicators.

### Features Used:

* Interest Rate
* Inflation
* Unemployment
* GDP

### Result:

* Model achieved moderate predictive performance (R² score varies)

### Interpretation:

* Macroeconomic indicators alone are not sufficient for highly accurate predictions
* However, they provide useful directional insights

---

## 9. ⚠️ Limitations

* Analysis limited to a single stock (AAPL)
* Macroeconomic data frequency mismatch (monthly vs daily)
* External factors (news, sentiment) not included
* Correlation does not imply causation

---

## 10. 🚀 Future Improvements

* Include multiple stocks (S&P 500 level analysis)
* Use advanced models (XGBoost, LSTM)
* Integrate real-time data pipeline
* Add sentiment analysis from news/social media

---

## 11. 🧠 Conclusion

This project demonstrates that macroeconomic indicators influence stock performance, often with delayed effects.

While predictive power is limited using only macro data, combining it with other factors can significantly improve forecasting.

The project highlights the importance of time-series analysis, feature engineering, and data normalization in financial analytics.

---
