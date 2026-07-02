"""Metrics — risk-adjusted performance measures computed from an equity curve."""
import numpy as np


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