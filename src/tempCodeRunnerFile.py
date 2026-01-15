import numpy as np
import pandas as pd
from scipy.stats import percentileofscore
from sklearn.cluster import KMeans


def detect_anomalies(df_features, train_df, val_df, test_df):
    df_features = df_features.copy()

    # ---------- KMeans anomaly (example logic) ----------
    feature_cols = ['ret_z', 'volz', 'range_pct']
    X_train = train_df[feature_cols].values

    km = KMeans(n_clusters=2, random_state=42, n_init=10)
    km.fit(X_train)

    # Initialize column with correct dtype (IMPORTANT)
    df_features['km_anom'] = False

    # Predict only on train set here (adjust if needed)
    km_labels_train = km.predict(X_train)

    # Smaller cluster = anomaly
    counts = np.bincount(km_labels_train)
    anomaly_cluster = np.argmin(counts)

    km_anom_train = km_labels_train == anomaly_cluster
    df_features.loc[train_df.index, 'km_anom'] = km_anom_train

    # ---------- Hybrid anomaly flag ----------
    df_features['hybrid_anom'] = (
        (df_features['km_anom']) |
        (df_features['ret_z'].abs() > 3) |
        (df_features['volz'].abs() > 3)
    )

    # ---------- Severity score ----------
    ret_z_abs = abs(df_features['ret_z'].dropna())
    volz_abs = abs(df_features['volz'].dropna())

    def severity_fn(row):
        scores = []

        if not pd.isna(row['ret_z']):
            scores.append(
                percentileofscore(ret_z_abs, abs(row['ret_z']))
            )

        if not pd.isna(row['volz']):
            scores.append(
                percentileofscore(volz_abs, abs(row['volz']))
            )

        return np.mean(scores) if scores else np.nan

    df_features['severity'] = df_features.apply(severity_fn, axis=1)

    # ---------- Final labels ----------
    df_features['anomaly_flag'] = df_features['hybrid_anom']
    df_features['type'] = np.where(df_features['km_anom'], 'cluster', 'rule')
    df_features['why'] = np.where(
        df_features['km_anom'],
        'Cluster outlier',
        'Extreme z-score'
    )

    return df_features
