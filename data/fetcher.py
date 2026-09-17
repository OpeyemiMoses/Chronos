import os
from typing import Tuple, Optional, Dict, List
import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    yf = None

ASSET_CONFIGS = {
    "rNVDA": {"ticker": "NVDA", "beta": 1.45, "annual_vol": 0.48, "base_price": 128.50, "noise_scale": 0.0035},
    "rTSLA": {"ticker": "TSLA", "beta": 1.85, "annual_vol": 0.58, "base_price": 242.80, "noise_scale": 0.0045},
    "rAAPL": {"ticker": "AAPL", "beta": 0.95, "annual_vol": 0.28, "base_price": 224.30, "noise_scale": 0.0022},
    "rCOIN": {"ticker": "COIN", "beta": 2.40, "annual_vol": 0.72, "base_price": 218.00, "noise_scale": 0.0055},
    "rMSTR": {"ticker": "MSTR", "beta": 2.85, "annual_vol": 0.85, "base_price": 142.50, "noise_scale": 0.0065},
    "rSPY":  {"ticker": "SPY",  "beta": 0.40, "annual_vol": 0.16, "base_price": 555.20, "noise_scale": 0.0015},
    "rQQQ":  {"ticker": "QQQ",  "beta": 0.65, "annual_vol": 0.22, "base_price": 482.10, "noise_scale": 0.0020}
}


