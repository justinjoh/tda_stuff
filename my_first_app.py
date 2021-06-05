"""
based on https://tda-api.readthedocs.io/en/latest/example.html
try:
>> python3 my_first_app.py AAPL plot
>> python3 my_first_app.py AAPL backtest
"""
import datetime
import sys
import random

from utils import (
    PERIOD_TYPE,
    PERIOD,
    FREQUENCY_TYPE,
    FREQUENCY,
    WEEKDAYS,
    get_price_history
)
import pandas as pd
import mplfinance as mpf


def dummy_backtest(ticker: str):
    """
    Using this to test the most basic possible aspects of backtesting
    e.g. checking prices at certain dates, working with some version of start/end capital, etc.
    """
    candles = get_price_history(
        ticker,
        PERIOD_TYPE.YEAR,
        PERIOD.FIVE_YEARS,
        FREQUENCY_TYPE.DAILY,
        FREQUENCY.DAILY
    )
    start_capital = 100
    day_start_capital = start_capital  # dollars
    # on every Monday: buy at open, sell at close
    total = 0
    for candle in candles:
        timestamp = candle['datetime']
        dt = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
        if dt.weekday() != 0:
            continue
        open = candle['open']
        close = candle['close']
        day_end_capital = day_start_capital * (close / open)
        day_start_capital = day_end_capital
    print('total from dummy strategy:', day_end_capital)

    # what would buy-and-hold have given?
    start_candle = candles[0]
    start_price = start_candle['open']
    end_candle = candles[-1]
    end_price = end_candle['close']
    buy_and_hold_val = start_capital * (end_price / start_price)
    print(f'total from just buying and holding: {buy_and_hold_val}')

        


def plot_candles_ticker(ticker: str):
    """
    Show history of ticker in a candle plot
    For now, period type/period and frequency type/frequency are just hardcoded
    TODO: pass hardcoded things as params
    Return None
    """
    candles = get_price_history(
        ticker,
        PERIOD_TYPE.YEAR,
        PERIOD.FIVE_YEARS,
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
        show_nontrading=True,
        warn_too_much_data=9999999,  # dumb way of suppressing warning message
    )
    return None


def main():
    args = sys.argv[1:]
    # ticker = 'AAPL'
    ticker = args[0]
    mode = args[1]
    if mode == 'plot':
        print(f'plotting {ticker}')
        plot_candles_ticker(ticker)
    elif mode == 'backtest':
        dummy_backtest(ticker)


if __name__ == '__main__':
    main()