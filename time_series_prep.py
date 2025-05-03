import yfinance as yf 
import datetime
import matplotlib.pyplot as plt
import pandas as pd

def download_sptl(start, end):

    sptl_close = yf.download("SPTL", start, end)["Close"]
    return sptl_close

def get_effr(start, end):
    effr = pd.read_excel("effr.xlsx",  engine="openpyxl")[["Effective Date", "Rate (%)"]].iloc[::-1]
    effr["Effective Date"] = pd.to_datetime(effr["Effective Date"])
    effr.rename(columns = {"Rate (%)": "EFFR Annual Rate", "Effective Date": "Date"}, inplace=True)
    effr.set_index("Date", drop=True, inplace = True)
    effr["EFFR Daily Rate"] = effr["EFFR Annual Rate"] * (1/252)
    return effr

def plot_all(df):
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    # Plot SPTL Return Time Series
    axes[0].plot(df.index, df["SPTL"], label="SPTL")
    axes[0].set_title("SPTL Price Time Series")
    axes[0].legend()
    
    # Plot EFFR Annual Rate
    axes[1].plot(df.index, df["EFFR Daily Rate"], color='orange', label="EFFR")
    axes[1].set_title("Daily EFFR")
    axes[1].legend()
    
    # Plot Daily Excess Return
    axes[2].plot(df.index, df["Daily Excess Return"], color='green', label="Daily Excess Return")
    axes[2].set_title("Excess Return per Unit of SPTL")
    axes[2].legend()
    
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig("time_series_prep_figs.png")

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["SPTL"], label="SPTL")
    plt.title("SPTL Price Time Series")
    plt.legend()
    plt.savefig("sptl_price_time_series.png")

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["EFFR Daily Rate"], color='orange', label="EFFR")
    plt.title("Daily EFFR")
    plt.legend()
    plt.savefig("daily_effr.png")

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["Daily Excess Return"], color='green', label="Daily Excess Return")
    plt.title("Excess Return per Unit of SPTL")
    plt.legend()
    plt.savefig("excess_returns.png")

def combined_df():
    start = datetime.datetime(2023, 1, 1)
    end = datetime.datetime(2023, 12, 31)
    sptl = download_sptl(start, end)
    effr = get_effr(start, end)
    df = pd.concat([sptl, effr], axis = 1).fillna(method='ffill')
    df["Daily Excess Return"] = sptl["SPTL"].diff()/sptl["SPTL"].shift(1) - effr["EFFR Daily Rate"].shift(1)
    return df
    

if __name__ == "__main__":
    df = combined_df()
    print(df)
    plot_all(df)