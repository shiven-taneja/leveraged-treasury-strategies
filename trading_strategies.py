import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from time_series_prep import combined_df

def MACD(df):

    df['EMA_12'] = df["SPTL"].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df["SPTL"].ewm(span=26, adjust=False).mean()

    df["MACD"] =  df['EMA_26'] - df['EMA_12']

    n = len(df)
    theta = np.zeros(n)
    V_total = np.zeros(n)
    V_total[0] = 100000
    L = 10

    delta_V = np.zeros(n)
    delta_V_cap = np.zeros(n)

    for t in range(1, n):
        if t  < 26: 
            theta[t] = 0.0
            V_total[t] = V_total[t-1]
            continue 

        if df["MACD"].iloc[t] > 0 and df["SPTL"].iloc[t]  - df['EMA_26'].iloc[t] > 0: 
            theta[t] = np.floor((V_total[t-1]*L)/df["SPTL"].iloc[t])*df["SPTL"].iloc[t] 
        elif df["MACD"].iloc[t] < 0 and df["SPTL"].iloc[t] - df['EMA_26'].iloc[t] < 0:
            theta[t] = -np.floor((V_total[t-1]*L)/df["SPTL"].iloc[t])*df["SPTL"].iloc[t] 
        else: 
            theta[t] = 0
        
        daily_return = (df["SPTL"].iloc[t] - df["SPTL"].iloc[t-1]) / df["SPTL"].iloc[t-1]

        delta_V[t] = (daily_return - df["EFFR Daily Rate"].iloc[t-1]) * theta[t-1]

        used_margin = abs(theta[t-1]) / L 
        delta_V_cap[t] = (V_total[t-1] - used_margin) * df["EFFR Daily Rate"].iloc[t-1]

        V_total[t] = V_total[t-1] + delta_V[t] + delta_V_cap[t]

    df["MACD theta"] = theta
    df["MACD V"] = V_total
    print(df["MACD V"].iloc[-1])

    df["MACD Delta V"] = delta_V
    df["MACD Delta V Cap"] = delta_V_cap
    df["MACD Delta V Total"] = df["MACD Delta V"] + df["MACD Delta V Cap"]

    df["MACD cumulative Delta V"] = df["MACD Delta V"].cumsum()
    df["MACD cumulative Delta V Cap"] = df["MACD Delta V Cap"].cumsum()
    df["MACD cumulative Delta V Total"] = df["MACD Delta V Total"].cumsum()


    return df

def mean_reversion_bollinger_bands(df):

    df["MA20"] = df["SPTL"].rolling(20).mean()
    df["SD20"] = df["SPTL"].rolling(20).std()
    df["UB"] = df["MA20"] + 2 * df["SD20"]
    df["LB"] = df["MA20"] - 2 * df["SD20"]

    n = len(df)
    theta = np.zeros(n)
    V_total = np.zeros(n)
    V_total[0] = 100000
    L = 10

    delta_V = np.zeros(n)
    delta_V_cap = np.zeros(n)


    for t in range(1, n):
        if t < 20: 
            theta[t] = 0.0
            V_total[t] = V_total[t-1]
            continue 

        if df["SPTL"].iloc[t] > df["UB"].iloc[t]:
            theta[t] = -np.floor((V_total[t-1]*L)/df["SPTL"].iloc[t])*df["SPTL"].iloc[t] 
        elif df["SPTL"].iloc[t] < df["LB"].iloc[t]:
            theta[t] = np.floor((V_total[t-1]*L)/df["SPTL"].iloc[t])*df["SPTL"].iloc[t]
        else: 
            theta[t] = 0

        daily_return = (df["SPTL"].iloc[t] - df["SPTL"].iloc[t-1]) / df["SPTL"].iloc[t-1]

        delta_V[t] = (daily_return - df["EFFR Daily Rate"].iloc[t-1]) * theta[t-1]

        used_margin = abs(theta[t-1]) / L 
        delta_V_cap[t] = (V_total[t-1] - used_margin) * df["EFFR Daily Rate"].iloc[t-1]

        V_total[t] = V_total[t-1] + delta_V[t] + delta_V_cap[t]
    df["BB theta"] = theta
    df["BB V"] = V_total
    print(df["BB V"].iloc[-1])
    
    df["BB Delta V"] = delta_V
    df["BB Delta V Cap"] = delta_V_cap
    df["BB Delta V Total"] = df["BB Delta V"] + df["BB Delta V Cap"]

    df["BB cumulative Delta V"] = df["BB Delta V"].cumsum()
    df["BB cumulative Delta V Cap"] = df["BB Delta V Cap"].cumsum()
    df["BB cumulative Delta V Total"] = df["BB Delta V Total"].cumsum()
    return df

def run_trading_strategies():
    df = combined_df()

    df = MACD(df)
    df = mean_reversion_bollinger_bands(df)
    return df
    

if __name__ == "__main__":
    df = run_trading_strategies()

    #MACD Daily 
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["MACD Delta V"], label="MACD ΔV")
    plt.plot(df.index, df["MACD Delta V Cap"], label="MACD ΔV Cap")
    plt.plot(df.index, df["MACD Delta V Total"], label="MACD ΔV Total")
    plt.title("MACD Strategy: Daily Changes")
    plt.legend()
    plt.tight_layout()
    plt.savefig("MACD Strategy: Daily Changes.png")

    # Bollinger daily
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["BB Delta V"], label="Bollinger Bands  ΔV")
    plt.plot(df.index, df["BB Delta V Cap"], label="Bollinger Bands  ΔV Cap")
    plt.plot(df.index, df["BB Delta V Total"], label="Bollinger Bands  ΔV Total")
    plt.title("Bollinger Mean Reversion: Daily Changes")
    plt.legend()
    plt.tight_layout()
    plt.savefig("Bollinger Mean Reversion: Daily Changes.png")

    # MACD cumulative
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["MACD cumulative Delta V"], label="Cumulative MACD ΔV")
    plt.plot(df.index, df["MACD cumulative Delta V Cap"], label="Cumulative MACD ΔV_cap")
    plt.plot(df.index, df["MACD cumulative Delta V Total"], label="Cumulative MACD ΔV_total")
    plt.title("MACD Strategy: Cumulative Changes")
    plt.legend()
    plt.tight_layout()
    plt.savefig("MACD Strategy: Cumulative Changes.png")

    # Bollinger cumulative
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["BB cumulative Delta V"], label="Bollinger Bands Cumulative ΔV")
    plt.plot(df.index, df["BB cumulative Delta V Cap"], label="Bollinger Bands Cumulative ΔV_cap")
    plt.plot(df.index, df["BB cumulative Delta V Total"], label="Bollinger Bands Cumulative ΔV_total")
    plt.title("Bollinger Mean Reversion: Cumulative Changes")
    plt.legend()
    plt.tight_layout()
    plt.savefig("Bollinger Mean Reversion: Cumulative Changes.png")

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["BB V"], label = "Bollinger Bands Performance")
    plt.plot(df.index, df["MACD V"], label = "MACD Performance")
    plt.title("Overall Performance of both Trading Strategies")
    plt.legend()
    plt.tight_layout()
    plt.savefig("Overall Performance of both Trading Strategies.png")