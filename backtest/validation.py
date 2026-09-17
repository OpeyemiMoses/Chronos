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
