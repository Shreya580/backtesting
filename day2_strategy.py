"""
Day 2 — Strategy layer.
Goal: compute 50-day & 200-day SMA, generate buy/sell signal, plot to verify.
No trades yet — just decide IN (1) or OUT (-1) for each day.
"""

import yfinance as yf
import matplotlib.pyplot as plt

# --- Step 1: get data (same as Day 1) ---------------------------------------
data = yf.download("AAPL", period="5y", interval="1d", auto_adjust=True)

# Flatten the MultiIndex columns so data['Close'] gives numbers directly.
data.columns = data.columns.get_level_values(0)

# --- Step 2: compute the two moving averages --------------------------------
# .rolling(window=N) makes a sliding window of N rows.
# .mean() averages each window. Result: one SMA value per day.
data["SMA50"] = data["Close"].rolling(window=50).mean()
data["SMA200"] = data["Close"].rolling(window=200).mean()

# --- Step 3: generate the signal --------------------------------------------
# Where SMA50 > SMA200 -> 1 (be in). Otherwise -> -1 (be out).
data["signal"] = 0                                  # default
data.loc[data["SMA50"] > data["SMA200"], "signal"] = 1
data.loc[data["SMA50"] <= data["SMA200"], "signal"] = -1

# --- Step 4: inspect ---------------------------------------------------------
print("Rows where SMA200 is still NaN (not enough history):",
      data["SMA200"].isna().sum())

print("\nSignal counts (how many days IN vs OUT):")
print(data["signal"].value_counts())

print("\nSample rows (day 200 onward, once both SMAs exist):")
print(data[["Close", "SMA50", "SMA200", "signal"]].iloc[200:210])

# --- Step 5: plot ------------------------------------------------------------
plt.figure(figsize=(14, 7))
plt.plot(data.index, data["Close"], label="Close", alpha=0.5)
plt.plot(data.index, data["SMA50"], label="SMA50")
plt.plot(data.index, data["SMA200"], label="SMA200")
plt.title("AAPL — Close with 50 & 200 day moving averages")
plt.legend()
plt.savefig("day2_plot.png", dpi=100)
print("\nPlot saved to day2_plot.png")
plt.show()