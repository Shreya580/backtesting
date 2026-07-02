"""Strategies — each takes price data, returns a signal Series of 1 / -1."""
import pandas as pd


def sma_crossover(data, fast=50, slow=200):
    fast_ma = data["Close"].rolling(fast).mean()
    slow_ma = data["Close"].rolling(slow).mean()
    signal = pd.Series(0, index=data.index)
    signal[fast_ma > slow_ma] = 1
    signal[fast_ma <= slow_ma] = -1
    return signal


def momentum(data, lookback=20):
    past = data["Close"].shift(lookback)
    signal = pd.Series(0, index=data.index)
    signal[data["Close"] > past] = 1
    signal[data["Close"] <= past] = -1
    return signal


# Registry: pick a strategy by name (used by the API later).
STRATEGIES = {
    "sma_crossover": sma_crossover,
    "momentum": momentum,
}