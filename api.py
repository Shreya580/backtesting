"""HTTP API — exposes the backtest engine as a web endpoint for the frontend."""
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backtest import get_data, STRATEGIES, run_backtest, buy_and_hold, metrics

app = FastAPI(title="Backtesting API")

# Allow the React dev server (different port) to call this API. See note below.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # dev only; tighten for production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/strategies")
def list_strategies():
    """Return the names of available strategies (feeds the UI dropdown)."""
    return {"strategies": list(STRATEGIES.keys())}


@app.get("/backtest")
def backtest(ticker: str = "AAPL", strategy: str = "momentum", period: str = "5y"):
    """Run a backtest and return the equity curve, benchmark, and metrics."""
    if strategy not in STRATEGIES:
        return {"error": f"Unknown strategy '{strategy}'. "
                         f"Available: {list(STRATEGIES.keys())}"}

    data = get_data(ticker, period)
    signal = STRATEGIES[strategy](data)
    equity, trades = run_backtest(data, signal)
    benchmark = buy_and_hold(data)
    m = metrics(equity, trades)

    return {
        "ticker": ticker,
        "strategy": strategy,
        "dates": [d.strftime("%Y-%m-%d") for d in data.index],
        "equity": equity.tolist(),
        "benchmark": benchmark.tolist(),
        "metrics": {k: (None if v is None else float(v)) for k, v in m.items()},
    }