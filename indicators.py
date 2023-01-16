import pandas as pd

def sma(close, n):
    return close.rolling(n).mean()

def rsi(high, low, n):
    high_ma = high.rolling(n).mean()
    low_ma = low.rolling(n).mean()
    high_ma.fillna(method = "bfill", inplace=True)
    low_ma.fillna(method = "bfill", inplace=True)
    rsi_list = []
    for i in range(len(high)):
        rsi_list.append(100-(100/(1+high_ma[i]/low_ma[i])))
    return pd.Series(rsi_list)