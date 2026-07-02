"""
Day 4 — Risk metrics.
Compute total return, CAGR, Sharpe, max drawdown, win rate, profit factor
for BOTH the strategy and the buy-and-hold benchmark, side by side.
"""

import numpy as np
import yfinance as yf

# --- Rebuild Days 1-3 (data -> signal -> simulation) ------------------------
data = yf.download("AAPL", period="5y", interval="1d", auto_adjust=True)
data.columns = data.columns.get_level_values(0)

data["SMA50"] = data["Close"].rolling(window=50).mean()
data["SMA200"] = data["Close"].rolling(window=200).mean()
data["signal"] = 0
data.loc[data["SMA50"] > data["SMA200"], "signal"] = 1
data.loc[data["SMA50"] <= data["SMA200"], "signal"] = -1

STARTING_CASH = 100_000
COST_PER_TRADE = 0.0

cash, shares, buy_price = STARTING_CASH, 0, None
equity_curve, trades = [], []
prices = data["Close"].values
signals = data["signal"].values

for i in range(len(data)):
    price = prices[i]
    sig = signals[i - 1] if i > 0 else 0
    if sig == 1 and shares == 0:
        shares = int(cash // price)
        cash = cash - shares * price - COST_PER_TRADE
        buy_price = price
    elif sig == -1 and shares > 0:
        cash = cash + shares * price - COST_PER_TRADE
        trades.append((price - buy_price) * shares)
        shares = 0
        buy_price = None
    equity_curve.append(cash + shares * price)

data["equity"] = equity_curve
bh_shares = STARTING_CASH // prices[0]
data["benchmark"] = bh_shares * data["Close"]


# --- Metric functions --------------------------------------------------------
def total_return(equity):
    return equity[-1] / equity[0] - 1

def cagr(equity):
    years = len(equity) / 252
    return (equity[-1] / equity[0]) ** (1 / years) - 1

def sharpe(equity):
    equity = np.asarray(equity, dtype=float)
    daily_returns = equity[1:] / equity[:-1] - 1     # pct change day to day
    if daily_returns.std() == 0:
        return 0.0
    return (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)

def max_drawdown(equity):
    equity = np.asarray(equity, dtype=float)
    peak = np.maximum.accumulate(equity)             # running max
    drawdown = (equity - peak) / peak
    return drawdown.min()                            # most negative

def win_rate(trades):
    if not trades:
        return None
    return sum(1 for t in trades if t > 0) / len(trades)

def profit_factor(trades):
    gains = sum(t for t in trades if t > 0)
    losses = abs(sum(t for t in trades if t < 0))
    if losses == 0:
        return None
    return gains / losses


# --- Report ------------------------------------------------------------------
strat = np.asarray(equity_curve, dtype=float)
bench = data["benchmark"].values

print("=" * 55)
print(f"{'METRIC':<20}{'STRATEGY':>15}{'BUY & HOLD':>15}")
print("=" * 55)
print(f"{'Total return':<20}{total_return(strat)*100:>14.2f}%{total_return(bench)*100:>14.2f}%")
print(f"{'CAGR':<20}{cagr(strat)*100:>14.2f}%{cagr(bench)*100:>14.2f}%")
print(f"{'Sharpe ratio':<20}{sharpe(strat):>15.2f}{sharpe(bench):>15.2f}")
print(f"{'Max drawdown':<20}{max_drawdown(strat)*100:>14.2f}%{max_drawdown(bench)*100:>14.2f}%")
print("=" * 55)
print(f"Trades: {len(trades)}   Win rate: {win_rate(trades)}   "
      f"Profit factor: {profit_factor(trades)}")
print("=" * 55)