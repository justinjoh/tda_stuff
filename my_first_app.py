"""
based on https://tda-api.readthedocs.io/en/latest/example.html
"""
import datetime

from utils import (
    # get_fundamentals, 
    PERIOD_TYPE,
    PERIOD,
    FREQUENCY_TYPE,
    FREQUENCY,
    get_price_history
)
import pandas as pd
import mplfinance as mpf
# import numpy as np
# import matplotlib.pyplot as plt


def plot_candles_ticker(ticker: str):
    """
    Show history of ticker in a candle plot
    Return None
    """
    candles = get_price_history(
        ticker,
        PERIOD_TYPE.YEAR,
        # PERIOD.ONE_YEAR,
        PERIOD.FIFTEEN_YEARS,
        FREQUENCY_TYPE.DAILY,
        FREQUENCY.DAILY
        )
    for c in candles:
        timestamp = c['datetime']
        my_dt = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
        pd_dt = pd.to_datetime(my_dt)
        c['datetime'] = pd_dt
    
    df = pd.DataFrame.from_records(candles)
    df.index = pd.DatetimeIndex(df['datetime'])
    df.index.name = 'datetime'
    mpf.plot(
        df, 
        type='candle', 
        style='charles',
        title=ticker,
        mav=(3, 6, 9), 
        volume=True, 
        show_nontrading=True
    )
    return None


def main():
    ticker = 'AAPL'
    print(f'plotting {ticker}')
    plot_candles_ticker(ticker)


if __name__ == '__main__':
    main()