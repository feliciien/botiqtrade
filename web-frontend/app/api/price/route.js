import fetch from 'node-fetch';

export async function GET(req) {
  const { searchParams } = new URL(req.url);
  const symbol = (searchParams.get('symbol') || 'BTCUSD').toUpperCase();
  try {
    if (symbol === 'BTCUSD') {
      const r = await fetch('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT');
      const data = await r.json();
      if (data.price) {
        return Response.json({ symbol, price: parseFloat(data.price) });
      } else {
        return Response.json({ error: 'Could not fetch BTCUSD price', details: data }, { status: 500 });
      }
    } else if (symbol === 'EURUSD') {
      const r = await fetch('https://api.frankfurter.app/latest?from=EUR&to=USD');
      const data = await r.json();
      if (data.rates && data.rates.USD) {
        return Response.json({ symbol, price: parseFloat(data.rates.USD) });
      } else {
        return Response.json({ error: 'Could not fetch EURUSD price', details: data }, { status: 500 });
      }
    } else {
      return Response.json({ error: 'Unsupported symbol' }, { status: 400 });
    }
  } catch (e) {
    return Response.json({ error: e.message }, { status: 500 });
  }
}