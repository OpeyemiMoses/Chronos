"""
Chronos Autonomous Self-Auditing & Adaptive Reflection Engine
Analyzes completed trade lifecycles, diagnoses root causes of losses/suboptimal exits,
maintains persistent audit memory, and dynamically tunes strategy parameters
to prevent recurring mistakes.
"""

import json
import logging
import os
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional
from tabulate import tabulate

logger = logging.getLogger("Chronos.SelfAuditor")


@dataclass
class TradeAuditEvaluation:
    trade_id: str
    symbol: str
    side: str
    return_pct: float
    pnl_usd: float
    exit_reason: str
    entry_z: float
    exit_z: float
    mae_pct: float
    beta_deviation_pct: float
    verdict: str
    root_cause: str
    corrective_action: str
    timestamp: str


class TradeAuditor:
    """
    Closed-loop self-auditing intelligence for Chronos:
    1. Audits every trade outcome (Win/Loss, MAE, Beta deviation).
    2. Diagnoses root causes (Retail Momentum Overrun, Beta Decoupling, Slippage, Latency).
    3. Adapts strategy parameters (Z-thresholds, single-asset caps, stop-loss buffers).
    4. Persists learned lessons into data/audit_memory.json.
    """

    def __init__(self, memory_path: str = "data/audit_memory.json"):
        self.memory_path = memory_path
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        self.memory = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        """Loads persistent trade audit history and adapted parameter states."""
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not read audit memory ({e}). Initializing fresh.")

        # Default baseline memory
        return {
            "total_audited_trades": 0,
            "win_count": 0,
            "loss_count": 0,
            "cumulative_pnl_usd": 0.0,
            "asset_adjustments": {
                "rNVDA": {"z_entry": 2.0, "weight_cap": 0.25, "consecutive_losses": 0},
                "rTSLA": {"z_entry": 2.0, "weight_cap": 0.25, "consecutive_losses": 0},
                "rAAPL": {"z_entry": 2.0, "weight_cap": 0.25, "consecutive_losses": 0},
                "rCOIN": {"z_entry": 2.0, "weight_cap": 0.25, "consecutive_losses": 0},
                "rMSTR": {"z_entry": 2.0, "weight_cap": 0.25, "consecutive_losses": 0},
                "rSPY":  {"z_entry": 2.0, "weight_cap": 0.25, "consecutive_losses": 0},
                "rQQQ":  {"z_entry": 2.0, "weight_cap": 0.25, "consecutive_losses": 0}
            },
            "recent_post_mortems": []
        }

    def _save_memory(self) -> None:
        """Persists learned parameters and post-mortem logs."""
        try:
            with open(self.memory_path, "w") as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save audit memory: {e}")

    def audit_trade(self, trade: Dict[str, Any]) -> TradeAuditEvaluation:
        """
        Performs rigorous post-trade diagnostic audit on a closed trade.
        """
        sym = trade.get("symbol", "rNVDA")
        side = trade.get("side", "SELL_SHORT")
        entry_px = trade.get("entry_price", 100.0)
        exit_px = trade.get("exit_price", 100.0)
        qty = trade.get("quantity", 10)
        entry_z = trade.get("entry_z", 2.1)
        exit_z = trade.get("exit_z", 0.3)
        exit_reason = trade.get("exit_reason", "Monday Convergence Exit")
        mae_pct = trade.get("mae_pct", 0.012)
        expected_beta = trade.get("expected_beta", 1.5)
        realized_beta = trade.get("realized_beta", 1.5)

        # Calculate exact Return and PnL
        if "SHORT" in side:
            ret_pct = (entry_px - exit_px) / entry_px
        else:
            ret_pct = (exit_px - entry_px) / entry_px

        pnl_usd = ret_pct * (entry_px * qty)
        beta_dev = abs(realized_beta - expected_beta) / max(expected_beta, 1e-4)

        # 1. Diagnose Root Cause & Determine Corrective Action
        if ret_pct > 0:
            verdict = "PROFITABLE_ALPHA_CONVERGENCE"
            root_cause = "Clean Monday institutional liquidity convergence"
            corrective_action = "Maintain baseline model parameters"
            is_win = True
        else:
            is_win = False
            # Differentiate failure modes
            if "Stop-Loss" in exit_reason or mae_pct >= 0.035:
                if beta_dev > 0.35:
                    verdict = "BETA_DECOUPLING"
                    root_cause = f"Asset decoupled from BTC macro beta (Beta err: {beta_dev*100:.1f}%)"
                    corrective_action = f"Reduce {sym} position cap to 15%; expand beta lookback"
                else:
                    verdict = "RETAIL_MOMENTUM_OVERRUN"
                    root_cause = f"Premature entry at {entry_z:.2f}σ; retail hype pushed beyond entry point"
                    corrective_action = f"Raise {sym} entry threshold Z-score from {self.get_asset_z_threshold(sym):.2f}σ to {self.get_asset_z_threshold(sym)+0.25:.2f}σ"
            elif beta_dev > 0.40:
                verdict = "BETA_DECOUPLING"
                root_cause = f"Macro benchmark mismatch during weekend session"
                corrective_action = f"Widen covariance lookback window from 24h to 48h for {sym}"
            else:
                verdict = "CONVERGENCE_LATENCY"
                root_cause = f"Price converged slower than expected in pre-market window"
                corrective_action = f"Extend pre-market exit buffer until 09:15 EST"

        # 2. Closed-Loop Adaptation: Apply parameter adjustments
        asset_state = self.memory["asset_adjustments"].setdefault(sym, {"z_entry": 2.0, "weight_cap": 0.25, "consecutive_losses": 0})
        if not is_win:
            asset_state["consecutive_losses"] += 1
            if verdict == "RETAIL_MOMENTUM_OVERRUN":
                asset_state["z_entry"] = round(min(asset_state["z_entry"] + 0.25, 2.75), 2)
            elif verdict == "BETA_DECOUPLING":
                asset_state["weight_cap"] = round(max(asset_state["weight_cap"] - 0.05, 0.10), 2)
        else:
            # Win reset / decay back to optimal baseline
            asset_state["consecutive_losses"] = 0
            if asset_state["z_entry"] > 2.0:
                asset_state["z_entry"] = round(max(asset_state["z_entry"] - 0.05, 2.0), 2)
            if asset_state["weight_cap"] < 0.25:
                asset_state["weight_cap"] = round(min(asset_state["weight_cap"] + 0.02, 0.25), 2)

        # 3. Update Audit Memory
        self.memory["total_audited_trades"] += 1
        if is_win:
            self.memory["win_count"] += 1
        else:
            self.memory["loss_count"] += 1
        self.memory["cumulative_pnl_usd"] += pnl_usd

        eval_obj = TradeAuditEvaluation(
            trade_id=trade.get("trade_id", f"tr_{int(time.time()*1000)}"),
            symbol=sym,
            side=side,
            return_pct=round(ret_pct * 100, 2),
            pnl_usd=round(pnl_usd, 2),
            exit_reason=exit_reason,
            entry_z=round(entry_z, 2),
            exit_z=round(exit_z, 2),
            mae_pct=round(mae_pct * 100, 2),
            beta_deviation_pct=round(beta_dev * 100, 1),
            verdict=verdict,
            root_cause=root_cause,
            corrective_action=corrective_action,
            timestamp=trade.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S EST"))
        )

        self.memory["recent_post_mortems"].insert(0, asdict(eval_obj))
        self.memory["recent_post_mortems"] = self.memory["recent_post_mortems"][:20]
        self._save_memory()

        return eval_obj

    def get_asset_z_threshold(self, symbol: str) -> float:
        """Returns the currently adapted entry threshold for an asset."""
        return self.memory["asset_adjustments"].get(symbol, {}).get("z_entry", 2.0)

    def get_asset_weight_cap(self, symbol: str) -> float:
        """Returns the currently adapted position cap for an asset."""
        return self.memory["asset_adjustments"].get(symbol, {}).get("weight_cap", 0.25)

    def generate_post_mortem_table(self, audits: List[TradeAuditEvaluation]) -> str:
        """Formats an institutional diagnostic table for the terminal."""
        table_data = []
        for a in audits:
            status = f"+{a.return_pct:.2f}%" if a.return_pct > 0 else f"{a.return_pct:.2f}%"
            table_data.append([
                a.symbol,
                a.side,
                status,
                f"${a.pnl_usd:,.2f}",
                a.verdict,
                a.root_cause,
                a.corrective_action
            ])

        headers = ["Asset", "Side", "Return", "PnL", "Audit Verdict", "Diagnosis / Root Cause", "Self-Adapted Action"]
        return tabulate(table_data, headers=headers, tablefmt="grid")
