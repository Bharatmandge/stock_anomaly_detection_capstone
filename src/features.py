import numpy as np

W_RETURN = 63
W_VOLUME = 21
W_RANGE  = 63

def add_features(df):
    df = df.copy()

    df["range"] = (df["High"] - df["Low"]) / df["Close"]

    df["ret_z"] = (
        df.groupby("Ticker")["ret"]
        .transform(lambda x: (x - x.rolling(W_RETURN).mean().shift(1)) /
                             x.rolling(W_RETURN).std().shift(1))
    )

    df["volz"] = (
        df.groupby("Ticker")["log_volume"]
        .transform(lambda x: (x - x.rolling(W_VOLUME).mean().shift(1)) /
                             x.rolling(W_VOLUME).std().shift(1))
    )

    def range_pct(x):
        out = np.full(len(x), np.nan)
        for i in range(W_RANGE, len(x)):
            out[i] = (x.iloc[i-W_RANGE:i] < x.iloc[i]).mean() * 100
        return out

    df["range_pct"] = df.groupby("Ticker")["range"].transform(range_pct)

    return df
