"""Engine — simulates trades from ANY signal. Strategy-agnostic."""
import numpy as np


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