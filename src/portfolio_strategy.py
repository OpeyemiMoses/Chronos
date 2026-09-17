"""
Institutional Multi-Asset Chronos Strategy
Manages a 7-asset tokenized US equity basket with cross-asset correlation tracking,
dynamic risk-parity allocation, and disciplined Monday convergence exits.
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


class MultiAssetChronosStrategy:
    """
    Coordinates weekend after-hours alpha extraction across an institutional basket:
    - Mega-cap Tech: rNVDA, rTSLA, rAAPL
    - Crypto-Equities: rCOIN, rMSTR
    - Macro Indices: rSPY, rQQQ
    """

    def __init__(
        self,
        assets: Optional[List[str]] = None,
        z_entry_threshold: float = 2.0,
        z_exit_threshold: float = 0.4,
        stop_loss_pct: float = 0.035,
        max_gross_leverage: float = 1.20,
        max_single_weight: float = 0.25,
        rolling_beta_window: int = 14 * 24,
        rolling_vol_window: int = 7 * 24
    ):
        self.assets = assets or ["rNVDA", "rTSLA", "rAAPL", "rCOIN", "rMSTR", "rSPY", "rQQQ"]
        self.z_entry_threshold = z_entry_threshold
        self.z_exit_threshold = z_exit_threshold
        self.stop_loss_pct = stop_loss_pct
        self.max_gross_leverage = max_gross_leverage
        self.max_single_weight = max_single_weight
        self.rolling_beta_window = rolling_beta_window
        self.rolling_vol_window = rolling_vol_window

    def compute_asset_signals(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Runs per-asset state machine tracking anchors, beta, drift, stops, and Monday convergence.
        """
        asset_frames = {}
        weekdays = df.index.weekday
        hours = df.index.hour

        is_friday_anchor = (weekdays == 4) & (hours == 16)
        is_weekend_window = (
            ((weekdays == 4) & (hours >= 17)) |
            (weekdays == 5) |
            (weekdays == 6) |
            ((weekdays == 0) & (hours < 8))
        )
        is_monday_convergence = (weekdays == 0) & (hours >= 8) & (hours <= 9)

        macro_close = df['macro_close']
        macro_ret = macro_close.pct_change()
        weekend_id = is_friday_anchor.cumsum()

        for sym in self.assets:
            col_close = f"{sym}_close"
            if col_close not in df.columns:
                continue

            price = df[col_close]
            ret = price.pct_change()

            # 1. Rolling Beta to Macro
            rolling_cov = ret.rolling(self.rolling_beta_window, min_periods=24).cov(macro_ret)
            rolling_var = macro_ret.rolling(self.rolling_beta_window, min_periods=24).var()
            beta = (rolling_cov / (rolling_var + 1e-8)).fillna(1.2).clip(0.2, 3.5)

            # 2. Friday 16:00 EST Anchors forward-filled across the weekend
            fri_stock = np.where(is_friday_anchor, price, np.nan)
            fri_macro = np.where(is_friday_anchor, macro_close, np.nan)
            
            anchor_stock = pd.Series(fri_stock, index=df.index).groupby(weekend_id).ffill()
            anchor_macro = pd.Series(fri_macro, index=df.index).groupby(weekend_id).ffill()

            # 3. Excess Retail Drift
            stock_drift = np.where(is_weekend_window & anchor_stock.notna(), (price - anchor_stock) / anchor_stock, 0.0)
            macro_drift = np.where(is_weekend_window & anchor_macro.notna(), (macro_close - anchor_macro) / anchor_macro, 0.0)
            justified_drift = beta * macro_drift
            excess_drift = pd.Series(stock_drift - justified_drift, index=df.index)

            # 4. Z-Score
            rolling_std = excess_drift.rolling(window=self.rolling_vol_window, min_periods=24).std().fillna(0.015).clip(lower=0.003)
            z_score = excess_drift / rolling_std

            # 5. State Machine execution for positions
            n = len(df)
            positions = np.zeros(n)
            curr_pos = 0
            entry_px = 0.0

            for i in range(1, n):
                in_weekend = bool(is_weekend_window[i])
                in_conv = bool(is_monday_convergence[i])
                z = z_score.iloc[i]
                p = price.iloc[i]

                if curr_pos != 0:
                    ret_since = (p - entry_px) / entry_px if curr_pos == 1 else (entry_px - p) / entry_px
                    if ret_since <= -self.stop_loss_pct:
                        curr_pos = 0
                    elif in_conv:
                        curr_pos = 0
                    elif (curr_pos == 1 and z >= -self.z_exit_threshold) or (curr_pos == -1 and z <= self.z_exit_threshold):
                        curr_pos = 0
                    elif not in_weekend and not in_conv:
                        curr_pos = 0

                if curr_pos == 0 and in_weekend:
                    if z >= self.z_entry_threshold:
                        curr_pos = -1
                        entry_px = p
                    elif z <= -self.z_entry_threshold:
                        curr_pos = 1
                        entry_px = p

                positions[i] = curr_pos

            rolling_vol = ret.rolling(self.rolling_vol_window, min_periods=24).std() * np.sqrt(24 * 365.25)
            rolling_vol = rolling_vol.fillna(0.35).clip(0.12, 1.20)

            adf = pd.DataFrame(index=df.index)
            adf['price'] = price
            adf['beta'] = beta
            adf['excess_drift'] = excess_drift
            adf['z_score'] = z_score
            adf['signal'] = positions
            adf['volatility'] = rolling_vol

            asset_frames[sym] = adf

        return asset_frames

    def compute_correlation_matrix(self, asset_frames: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Computes empirical cross-asset correlation matrix of hourly drift returns.
        """
        drifts = pd.DataFrame({sym: frame['excess_drift'] for sym, frame in asset_frames.items()})
        corr = drifts.corr().round(3)
        return corr

    def compute_portfolio_weights(
        self,
        asset_frames: Dict[str, pd.DataFrame],
        corr_matrix: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Applies Risk-Parity (inverse-volatility) capital allocation across active signals,
        enforcing gross leverage and maximum single-asset position caps.
        """
        common_index = list(asset_frames.values())[0].index
        weights_df = pd.DataFrame(0.0, index=common_index, columns=self.assets)

        for i in range(len(common_index)):
            active_assets = []
            inv_vols = []
            directions = []

            for sym in self.assets:
                sig = asset_frames[sym]['signal'].iloc[i]
                vol = asset_frames[sym]['volatility'].iloc[i]
                if sig != 0 and not np.isnan(vol) and vol > 0:
                    active_assets.append(sym)
                    inv_vols.append(1.0 / vol)
                    directions.append(sig)

            if not active_assets:
                continue

            inv_vols = np.array(inv_vols)
            raw_weights = (inv_vols / np.sum(inv_vols)) * np.array(directions)

            gross = np.sum(np.abs(raw_weights))
            if gross > self.max_gross_leverage:
                raw_weights = raw_weights * (self.max_gross_leverage / gross)

            for idx, w in enumerate(raw_weights):
                sym = active_assets[idx]
                capped_w = np.clip(w, -self.max_single_weight, self.max_single_weight)
                weights_df.loc[common_index[i], sym] = capped_w

        return weights_df
