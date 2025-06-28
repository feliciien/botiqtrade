from utils import get_btcusd_price, get_eurusd_price
import json

def handler(request):
    try:
        symbol = request.args.get('symbol', 'BTCUSD').upper()
        if symbol == 'BTCUSD':
            price = get_btcusd_price()
        elif symbol == 'EURUSD':
            price = get_eurusd_price()
        else:
            return (
                json.dumps({'error': 'Unsupported symbol'}),
                400,
                {'Content-Type': 'application/json'}
            )
        if price is not None:
            return (
                json.dumps({'symbol': symbol, 'price': price}),
                200,
                {'Content-Type': 'application/json'}
            )
        else:
            return (
                json.dumps({'error': 'Could not fetch price'}),
                500,
                {'Content-Type': 'application/json'}
            )
    except Exception as e:
        print("API ERROR:", str(e))
        return (
            json.dumps({'error': f'Exception: {str(e)}'}),
            500,
            {'Content-Type': 'application/json'}
        )