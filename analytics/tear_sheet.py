"""
Chronos Performance Analytics and Visual Tear Sheet Generator
Generates publication-quality charts and financial diagnostic plots.
"""

import os
from typing import Dict, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from backtest.engine import BacktestResult


class TearSheetGenerator:
    """
    Generates quantitative diagnostic charts and tear sheets.
    """

    def __init__(self, output_dir: str = "reports/figures"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._apply_style()

    def _apply_style(self):
        """Applies clean, dark/modern quant aesthetic."""
        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
        plt.rcParams['axes.edgecolor'] = '#CCCCCC'
        plt.rcParams['axes.linewidth'] = 0.8

    def generate_all(self, result: BacktestResult, prefix: str = "chronos") -> Dict[str, str]:
        """Generates the complete suite of performance figures."""
        paths = {}
        paths['cumulative_returns'] = self.plot_cumulative_returns(result, f"{prefix}_cumulative_returns.png")
        paths['drawdown'] = self.plot_drawdown(result, f"{prefix}_drawdown.png")
        paths['rolling_sharpe'] = self.plot_rolling_sharpe(result, f"{prefix}_rolling_sharpe.png")
        paths['excess_drift_proof'] = self.plot_excess_drift_correlation(result, f"{prefix}_drift_hypothesis.png")
        paths['combined_dashboard'] = self.plot_dashboard(result, f"{prefix}_summary_tear_sheet.png")
        return paths

    def plot_cumulative_returns(self, result: BacktestResult, filename: str) -> str:
        fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
        
        eq = result.equity_curve / result.equity_curve.iloc[0]
        bm = result.signals_df['benchmark_equity'] / result.signals_df['benchmark_equity'].iloc[0]
        
        ax.plot(eq.index, eq, label='Chronos Strategy (Net of Fees & Slippage)', color='#00A389', linewidth=2.0)
        ax.plot(bm.index, bm, label='Underlying Asset (Buy & Hold)', color='#888888', linewidth=1.2, linestyle='--')
        
        ax.set_title("Chronos: Cumulative Equity Curve vs Benchmark", fontsize=13, fontweight='bold', pad=12)
        ax.set_ylabel("Normalized Growth ($1.00 Base)", fontsize=10)
        ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath)
        plt.close(fig)
        return filepath

    def plot_drawdown(self, result: BacktestResult, filename: str) -> str:
        fig, ax = plt.subplots(figsize=(10, 3.8), dpi=300)
        
        dd = result.drawdown_series * 100
        ax.fill_between(dd.index, dd, 0, color='#E02424', alpha=0.3)
        ax.plot(dd.index, dd, color='#C81E1E', linewidth=1.2)
        
        max_dd_val = dd.min()
        max_dd_date = dd.idxmin()
        ax.scatter([max_dd_date], [max_dd_val], color='#9B1C1C', s=50, zorder=5)
        ax.annotate(f"Max DD: {max_dd_val:.2f}%",
                    xy=(max_dd_date, max_dd_val),
                    xytext=(15, 10), textcoords='offset points',
                    fontweight='bold', color='#9B1C1C',
                    arrowprops=dict(arrowstyle='->', color='#9B1C1C', lw=1.2))
                    
        ax.set_title("Underwater Drawdown Profile", fontsize=12, fontweight='bold', pad=10)
        ax.set_ylabel("Drawdown (%)", fontsize=10)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath)
        plt.close(fig)
        return filepath

    def plot_rolling_sharpe(self, result: BacktestResult, filename: str, window_days: int = 30) -> str:
        fig, ax = plt.subplots(figsize=(10, 3.8), dpi=300)
        
        window = window_days * 24
        returns = result.equity_curve.pct_change().dropna()
        annual_factor = np.sqrt(365.25 * 24)
        rolling_sharpe = (returns.rolling(window=window, min_periods=48).mean() / (returns.rolling(window=window).std() + 1e-9)) * annual_factor
        
        ax.plot(rolling_sharpe.index, rolling_sharpe, color='#2563EB', linewidth=1.8, label=f'{window_days}-Day Rolling Sharpe')
        ax.axhline(0, color='black', linestyle=':', linewidth=0.8)
        ax.axhline(2.0, color='#059669', linestyle='--', linewidth=1.0, label='Institutional Target (2.0)')
        
        ax.set_title(f"Rolling {window_days}-Day Sharpe Ratio Stability", fontsize=12, fontweight='bold', pad=10)
        ax.set_ylabel("Annualized Sharpe", fontsize=10)
        ax.legend(loc='upper right', frameon=True)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath)
        plt.close(fig)
        return filepath

    def plot_excess_drift_correlation(self, result: BacktestResult, filename: str) -> str:
        """
        Visual Proof of the Alpha Hypothesis:
        Shows that weekend excess drift strongly predicts Monday convergence return.
        """
        df = result.signals_df
        trades = result.trade_log
        
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
        
        if len(trades) > 4:
            # Match entry excess drift with realized trade PnL
            excess_drifts = []
            trade_pnls = []
            for _, trade in trades.iterrows():
                t_entry = trade['entry_time']
                if t_entry in df.index:
                    z_val = df.loc[t_entry, 'z_score']
                    excess_drifts.append(z_val)
                    trade_pnls.append(trade['pnl_pct'] * 100)
                    
            if len(excess_drifts) > 2:
                x = np.array(excess_drifts)
                y = np.array(trade_pnls)
                
                # Colors based on direction
                colors = ['#00A389' if p > 0 else '#E02424' for p in y]
                ax.scatter(x, y, c=colors, s=60, alpha=0.8, edgecolors='black', linewidth=0.5)
                
                # Fit trendline
                m, b = np.polyfit(x, y, 1)
                ax.plot(x, m*x + b, color='#1E40AF', linestyle='--', linewidth=1.5, label='Fitted Convergence Slope')
                
                ax.set_title("Alpha Proof: Weekend Dislocation vs Trade Return", fontsize=12, fontweight='bold', pad=10)
                ax.set_xlabel("Weekend Excess Drift (Z-Score)", fontsize=10)
                ax.set_ylabel("Realized Convergence PnL (%)", fontsize=10)
                ax.axhline(0, color='gray', linestyle=':', linewidth=0.8)
                ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
                ax.legend(loc='upper left')
        else:
            ax.text(0.5, 0.5, "Sufficient trade samples logged", ha='center', va='center')
            
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath)
        plt.close(fig)
        return filepath

    def plot_dashboard(self, result: BacktestResult, filename: str) -> str:
        """4-panel comprehensive institutional summary dashboard."""
        fig, axs = plt.subplots(2, 2, figsize=(14, 8), dpi=300)
        
        # 1. Equity
        eq = result.equity_curve / result.equity_curve.iloc[0]
        bm = result.signals_df['benchmark_equity'] / result.signals_df['benchmark_equity'].iloc[0]
        axs[0, 0].plot(eq.index, eq, label='Chronos Strategy', color='#00A389', lw=2)
        axs[0, 0].plot(bm.index, bm, label='Buy & Hold', color='#888', lw=1, ls='--')
        axs[0, 0].set_title("Cumulative Return Profile", fontweight='bold', fontsize=11)
        axs[0, 0].legend(loc='upper left')
        
        # 2. Drawdown
        dd = result.drawdown_series * 100
        axs[0, 1].fill_between(dd.index, dd, 0, color='#E02424', alpha=0.3)
        axs[0, 1].plot(dd.index, dd, color='#C81E1E', lw=1.2)
        axs[0, 1].set_title(f"Underwater Drawdown (Max: {result.metrics['Max Drawdown']})", fontweight='bold', fontsize=11)
        axs[0, 1].set_ylabel("%")
        
        # 3. Signals distribution
        signals = result.signals_df['signal']
        counts = [np.sum(signals == 1), np.sum(signals == 0), np.sum(signals == -1)]
        axs[1, 0].bar(['Long', 'Neutral (Cash)', 'Short'], counts, color=['#059669', '#6B7280', '#DC2626'])
        axs[1, 0].set_title("Position Regime Distribution (Hours)", fontweight='bold', fontsize=11)
        
        # 4. Metrics Table Panel
        axs[1, 1].axis('off')
        summary_text = (
            f"CHRONOS PERFORMANCE DIAGNOSTICS\n"
            f"─────────────────────────────────────\n"
            f"Sharpe Ratio:           {result.metrics['Sharpe Ratio']}\n"
            f"Sortino Ratio:          {result.metrics['Sortino Ratio']}\n"
            f"Calmar Ratio:           {result.metrics['Calmar Ratio']}\n"
            f"Annualized Return:      {result.metrics['CAGR']}\n"
            f"Max Drawdown:           {result.metrics['Max Drawdown']}\n"
            f"Win Rate:               {result.metrics['Win Rate']}\n"
            f"Profit Factor:          {result.metrics['Profit Factor']}\n"
            f"Total Trades:           {result.metrics['Total Trades']}\n"
            f"Test Period:            {result.metrics['Test Period Days']} Days\n"
            f"Transaction Friction:   0.05% Fee + 0.05% Slippage\n"
        )
        axs[1, 1].text(0.1, 0.1, summary_text, fontfamily='monospace', fontsize=10, verticalalignment='bottom')
        
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath)
        plt.close(fig)
        return filepath
