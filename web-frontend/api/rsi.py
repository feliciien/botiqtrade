from utils import get_price_series, compute_rsi
import json

def handler(request):
    symbol = request.args.get('symbol', 'BTCUSD').upper()
    closes = get_price_series(symbol)
    if closes is not None:
        rsi_val = compute_rsi(closes)
        return (
            json.dumps({'symbol': symbol, 'rsi': rsi_val}),
            200,
            {'Content-Type': 'application/json'}
        )
    else:
        return (
            json.dumps({'error': 'Could not compute RSI'}),
            500,
            {'Content-Type': 'application/json'}
        )