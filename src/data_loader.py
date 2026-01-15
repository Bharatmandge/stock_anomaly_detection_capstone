import pandas as pd
import numpy as np
from pathlib import Path

RAW_DIR = Path("data/raw")

TICKERS = {
    "AAPL.csv": "AAPL",
    "AMZN.csv": "AMZN",
    "MET.csv": "META",
    "MSFT.csv": "MSFT",
    "NVDA.csv": "NVDA",
    "QQQX.csv": "QQQ",
}

def load_data():
    dfs = []

    for file, ticker in TICKERS.items():
        path = RAW_DIR / file
        df = pd.read_csv(path)

        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        df["Ticker"] = ticker
        df["ret"] = df["Adj Close"].pct_change()
        df["log_volume"] = np.log(df["Volume"].replace(0, np.nan))

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
