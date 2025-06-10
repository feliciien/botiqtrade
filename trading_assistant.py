import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import openai
import requests
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class TradingAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("EUR/USD Trading Assistant 🤖💰")
        self.root.geometry("800x600")
        
        # Configure API keys
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.exchangerate_key = os.getenv("EXCHANGERATE_API_KEY")
        
        # Store historical prices
        self.price_history = pd.DataFrame()
        
        self.setup_ui()
        
    def setup_ui(self):
        # API Key Configuration Frame
        key_frame = ttk.LabelFrame(self.root, text="API Configuration", padding="10")
        key_frame.pack(fill="x", padx=10, pady=5)
        
        if not self.openai_key:
            ttk.Label(key_frame, text="OpenAI API Key:").pack(side="left", padx=5)
            self.openai_entry = ttk.Entry(key_frame, show="*")
            self.openai_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        if not self.exchangerate_key:
            ttk.Label(key_frame, text="ExchangeRate API Key:").pack(side="left", padx=5)
            self.exchangerate_entry = ttk.Entry(key_frame, show="*")
            self.exchangerate_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Market Data Frame
        market_frame = ttk.LabelFrame(self.root, text="Market Data", padding="10")
        market_frame.pack(fill="x", padx=10, pady=5)
        
        self.price_label = ttk.Label(market_frame, text="EUR/USD: --")
        self.price_label.pack(side="left", padx=20)
        
        self.rsi_label = ttk.Label(market_frame, text="RSI: --")
        self.rsi_label.pack(side="left", padx=20)
        
        self.macd_label = ttk.Label(market_frame, text="MACD: --")
        self.macd_label.pack(side="left", padx=20)
        
        # Question Input Frame
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Ask your trading question:").pack(fill="x")
        self.question_entry = ttk.Entry(input_frame)
        self.question_entry.pack(fill="x", pady=5)
        self.question_entry.bind("<Return>", self.on_submit)
        
        submit_btn = ttk.Button(input_frame, text="Get Advice", command=self.on_submit)
        submit_btn.pack(pady=5)
        
        # Response Display
        response_frame = ttk.LabelFrame(self.root, text="Trading Advice", padding="10")
        response_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.response_text = scrolledtext.ScrolledText(response_frame, wrap=tk.WORD, height=10)
        self.response_text.pack(fill="both", expand=True)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief="sunken")
        self.status_bar.pack(fill="x", side="bottom", padx=10, pady=5)
        
        # Update market data periodically
        self.update_market_data()

    def get_eurusd_price(self):
        """Fetch EUR/USD price data from ExchangeRate API and simulate short-term data"""
        try:
            api_key = self.exchangerate_key or self.exchangerate_entry.get()
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/EUR/USD"
            r = requests.get(url)
            data = r.json()
            
            if 'result' not in data or data['result'] != 'success':
                raise Exception("Error fetching price data. Please check your ExchangeRate API key.")
                
            current_rate = data['conversion_rate']
            
            # Create simulated price data for technical analysis
            # Generate 100 data points with small random variations around the current price
            timestamps = [datetime.now() - timedelta(minutes=5*i) for i in range(100)]
            noise = np.random.normal(0, 0.0002, 100)  # Small random variations
            prices = [current_rate * (1 + n) for n in noise]
            
            df = pd.DataFrame({
                'close': prices,
                'timestamp': timestamps
            }).set_index('timestamp').sort_index()
            
            self.price_history = df
            return df
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return pd.DataFrame()

    def compute_indicators(self, df):
        """Calculate technical indicators"""
        if df.empty:
            return 0, 0
        rsi = RSIIndicator(df['close']).rsi().iloc[-1]
        macd = MACD(df['close']).macd_diff().iloc[-1]
        return rsi, macd

    def build_prompt(self, user_input, price, rsi, macd):
        """Build the prompt for OpenAI"""
        trend = "Uptrend" if macd > 0 else "Downtrend"
        prompt = f"""
You are a professional forex trading assistant. Analyze EUR/USD based on the following:

Current Price: {price:.5f}
RSI: {rsi:.2f}
MACD: {macd:.2f}
Trend: {trend}

User Question: {user_input}

Give clear advice (Buy, Sell, or Wait) and explain your reasoning in 1-2 lines. Include a sample trading plan (entry, stop-loss, take-profit).
"""
        return prompt

    def get_openai_response(self, prompt):
        """Get trading advice from OpenAI"""
        try:
            openai.api_key = self.openai_key or self.openai_entry.get()
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a trading expert."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            return f"Error getting AI response: {str(e)}"

    def update_market_data(self):
        """Update market data periodically"""
        try:
            df = self.get_eurusd_price()
            if not df.empty:
                last_price = df['close'].iloc[-1]
                rsi, macd = self.compute_indicators(df)
                
                self.price_label.config(text=f"EUR/USD: {last_price:.5f}")
                self.rsi_label.config(text=f"RSI: {rsi:.2f}")
                self.macd_label.config(text=f"MACD: {macd:.2f}")
                
                self.status_bar.config(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            self.status_bar.config(text=f"Error updating market data: {str(e)}")
            
        # Schedule next update in 60 seconds
        self.root.after(60000, self.update_market_data)

    def on_submit(self, event=None):
        """Handle question submission"""
        question = self.question_entry.get()
        if not question:
            return
            
        self.status_bar.config(text="Getting trading advice...")
        self.root.update()
        
        df = self.get_eurusd_price()
        if not df.empty:
            last_price = df['close'].iloc[-1]
            rsi, macd = self.compute_indicators(df)
            
            prompt = self.build_prompt(question, last_price, rsi, macd)
            advice = self.get_openai_response(prompt)
            
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, advice)
            
        self.status_bar.config(text="Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingAssistant(root)
    root.mainloop()