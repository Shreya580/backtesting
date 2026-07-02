"""Data layer — fetch historical OHLCV price data."""
import yfinance as yf


def get_data(ticker="AAPL", period="5y"):
    data = yf.download(ticker, period=period, interval="1d", auto_adjust=True)
    data.columns = data.columns.get_level_values(0)   # flatten MultiIndex
    return data