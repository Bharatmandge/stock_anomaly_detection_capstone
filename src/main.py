from data_loader import load_data
from features import add_features
from detector import detect_anomalies
from market import market_days
from monthly import monthly_report

df = load_data()
df = add_features(df)
df = detect_anomalies(df)

market = market_days(df)

df[
    ["Date","Ticker","anomaly_flag","type","ret","ret_z","volz","range_pct","why"]
].to_csv("outputs/daily_anomalies.csv", index=False)

market.to_csv("outputs/market_days.csv", index=False)

monthly_report(df, market, 2020, 2).to_csv(
    "outputs/monthly_report_2020_02.csv", index=False
)

print("PROJECT FINISHED SUCCESSFULLY")
