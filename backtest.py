"""
Backtesting engine — strategy-agnostic.
A STRATEGY is a function: data -> signal (Series of 1/-1).
The ENGINE simulates trades from any signal and computes metrics.
Add a new strategy = write one new function. Engine never changes.
"""

import numpy as np
import pandas as pd
import yfinance as yf


# =============================================================================
# DATA
# =============================================================================
def get_data(ticker="AAPL", period="5y"):
    data = yf.download(ticker, period=period, interval="1d", auto_adjust=True)
    data.columns = data.columns.get_level_values(0)   # flatten MultiIndex
    return data


# =============================================================================
# STRATEGIES  — each takes `data`, returns a signal Series of 1 / -1
# =============================================================================
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


# A registry so we can pick a strategy by name (handy for the API later).
STRATEGIES = {
    "sma_crossover": sma_crossover,
    "momentum": momentum,
}


# =============================================================================
# ENGINE  — simulates trades from ANY signal. Strategy-agnostic.
# =============================================================================
def run_backtest(data, signal, starting_cash=100_000, cost_per_trade=0.0):
    cash, shares, buy_price = starting_cash, 0, None
    equity_curve, trades = [], []
    prices = data["Close"].values
    sig = signal.values

    for i in range(len(data)):
        price = prices[i]
        s = sig[i - 1] if i > 0 else 0           # yesterday's signal: no lookahead
        if s == 1 and shares == 0:
            shares = int(cash // price)
            cash = cash - shares * price - cost_per_trade
            buy_price = price
        elif s == -1 and shares > 0:
            cash = cash + shares * price - cost_per_trade
            trades.append((price - buy_price) * shares)
            shares = 0
            buy_price = None
        equity_curve.append(cash + shares * price)

    return np.array(equity_curve, dtype=float), trades


# =============================================================================
# METRICS
# =============================================================================
def total_return(equity):
    return equity[-1] / equity[0] - 1

def cagr(equity):
    years = len(equity) / 252
    return (equity[-1] / equity[0]) ** (1 / years) - 1

def sharpe(equity):
    r = equity[1:] / equity[:-1] - 1
    return 0.0 if r.std() == 0 else (r.mean() / r.std()) * np.sqrt(252)

def max_drawdown(equity):
    peak = np.maximum.accumulate(equity)
    return ((equity - peak) / peak).min()

def win_rate(trades):
    return None if not trades else sum(t > 0 for t in trades) / len(trades)

def profit_factor(trades):
    gains = sum(t for t in trades if t > 0)
    losses = abs(sum(t for t in trades if t < 0))
    return None if losses == 0 else gains / losses

def metrics(equity, trades):
    return {
        "total_return": total_return(equity),
        "cagr": cagr(equity),
        "sharpe": sharpe(equity),
        "max_drawdown": max_drawdown(equity),
        "win_rate": win_rate(trades),
        "profit_factor": profit_factor(trades),
    }


# =============================================================================
# RUN  — glue it together. Pick a strategy by name, print metrics.
# =============================================================================
if __name__ == "__main__":
    data = get_data("AAPL", "5y")

    strategy_name = "momentum"          # <-- change this to "momentum" to swap
    strategy_fn = STRATEGIES[strategy_name]
    signal = strategy_fn(data)

    equity, trades = run_backtest(data, signal)
    m = metrics(equity, trades)

    print(f"Strategy: {strategy_name}   Trades: {len(trades)}")
    for name, value in m.items():
        print(f"  {name:15}: {value}")