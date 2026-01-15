def detect_anomalies(df):
    df = df.copy()

    df["anomaly_flag"] = (
        (df["ret_z"].abs() > 2.5) |
        (df["volz"] > 2.5) |
        (df["range_pct"] > 95)
    ).astype(int)

    def anomaly_type(r):
        t = []
        if r["ret_z"] < -2.5:
            t.append("crash")
        if r["ret_z"] > 2.5:
            t.append("spike")
        if r["volz"] > 2.5:
            t.append("volume_shock")
        return " + ".join(t) if t else None

    df["type"] = df.apply(anomaly_type, axis=1)

    def why(r):
        w = []
        if abs(r["ret_z"]) > 2.5:
            w.append("|ret_z| > 2.5")
        if r["volz"] > 2.5:
            w.append("volz > 2.5")
        if r["range_pct"] > 95:
            w.append("range_pct > 95")
        return "; ".join(w) if r["anomaly_flag"] else None

    df["why"] = df.apply(why, axis=1)

    return df
