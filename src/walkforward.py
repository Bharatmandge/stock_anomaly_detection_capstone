def split_data(df):
    train = df[df["Date"] < "2020-01-01"]
    test  = df[df["Date"] >= "2020-01-01"]
    return train, test
