import requests
import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

def get_btcusd_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if 'price' in data:
            return float(data['price'])
        print("Binance API response (no price):", data)
    except Exception as e:
        print("Error fetching BTCUSD price:", str(e))
    return None

def get_eurusd_price():
    url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if 'rates' in data and 'USD' in data['rates']:
            return float(data['rates']['USD'])
        print("Frankfurter API response (no USD):", data)
    except Exception as e:
        print("Error fetching EURUSD price:", str(e))
    return None

def get_price_series(symbol):
    if symbol == 'BTCUSD':
        price = get_btcusd_price()
        if price is not None:
            closes = [price * (1 + n) for n in np.random.normal(0, 0.002, 100)]
            return pd.Series(closes)
    elif symbol == 'EURUSD':
        price = get_eurusd_price()
        if price is not None:
            closes = [price * (1 + n) for n in np.random.normal(0, 0.0002, 100)]
            return pd.Series(closes)
    return None

def compute_rsi(series):
    return float(RSIIndicator(series).rsi().iloc[-1])

def compute_macd(series):
    return float(MACD(series).macd_diff().iloc[-1])