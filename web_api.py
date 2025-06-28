from flask import Flask, request, jsonify
import requests
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

def get_btcusd_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    r = requests.get(url, timeout=10)
    data = r.json()
    if 'price' in data:
        return float(data['price'])
    return None

def get_eurusd_price():
    url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
    r = requests.get(url, timeout=10)
    data = r.json()
    if 'rates' in data and 'USD' in data['rates']:
        return float(data['rates']['USD'])
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

@app.route('/price')
def price():
    symbol = request.args.get('symbol', 'BTCUSD').upper()
    if symbol == 'BTCUSD':
        price = get_btcusd_price()
    elif symbol == 'EURUSD':
        price = get_eurusd_price()
    else:
        return jsonify({'error': 'Unsupported symbol'}), 400
    if price is not None:
        return jsonify({'symbol': symbol, 'price': price})
    else:
        return jsonify({'error': 'Could not fetch price'}), 500

@app.route('/rsi')
def rsi():
    symbol = request.args.get('symbol', 'BTCUSD').upper()
    closes = get_price_series(symbol)
    if closes is not None:
        rsi_val = float(RSIIndicator(closes).rsi().iloc[-1])
        return jsonify({'symbol': symbol, 'rsi': rsi_val})
    else:
        return jsonify({'error': 'Could not compute RSI'}), 500

@app.route('/advice', methods=['POST'])
def advice():
    import openai
    from dotenv import load_dotenv
    load_dotenv()
    data = request.get_json()
    symbol = data.get('symbol', 'BTCUSD').upper()
    question = data.get('question', '')

    closes = get_price_series(symbol)
    if closes is None:
        return jsonify({'error': 'Could not fetch price data for indicators.'}), 500

    rsi_val = float(RSIIndicator(closes).rsi().iloc[-1])
    macd_val = float(MACD(closes).macd_diff().iloc[-1])
    support = float(closes.min())
    resistance = float(closes.max())
    last_price = float(closes.iloc[-1])

    # Build prompt for OpenAI
    prompt = (
        f"You are a professional trading assistant. Analyze {symbol} based on the following:\n"
        f"Current Price: {last_price:.5f}\n"
        f"RSI: {rsi_val:.2f}\n"
        f"MACD: {macd_val:.2f}\n"
        f"Support: {support:.2f}\n"
        f"Resistance: {resistance:.2f}\n"
        f"User Question: {question}\n"
        "Give clear advice (Buy, Sell, or Wait) and explain your reasoning in 1-2 lines. "
        "Include a sample trading plan (entry, stop-loss, take-profit), and for stop-loss and take-profit, also provide the distance in pips. "
        "After your advice, add a brief explanation of which indicators or patterns (e.g., RSI, MACD, support/resistance, price action) were most influential in your recommendation, and why."
    )

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        return jsonify({
            'error': 'OpenAI API key not set in .env. Please add OPENAI_API_KEY to your .env file.'
        }), 500

    openai.api_key = openai_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a trading expert."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_advice = response.choices[0].message['content']
    except Exception as e:
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500

    return jsonify({
        'symbol': symbol,
        'question': question,
        'advice': ai_advice,
        'indicators': {
            'price': last_price,
            'rsi': rsi_val,
            'macd': macd_val,
            'support': support,
            'resistance': resistance
        }
    })

@app.route('/')
def index():
    return jsonify({'message': 'Trading Assistant API is running.'})

if __name__ == '__main__':
    app.run(debug=True)