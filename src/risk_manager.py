"""
Chronos Risk Management Engine
Handles position sizing, volatility targeting, and dynamic risk controls.
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class RiskConfig:
    target_annual_vol: float = 0.18      # 18% target annualized volatility
    max_position_size: float = 1.0       # Max portfolio allocation (no excessive leverage)
    circuit_breaker_dd: float = 0.08     # Scale down if portfolio drawdown exceeds 8%
    atr_period: int = 14                 # ATR period for volatility stops
    atr_multiplier: float = 2.5          # Trailing stop multiplier


class RiskManager:
    """
    Manages portfolio risk, dynamic position sizing, and volatility targeting.
    """

    def __init__(self, config: RiskConfig = RiskConfig()):
        self.config = config

    def calculate_volatility_scalar(self, price_series: pd.Series, window: int = 24 * 7) -> pd.Series:
        """
        Calculates volatility-targeted sizing scalar based on hourly rolling realized volatility.
        Annualized volatility = hourly_std * sqrt(365.25 * 24)
        """
        returns = price_series.pct_change().fillna(0)
        annual_factor = np.sqrt(365.25 * 24)
        rolling_vol = (returns.rolling(window=window, min_periods=24).std() * annual_factor).clip(lower=0.08)
        
        # Sizing scalar = target_vol / realized_vol
        sizing_scalar = (self.config.target_annual_vol / rolling_vol).clip(lower=0.2, upper=self.config.max_position_size)
        return sizing_scalar.fillna(self.config.max_position_size)

    def calculate_atr(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculates Average True Range (ATR) for volatility stop-loss thresholds.
        """
        tr1 = high - low
        tr2 = (high - close.shift(1)).abs()
        tr3 = (low - close.shift(1)).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period, min_periods=1).mean()
