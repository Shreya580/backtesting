"""Run a backtest from the command line."""
from backtest import get_data, STRATEGIES, run_backtest, metrics

data = get_data("AAPL", "5y")

strategy_name = "momentum"                 # change to "sma_crossover" to swap
signal = STRATEGIES[strategy_name](data)
equity, trades = run_backtest(data, signal)

print(f"Strategy: {strategy_name}   Trades: {len(trades)}")
for name, value in metrics(equity, trades).items():
    print(f"  {name:15}: {value}")