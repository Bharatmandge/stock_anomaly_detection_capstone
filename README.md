# Stock Market Anomaly Detection  
### Rule-Based & Unsupervised Analysis on Financial Time Series

This project implements a **leakage-safe, interpretable system to detect abnormal behavior in stock markets** using daily price and volume data.  
The focus is on **detecting unusual market days and stock days**, not on predicting future prices.

The project is designed as an **educational analytics capstone**, emphasizing time-series hygiene, rolling statistics, and unsupervised anomaly detection.

---

## 📌 Project Objectives

- Detect **stock-level anomalies** such as crashes, spikes, and volume shocks
- Identify **market-wide stress days**
- Use **only past information** (no data leakage)
- Avoid complex black-box models
- Produce **clear, explainable outputs** suitable for analysis and reporting

---

## 📊 Dataset

- **Source:** Kaggle – Daily NASDAQ OHLCV data  
- **Frequency:** Daily  
- **Columns:** Date, Open, High, Low, Close, Adj Close, Volume  
- **Assets Used:**
  - QQQ (Market proxy)
  - AAPL, MSFT, AMZN, NVDA, META

**Adjusted Close** prices are used to compute returns to account for corporate actions.

---

## 🧠 Methodology Overview

### 1. Feature Engineering (Leakage-Safe)

All features are computed using **rolling windows based only on past data**.

**Per-Stock Features:**
- **Daily Return**
- **Return Z-Score (63 days)**  
- **Log-Volume Z-Score (21 days)**  
- **Intraday Range Percentile (63 days)**  

A warm-up period is enforced so no day is scored without sufficient history.

---

### 2. Rule-Based Anomaly Detection

A stock-day is flagged as anomalous if **any** of the following conditions hold:

- `|ret_z| > 2.5`
- `volz > 2.5`
- `range_pct > 95`

Each anomaly is labeled for interpretability:
- **Crash** (large negative return)
- **Spike** (large positive return)
- **Volume Shock** (unusual trading activity)

A human-readable **`why`** field explains the trigger conditions.

---

### 3. Market-Level Context

To detect systemic stress, daily market metrics are computed:

- **Market Return:** Mean return across all tickers
- **Breadth:** Fraction of stocks with positive returns
- **Market Anomaly Flag:** Indicates abnormal market days

This distinguishes isolated stock events from market-wide turmoil.

---

### 4. Unsupervised Learning (Optional Enhancement)

Unsupervised clustering is applied to the feature space:

- **K-Means:** Distance from centroid used as anomaly score
- **DBSCAN:** Density-based detection of rare observations

These models **do not replace** the rule-based detector but provide additional validation.

---

## 🗂 Project Structure

stock-market-anomaly-detection/
│
├── data/
│ ├── raw/ # Raw Kaggle CSV files (ignored in Git)
│ └── processed/
│
├── outputs/
│ ├── daily_anomalies.csv
│ ├── market_days.csv
│ └── monthly_report_2020_02.csv
│
├── src/
│ ├── data_loader.py
│ ├── features.py
│ ├── detector.py
│ ├── market.py
│ ├── clustering.py
│ ├── monthly.py
│ └── main.py
│
├── .gitignore
├── requirements.txt
└── README.md

yaml
Copy code

---

## 📈 Outputs

The project generates the following **PDF-aligned deliverables**:

### 1. Daily Anomaly Card
**`outputs/daily_anomalies.csv`**

Contains stock-level anomalies with explanations:
- Date, Ticker
- Anomaly Flag
- Type (crash/spike/volume shock)
- Feature values
- Reason for detection

---

### 2. Market-Day Table
**`outputs/market_days.csv`**

Daily market stress indicators:
- Market return
- Breadth
- Market anomaly flag

---

### 3. Monthly Mini-Report
**`outputs/monthly_report_2020_02.csv`**

Summary of abnormal events for a given month with market context.

---

## ▶️ How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
2. Add Data
Place raw CSV files in:

bash
Copy code
data/raw/
3. Run the Pipeline
bash
Copy code
python src/main.py
All outputs will be generated in the outputs/ folder.
