import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from trading_strategies import run_trading_strategies


def total_returns(df):
    df["MACD return"] = df["MACD Delta V Total"] / df["MACD V"].shift(1)
    df["MACD return"].dropna(inplace = True)
    df["BB return"] = df["BB Delta V Total"] / df["BB V"].shift(1)
    df["BB return"].dropna(inplace = True)
    return df

def sharpe(df):
    df["MACD Sharpe"] = (df["MACD return"].mean() / df["MACD return"].std()) * np.sqrt(252)
    df["BB Sharpe"] = (df["BB return"].mean() / df["BB return"].std()) * np.sqrt(252)
    print(f"MACD Sharpe Ratio: {df['MACD Sharpe'].iloc[-1]}, BB Sharpe Ratio {df['BB Sharpe'].iloc[-1]}")

def calmar(df):
    MACD_max_drawdown = maximum_drawdown(df["MACD V"])
    BB_max_drawdown = maximum_drawdown(df["BB V"])
    df["MACD Calmar"] = (df["MACD return"].mean()* 252) / MACD_max_drawdown
    df["BB Calmar"] = (df["BB return"].mean() * 252) / BB_max_drawdown

    print(f" MACD Calmar: {df['MACD Calmar'].iloc[-1]}, BB Calmar: {df['BB Calmar'].iloc[-1]}")


def maximum_drawdown(V):
    V = V.dropna()
    rolling_max = V.cummax()
    drawdown = (V - rolling_max) / rolling_max
    max_drawdown = abs(drawdown.min())
    return max_drawdown


if __name__ == "__main__":
    df = run_trading_strategies()
    df = total_returns(df)
    sharpe(df)
    calmar(df)