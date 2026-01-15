def date_query(df, market_df, date):
    print("\nMarket status:")
    print(market_df[market_df["Date"] == date])

    print("\nStock anomalies:")
    print(
        df[(df["Date"] == date) & (df["anomaly_flag"] == 1)]
        [["Ticker", "type", "ret_z", "volz", "range_pct", "why"]]
    )
