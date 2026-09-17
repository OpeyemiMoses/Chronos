"""
Chronos Master Pipeline
Runs the complete quantitative workflow:
1. Historical data ingestion & 24/7 calendar alignment
2. Full period backtesting with transaction frictions
3. In-Sample (60d) vs Out-of-Sample (30d+) walk-forward validation (OS >= 0.5 * IS check)
4. Performance tear sheet figure generation
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.fetcher import ChronosDataFetcher
from src.strategy import ChronosConfig
from backtest.engine import BacktestEngine
from backtest.validation import ChronosValidator
from analytics.tear_sheet import TearSheetGenerator


def run_pipeline():
    print("=" * 70)
    print("  CHRONOS: 24/7 AFTER-HOURS INFORMATION PRICING ENGINE")
    print("  Bitget AI Hackathon S2 - Track 1: Alpha Factory Submission")
    print("=" * 70)

    # 1. Fetch data
    fetcher = ChronosDataFetcher(cache_dir="data/cache")
    df = fetcher.fetch_historical_series(
        token_symbol="NVDA",
        macro_symbol="BTC-USD",
        period="180d",
        interval="1h"
    )

    config = ChronosConfig(
        symbol="rNVDA",
        macro_benchmark="BTC-USD",
        z_entry_threshold=2.0,
        z_exit_threshold=0.4,
        stop_loss_pct=0.035,
        taker_fee_pct=0.0005,
        slippage_pct=0.0005
    )

    # 2. Run Full Backtest
    print("\n[Step 1] Running Full Horizon Backtest...")
    engine = BacktestEngine(config)
    full_result = engine.run(df)

    print("\n" + "=" * 50)
    print("  FULL BACKTEST PERFORMANCE SUMMARY")
    print("=" * 50)
    for k, v in full_result.metrics.items():
        print(f"  {k:<26}: {v}")
    print("=" * 50)

    # 3. Strict Walk-Forward Out-of-Sample Validation
    print("\n[Step 2] Performing In-Sample (60d) vs Out-of-Sample (35d+) Audit...")
    validator = ChronosValidator(config)
    is_res, oos_res, val_report = validator.validate_split(df, is_days=60, oos_days=35)

    print("\n" + val_report.summary_table)

    if val_report.passed_decay_threshold:
        print("\n✅ AUDIT PASSED: Out-of-Sample Sharpe decay constraint met (OOS Sharpe >= 0.5 * IS Sharpe).")
    else:
        print("\n⚠️ AUDIT ALERT: Out-of-Sample Sharpe decayed below 50% threshold.")

    # 4. Generate Visual Tear Sheets
    print("\n[Step 3] Generating Publication-Grade Tear Sheets...")
    generator = TearSheetGenerator(output_dir="reports/figures")
    fig_paths = generator.generate_all(full_result, prefix="chronos")

    for name, path in fig_paths.items():
        print(f"  Generated: {path}")

    print("\n" + "=" * 70)
    print("  PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("  Reports and figures saved to: reports/figures/")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
