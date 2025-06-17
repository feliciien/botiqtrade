import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import openai
import requests
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import base64
from tkinter import font
import tkinterdnd2 as tkdnd
import plotly.graph_objects as go
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

# Load environment variables
load_dotenv()

class TradingAssistant:
    def __init__(self, root):
        if not isinstance(root, tkdnd.Tk):
            root.destroy()
            root = tkdnd.Tk()
        self.root = root
        self.root.title("EUR/USD Trading Assistant 🤖💰")
        
        # Initialize _after_id
        self._after_id = None
        
        # Load user preferences
        self.load_preferences()
        
        # Set theme and configure styles
        self.setup_theme()
        
        # Make window responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Initialize main containers
        self.setup_containers()
        
        # Configure API keys
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.exchangerate_key = os.getenv("EXCHANGERATE_API_KEY")
        
        # Store historical prices and uploaded file
        self.price_history = pd.DataFrame()
        self.uploaded_file_path = None
        self.uploaded_image = None
        
        # Load window geometry
        self.load_window_geometry()
        
        # Store last window state
        self.root.bind('<Configure>', self.on_window_configure)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_ui()
    
    def load_preferences(self):
        """Load user preferences from file"""
        self.preferences = {
            'theme': 'light',
            'chart_style': 'line',
            'update_interval': 60,  # seconds
            'font_size': 12
        }
        try:
            if os.path.exists('preferences.json'):
                with open('preferences.json', 'r') as f:
                    saved_prefs = json.load(f)
                    self.preferences.update(saved_prefs)
        except Exception:
            pass
            
    def save_preferences(self):
        """Save user preferences to file"""
        try:
            with open('preferences.json', 'w') as f:
                json.dump(self.preferences, f)
        except Exception:
            pass

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.preferences['theme'] = 'dark' if self.preferences['theme'] == 'light' else 'light'
        self.setup_theme()
        self.save_preferences()
        
    def setup_theme(self):
        """Configure the application theme and styles"""
        self.style = ttk.Style()
        available_themes = self.style.theme_names()
        # Use 'clam' theme if available, otherwise fallback to default
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        
        # Configure colors based on theme
        if self.preferences['theme'] == 'dark':
            self.colors = {
                'primary': '#bb86fc',
                'secondary': '#3700b3',
                'accent': '#03dac6',
                'success': '#00e676',
                'warning': '#ffab00',
                'danger': '#cf6679',
                'background': '#121212',
                'surface': '#1e1e1e',
                'text': '#ffffff'
            }
        else:
            self.colors = {
                'primary': '#2c3e50',
                'secondary': '#34495e',
                'accent': '#3498db',
                'success': '#2ecc71',
                'warning': '#f1c40f',
                'danger': '#e74c3c',
                'background': '#ecf0f1',
                'surface': '#ffffff',
                'text': '#2c3e50'
            }
        
        # Configure styles
        self.style.configure('Header.TLabel', 
                           font=('Helvetica', 14, 'bold'),
                           foreground=self.colors['primary'],
                           background=self.colors['background'])
        
        self.style.configure('Trading.TFrame', 
                           background=self.colors['background'])
        
        self.style.configure('Market.TLabel',
                           font=('Helvetica', 12),
                           padding=5,
                           background=self.colors['background'],
                           foreground=self.colors['text'])
        
        self.style.configure('Accent.TButton',
                           padding=5,
                           background=self.colors['accent'])
        
        self.style.configure('Dropzone.TFrame',
                           relief='solid',
                           borderwidth=2,
                           background=self.colors['surface'])
                           
        self.style.configure('Dropzone.Active.TFrame',
                           background=self.colors['accent'],
                           relief='solid',
                           borderwidth=2)
        
        # Configure window
        self.root.configure(bg=self.colors['background'])
        
        # Update all existing widgets with new theme
        self.update_widget_colors(self.root)
        
    def update_widget_colors(self, widget):
        """Recursively update widget colors based on theme"""
        try:
            widget.configure(bg=self.colors['background'], fg=self.colors['text'])
        except:
            pass
            
        try:
            widget.configure(background=self.colors['background'], foreground=self.colors['text'])
        except:
            pass
            
        for child in widget.winfo_children():
            self.update_widget_colors(child)
        
    def setup_containers(self):
        """Setup main container frames"""
        # Main container
        self.main_container = ttk.Frame(self.root, style='Trading.TFrame')
        self.main_container.grid(row=0, column=0, sticky='nsew', padx=10, pady=5)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create a paned window for flexible layout
        self.paned = ttk.PanedWindow(self.main_container, orient=tk.HORIZONTAL)
        self.paned.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Left panel for market data and trading
        self.left_panel = ttk.Frame(self.paned, style='Trading.TFrame')
        
        # Right panel for file analysis
        self.right_panel = ttk.Frame(self.paned, style='Trading.TFrame')
        
        self.paned.add(self.left_panel, weight=60)
        self.paned.add(self.right_panel, weight=40)
        
        # Configure row and column weights for responsive design
        for panel in [self.left_panel, self.right_panel]:
            panel.grid_rowconfigure(0, weight=1)
            panel.grid_columnconfigure(0, weight=1)
        
    def setup_ui(self):
        # Create main grid layout
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Left panel layout
        self.left_panel.grid_columnconfigure(0, weight=1)
        current_row = 0
        
        # API Key Configuration Frame
        key_frame = ttk.LabelFrame(self.left_panel, text="API Configuration", padding="10")
        key_frame.grid(row=current_row, column=0, sticky='nsew', padx=10, pady=5)
        key_frame.grid_columnconfigure(1, weight=1)
        
        if not self.openai_key:
            ttk.Label(key_frame, text="OpenAI API Key:").grid(row=0, column=0, padx=5)
            self.openai_entry = ttk.Entry(key_frame, show="*")
            self.openai_entry.grid(row=0, column=1, sticky='ew', padx=5)
        
        if not self.exchangerate_key:
            ttk.Label(key_frame, text="ExchangeRate API Key:").grid(row=1, column=0, padx=5)
            self.exchangerate_entry = ttk.Entry(key_frame, show="*")
            self.exchangerate_entry.grid(row=1, column=1, sticky='ew', padx=5)
        
        current_row += 1
        
        # Market Data Frame
        market_frame = ttk.LabelFrame(self.left_panel, text="Market Data", padding="10")
        market_frame.grid(row=current_row, column=0, sticky='ew', padx=10, pady=5)
        market_frame.grid_columnconfigure(3, weight=1)
        
        self.price_label = ttk.Label(market_frame, text="EUR/USD: --", style='Market.TLabel')
        self.price_label.grid(row=0, column=0, padx=20)
        
        self.rsi_label = ttk.Label(market_frame, text="RSI: --", style='Market.TLabel')
        self.rsi_label.grid(row=0, column=1, padx=20)
        
        self.macd_label = ttk.Label(market_frame, text="MACD: --", style='Market.TLabel')
        self.macd_label.grid(row=0, column=2, padx=20)
        
        # Add refresh button
        refresh_btn = ttk.Button(market_frame, text="⟳", 
                               command=self.update_market_data,
                               style='Accent.TButton',
                               width=3)
        refresh_btn.grid(row=0, column=3, padx=5, sticky='e')
        self.create_tooltip(refresh_btn, "Refresh market data\nF5")
        
        current_row += 1
        
        # Chart Frame - Initialize it here
        self.chart_frame = ttk.LabelFrame(self.left_panel, text="Price Chart", padding="10")
        self.chart_frame.grid(row=current_row, column=0, sticky='nsew', padx=10, pady=5)
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_rowconfigure(0, weight=1)
        
        # Create figure for the chart
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        current_row += 1
        
        # Question Input Frame
        input_frame = ttk.Frame(self.left_panel, padding="10")
        input_frame.grid(row=current_row, column=0, sticky='ew', padx=10, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(input_frame, text="Ask your trading question:").grid(row=0, column=0, sticky='w')
        self.question_entry = ttk.Entry(input_frame)
        self.question_entry.grid(row=1, column=0, sticky='ew', pady=5)
        self.question_entry.bind("<Return>", self.on_submit)
        
        submit_btn = ttk.Button(input_frame, text="Get Advice", command=self.on_submit, style='Accent.TButton')
        submit_btn.grid(row=2, column=0, pady=5)
        
        current_row += 1
        
        # Response Display
        response_frame = ttk.LabelFrame(self.left_panel, text="Trading Advice", padding="10")
        response_frame.grid(row=current_row, column=0, sticky='nsew', padx=10, pady=5)
        response_frame.grid_columnconfigure(0, weight=1)
        response_frame.grid_rowconfigure(0, weight=1)
        
        self.response_text = scrolledtext.ScrolledText(response_frame, wrap=tk.WORD, height=10)
        self.response_text.grid(row=0, column=0, sticky='nsew')
        
        # Configure row weights for left panel
        self.left_panel.grid_rowconfigure(current_row, weight=1)
        
        # Right panel layout
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        
        # File Upload Frame
        upload_frame = ttk.LabelFrame(self.right_panel, text="Document/Image Analysis", padding="10")
        upload_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        upload_frame.grid_columnconfigure(0, weight=1)

        # Create drop zone
        self.drop_zone = ttk.Frame(upload_frame, style='Dropzone.TFrame')
        self.drop_zone.grid(row=0, column=0, sticky='nsew', pady=10, ipady=20)
        self.drop_zone.grid_columnconfigure(0, weight=1)
        
        # Drop zone contents
        drop_label = ttk.Label(self.drop_zone, text="Drag and drop files here\nor")
        drop_label.grid(row=0, column=0, pady=5)
        
        upload_btn = ttk.Button(self.drop_zone, text="Upload File", command=self.upload_file, style='Accent.TButton')
        upload_btn.grid(row=1, column=0, pady=5)
        
        self.file_label = ttk.Label(self.drop_zone, text="No file selected")
        self.file_label.grid(row=2, column=0, pady=5)
        
        analyze_btn = ttk.Button(upload_frame, text="Analyze File", command=self.analyze_file, style='Accent.TButton')
        analyze_btn.grid(row=1, column=0, pady=5)

        # Register drag and drop events
        self.drop_zone.drop_target_register(tkdnd.DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', self.handle_drop)
        self.drop_zone.dnd_bind('<<DragEnter>>', lambda e: self.drop_zone.state(['active']))
        self.drop_zone.dnd_bind('<<DragLeave>>', lambda e: self.drop_zone.state(['!active']))

        # Preview Frame
        self.preview_frame = ttk.LabelFrame(self.right_panel, text="File Preview", padding="10")
        self.preview_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=1)
        
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.grid(row=0, column=0, sticky='nsew')
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief="sunken")
        self.status_bar.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        
        # Add tooltips
        self.create_tooltip(self.price_label, 
            "Current EUR/USD exchange rate\nUpdates every minute")
        self.create_tooltip(self.rsi_label, 
            "Relative Strength Index (RSI)\n" +
            "Above 70: Overbought\n" +
            "Below 30: Oversold")
        self.create_tooltip(self.macd_label, 
            "Moving Average Convergence Divergence\n" +
            "Positive: Upward momentum\n" +
            "Negative: Downward momentum")
        self.create_tooltip(self.question_entry, 
            "Enter your trading question\nCtrl+Enter to submit")
        self.create_tooltip(upload_btn, 
            "Upload a file for analysis\nCtrl+U")
            
        # Setup keyboard shortcuts
        self.setup_bindings()
        
        # Start market data updates
        self.update_market_data()
        
        # Initialize empty chart
        self.update_chart()
        
        # Setup toolbar
        self.setup_toolbar()
        
    def create_tooltip(self, widget, text):
        """Create a tooltip for a given widget"""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
            
            # Creates a toplevel window
            self.tooltip = tk.Toplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(self.tooltip, text=text, justify='left',
                            background=self.colors['secondary'],
                            foreground="white",
                            relief='solid', borderwidth=1,
                            padding=(5, 5))
            label.pack()

        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def get_eurusd_price(self):
        """Fetch EUR/USD price data from Frankfurter API and simulate short-term data"""
        try:
            url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
            try:
                r = requests.get(url, timeout=10)  # Add timeout
                data = r.json()
            except requests.exceptions.ConnectionError as e:
                raise Exception("Failed to connect to Frankfurter API. Please check your internet connection.") from e
            except requests.exceptions.Timeout:
                raise Exception("Connection to Frankfurter API timed out. Please try again.") from e
            except requests.exceptions.RequestException as e:
                raise Exception(f"Error connecting to Frankfurter API: {str(e)}") from e
            
            if 'rates' not in data:
                error_msg = data.get('error', 'Unknown error')
                raise Exception(f"API Error: {error_msg}")
                
            current_rate = data['rates']['USD']
            
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
            error_msg = str(e)
            # Show error in GUI
            messagebox.showerror("API Error", error_msg)
            self.status_bar.config(text=f"Error: {error_msg}")
            return pd.DataFrame()

    def compute_indicators(self, df):
        """Calculate technical indicators"""
        if df.empty:
            return 0, 0
        rsi = RSIIndicator(df['close']).rsi().iloc[-1]
        macd = MACD(df['close']).macd_diff().iloc[-1]
        return rsi, macd

    def predict_next_price(self, df, window=20):
        """
        Improved swing trade prediction using RandomForestRegressor and technical indicators.
        Features: time index, RSI, MACD, SMA.
        Returns the predicted price or None if not enough data.
        """
        if df.empty or len(df) < window + 10:
            # Not enough data for indicators, fallback to linear regression
            if df.empty or len(df) < window:
                return None
            y = df['close'].tail(window).values
            X = np.arange(window).reshape(-1, 1)
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X, y)
            next_time = np.array([[window]])
            next_price = model.predict(next_time)[0]
            return float(next_price)

        # Compute indicators
        closes = df['close'].tail(window + 1)
        rsi_series = RSIIndicator(closes).rsi()
        macd_series = MACD(closes).macd_diff()
        sma_series = closes.rolling(window=5).mean()

        # Drop initial NaNs
        features_df = pd.DataFrame({
            'close': closes.values,
            'rsi': rsi_series.values,
            'macd': macd_series.values,
            'sma': sma_series.values,
            'time': np.arange(len(closes))
        }).dropna()

        if len(features_df) < window:
            return None

        # Prepare features and target
        X = features_df[['time', 'rsi', 'macd', 'sma']].iloc[:-1].values
        y = features_df['close'].iloc[1:].values  # Predict next close

        # Train model
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        # Prepare next feature row
        last_row = features_df[['time', 'rsi', 'macd', 'sma']].iloc[-1].values.reshape(1, -1)
        next_price = model.predict(last_row)[0]
        return float(next_price)

    def build_prompt(self, user_input, price, rsi, macd, predicted_price=None):
        """Build the prompt for OpenAI"""
        trend = "Uptrend" if macd > 0 else "Downtrend"
        pred_str = f"\nPredicted Next Price: {predicted_price:.5f}" if predicted_price is not None else ""
        prompt = f"""
You are a professional forex trading assistant. Analyze EUR/USD based on the following:

Current Price: {price:.5f}
RSI: {rsi:.2f}
MACD: {macd:.2f}
Trend: {trend}{pred_str}

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

    def setup_chart(self):
        """Setup the price chart"""
        chart_frame = ttk.LabelFrame(self.left_panel, text="Price Chart", padding="10")
        chart_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=5)
        
        # Create figure for the chart
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        # Initialize empty chart
        self.update_chart()
        
    def update_chart(self):
        """Update the price chart with new data"""
        if self.price_history.empty:
            return
            
        self.ax.clear()
        
        if self.preferences['chart_style'] == 'candlestick':
            # Convert data for candlestick
            df = self.price_history.copy()
            df['open'] = df['close'].shift(1)
            df['high'] = df[['open', 'close']].max(axis=1)
            df['low'] = df[['open', 'close']].min(axis=1)
            
            # Plot candlesticks
            up = df[df.close >= df.open]
            down = df[df.close < df.open]
            
            # Up candlesticks
            self.ax.bar(up.index, up.close - up.open, bottom=up.open, 
                       width=0.8, color=self.colors['success'])
            self.ax.bar(up.index, up.high - up.close, bottom=up.close,
                       width=0.1, color=self.colors['success'])
            self.ax.bar(up.index, up.low - up.open, bottom=up.open,
                       width=0.1, color=self.colors['success'])
            
            # Down candlesticks
            self.ax.bar(down.index, down.close - down.open, bottom=down.open,
                       width=0.8, color=self.colors['danger'])
            self.ax.bar(down.index, down.high - down.open, bottom=down.open,
                       width=0.1, color=self.colors['danger'])
            self.ax.bar(down.index, down.low - down.close, bottom=down.close,
                       width=0.1, color=self.colors['danger'])
        else:
            # Line chart
            self.ax.plot(self.price_history.index, self.price_history['close'],
                        color=self.colors['accent'], linewidth=2)
        
        # Add timeframe selector if not exists
        if not hasattr(self, 'timeframe_var'):
            self.setup_chart_controls()
        
        self.ax.set_title('EUR/USD Price History')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Price')
        self.ax.grid(True, alpha=0.3)
        self.fig.autofmt_xdate()
        self.canvas.draw()
        
    def setup_chart_controls(self):
        """Setup chart control panel with zoom controls"""
        control_frame = ttk.Frame(self.chart_frame)
        control_frame.grid(row=1, column=0, sticky='ew', pady=5)
        control_frame.grid_columnconfigure(1, weight=1)
        
        # Zoom controls
        zoom_frame = ttk.Frame(control_frame)
        zoom_frame.grid(row=0, column=0, sticky='w', padx=5)
        
        zoom_in_btn = ttk.Button(zoom_frame, text="🔍+", 
                                command=lambda: self.zoom_chart(1.2),
                                width=3)
        zoom_in_btn.grid(row=0, column=0, padx=2)
        self.create_tooltip(zoom_in_btn, "Zoom In (Ctrl +)")
        
        zoom_out_btn = ttk.Button(zoom_frame, text="🔍-",
                                 command=lambda: self.zoom_chart(0.8),
                                 width=3)
        zoom_out_btn.grid(row=0, column=1, padx=2)
        self.create_tooltip(zoom_out_btn, "Zoom Out (Ctrl -)")
        
        reset_zoom_btn = ttk.Button(zoom_frame, text="⟲",
                                  command=self.reset_zoom,
                                  width=3)
        reset_zoom_btn.grid(row=0, column=2, padx=2)
        self.create_tooltip(reset_zoom_btn, "Reset Zoom (Ctrl 0)")
        
        # Timeframe selector
        ttk.Label(control_frame, text="Timeframe:").grid(row=0, column=0, padx=5)
        self.timeframe_var = tk.StringVar(value='5m')
        timeframe_combo = ttk.Combobox(control_frame, 
                                     textvariable=self.timeframe_var,
                                     values=['1m', '5m', '15m', '30m', '1h', '4h', '1d'],
                                     state='readonly',
                                     width=10)
        timeframe_combo.grid(row=0, column=1, padx=5, sticky='w')
        timeframe_combo.bind('<<ComboboxSelected>>', lambda e: self.update_market_data())
        
        # Style selector
        ttk.Label(control_frame, text="Style:").grid(row=0, column=2, padx=5)
        self.chart_style_var = tk.StringVar(value=self.preferences['chart_style'])
        style_combo = ttk.Combobox(control_frame,
                                 textvariable=self.chart_style_var,
                                 values=['line', 'candlestick'],
                                 state='readonly',
                                 width=10)
        style_combo.grid(row=0, column=3, padx=5)
        style_combo.bind('<<ComboboxSelected>>', self.on_chart_style_change)
        
    def on_chart_style_change(self, event=None):
        """Handle chart style change"""
        self.preferences['chart_style'] = self.chart_style_var.get()
        self.save_preferences()
        self.update_chart()
        
    def update_market_data(self):
        """Update market data periodically"""
        try:
            df = self.get_eurusd_price()
            if not df.empty:
                last_price = df['close'].iloc[-1]
                rsi, macd = self.compute_indicators(df)
                predicted_price = self.predict_next_price(df)
                
                # Update labels with colors based on values
                self.price_label.config(
                    text=f"EUR/USD: {last_price:.5f}",
                    foreground=self.colors['text']
                )
                
                self.rsi_label.config(
                    text=f"RSI: {rsi:.2f}",
                    foreground=self.colors['danger'] if rsi > 70 or rsi < 30 else self.colors['text']
                )
                
                self.macd_label.config(
                    text=f"MACD: {macd:.2f}",
                    foreground=self.colors['success'] if macd > 0 else self.colors['danger']
                )

                # Show predicted price in status bar
                if predicted_price is not None:
                    self.status_bar.config(
                        text=f"Last updated: {datetime.now().strftime('%H:%M:%S')} | Predicted Next Price: {predicted_price:.5f}"
                    )
                else:
                    self.status_bar.config(
                        text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}"
                    )
                
                # Update chart
                self.update_chart()
        except Exception as e:
            self.status_bar.config(text=f"Error updating market data: {str(e)}")
            
        # Schedule next update in 60 seconds
        self._after_id = self.root.after(60000, self.update_market_data)

    def on_submit(self, event=None):
        """Handle question submission"""
        question = self.question_entry.get()
        if not question:
            return
            
        self.show_loading("Getting trading advice...")
        self.status_bar.config(text="Getting trading advice...")
        self.root.update()
        
        try:
            df = self.get_eurusd_price()
            if not df.empty:
                last_price = df['close'].iloc[-1]
                rsi, macd = self.compute_indicators(df)
                predicted_price = self.predict_next_price(df)
                
                prompt = self.build_prompt(question, last_price, rsi, macd, predicted_price)
                advice = self.get_openai_response(prompt)
                
                self.response_text.delete(1.0, tk.END)
                if predicted_price is not None:
                    self.response_text.insert(tk.END, f"Model Predicted Next Price: {predicted_price:.5f}\n\n")
                self.response_text.insert(tk.END, advice)
                
        finally:
            self.hide_loading()
            self.status_bar.config(text="Ready")

    def upload_file(self):
        """Upload a file for analysis"""
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.uploaded_file_path = file_path
        self.file_label.config(text=os.path.basename(file_path))

        # Preview the uploaded file (text or image)
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg']:
            self.preview_image(file_path)
        elif ext in ['.txt', '.csv', '.xlsx']:
            self.preview_text_file(file_path)
        else:
            messagebox.showerror("Unsupported file type", "Please upload an image or text file.")

    def preview_image(self, file_path):
        """Preview the uploaded image file"""
        try:
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.uploaded_image = ImageTk.PhotoImage(img)

            self.preview_label.config(image=self.uploaded_image)
            self.preview_label.image = self.uploaded_image
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {str(e)}")

    def preview_text_file(self, file_path):
        """Preview the uploaded text or CSV file"""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                text = df.head().to_string()
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
                text = df.head().to_string()
            else:
                with open(file_path, 'r') as file:
                    text = file.read()

            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, text)
            self.preview_label.config(image='', text='')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def chunk_content(self, content, max_chunk_size=4000):
        """Split content into chunks that fit within token limits"""
        chunks = []
        current_chunk = ""
        
        # For text content, split by newlines
        if isinstance(content, str):
            lines = content.split('\n')
            for line in lines:
                if len(current_chunk) + len(line) < max_chunk_size:
                    current_chunk += line + '\n'
                else:
                    chunks.append(current_chunk)
                    current_chunk = line + '\n'
            if current_chunk:
                chunks.append(current_chunk)
        # For binary content (images), use base64 chunks
        else:
            encoded = base64.b64encode(content).decode('utf-8')
            chunk_size = max_chunk_size
            chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
        
        return chunks

    def analyze_file(self):
        """Analyze the uploaded file with OpenAI"""
        if not self.uploaded_file_path:
            messagebox.showwarning("No file selected", "Please upload a file first.")
            return

        self.show_loading("Analyzing file...")
        self.status_bar.config(text="Analyzing file...")
        self.root.update()

        try:
            with open(self.uploaded_file_path, 'rb') as file:
                file_content = file.read()

            # Determine if it's a text file
            is_text = False
            ext = os.path.splitext(self.uploaded_file_path)[1].lower()
            if ext in ['.txt', '.csv', '.xlsx']:
                try:
                    file_content = file_content.decode('utf-8')
                    is_text = True
                except UnicodeDecodeError:
                    pass

            if not is_text:
                try:
                    # For images, convert to base64 and analyze
                    encoded_image = base64.b64encode(file_content).decode('utf-8')
                    base64_uri = f"data:image/jpeg;base64,{encoded_image}"
                    
                    openai.api_key = self.openai_key or self.openai_entry.get()
                    response = openai.ChatCompletion.create(
                        model="gpt-4o",  # Updated to use new model
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Please analyze this trading chart or financial image and provide detailed observations about the market patterns, indicators, and potential trading opportunities:"
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": base64_uri,
                                            "detail": "high"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=500
                    )
                    
                    analysis = response.choices[0].message['content']
                    self.response_text.delete(1.0, tk.END)
                    self.response_text.insert(tk.END, f"Image Analysis:\n{analysis}")
                    
                except Exception as e:
                    self.response_text.delete(1.0, tk.END)
                    self.response_text.insert(tk.END, f"Error analyzing image: {str(e)}")
                    # Fallback to gpt-4o-mini if gpt-4o fails
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-4o-mini",
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Please analyze this trading chart or financial image and provide detailed observations about the market patterns, indicators, and potential trading opportunities:"
                                        },
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": base64_uri,
                                                "detail": "high"
                                            }
                                        }
                                    ]
                                }
                            ],
                            max_tokens=500
                        )
                        analysis = response.choices[0].message['content']
                        self.response_text.delete(1.0, tk.END)
                        self.response_text.insert(tk.END, f"Image Analysis (using backup model):\n{analysis}")
                    except Exception as e2:
                        self.response_text.insert(tk.END, f"\nBackup model also failed: {str(e2)}")
            else:
                # Handle text files with chunks
                chunks = self.chunk_content(file_content)
                combined_analysis = ""
                
                for i, chunk in enumerate(chunks):
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are a data analysis expert."},
                                {"role": "user", "content": f"Analyze this text content (part {i+1}/{len(chunks)}):\n\n{chunk}\n\nProvide insights and summary."}
                            ],
                            max_tokens=1000
                        )
                        chunk_analysis = response.choices[0].message['content']
                        combined_analysis += f"\nPart {i+1} Analysis:\n{chunk_analysis}\n"
                        
                        self.status_bar.config(text=f"Analyzing part {i+1}/{len(chunks)}...")
                        self.root.update()
                        
                    except Exception as e:
                        combined_analysis += f"\nError analyzing part {i+1}: {str(e)}\n"

                # Display combined analysis
                self.response_text.delete(1.0, tk.END)
                self.response_text.insert(tk.END, combined_analysis)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze file: {str(e)}")
        finally:
            self.hide_loading()
            self.status_bar.config(text="Ready")

    def handle_drop(self, event):
        """Handle dropped files"""
        self.drop_zone.state(['!active'])  # Remove active state
        file_path = event.data
        
        # Remove the curly braces and any extra quotes that Windows might add
        file_path = file_path.strip('{}').strip('"')
        
        if os.path.exists(file_path):
            self.uploaded_file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            
            # Preview the file
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg']:
                self.preview_image(file_path)
            elif ext in ['.txt', '.csv', '.xlsx']:
                self.preview_text_file(file_path)
            else:
                messagebox.showerror("Unsupported file type", "Please upload an image or text file.")
        else:
            messagebox.showerror("Error", "File not found")

    def show_loading(self, message="Loading..."):
        """Show loading indicator"""
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.transient(self.root)
        self.loading_window.grab_set()
        
        # Center the loading window
        window_width = 200
        window_height = 100
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.loading_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        self.loading_window.title("Processing")
        self.loading_window.configure(bg=self.colors['background'])
        
        # Loading message
        ttk.Label(self.loading_window, text=message,
                 style='Header.TLabel').pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.loading_window, mode='indeterminate')
        self.progress.pack(fill='x', padx=20)
        self.progress.start(10)
        
        self.root.update()

    def hide_loading(self):
        """Hide loading indicator"""
        if hasattr(self, 'loading_window'):
            self.progress.stop()
            self.loading_window.destroy()

    def setup_bindings(self):
        """Setup keyboard shortcuts"""
        # Existing shortcuts
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<Control-u>', lambda e: self.upload_file())
        self.root.bind('<F5>', lambda e: self.update_market_data())
        self.question_entry.bind('<Control-Return>', self.on_submit)
        
        # New shortcuts
        self.root.bind('<Control-plus>', lambda e: self.zoom_chart(1.2))
        self.root.bind('<Control-minus>', lambda e: self.zoom_chart(0.8))
        self.root.bind('<Control-0>', lambda e: self.reset_zoom())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())
        self.root.bind('<Control-s>', lambda e: self.show_settings())

    def setup_toolbar(self):
        """Setup toolbar with theme toggle and settings"""
        toolbar = ttk.Frame(self.main_container, style='Trading.TFrame')
        toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=2)
        toolbar.grid_columnconfigure(2, weight=1)  # Push buttons to left
        
        # Theme toggle button
        theme_btn = ttk.Button(toolbar, 
                             text="🌓" if self.preferences['theme'] == 'light' else "🌙",
                             command=self.toggle_theme,
                             width=3,
                             style='Accent.TButton')
        theme_btn.grid(row=0, column=0, padx=2)
        self.create_tooltip(theme_btn, "Toggle Dark/Light Theme")
        
        # Settings button
        settings_btn = ttk.Button(toolbar,
                                text="⚙️",
                                command=self.show_settings,
                                width=3,
                                style='Accent.TButton')
        settings_btn.grid(row=0, column=1, padx=2)
        self.create_tooltip(settings_btn, "Settings")
        
    def show_settings(self):
        """Show settings dialog"""
        settings = tk.Toplevel(self.root)
        settings.title("Settings")
        settings.geometry("400x300")
        settings.transient(self.root)
        settings.grab_set()
        
        # Center window
        settings.update_idletasks()
        x = (settings.winfo_screenwidth() - settings.winfo_width()) // 2
        y = (settings.winfo_screenheight() - settings.winfo_height()) // 2
        settings.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(settings, padding="10")
        main_frame.grid(row=0, column=0, sticky='nsew')
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Update interval
        ttk.Label(main_frame, text="Update Interval (seconds):").grid(row=0, column=0, sticky='w', pady=5)
        interval_var = tk.StringVar(value=str(self.preferences['update_interval']))
        interval_entry = ttk.Entry(main_frame, textvariable=interval_var)
        interval_entry.grid(row=0, column=1, sticky='ew', padx=5)
        
        # Font size
        ttk.Label(main_frame, text="Font Size:").grid(row=1, column=0, sticky='w', pady=5)
        font_var = tk.StringVar(value=str(self.preferences['font_size']))
        font_entry = ttk.Entry(main_frame, textvariable=font_var)
        font_entry.grid(row=1, column=1, sticky='ew', padx=5)
        
        # Chart style
        ttk.Label(main_frame, text="Chart Style:").grid(row=2, column=0, sticky='w', pady=5)
        style_var = tk.StringVar(value=self.preferences['chart_style'])
        style_combo = ttk.Combobox(main_frame, textvariable=style_var, 
                                 values=['line', 'candlestick'],
                                 state='readonly')
        style_combo.grid(row=2, column=1, sticky='ew', padx=5)
        
        # Save button
        def save_settings():
            try:
                self.preferences['update_interval'] = int(interval_var.get())
                self.preferences['font_size'] = int(font_var.get())
                self.preferences['chart_style'] = style_var.get()
                self.save_preferences()
                self.apply_settings()
                settings.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input values")
        
        save_btn = ttk.Button(main_frame, text="Save", command=save_settings, style='Accent.TButton')
        save_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
    def apply_settings(self):
        """Apply settings changes"""
        # Update font sizes
        font_size = self.preferences['font_size']
        self.style.configure('Header.TLabel', font=('Helvetica', font_size + 2, 'bold'))
        self.style.configure('Market.TLabel', font=('Helvetica', font_size))
        
        # Update chart style
        self.update_chart()
        
        # Update market data refresh interval
        self.root.after_cancel(self._after_id)
        self.update_market_data()
        
    def load_window_geometry(self):
        """Load saved window position and size"""
        try:
            if 'window_geometry' in self.preferences:
                self.root.geometry(self.preferences['window_geometry'])
        except Exception:
            # Default window size
            self.root.geometry('1200x800')
            
    def on_window_configure(self, event=None):
        """Save window geometry when it changes"""
        if event is not None and event.widget == self.root:
            self.preferences['window_geometry'] = self.root.geometry()
            self.save_preferences()
            
    def on_closing(self):
        """Handle window closing"""
        self.save_preferences()
        self.root.destroy()
        
    def zoom_chart(self, factor):
        """Zoom in or out of the chart"""
        try:
            current_xlim = self.ax.get_xlim()
            current_ylim = self.ax.get_ylim()
            
            # Calculate new limits
            center_x = sum(current_xlim) / 2
            center_y = sum(current_ylim) / 2
            
            new_range_x = (current_xlim[1] - current_xlim[0]) / factor
            new_range_y = (current_ylim[1] - current_ylim[0]) / factor
            
            self.ax.set_xlim(center_x - new_range_x/2, center_x + new_range_x/2)
            self.ax.set_ylim(center_y - new_range_y/2, center_y + new_range_y/2)
            
            self.canvas.draw()
        except Exception as e:
            self.status_bar.config(text=f"Error zooming chart: {str(e)}")

    def reset_zoom(self):
        """Reset chart zoom to default"""
        try:
            if not self.price_history.empty:
                self.ax.relim()
                self.ax.autoscale()
                self.canvas.draw()
        except Exception as e:
            self.status_bar.config(text=f"Error resetting zoom: {str(e)}")

    # ...existing code...
if __name__ == "__main__":
    try:
        root = tkdnd.Tk()  # Use tkdnd.Tk() instead of tk.Tk() for drag and drop support
        app = TradingAssistant(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
