import os
import json
from utils import get_price_series, compute_rsi, compute_macd
from dotenv import load_dotenv
import openai

load_dotenv()

def handler(request):
    if request.method != "POST":
        return (
            json.dumps({'error': 'Method not allowed'}),
            405,
            {'Content-Type': 'application/json'}
        )
    try:
        data = request.json
        symbol = data.get('symbol', 'BTCUSD').upper()
        question = data.get('question', '')

        closes = get_price_series(symbol)
        if closes is None:
            return (
                json.dumps({'error': 'Could not fetch price data for indicators.'}),
                500,
                {'Content-Type': 'application/json'}
            )

        rsi_val = compute_rsi(closes)
        macd_val = compute_macd(closes)
        support = float(closes.min())
        resistance = float(closes.max())
        last_price = float(closes.iloc[-1])

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
            return (
                json.dumps({'error': 'OpenAI API key not set in .env. Please add OPENAI_API_KEY to your .env file.'}),
                500,
                {'Content-Type': 'application/json'}
            )

        openai.api_key = openai_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a trading expert."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_advice = response.choices[0].message['content']

        return (
            json.dumps({
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
            }),
            200,
            {'Content-Type': 'application/json'}
        )
    except Exception as e:
        return (
            json.dumps({'error': f'OpenAI API error: {str(e)}'}),
            500,
            {'Content-Type': 'application/json'}
        )