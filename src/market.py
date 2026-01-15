def market_days(df):
    return (
        df.groupby("Date")
        .agg(
            market_ret=("ret", "mean"),
            breadth=("ret", lambda x: (x > 0).mean()),
            market_anomaly_flag=("anomaly_flag", "max")
        )
        .reset_index()
    )
