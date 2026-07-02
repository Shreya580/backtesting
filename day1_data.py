"""
Day 1 — Data layer.
Goal: pull AAPL daily price history, load into pandas, inspect it.
Nothing else. Understand the data before building anything on top.
"""

import yfinance as yf

# --- Step 1: download data ---------------------------------------------------
# yf.download() fetches historical OHLCV from Yahoo Finance.
#   ticker   = which stock ("AAPL" = Apple)
#   period   = how far back ("5y" = 5 years)
#   interval = bar size ("1d" = one row per trading day)
# auto_adjust=True adjusts prices for stock splits & dividends so the series
# is continuous and honest (a split would otherwise look like a 50% crash).
data = yf.download("AAPL", period="5y", interval="1d", auto_adjust=True)

# --- Step 2: inspect ---------------------------------------------------------
print("=" * 60)
print("SHAPE (rows, columns):", data.shape)
print("=" * 60)

print("\nCOLUMNS:", list(data.columns))

print("\nDATE RANGE:", data.index.min(), "->", data.index.max())

print("\nFIRST 5 ROWS:")
print(data.head())

print("\nLAST 5 ROWS:")
print(data.tail())

print("\nMISSING VALUES per column:")
print(data.isna().sum())

print("\nSTATS (count/mean/min/max etc.):")
print(data.describe())
