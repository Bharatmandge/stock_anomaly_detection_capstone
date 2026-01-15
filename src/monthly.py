import pandas as pd

def monthly_report(df, market_df, year, month):
    start = pd.Timestamp(year, month, 1)
    end   = start + pd.offsets.MonthEnd(1)

    report = df[
        (df["Date"] >= start) &
        (df["Date"] <= end) &
        (df["anomaly_flag"] == 1)
    ]

    report = report.merge(
        market_df[["Date", "market_anomaly_flag"]],
        on="Date",
        how="left"
    )

    return report[
        ["Date","Ticker","type","ret_z","volz","market_anomaly_flag","why"]
    ]
