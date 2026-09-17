"""
Chronos: 24/7 After-Hours Information Pricing & Weekend Drift Engine
Core Strategy Logic for Tokenized US Stocks (rTokens)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


@dataclass
class ChronosConfig:
    """Configuration parameters for the Chronos alpha model."""
    symbol: str = "rNVDA"
    macro_benchmark: str = "BTC-USD"
    
    # Timing windows (EST / UTC-5 aligned)
    anchor_weekday: int = 4        # Friday
    anchor_hour: int = 16          # 4:00 PM EST (US market close)
    exit_weekday: int = 0          # Monday
    exit_hour_start: int = 8       # 8:00 AM EST (US Pre-Market)
    exit_hour_end: int = 9         # 9:30 AM EST (Cash Market Open)
    
    # Signal thresholds
    z_entry_threshold: float = 2.0       # Enter when excess drift exceeds 2.0 std
    z_exit_threshold: float = 0.4        # Take profit when excess drift mean-reverts to 0.4 std
    rolling_beta_window: int = 14 * 24   # 14 days of hourly data for beta estimation
    rolling_vol_window: int = 7 * 24     # 7 days of hourly data for excess drift volatility
    
    # Execution and friction model
    taker_fee_pct: float = 0.0005        # 0.05% exchange taker fee
    slippage_pct: float = 0.0005         # 0.05% bid-ask slippage per trade
    
    # Risk controls
    stop_loss_pct: float = 0.035         # 3.5% maximum adverse excursion stop-loss
    max_position_size: float = 1.0       # Maximum portfolio allocation
    leverage: float = 1.0                # Base leverage


class ChronosStrategy:
    """
    Chronos Quantitative Strategy Engine.
    
    Isolates Excess Retail Drift from Justified Macro Drift on 24/7 tokenized stocks (rTokens)
    and exploits mean-reversion at Monday opening bell liquidity convergence.
    """

    def __init__(self, config: Optional[ChronosConfig] = None):
        self.config = config or ChronosConfig()
        
    def compute_macro_beta(self, token_returns: pd.Series, macro_returns: pd.Series) -> pd.Series:
        """
        Computes rolling covariance/variance beta between rToken and Macro benchmark.
        """
        rolling_cov = token_returns.rolling(window=self.config.rolling_beta_window, min_periods=48).cov(macro_returns)
        rolling_var = macro_returns.rolling(window=self.config.rolling_beta_window, min_periods=48).var()
        
        beta = (rolling_cov / rolling_var).clip(lower=0.2, upper=2.5)
        # Default beta to 1.0 if not enough warmup data
        return beta.fillna(1.0)

    def identify_market_sessions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Tags market regime states:
        - is_weekend: True between Friday 16:00 and Monday 09:30
        - is_friday_anchor: True at Friday 16:00
        - is_monday_convergence: True between Monday 08:00 and 09:30
        """
        df = df.copy()
        
        # Ensure datetime index
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
            
        weekdays = df.index.weekday
        hours = df.index.hour
        
        # Friday Anchor: Friday 16:00
        df['is_friday_anchor'] = (weekdays == self.config.anchor_weekday) & (hours == self.config.anchor_hour)
        
        # Monday Convergence Window: Monday 08:00 to 09:00 inclusive
        df['is_monday_convergence'] = (weekdays == self.config.exit_weekday) & (
            (hours >= self.config.exit_hour_start) & (hours <= self.config.exit_hour_end)
        )
        
        # Weekend period: Friday >= 16:00, all Saturday (5), all Sunday (6), Monday < 09:30
        is_fri_evening = (weekdays == 4) & (hours >= 16)
        is_sat_sun = (weekdays == 5) | (weekdays == 6)
        is_mon_morning = (weekdays == 0) & (hours < 10)
        df['is_weekend_window'] = is_fri_evening | is_sat_sun | is_mon_morning
        
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates Friday anchors, continuous weekend drift, macro-adjusted excess drift,
        and generates long (+1), short (-1), and exit (0) trading signals.
        """
        df = self.identify_market_sessions(df)
        
        # Return calculations
        token_ret = df['token_close'].pct_change()
        macro_ret = df['macro_close'].pct_change()
        df['rolling_beta'] = self.compute_macro_beta(token_ret, macro_ret)
        
        # Forward-fill Friday 16:00 anchor prices through the weekend
        df['anchor_token_price'] = np.where(df['is_friday_anchor'], df['token_close'], np.nan)
        df['anchor_macro_price'] = np.where(df['is_friday_anchor'], df['macro_close'], np.nan)
        
        # We create weekend session IDs to group each weekend uniquely
        weekend_id = (df['is_friday_anchor']).cumsum()
        df['weekend_id'] = weekend_id
        
        # Forward-fill anchor prices within each weekend
        df['anchor_token_price'] = df.groupby('weekend_id')['anchor_token_price'].ffill()
        df['anchor_macro_price'] = df.groupby('weekend_id')['anchor_macro_price'].ffill()
        
        # Compute cumulative drift from Friday close
        df['token_drift'] = np.where(
            df['is_weekend_window'] & df['anchor_token_price'].notna(),
            (df['token_close'] - df['anchor_token_price']) / df['anchor_token_price'],
            0.0
        )
        
        df['macro_drift'] = np.where(
            df['is_weekend_window'] & df['anchor_macro_price'].notna(),
            (df['macro_close'] - df['anchor_macro_price']) / df['anchor_macro_price'],
            0.0
        )
        
        # Justified drift based on macro beta
        df['justified_drift'] = df['rolling_beta'] * df['macro_drift']
        
        # Excess Retail Drift = Actual Drift - Justified Drift
        df['excess_drift'] = df['token_drift'] - df['justified_drift']
        
        # Compute rolling volatility of excess drift to normalize Z-score
        rolling_std = df['excess_drift'].rolling(window=self.config.rolling_vol_window, min_periods=24).std()
        df['excess_drift_std'] = rolling_std.fillna(0.015)  # baseline 1.5% std
        
        # Avoid division by zero
        df['z_score'] = np.where(
            df['excess_drift_std'] > 1e-6,
            df['excess_drift'] / df['excess_drift_std'],
            0.0
        )
        
        # Signal Generation State Machine
        signals = np.zeros(len(df))
        positions = np.zeros(len(df))
        trade_reasons = [''] * len(df)
        
        current_pos = 0
        entry_price = 0.0
        
        for i in range(1, len(df)):
            is_weekend = df['is_weekend_window'].iloc[i]
            is_convergence = df['is_monday_convergence'].iloc[i]
            z = df['z_score'].iloc[i]
            price = df['token_close'].iloc[i]
            
            # 1. Active Position Management
            if current_pos != 0:
                # Stop-Loss Check
                ret_since_entry = (price - entry_price) / entry_price if current_pos == 1 else (entry_price - price) / entry_price
                if ret_since_entry <= -self.config.stop_loss_pct:
                    current_pos = 0
                    trade_reasons[i] = "Stop-Loss Triggered"
                
                # Convergence Exit on Monday morning open
                elif is_convergence:
                    current_pos = 0
                    trade_reasons[i] = "Monday Convergence Exit"
                    
                # Early Mean-Reversion Take Profit
                elif (current_pos == 1 and z >= -self.config.z_exit_threshold) or \
                     (current_pos == -1 and z <= self.config.z_exit_threshold):
                    current_pos = 0
                    trade_reasons[i] = "Mean-Reversion Take Profit"
                    
                # Exit when weekend session ends
                elif not is_weekend:
                    current_pos = 0
                    trade_reasons[i] = "Session End Exit"
            
            # 2. Entry Logic (Only during active weekend drift window)
            if current_pos == 0 and is_weekend and not is_convergence:
                # Oversold (Unjustified retail discount) -> GO LONG
                if z <= -self.config.z_entry_threshold:
                    current_pos = 1
                    entry_price = price
                    trade_reasons[i] = f"Long Entry (Z={z:.2f})"
                
                # Overbought (Unjustified retail speculative premium) -> GO SHORT
                elif z >= self.config.z_entry_threshold:
                    current_pos = -1
                    entry_price = price
                    trade_reasons[i] = f"Short Entry (Z={z:.2f})"
            
            positions[i] = current_pos
            
        df['signal'] = positions
        df['trade_reason'] = trade_reasons
        
        return df
