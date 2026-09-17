"""
Chronos Execution and Friction Model
Simulates exchange fees, bid-ask spread slippage, and net trade fills.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ExecutionModel:
    """
    Simulates institutional execution frictions.
    Bitget VIP / Standard UTA taker fee is typically ~0.04% - 0.06%.
    Bid-ask spread on tokenized assets is ~0.03% - 0.08%.
    """
    taker_fee_pct: float = 0.0005      # 0.05% fee per transaction
    slippage_pct: float = 0.0005       # 0.05% slippage per fill
    
    @property
    def total_one_way_friction(self) -> float:
        return self.taker_fee_pct + self.slippage_pct
        
    def calculate_trade_cost(self, notional_value: float) -> float:
        """Computes dollar cost of a trade execution."""
        return notional_value * self.total_one_way_friction

    def apply_slippage(self, price: float, direction: int) -> float:
        """
        Adjusts execution price adversely based on direction:
        - direction = +1 (Buy): pays higher price (price * (1 + slippage))
        - direction = -1 (Sell): receives lower price (price * (1 - slippage))
        """
        if direction > 0:
            return price * (1.0 + self.slippage_pct)
        elif direction < 0:
            return price * (1.0 - self.slippage_pct)
        return price
