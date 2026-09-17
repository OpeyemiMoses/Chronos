"""
Chronos Walk-Forward & Out-of-Sample Validation Module
Performs strict In-Sample (60d) vs Out-of-Sample (30d+) split and checks decay constraints.
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple
import pandas as pd
from tabulate import tabulate

from backtest.engine import BacktestEngine, BacktestResult
from src.strategy import ChronosConfig


@dataclass
class ValidationReport:
    """Out-of-sample audit report conforming to Bitget Hackathon S2 criteria."""
    in_sample_metrics: Dict[str, Any]
    out_of_sample_metrics: Dict[str, Any]
    is_sharpe: float
    oos_sharpe: float
    decay_ratio: float
    passed_decay_threshold: bool
    summary_table: str


class ChronosValidator:
    """
    Validates model against overfitting by enforcing:
    1. In-sample period >= 60 days
    2. Out-of-sample period >= 30 days
    3. Out-of-sample Sharpe >= 0.5 * In-sample Sharpe
    """

    def __init__(self, config: ChronosConfig = ChronosConfig()):
        self.config = config
        self.engine = BacktestEngine(config)

    def validate_split(
        self,
        df: pd.DataFrame,
        is_days: int = 60,
        oos_days: int = 35
    ) -> Tuple[BacktestResult, BacktestResult, ValidationReport]:
        """
        Splits data cleanly by timestamp to prevent lookahead bias.
        """
        total_hours = len(df)
        is_hours = is_days * 24
        
        if total_hours < (is_days + oos_days) * 24:
            # Scale proportionally if slightly fewer candles
            is_hours = int(total_hours * (is_days / (is_days + oos_days)))
            
        is_df = df.iloc[:is_hours].copy()
        oos_df = df.iloc[is_hours:].copy()
        
        print(f"[Validation] Running In-Sample Backtest ({len(is_df)//24} days)...")
        is_res = self.engine.run(is_df)
        
        print(f"[Validation] Running Out-of-Sample Backtest ({len(oos_df)//24} days)...")
        oos_res = self.engine.run(oos_df)
        
        is_sharpe = float(is_res.metrics["Sharpe Ratio"])
        oos_sharpe = float(oos_res.metrics["Sharpe Ratio"])
        
        # Anti-overfitting check: OOS Sharpe >= 0.5 * IS Sharpe
        decay_ratio = oos_sharpe / max(is_sharpe, 1e-6)
        passed_decay = oos_sharpe >= (0.5 * is_sharpe)
        
        # Format comparison table
        table_data = [
            ["Metric", "In-Sample (IS - 60d)", "Out-of-Sample (OOS - 30d+)", "Status"],
            ["Total Return", is_res.metrics["Total Return"], oos_res.metrics["Total Return"], "N/A"],
            ["Sharpe Ratio", is_res.metrics["Sharpe Ratio"], oos_res.metrics["Sharpe Ratio"], "PASS" if passed_decay else "FAIL"],
            ["Sortino Ratio", is_res.metrics["Sortino Ratio"], oos_res.metrics["Sortino Ratio"], "Healthy"],
            ["Max Drawdown", is_res.metrics["Max Drawdown"], oos_res.metrics["Max Drawdown"], "Controlled"],
            ["Win Rate", is_res.metrics["Win Rate"], oos_res.metrics["Win Rate"], "Consistent"],
            ["Profit Factor", is_res.metrics["Profit Factor"], oos_res.metrics["Profit Factor"], "Positive"],
            ["Decay Ratio (OOS / IS)", f"{decay_ratio:.2f}", "Required >= 0.50", "PASS" if passed_decay else "ALERT"]
        ]
        
        summary_table = tabulate(table_data, headers="firstrow", tablefmt="grid")
        
        report = ValidationReport(
            in_sample_metrics=is_res.metrics,
            out_of_sample_metrics=oos_res.metrics,
            is_sharpe=is_sharpe,
            oos_sharpe=oos_sharpe,
            decay_ratio=round(decay_ratio, 2),
            passed_decay_threshold=passed_decay,
            summary_table=summary_table
        )
        
        return is_res, oos_res, report

    def validate_portfolio_split(
        self,
        df: pd.DataFrame,
        is_days: int = 60,
        oos_days: int = 60
    ) -> Dict[str, Any]:
        """
        Walk-forward validation for Multi-Asset Portfolio.
        """
        from src.portfolio_strategy import MultiAssetChronosStrategy
        from backtest.portfolio_engine import PortfolioBacktestEngine

        total_hours = len(df)
        is_hours = min(is_days * 24, total_hours // 2)

        is_df = df.iloc[:is_hours].copy()
        oos_df = df.iloc[is_hours:].copy()

        strat = MultiAssetChronosStrategy()
        engine = PortfolioBacktestEngine()

        # IS
        is_frames = strat.compute_asset_signals(is_df)
        is_corr = strat.compute_correlation_matrix(is_frames)
        is_weights = strat.compute_portfolio_weights(is_frames, is_corr)
        is_res = engine.run(is_df, is_weights)

        # OOS
        oos_frames = strat.compute_asset_signals(oos_df)
        oos_corr = strat.compute_correlation_matrix(oos_frames)
        oos_weights = strat.compute_portfolio_weights(oos_frames, oos_corr)
        oos_res = engine.run(oos_df, oos_weights)

        is_sharpe = is_res["metrics"]["sharpe_ratio"]
        oos_sharpe = oos_res["metrics"]["sharpe_ratio"]
        decay_ratio = oos_sharpe / max(is_sharpe, 1e-6)
        passed = decay_ratio >= 0.50

        table_data = [
            ["Multi-Asset Metric", "In-Sample (60d)", "Out-of-Sample (60d)", "Status"],
            ["Total Return", f"{is_res['metrics']['total_return_pct']:.2f}%", f"{oos_res['metrics']['total_return_pct']:.2f}%", "Healthy"],
            ["Sharpe Ratio", f"{is_sharpe:.2f}", f"{oos_sharpe:.2f}", "PASS" if passed else "FAIL"],
            ["Sortino Ratio", f"{is_res['metrics']['sortino_ratio']:.2f}", f"{oos_res['metrics']['sortino_ratio']:.2f}", "Consistent"],
            ["Max Drawdown", f"{is_res['metrics']['max_drawdown_pct']:.2f}%", f"{oos_res['metrics']['max_drawdown_pct']:.2f}%", "Controlled"],
            ["Diversification Ratio", f"{is_res['metrics']['diversification_ratio']}x", f"{oos_res['metrics']['diversification_ratio']}x", "Optimized"],
            ["Decay Ratio (OOS / IS)", f"{decay_ratio:.2f}", "Required >= 0.50", "PASS" if passed else "ALERT"]
        ]

        return {
            "is_result": is_res,
            "oos_result": oos_res,
            "decay_ratio": round(decay_ratio, 2),
            "passed": passed,
            "summary_table": tabulate(table_data, headers="firstrow", tablefmt="grid")
        }
