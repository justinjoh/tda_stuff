"""
utils
...
"""
import tda
import httpx
import datetime
import atexit
import json
from enum import Enum


WEEKDAYS = {
    0: 'monday',
    1: 'tuesday',
    2: 'wednesday',
    3: 'thursday',
    4: 'friday',
    5: 'saturday',
    6: 'sunday'
}


def _get_secrets(secrets_location: str):
    """
    don't commit this stuff, ofcourse
    """
    with open(secrets_location) as handle:
        secrets_dict = json.load(handle)
    api_key = secrets_dict['API_KEY']
    redirect_uri = secrets_dict['REDIRECT_URI']
    return api_key, redirect_uri


API_KEY, REDIRECT_URI = _get_secrets("./secret_stuff.json")
TOKEN_PATH = 'ameritrade-credentials.json'
YOUR_BIRTHDAY = datetime.datetime(year=1900, month=6, day=1)
SP500_URL = "https://tda-api.readthedocs.io/en/latest/_static/sp500.txt"


def _make_webdriver():
    # Import selenium here because it's slow to import
    from selenium import webdriver

    driver = webdriver.Chrome()
    atexit.register(lambda: driver.quit())
    return driver


# Create a new client
# will designate as global/for export for now, assuming it's going to be used everywhere
CLIENT = tda.auth.easy_client(
    API_KEY,
    REDIRECT_URI,
    TOKEN_PATH,
    _make_webdriver
)


def get_fundamentals(ticker: str):
    """
    """
    r = CLIENT.search_instruments(ticker, tda.client.Client.Instrument.Projection.FUNDAMENTAL)
    assert r.status_code == httpx.codes.OK, r.raise_for_status()
    for _, f in r.json().items():
        return f['fundamental']
        # fundamentals = f['fundamental']
        # for k, v in fundamentals.items():
            # print(f'\t{k}: {v}')

# get enums for convenience
PRICE_HISTORY = tda.client.Client.PriceHistory
FREQUENCY = PRICE_HISTORY.Frequency
FREQUENCY_TYPE = PRICE_HISTORY.FrequencyType
PERIOD = PRICE_HISTORY.Period
PERIOD_TYPE = PRICE_HISTORY.PeriodType


def get_price_history(
        ticker: str, 
        period_type: PERIOD_TYPE, 
        period: PERIOD, 
        frequency_type: FREQUENCY_TYPE, 
        frequency: FREQUENCY
    ):
    """
    format of r.json()
        {
        "candles": [
            {
            "close": 0,
            "datetime": 0,
            "high": 0,
            "low": 0,
            "open": 0,
            "volume": 0
            }
        ],
        "empty": false,
        "symbol": "string"
        }
    """
    if not is_valid_history(period_type, period, frequency_type, frequency):
        raise ValueError("Period and frequency combinations do not form a valid request")
    r: httpx.Response = CLIENT.get_price_history(
        ticker, 
        period_type=period_type,
        period=period, 
        frequency_type=frequency_type, 
        frequency=frequency, 
        need_extended_hours_data=False
        )
    assert r.status_code == httpx.codes.OK, r.raise_for_status()
    dict_= r.json()
    empty = dict_['empty']
    assert(not empty)
    candles = dict_['candles']
    return candles


def is_valid_history(period_type: PERIOD_TYPE, period: PERIOD, frequency_type: FREQUENCY_TYPE, frequency: FREQUENCY):
    """
    Ensure the period/frequency combinations will form a valid request
    See Query Parameters: 
        https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory#
    """
    if period_type == PERIOD_TYPE.DAY:
        if period not in [
            PERIOD.ONE_DAY, 
            PERIOD.TWO_DAYS, 
            PERIOD.THREE_DAYS, 
            PERIOD.FOUR_DAYS, 
            PERIOD.FIVE_DAYS, 
            PERIOD.TEN_DAYS
        ]:
            return False
    elif period_type == PERIOD_TYPE.MONTH:
        if period not in [PERIOD.ONE_MONTH, PERIOD.TWO_MONTHS, PERIOD.THREE_MONTHS, PERIOD.SIX_MONTHS]:
            return False
    elif period_type == PERIOD_TYPE.YEAR:
        if period not in [
            PERIOD.ONE_YEAR, 
            PERIOD.TWO_YEARS, 
            PERIOD.THREE_YEARS, 
            PERIOD.FIVE_YEARS, 
            PERIOD.TEN_YEARS, 
            PERIOD.FIFTEEN_YEARS, 
            PERIOD.TWENTY_YEARS
        ]:
            return False
    elif period_type == PERIOD_TYPE.YEAR_TO_DATE:
        if period not in [PERIOD.YEAR_TO_DATE]:
            return False
    return True