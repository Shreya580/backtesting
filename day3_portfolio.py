"""
Day 3 — Portfolio simulation.
Turn the Day-2 signal into real simulated trades. Track cash, shares, equity.
Produce the equity curve + a buy-and-hold benchmark to compare against.
"""

import yfinance as yf
import matplotlib.pyplot as plt

# --- Rebuild Day 1 + Day 2 (data -> SMAs -> signal) -------------------------
data = yf.download("AAPL", period="5y", interval="1d", auto_adjust=True)
data.columns = data.columns.get_level_values(0)

data["SMA50"] = data["Close"].rolling(window=50).mean()
data["SMA200"] = data["Close"].rolling(window=200).mean()

data["signal"] = 0
data.loc[data["SMA50"] > data["SMA200"], "signal"] = 1
data.loc[data["SMA50"] <= data["SMA200"], "signal"] = -1

# --- Simulation settings -----------------------------------------------------
STARTING_CASH = 100_000
COST_PER_TRADE = 0.0          # dollars per buy or sell. 0 for now.

# --- Portfolio state ---------------------------------------------------------
cash = STARTING_CASH
shares = 0
equity_curve = []             # account value each day
trades = []                   # record each completed round-trip's P/L

buy_price = None              # price we last bought at (to compute trade P/L)

# Pull raw arrays for the loop.
prices = data["Close"].values
signals = data["signal"].values

# --- The simulation loop -----------------------------------------------------
for i in range(len(data)):
    price = prices[i]

    # Act on YESTERDAY'S signal to avoid lookahead. Day 0 has no yesterday.
    sig = signals[i - 1] if i > 0 else 0

    # BUY: signal says IN, and we're currently in cash.
    if sig == 1 and shares == 0:
        shares = int(cash // price)        # whole shares only
        cost = shares * price
        cash = cash - cost - COST_PER_TRADE
        buy_price = price

    # SELL: signal says OUT, and we're currently holding shares.
    elif sig == -1 and shares > 0:
        proceeds = shares * price
        cash = cash + proceeds - COST_PER_TRADE
        # record this round-trip's profit/loss
        trades.append((price - buy_price) * shares)
        shares = 0
        buy_price = None

    # Record total account value for this day.
    equity_curve.append(cash + shares * price)

# Store the curve back on the DataFrame for plotting.
data["equity"] = equity_curve

# --- Benchmark: buy-and-hold -------------------------------------------------
# Buy as many shares as $100k allows on day 1, hold to the end.
bh_shares = STARTING_CASH // prices[0]
data["benchmark"] = bh_shares * data["Close"]

# --- Results -----------------------------------------------------------------
final_strategy = equity_curve[-1]
final_benchmark = data["benchmark"].iloc[-1]

print("=" * 55)
print(f"Starting cash:        ${STARTING_CASH:,.2f}")
print(f"Strategy final value: ${final_strategy:,.2f}")
print(f"Buy & hold final:     ${final_benchmark:,.2f}")
print("=" * 55)
print(f"Strategy return:  {(final_strategy/STARTING_CASH - 1)*100:6.2f}%")
print(f"Buy & hold return:{(final_benchmark/STARTING_CASH - 1)*100:6.2f}%")
print(f"Number of completed trades: {len(trades)}")
wins = sum(1 for t in trades if t > 0)
print(f"Winning trades: {wins} / {len(trades)}")

# --- Plot both equity curves -------------------------------------------------
plt.figure(figsize=(14, 7))
plt.plot(data.index, data["equity"], label="SMA crossover strategy")
plt.plot(data.index, data["benchmark"], label="Buy & hold", alpha=0.7)
plt.title("Equity curve: strategy vs buy-and-hold ($100k start)")
plt.ylabel("Account value ($)")
plt.legend()
plt.savefig("day3_equity.png", dpi=100)
print("\nPlot saved to day3_equity.png")
plt.show()