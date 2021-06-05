"""
based on https://tda-api.readthedocs.io/en/latest/example.html
"""
import datetime

from utils import get_fundamentals, get_price_history
import pandas as pd
import mplfinance as mpf
# import numpy as np
# import matplotlib.pyplot as plt


def plot_candles_ticker(ticker: str):
    """
    Show history of ticker in a candle plot
    Return None
    """
    candles = get_price_history(ticker)
    for c in candles:
        timestamp = c['datetime']
        my_dt = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
        pd_dt = pd.to_datetime(my_dt)
        c['datetime'] = pd_dt
    
    df = pd.DataFrame.from_records(candles)
    df.index = pd.DatetimeIndex(df['datetime'])
    df.index.name = 'datetime'
    mpf.plot(df, type='candle', mav=4, volume=True, show_nontrading=True)
    return None


def main():
    plot_candles_ticker('AAPL')


if __name__ == '__main__':
    main()