# Backtesting Framework

A Python backtesting engine that simulates trading strategies on historical
stock data and reports risk-adjusted performance metrics.

## What it does

- Pulls historical OHLCV data (yfinance)
- Runs a strategy (produces buy/sell signals)
- Simulates trades day-by-day, tracking a virtual portfolio
- Computes Sharpe ratio, max drawdown, CAGR, win rate, profit factor
- Benchmarks against buy-and-hold

## Strategies

- `sma_crossover` — 50/200-day moving-average crossover
- `momentum` — buy when price is above its level N days ago

## Design

Strategies are decoupled from the engine. A strategy is any function
`data -> signal (1/-1)`. The engine simulates trades from any signal and
is strategy-agnostic. Adding a strategy = writing one function.

## Findings (AAPL, 5y)

| Metric       | SMA crossover | Momentum | Buy & hold |
| ------------ | ------------- | -------- | ---------- |
| CAGR         | -1.4%         | 6.2%     | 17.7%      |
| Sharpe       | 0.02          | 0.43     | 0.73       |
| Max drawdown | -33%          | -26%     | -33%       |

Neither strategy beats buy-and-hold on return — a demonstration of why
well-known signals rarely retain edge, and why lookahead bias, transaction
costs, and benchmarking matter.

## Run

\`\`\`bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backtest.py
\`\`\`
