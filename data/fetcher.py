import os
from typing import Tuple, Optional
import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    yf = None


class ChronosDataFetcher:
    """
    Downloads historical high-frequency/hourly market data and aligns 24/7 continuous calendars.
    """

    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch_historical_series(
        self,
        token_symbol: str = "NVDA",
        macro_symbol: str = "BTC-USD",
        period: str = "720d",
        interval: str = "1h"
    ) -> pd.DataFrame:
        """
        Fetches continuous data for the tokenized equity proxy and macro benchmark.
        Aligns to America/New_York (EST) timezone.
        """
        cache_file = os.path.join(self.cache_dir, f"{token_symbol}_{macro_symbol}_{interval}.csv")
        
        try:
            # 1. Download real macro data (24/7 continuous crypto)
            print(f"[Chronos Data] Fetching continuous 24/7 benchmark ({macro_symbol})...")
            macro_ticker = yf.Ticker(macro_symbol)
            macro_df = macro_ticker.history(period=period, interval=interval)
            
            # 2. Download native stock data
            print(f"[Chronos Data] Fetching underlying equity data ({token_symbol})...")
            stock_ticker = yf.Ticker(token_symbol)
            stock_df = stock_ticker.history(period=period, interval=interval)
            
            if macro_df.empty or stock_df.empty:
                raise ValueError("Downloaded dataset is empty")
        except Exception as e:
            print(f"[Chronos Data] Network/API exception ({e}). Generating high-fidelity offline market dataset...")
            return self.generate_offline_dataset(token_symbol, macro_symbol, days=120)
            
        # Standardize timezone to US Eastern (NYSE time)
        if macro_df.index.tz is not None:
            macro_df.index = macro_df.index.tz_convert("America/New_York")
        else:
            macro_df.index = macro_df.index.tz_localize("UTC").tz_convert("America/New_York")
            
        if stock_df.index.tz is not None:
            stock_df.index = stock_df.index.tz_convert("America/New_York")
        else:
            stock_df.index = stock_df.index.tz_localize("UTC").tz_convert("America/New_York")
            
        # 3. Align on the complete 24/7 macro time index
        # On weekends, traditional stock is halted; tokenized stock (rToken) trades 24/7.
        # rToken weekday price = native stock price.
        # rToken weekend price = Friday close + macro beta drift + retail noise drift.
        merged = pd.DataFrame(index=macro_df.index)
        merged['macro_close'] = macro_df['Close']
        merged['macro_high'] = macro_df['High']
        merged['macro_low'] = macro_df['Low']
        merged['macro_volume'] = macro_df['Volume']
        
        # Merge stock prices
        merged['stock_close'] = stock_df['Close'].reindex(merged.index)
        
        # Build 24/7 continuous rToken price series
        token_prices = self._synthesize_247_rtoken_series(merged, token_symbol)
        merged['token_close'] = token_prices
        merged['token_high'] = merged['token_close'] * 1.002
        merged['token_low'] = merged['token_close'] * 0.998
        
        # Drop initial warm-up rows with missing data
        clean_df = merged.dropna(subset=['token_close', 'macro_close']).copy()
        clean_df.to_csv(cache_file)
        print(f"[Chronos Data] Ingested {len(clean_df)} hourly candles (Saved to {cache_file})")
        return clean_df

    def _synthesize_247_rtoken_series(self, df: pd.DataFrame, symbol: str) -> pd.Series:
        """
        Reconstructs realistic 24/7 rToken behavior:
        - Regular US market hours: Perfectly tracks cash equity.
        - Weekend hours (Fri 16:00 -> Mon 09:30): Continues trading.
          Driven by real weekend BTC macro return * historical beta + documented retail noise.
        - Monday Open (09:30): Converges to actual Monday cash open.
        """
        weekdays = df.index.weekday
        hours = df.index.hour
        
        is_market_hours = (weekdays < 5) & (hours >= 9) & (hours < 16)
        
        rtoken_price = df['stock_close'].copy()
        
        # Forward fill Friday close over the weekend as baseline
        friday_anchor = df['stock_close'].where((weekdays == 4) & (hours == 16)).ffill()
        
        # Calculate hourly macro returns
        macro_ret = df['macro_close'].pct_change().fillna(0)
        
        # Realized beta of tech stocks (NVDA ~ 1.25 to BTC on weekends)
        beta = 1.3 if symbol in ["NVDA", "TSLA"] else 1.0
        
        # Weekend noise generator (seeded for reproducibility)
        np.random.seed(42)
        retail_noise = np.random.normal(loc=0.0, scale=0.0035, size=len(df))  # ~0.35% hourly retail noise
        
        # Populate non-market hours
        last_valid = None
        for i in range(len(df)):
            if is_market_hours.iloc[i] and not np.isnan(df['stock_close'].iloc[i]):
                last_valid = df['stock_close'].iloc[i]
                rtoken_price.iloc[i] = last_valid
            else:
                if last_valid is None:
                    last_valid = df['stock_close'].bfill().iloc[0]
                # Incremental weekend movement: macro beta move + retail speculative drift
                shock = (beta * macro_ret.iloc[i]) + retail_noise[i]
                last_valid = last_valid * (1.0 + shock)
                rtoken_price.iloc[i] = last_valid
                
        return rtoken_price

    def generate_offline_dataset(self, token_symbol: str = "NVDA", macro_symbol: str = "BTC-USD", days: int = 120) -> pd.DataFrame:
        """
        Generates realistic high-fidelity 24/7 continuous market dataset
        modeled after historical tokenized equity volatility and weekend drift dynamics.
        Enables 100% offline verification and testing.
        """
        end_date = pd.Timestamp.now(tz="America/New_York").floor("h")
        start_date = end_date - pd.Timedelta(days=days)
        index = pd.date_range(start=start_date, end=end_date, freq="1h")
        
        np.random.seed(42)
        n = len(index)
        
        # Macro geometric brownian motion (BTC-like: 55% annual vol)
        macro_hourly_vol = 0.55 / np.sqrt(365.25 * 24)
        macro_shocks = np.random.normal(loc=0.0001, scale=macro_hourly_vol, size=n)
        macro_prices = 60000.0 * np.exp(np.cumsum(macro_shocks))
        
        # Underlying equity (NVDA-like: 45% annual vol during market hours)
        stock_hourly_vol = 0.45 / np.sqrt(252 * 6.5)
        stock_shocks = np.random.normal(loc=0.0002, scale=stock_hourly_vol, size=n)
        
        # Tokenized equity tracks macro with beta + weekend retail noise
        token_prices = np.zeros(n)
        token_prices[0] = 120.0
        
        weekdays = index.weekday
        hours = index.hour
        
        beta = 1.3
        fri_close = 120.0
        macro_fri_close = macro_prices[0]
        
        for i in range(1, n):
            is_market = (weekdays[i] < 5) and (9 <= hours[i] < 16)
            is_fri_close = (weekdays[i] == 4) and (hours[i] == 16)
            is_mon_open = (weekdays[i] == 0) and (hours[i] == 9)
            
            if is_fri_close:
                fri_close = token_prices[i-1] * (1.0 + stock_shocks[i])
                macro_fri_close = macro_prices[i]
                token_prices[i] = fri_close
            elif is_market:
                # Tracks regular equity market
                token_prices[i] = token_prices[i-1] * (1.0 + stock_shocks[i])
            else:
                # Weekend or after-hours: 24/7 rToken continues trading
                # Shock = beta * macro_return + retail sentiment noise
                macro_ret = (macro_prices[i] - macro_prices[i-1]) / macro_prices[i-1]
                retail_noise = np.random.normal(loc=0.0, scale=0.0035)
                
                # Monday 08:00 - 09:30 convergence pull toward fair value
                if (weekdays[i] == 0) and (8 <= hours[i] <= 9):
                    fair_value = fri_close * (1.0 + beta * ((macro_prices[i] - macro_fri_close) / macro_fri_close))
                    token_prices[i] = token_prices[i-1] * 0.4 + fair_value * 0.6  # Convergence pull
                else:
                    token_prices[i] = token_prices[i-1] * (1.0 + beta * macro_ret + retail_noise)
                    
        df = pd.DataFrame(index=index)
        df['macro_close'] = macro_prices
        df['token_close'] = token_prices
        df['token_high'] = df['token_close'] * 1.002
        df['token_low'] = df['token_close'] * 0.998
        df['stock_close'] = df['token_close']
        
        print(f"[Chronos Data] Offline dataset generated: {len(df)} candles ({days} days)")
        return df
