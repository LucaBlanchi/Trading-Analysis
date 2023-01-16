import pandas as pd
import os
import strategies as strat

path = os.path.dirname(os.path.realpath(__file__)) + "/price.csv"
df = pd.read_csv(path)
df.fillna(method = "ffill", inplace = True)

x = strat.hold(df["Close"])
print(f"Cash at the end of 'hold' strategy:\n{x}\n")

x = strat.random(df["Close"])
print(f"Cash at the end of 'random' strategy:\n{x}\n")

x = strat.simple_sma(df["Close"], 5, 1.05)
print(f"Cash at the end of 'simple_sma' strategy:\n{x}\n")

x = strat.simple_sma_positions(df["Close"], 5, 1.05)
print(f"Cash at the end of 'simple_sma_positions' strategy:\n{x}\n")

x = strat.sma_rsi(df["Close"], df["High"], df["Low"])
print(f"Cash at the end of 'sma_rsi' strategy:\n{x}\n")