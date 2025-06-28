import fetch from 'node-fetch';
import { RSI, MACD } from 'technicalindicators';
import OpenAI from 'openai';

function simulateSeries(price, std) {
  return Array.from({ length: 100 }, () =>
    price * (1 + (Math.random() - 0.5) * std)
  );
}

export async function POST(req) {
  try {
    const body = await req.json();
    const { symbol = 'BTCUSD', question = '' } = body || {};
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
    if (!price) return Response.json({ error: 'Could not fetch price data for indicators.' }, { status: 500 });

    const closes = simulateSeries(price, std);
    const rsiArr = RSI.calculate({ values: closes, period: 14 });
    const macdArr = MACD.calculate({
      values: closes,
      fastPeriod: 12,
      slowPeriod: 26,
      signalPeriod: 9,
      SimpleMAOscillator: false,
      SimpleMASignal: false,
    });
    const rsi = rsiArr[rsiArr.length - 1];
    const macd = macdArr.length ? macdArr[macdArr.length - 1].MACD - macdArr[macdArr.length - 1].signal : 0;
    const support = Math.min(...closes);
    const resistance = Math.max(...closes);
    const last_price = closes[closes.length - 1];

    const prompt = `
You are a professional trading assistant. Analyze ${symbol} based on the following:
Current Price: ${last_price.toFixed(5)}
RSI: ${rsi.toFixed(2)}
MACD: ${macd.toFixed(2)}
Support: ${support.toFixed(2)}
Resistance: ${resistance.toFixed(2)}
User Question: ${question}
Give clear advice (Buy, Sell, or Wait) and explain your reasoning in 1-2 lines. 
Include a sample trading plan (entry, stop-loss, take-profit), and for stop-loss and take-profit, also provide the distance in pips. 
After your advice, add a brief explanation of which indicators or patterns (e.g., RSI, MACD, support/resistance, price action) were most influential in your recommendation, and why.
`;

    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        { role: "system", content: "You are a trading expert." },
        { role: "user", content: prompt }
      ]
    });

    const ai_advice = completion.choices[0].message.content;

    return Response.json({
      symbol,
      question,
      advice: ai_advice,
      indicators: {
        price: last_price,
        rsi,
        macd,
        support,
        resistance
      }
    });
  } catch (e) {
    return Response.json({ error: e.message }, { status: 500 });
  }
}