import fetch from 'node-fetch';
import { RSI } from 'technicalindicators';

function simulateSeries(price, std) {
  return Array.from({ length: 100 }, () =>
    price * (1 + (Math.random() - 0.5) * std)
  );
}

export async function GET(req) {
  const { searchParams } = new URL(req.url);
  const symbol = (searchParams.get('symbol') || 'BTCUSD').toUpperCase();
  try {
    let price = null;
    let std = 0.002;
    if (symbol === 'BTCUSD') {
      const r = await fetch('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT');
      const data = await r.json();
      if (data.price) price = parseFloat(data.price);
      std = 0.002;
    } else if (symbol === 'EURUSD') {
      const r = await fetch('https://api.frankfurter.app/latest?from=EUR&to=USD');
      const data = await r.json();
      if (data.rates && data.rates.USD) price = parseFloat(data.rates.USD);
      std = 0.0002;
    } else {
      return Response.json({ error: 'Unsupported symbol' }, { status: 400 });
    }
    if (!price) return Response.json({ error: 'Could not fetch price' }, { status: 500 });

    const closes = simulateSeries(price, std);
    const rsiArr = RSI.calculate({ values: closes, period: 14 });
    const rsi = rsiArr[rsiArr.length - 1];

    return Response.json({ symbol, rsi });
  } catch (e) {
    return Response.json({ error: e.message }, { status: 500 });
  }
}