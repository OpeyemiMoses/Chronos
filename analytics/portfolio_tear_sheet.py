"""
Multi-Asset Portfolio Tear Sheet Generator
Generates institutional publication-quality figures for the 7-asset Chronos basket.
"""

import os
from typing import Dict, Any, List
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class PortfolioTearSheet:
    """
    Renders multi-asset portfolio diagnostics, correlation heatmaps,
    and comparative benchmark plots.
    """

    def __init__(self, output_dir: str = "reports/figures"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._set_style()

    def _set_style(self):
        plt.style.use('dark_background')
        plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, sans-serif'
        plt.rcParams['axes.edgecolor'] = '#2A2E39'
        plt.rcParams['axes.linewidth'] = 0.8
        plt.rcParams['grid.color'] = '#1E222D'
        plt.rcParams['grid.linestyle'] = '--'
        plt.rcParams['grid.alpha'] = 0.6

    def plot_correlation_heatmap(self, corr_df: pd.DataFrame, filename: str = "chronos_correlation_matrix.png") -> str:
        """
        Renders cross-asset correlation matrix heatmap.
        """
        fig, ax = plt.subplots(figsize=(9, 8), dpi=200)
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')

        cax = ax.matshow(corr_df.values, cmap='coolwarm', vmin=-0.2, vmax=1.0)
        fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)

        labels = corr_df.columns.tolist()
        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=10, fontweight='bold', color='#E6EDF3')
        ax.set_yticklabels(labels, fontsize=10, fontweight='bold', color='#E6EDF3')

        # Annotate matrix values
        for i in range(len(labels)):
            for j in range(len(labels)):
                val = corr_df.iloc[i, j]
                text_color = "black" if 0.2 < val < 0.8 else "white"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=text_color, fontweight='bold', fontsize=9)

        ax.set_title("Chronos Multi-Asset Cross-Correlation Matrix (7 Equities + BTC)", fontsize=13, fontweight='bold', color='#00F0FF', pad=20)
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close(fig)
        return filepath

    def plot_comparative_performance(
        self,
        portfolio_equity: pd.DataFrame,
        single_equity: pd.DataFrame,
        filename: str = "chronos_portfolio_cumulative_returns.png"
    ) -> str:
        """
        Plots Comparative Cumulative Returns: Multi-Asset Basket vs Single rNVDA vs S&P 500 benchmark.
        """
        fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')

        if isinstance(portfolio_equity, pd.DataFrame) and 'cum_return' in portfolio_equity.columns:
            port_cum = portfolio_equity['cum_return'] * 100
        else:
            port_cum = (portfolio_equity / portfolio_equity.iloc[0] - 1.0) * 100

        if isinstance(single_equity, pd.DataFrame) and 'cum_return' in single_equity.columns:
            single_cum = single_equity['cum_return'] * 100
        else:
            single_cum = (single_equity / single_equity.iloc[0] - 1.0) * 100

        ax.plot(port_cum.index, port_cum.values, label="Chronos Multi-Asset Basket (7 Tokens, Risk-Parity)", color='#00F0FF', linewidth=2.4)
        ax.plot(single_cum.index, single_cum.values, label="Chronos Single-Asset ($rNVDA)", color='#FF007A', linewidth=1.8, linestyle='--')

        ax.axhline(0, color='#8B949E', linestyle=':', alpha=0.6)
        ax.set_title("Cumulative Performance: Multi-Asset Basket vs. Single-Asset Execution (Net of Fees)", fontsize=13, fontweight='bold', color='#FFFFFF', pad=15)
        ax.set_ylabel("Cumulative Return (%)", fontsize=11, color='#8B949E')
        ax.legend(loc='upper left', frameon=True, facecolor='#161B22', edgecolor='#30363D', fontsize=10)
        ax.grid(True)

        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close(fig)
        return filepath

    def plot_portfolio_summary_tear_sheet(
        self,
        portfolio_result: Dict[str, Any],
        weights_df: pd.DataFrame,
        filename: str = "chronos_portfolio_summary_tear_sheet.png"
    ) -> str:
        """
        Comprehensive multi-panel institutional tear sheet for the basket.
        """
        fig = plt.figure(figsize=(14, 10), dpi=200)
        fig.patch.set_facecolor('#0E1117')
        gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1], hspace=0.3)

        eq_df = portfolio_result["equity_df"]
        metrics = portfolio_result["metrics"]

        # Panel 1: NAV & Cumulative Returns
        ax1 = fig.add_subplot(gs[0])
        ax1.set_facecolor('#0E1117')
        ax1.plot(eq_df.index, eq_df['cum_return'] * 100, color='#00F0FF', lw=2.2, label="Multi-Asset NAV")
        ax1.set_title(
            f"Chronos Institutional Basket — Sharpe: {metrics['sharpe_ratio']} | Sortino: {metrics['sortino_ratio']} | Max DD: {metrics['max_drawdown_pct']}% | Diversification: {metrics['diversification_ratio']}x",
            fontsize=12, fontweight='bold', color='#00F0FF', pad=12
        )
        ax1.set_ylabel("Net Return (%)", color='#8B949E', fontsize=10)
        ax1.grid(True)
        ax1.legend(loc='upper left', facecolor='#161B22', edgecolor='#30363D')

        # Panel 2: Drawdown
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        ax2.set_facecolor('#0E1117')
        ax2.fill_between(eq_df.index, eq_df['drawdown'] * 100, 0, color='#FF4560', alpha=0.35)
        ax2.plot(eq_df.index, eq_df['drawdown'] * 100, color='#FF4560', lw=1.2)
        ax2.set_ylabel("Drawdown (%)", color='#8B949E', fontsize=10)
        ax2.grid(True)

        # Panel 3: Capital Allocation Breakdown Across 7 Assets
        ax3 = fig.add_subplot(gs[2], sharex=ax1)
        ax3.set_facecolor('#0E1117')
        colors = ['#00F0FF', '#7000FF', '#FF007A', '#00E396', '#FEB019', '#775DD0', '#546E7A']
        for idx, col in enumerate(weights_df.columns):
            ax3.plot(weights_df.index, weights_df[col] * 100, lw=1.2, label=col, color=colors[idx % len(colors)], alpha=0.85)
        ax3.set_ylabel("Asset Weight (%)", color='#8B949E', fontsize=10)
        ax3.axhline(0, color='#8B949E', linestyle=':', alpha=0.5)
        ax3.grid(True)
        ax3.legend(loc='upper left', ncol=7, facecolor='#161B22', edgecolor='#30363D', fontsize=8)

        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close(fig)
        return filepath
