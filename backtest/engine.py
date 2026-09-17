"""
Chronos Backtesting Engine
Executes vectorized and event-driven backtesting with institutional friction modeling.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd

from src.strategy import ChronosConfig, ChronosStrategy
from src.execution_model import ExecutionModel
from src.risk_manager import RiskManager


@dataclass
class BacktestResult:
    """Encapsulates all quantitative metrics and time series from a backtest run."""
    metrics: Dict[str, Any]
    equity_curve: pd.Series
    drawdown_series: pd.Series
    trade_log: pd.DataFrame
    signals_df: pd.DataFrame


class BacktestEngine:
    """
    High-precision backtesting engine for Chronos.
    """

    def __init__(
        self,
        config: Optional[ChronosConfig] = None,
        execution_model: Optional[ExecutionModel] = None,
        risk_manager: Optional[RiskManager] = None
    ):
        self.config = config or ChronosConfig()
        self.execution = execution_model or ExecutionModel(
            taker_fee_pct=self.config.taker_fee_pct,
            slippage_pct=self.config.slippage_pct
        )
        self.risk = risk_manager or RiskManager()
        self.strategy = ChronosStrategy(self.config)

    def run(self, df: pd.DataFrame, initial_capital: float = 100_000.0) -> BacktestResult:
        """
        Executes backtest over the provided DataFrame.
        """
        # 1. Generate strategy signals
        signals_df = self.strategy.generate_signals(df)
        
        # 2. Dynamic Position Sizing
        vol_scalar = self.risk.calculate_volatility_scalar(signals_df['token_close'])
        signals_df['target_weight'] = signals_df['signal'] * vol_scalar
        
        # 3. Simulate Bar-by-Bar Trade Accounting
        n = len(signals_df)
        cash = initial_capital
        position_units = 0.0
        equity = np.zeros(n)
        equity[0] = initial_capital
        
        trades = []
        current_trade = None
        
        prices = signals_df['token_close'].values
        signals = signals_df['signal'].values
        weights = signals_df['target_weight'].values
        timestamps = signals_df.index
        reasons = signals_df['trade_reason'].values
        
        for i in range(1, n):
            current_price = prices[i]
            prev_signal = signals[i - 1]
            curr_signal = signals[i]
            t = timestamps[i]
            
            # Position change event
            if curr_signal != prev_signal:
                # Close existing position if any
                if position_units != 0.0:
                    exit_direction = -1 if position_units > 0 else 1
                    exit_price = self.execution.apply_slippage(current_price, exit_direction)
                    notional_exit = abs(position_units) * exit_price
                    fee_exit = self.execution.calculate_trade_cost(notional_exit)
                    
                    pnl = position_units * (exit_price - current_trade['entry_price']) - fee_exit
                    cash += (position_units * exit_price) - fee_exit
                    
                    current_trade['exit_time'] = t
                    current_trade['exit_price'] = exit_price
                    current_trade['pnl'] = pnl
                    current_trade['pnl_pct'] = pnl / current_trade['notional']
                    current_trade['exit_reason'] = reasons[i] or "Signal Exit"
                    trades.append(current_trade)
                    
                    position_units = 0.0
                    current_trade = None
                
                # Open new position
                if curr_signal != 0:
                    desired_weight = weights[i]
                    portfolio_value = cash
                    target_notional = portfolio_value * abs(desired_weight)
                    
                    entry_direction = 1 if curr_signal > 0 else -1
                    entry_price = self.execution.apply_slippage(current_price, entry_direction)
                    
                    position_units = (target_notional / entry_price) * entry_direction
                    fee_entry = self.execution.calculate_trade_cost(target_notional)
                    cash -= (position_units * entry_price) + fee_entry
                    
                    current_trade = {
                        'entry_time': t,
                        'direction': 'LONG' if curr_signal > 0 else 'SHORT',
                        'entry_price': entry_price,
                        'units': abs(position_units),
                        'notional': target_notional,
                        'fee_entry': fee_entry
                    }
                    
            # Update mark-to-market equity
            equity[i] = cash + (position_units * current_price)
            
        signals_df['equity'] = equity
        signals_df['benchmark_equity'] = initial_capital * (prices / prices[0])
        
        # Calculate Drawdown series
        equity_series = pd.Series(equity, index=timestamps)
        running_max = equity_series.cummax()
        drawdown_series = (equity_series - running_max) / running_max
        signals_df['drawdown'] = drawdown_series
        
        # Trade Log DataFrame
        trade_log = pd.DataFrame(trades)
        
        # Calculate Quantitative Metrics
        metrics = self._calculate_metrics(equity_series, prices, trade_log, initial_capital)
        
        return BacktestResult(
            metrics=metrics,
            equity_curve=equity_series,
            drawdown_series=drawdown_series,
            trade_log=trade_log,
            signals_df=signals_df
        )

    def _calculate_metrics(
        self,
        equity: pd.Series,
        prices: np.ndarray,
        trade_log: pd.DataFrame,
        initial_capital: float
    ) -> Dict[str, Any]:
        """Calculates institutional performance ratios."""
        returns = equity.pct_change().dropna()
        annual_factor = 365.25 * 24  # Hourly candles -> annualized
        
        total_return = (equity.iloc[-1] - initial_capital) / initial_capital
        benchmark_return = (prices[-1] - prices[0]) / prices[0]
        
        # Annualized metrics
        n_days = (equity.index[-1] - equity.index[0]).total_seconds() / 86400
        cagr = ((1.0 + total_return) ** (365.25 / max(n_days, 1))) - 1.0
        
        ann_vol = returns.std() * np.sqrt(annual_factor)
        
        # Sharpe Ratio (Rf = 0%)
        sharpe = (returns.mean() / (returns.std() + 1e-9)) * np.sqrt(annual_factor)
        
        # Downside deviation for Sortino
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std() * np.sqrt(annual_factor)
        sortino = (returns.mean() * annual_factor) / (downside_std + 1e-9)
        
        # Maximum Drawdown
        running_max = equity.cummax()
        dd = (equity - running_max) / running_max
        max_dd = dd.min()
        
        # Calmar Ratio
        calmar = cagr / abs(max_dd) if abs(max_dd) > 0 else 0.0
        
        # Trade metrics
        total_trades = len(trade_log)
        if total_trades > 0:
            win_trades = trade_log[trade_log['pnl'] > 0]
            loss_trades = trade_log[trade_log['pnl'] <= 0]
            win_rate = len(win_trades) / total_trades
            gross_profit = win_trades['pnl'].sum() if len(win_trades) > 0 else 0.0
            gross_loss = abs(loss_trades['pnl'].sum()) if len(loss_trades) > 0 else 1e-6
            profit_factor = gross_profit / gross_loss
            avg_pnl = trade_log['pnl_pct'].mean()
        else:
            win_rate = 0.0
            profit_factor = 0.0
            avg_pnl = 0.0
            
        return {
            "Total Return": f"{total_return * 100:.2f}%",
            "Benchmark Return": f"{benchmark_return * 100:.2f}%",
            "CAGR": f"{cagr * 100:.2f}%",
            "Annualized Volatility": f"{ann_vol * 100:.2f}%",
            "Sharpe Ratio": round(float(sharpe), 2),
            "Sortino Ratio": round(float(sortino), 2),
            "Max Drawdown": f"{max_dd * 100:.2f}%",
            "Calmar Ratio": round(float(calmar), 2),
            "Total Trades": total_trades,
            "Win Rate": f"{win_rate * 100:.1f}%",
            "Profit Factor": round(float(profit_factor), 2),
            "Average PnL per Trade": f"{avg_pnl * 100:.2f}%",
            "Test Period Days": round(n_days, 1)
        }