class ChronosDataFetcher:
    """
    Downloads historical high-frequency/hourly market data and aligns 24/7 continuous calendars
    for single-asset and multi-asset tokenized equity universes.
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
        Fetches continuous data for the single tokenized equity proxy and macro benchmark.
        Aligns to America/New_York (EST) timezone.
        """
        cache_file = os.path.join(self.cache_dir, f"{token_symbol}_{macro_symbol}_{interval}.csv")
        
        try:
            if yf is None:
                raise ImportError("yfinance not available")
            print(f"[Chronos Data] Fetching continuous 24/7 benchmark ({macro_symbol})...")
            macro_ticker = yf.Ticker(macro_symbol)
            macro_df = macro_ticker.history(period=period, interval=interval)
            
            print(f"[Chronos Data] Fetching underlying equity data ({token_symbol})...")
            stock_ticker = yf.Ticker(token_symbol)
            stock_df = stock_ticker.history(period=period, interval=interval)
            
            if macro_df.empty or stock_df.empty:
                raise ValueError("Downloaded dataset is empty")
        except Exception as e:
            print(f"[Chronos Data] Network/API exception ({e}). Generating high-fidelity offline market dataset...")
            return self.generate_offline_dataset(token_symbol, macro_symbol, days=120)
            
        if macro_df.index.tz is not None:
            macro_df.index = macro_df.index.tz_convert("America/New_York")
        else:
            macro_df.index = macro_df.index.tz_localize("UTC").tz_convert("America/New_York")
            
        if stock_df.index.tz is not None:
            stock_df.index = stock_df.index.tz_convert("America/New_York")
        else:
            stock_df.index = stock_df.index.tz_localize("UTC").tz_convert("America/New_York")
            
        merged = pd.DataFrame(index=macro_df.index)
        merged['macro_close'] = macro_df['Close']
        merged['macro_high'] = macro_df['High']
        merged['macro_low'] = macro_df['Low']
        merged['macro_volume'] = macro_df['Volume']
        merged['stock_close'] = stock_df['Close'].reindex(merged.index)
        
        token_prices = self._synthesize_247_rtoken_series(merged, token_symbol)
        merged['token_close'] = token_prices
        merged['token_high'] = merged['token_close'] * 1.002
        merged['token_low'] = merged['token_close'] * 0.998
        
        clean_df = merged.dropna(subset=['token_close', 'macro_close']).copy()
        clean_df.to_csv(cache_file)
        print(f"[Chronos Data] Ingested {len(clean_df)} hourly candles (Saved to {cache_file})")
        return clean_df

    def _synthesize_247_rtoken_series(self, df: pd.DataFrame, symbol: str) -> pd.Series:
        weekdays = df.index.weekday
        hours = df.index.hour
        is_market_hours = (weekdays < 5) & (hours >= 9) & (hours < 16)
        rtoken_price = df['stock_close'].copy()
        macro_ret = df['macro_close'].pct_change().fillna(0)
        
        beta = 1.3 if symbol in ["NVDA", "TSLA"] else 1.0
        np.random.seed(42)
        retail_noise = np.random.normal(loc=0.0, scale=0.0035, size=len(df))
        
        last_valid = None
        for i in range(len(df)):
            if is_market_hours.iloc[i] and not np.isnan(df['stock_close'].iloc[i]):
                last_valid = df['stock_close'].iloc[i]
                rtoken_price.iloc[i] = last_valid
            else:
                if last_valid is None:
                    last_valid = df['stock_close'].bfill().iloc[0]
                shock = (beta * macro_ret.iloc[i]) + retail_noise[i]
                last_valid = last_valid * (1.0 + shock)
                rtoken_price.iloc[i] = last_valid
                
        return rtoken_price

    def generate_offline_dataset(self, token_symbol: str = "NVDA", macro_symbol: str = "BTC-USD", days: int = 120) -> pd.DataFrame:
        """
        Generates single-asset dataset for backwards compatibility.
        """
        multi_df = self.fetch_multi_asset_dataset(days=days)
        clean_sym = f"r{token_symbol}" if not token_symbol.startswith("r") else token_symbol
        df = pd.DataFrame(index=multi_df.index)
        df['macro_close'] = multi_df['macro_close']
        df['token_close'] = multi_df[f'{clean_sym}_close']
        df['token_high'] = multi_df[f'{clean_sym}_high']
        df['token_low'] = multi_df[f'{clean_sym}_low']
        df['stock_close'] = df['token_close']
        return df

    def fetch_multi_asset_dataset(self, days: int = 120) -> pd.DataFrame:
        """
        Generates/fetches full 7-asset continuous 24/7 cross-asset dataset.
        Includes BTC macro benchmark + rNVDA, rTSLA, rAAPL, rCOIN, rMSTR, rSPY, rQQQ.
        """
        cache_file = os.path.join(self.cache_dir, f"multi_asset_{days}d_1h.csv")
        if os.path.exists(cache_file):
            df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            if df.index.tz is None:
                df.index = df.index.tz_localize("America/New_York")
            print(f"[Chronos Data] Loaded cached multi-asset dataset: {len(df)} candles")
            return df

        end_date = pd.Timestamp.now(tz="America/New_York").floor("h")
        start_date = end_date - pd.Timedelta(days=days)
        index = pd.date_range(start=start_date, end=end_date, freq="1h")
        n = len(index)
        
        np.random.seed(42)
        
        # 1. Macro Benchmark (BTC-like: 55% annual vol)
        macro_hourly_vol = 0.55 / np.sqrt(365.25 * 24)
        macro_shocks = np.random.normal(loc=0.0001, scale=macro_hourly_vol, size=n)
        macro_prices = 60000.0 * np.exp(np.cumsum(macro_shocks))
        macro_rets = np.diff(macro_prices, prepend=macro_prices[0]) / macro_prices
        
        weekdays = index.weekday
        hours = index.hour

        df = pd.DataFrame(index=index)
        df['macro_close'] = macro_prices

        # 2. Generate each tokenized stock in the basket
        for sym, cfg in ASSET_CONFIGS.items():
            base_px = cfg["base_price"]
            beta = cfg["beta"]
            ann_vol = cfg["annual_vol"]
            hourly_stock_vol = ann_vol / np.sqrt(252 * 6.5)
            noise_scale = cfg["noise_scale"]
            
            # Stock market hours shocks
            stock_shocks = np.random.normal(loc=0.0001, scale=hourly_stock_vol, size=n)
            prices = np.zeros(n)
            prices[0] = base_px
            fri_close = base_px
            macro_fri_close = macro_prices[0]
            
            for i in range(1, n):
                is_market = (weekdays[i] < 5) and (9 <= hours[i] < 16)
                is_fri_close = (weekdays[i] == 4) and (hours[i] == 16)
                
                if is_fri_close:
                    fri_close = prices[i-1] * (1.0 + stock_shocks[i])
                    macro_fri_close = macro_prices[i]
                    prices[i] = fri_close
                elif is_market:
                    prices[i] = prices[i-1] * (1.0 + stock_shocks[i])
                else:
                    # Weekend / after-hours 24/7 trading
                    m_ret = macro_rets[i]
                    noise = np.random.normal(loc=0.0, scale=noise_scale)
                    
                    # Monday 08:00 - 09:30 pre-market institutional convergence
                    if (weekdays[i] == 0) and (8 <= hours[i] <= 9):
                        fair_val = fri_close * (1.0 + beta * ((macro_prices[i] - macro_fri_close) / macro_fri_close))
                        prices[i] = prices[i-1] * 0.45 + fair_val * 0.55
                    else:
                        prices[i] = prices[i-1] * (1.0 + beta * m_ret + noise)
            
            df[f"{sym}_close"] = prices
            df[f"{sym}_high"] = prices * 1.002
            df[f"{sym}_low"] = prices * 0.998
            
        df.to_csv(cache_file)
        print(f"[Chronos Data] Multi-asset dataset generated & cached: {len(df)} candles across {len(ASSET_CONFIGS)} assets")
        return df
