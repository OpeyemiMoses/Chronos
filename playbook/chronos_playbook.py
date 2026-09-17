"""
Bitget Playbook & GetAgent Integration Template for Chronos
Format compatible with Bitget Playbook / GetAgent Studio sandbox backtesting and paper-trading.
"""

from typing import Dict, Any


class BitgetPlaybookStrategy:
    """
    Chronos 24/7 Information Pricing Strategy adapted for Bitget Playbook environment.
    Can be deployed via:
    npx @bitget-ai/getagent-skill@latest install --client agent
    """

    def __init__(self):
        self.name = "Chronos: 24/7 Weekend Drift Convergence"
        self.symbol = "NVDAUSDT"
        self.benchmark = "BTCUSDT"
        self.timeframe = "1h"
        self.z_entry_threshold = 2.0
        self.z_exit_threshold = 0.4
        self.stop_loss = 0.035
        
    def on_init(self, context: Dict[str, Any]):
        """Initializes state variables and indicators in Bitget Playbook sandbox."""
        context["friday_anchor"] = None
        context["macro_anchor"] = None
        context["position"] = 0
        context["entry_price"] = 0.0
        print(f"[Playbook] {self.name} initialized for {self.symbol}")

    def on_bar(self, bar: Dict[str, Any], context: Dict[str, Any]):
        """
        Called on every hourly candle.
        Evaluates Friday close anchor, weekend excess drift, and Monday convergence.
        """
        timestamp = bar["timestamp"]
        weekday = timestamp.weekday()
        hour = timestamp.hour
        price = bar["close"]
        macro_price = bar.get("macro_close", price)
        
        # 1. Friday 16:00 EST Anchor snapshot
        if weekday == 4 and hour == 16:
            context["friday_anchor"] = price
            context["macro_anchor"] = macro_price
            return

        # 2. Weekend drift evaluation
        is_weekend = (weekday == 4 and hour >= 16) or (weekday in [5, 6]) or (weekday == 0 and hour < 10)
        is_monday_convergence = (weekday == 0 and 8 <= hour <= 9)
        
        # Exit rules
        if context["position"] != 0:
            if is_monday_convergence:
                # Close at Monday convergence
                self.close_position(context, reason="Monday Convergence")
                return
                
            # Stop-loss
            ret = (price - context["entry_price"]) / context["entry_price"] * context["position"]
            if ret <= -self.stop_loss:
                self.close_position(context, reason="Stop Loss")
                return

        # Entry rules
        if context["position"] == 0 and is_weekend and not is_monday_convergence:
            if context["friday_anchor"] is not None:
                token_drift = (price - context["friday_anchor"]) / context["friday_anchor"]
                macro_drift = (macro_price - context["macro_anchor"]) / context["macro_anchor"] if context["macro_anchor"] else 0.0
                
                # Excess drift with estimated beta = 1.3
                excess_drift = token_drift - (1.3 * macro_drift)
                
                # Z-score proxy (typical weekend std ~ 1.5%)
                z = excess_drift / 0.015
                
                if z <= -self.z_entry_threshold:
                    self.open_long(context, price)
                elif z >= self.z_entry_threshold:
                    self.open_short(context, price)

    def open_long(self, context: Dict[str, Any], price: float):
        context["position"] = 1
        context["entry_price"] = price
        print(f"[Playbook Order] BUY LONG {self.symbol} @ {price:.2f}")

    def open_short(self, context: Dict[str, Any], price: float):
        context["position"] = -1
        context["entry_price"] = price
        print(f"[Playbook Order] SELL SHORT {self.symbol} @ {price:.2f}")

    def close_position(self, context: Dict[str, Any], reason: str):
        print(f"[Playbook Order] CLOSE POSITION: {reason}")
        context["position"] = 0
        context["entry_price"] = 0.0
