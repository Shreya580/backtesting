"""Backtesting framework — strategy-agnostic engine + risk metrics."""
from .data import get_data
from .strategies import STRATEGIES, sma_crossover, momentum
from .engine import run_backtest
from .metrics import metrics