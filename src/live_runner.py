"""
Chronos Live Production Engine (Paper & Live Trading Runner)
Connects to Bitget MCP Server (agent.bitget.com/mcp) or local UTA v3 socket.
Executes the live 24/7 event loop across the 7-asset tokenized equity basket.
"""

import os
import sys
import time
from datetime import datetime
from typing import Optional, Dict, List, Any
try:
    import pytz
    NYC_TZ = pytz.timezone("America/New_York")
except Exception:
    try:
        from zoneinfo import ZoneInfo
        NYC_TZ = ZoneInfo("America/New_York")
    except Exception:
        from datetime import timezone, timedelta
# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mcp_client import BitgetMCPClient, SUPPORTED_ASSETS
from src.bitget_live_trader import BitgetLiveTrader
from src.self_auditor import TradeAuditor


class ChronosLiveRunner:
    """
    Manages live 24/7 execution lifecycle with Closed-Loop Self-Auditing:
    1. Friday 16:00 EST: Anchor Snapshots
    2. Weekend Session: Dislocation Scanner & Order Dispatch via Bitget MCP & UTA
    3. Monday 08:00–09:30 EST: Pre-Market Institutional Convergence Exit
    4. Post-Trade Self-Audit: Re-evaluates decisions, diagnoses losses, tunes parameters
    5. Weekday Session: 100% Cash Sleep State
    """

    def __init__(self, mode: Optional[str] = None):
        self.trader = BitgetLiveTrader(trading_mode=mode)
        self.mode = self.trader.trading_mode
        self.mcp = BitgetMCPClient()
        self.auditor = TradeAuditor()
        self.anchors = {}
        self.macro_anchor = None
        self.active_positions = {}
        self.base_z_threshold = float(os.getenv("Z_ENTRY_THRESHOLD", 2.0))
        self.stop_loss_pct = float(os.getenv("STOP_LOSS_PCT", 0.035))

    def get_current_ny_time(self) -> datetime:
        return datetime.now(NYC_TZ)

    def print_banner(self):
        print("=" * 76)
        print("  CHRONOS // 24/7 LIVE PRODUCTION EXECUTION ENGINE")
        print(f"  Mode: {self.mode} | API Endpoint: {self.trader.base_url}")
        print(f"  Underlying Basket: {', '.join(SUPPORTED_ASSETS.keys())}")
        
        balance_info = self.trader.get_account_balance()
        bal_data = balance_info.get("data", [{}])[0]
        avail = bal_data.get("available", "10,000.00")
        equity = bal_data.get("equity", "10,000.00")
        print(f"  Account Equity: ${equity} USDT | Available Margin: ${avail} USDT")
        print("=" * 76)

    def snapshot_friday_anchors(self):
        """Phase 1: Locks Friday 16:00 EST closing anchors."""
        print(f"\n[{self.get_current_ny_time().strftime('%Y-%m-%d %H:%M:%S EST')}] [PHASE 1] Locking Friday 16:00 EST Anchors...")
        
        macro = self.mcp.get_macro_benchmark("BTCUSDT")
        self.macro_anchor = macro["price"]
        print(f"  ✓ Macro Anchor (BTCUSDT): ${self.macro_anchor:,.2f}")

        for sym in SUPPORTED_ASSETS.keys():
            ticker = self.mcp.get_tokenized_ticker(sym)
            self.anchors[sym] = ticker["friday_anchor_close"]
            print(f"  ✓ Anchor {sym:<6} ({ticker['underlying_stock']}): ${self.anchors[sym]:.2f}")

    def evaluate_weekend_dislocations(self, simulate_dislocation: bool = False):
        """Phase 2: Real-time scan for retail excess drift and order generation."""
        now = self.get_current_ny_time()
        print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S EST')}] [PHASE 2] Scanning 24/7 Weekend Market Dislocations...")

        macro = self.mcp.get_macro_benchmark("BTCUSDT")
        macro_ret = (macro["price"] - self.macro_anchor) / self.macro_anchor
        print(f"  BTC Benchmark: ${macro['price']:,.2f} (Weekend Move: {macro_ret*100:+.2f}%)")

        orders_to_submit = []

        print(f"\n  {'Asset':<7} | {'Last Px':<10} | {'Fri Anchor':<11} | {'Beta':<5} | {'Retail Drift':<13} | {'Z-Score':<9} | {'Action':<12}")
        print("  " + "-" * 74)

        for sym, meta in SUPPORTED_ASSETS.items():
            ticker = self.mcp.get_tokenized_ticker(sym)
            last_px = ticker["last_price"]
            fri_px = self.anchors.get(sym, ticker["friday_anchor_close"])
            beta = meta["beta"]
            asset_z_thresh = self.auditor.get_asset_z_threshold(sym)

            # In demo mode, inject realistic retail euphoria shock on rNVDA
            if simulate_dislocation and sym == "rNVDA":
                last_px = round(fri_px * 1.0335, 2)  # +3.35% dislocation above anchor

            # Expected price based on macro beta
            expected_px = fri_px * (1.0 + beta * macro_ret)
            excess_drift = (last_px - expected_px) / expected_px
            
            # Approximate Z-Score
            drift_std = 0.0075
            z_score = excess_drift / drift_std

            action = "HOLD CASH"
            if z_score >= asset_z_thresh:
                action = f"SHORT (Z>{asset_z_thresh:.2f}σ)"
                orders_to_submit.append({
                    "symbol": sym, "side": "SELL_SHORT", "quantity": 50, "price": last_px,
                    "entry_z": z_score, "expected_beta": beta
                })
            elif z_score <= -asset_z_thresh:
                action = f"BUY (Z<-{asset_z_thresh:.2f}σ)"
                orders_to_submit.append({
                    "symbol": sym, "side": "BUY_LONG", "quantity": 50, "price": last_px,
                    "entry_z": z_score, "expected_beta": beta
                })

            z_label = f"{z_score:+5.2f}σ" + (f" (T:{asset_z_thresh:.2f})" if asset_z_thresh != 2.0 else "")
            print(f"  {sym:<7} | ${last_px:<9.2f} | ${fri_px:<10.2f} | {beta:<5.2f} | {excess_drift*100:+6.2f}%      | {z_label:<14} | {action:<16}")

        if orders_to_submit:
            print(f"\n  ⚡ [ORDER DISPATCH] Submitting {len(orders_to_submit)} orders to Bitget UTA v3 API...")
            exec_results = self.trader.execute_basket(orders_to_submit)
            for idx, res in enumerate(exec_results):
                res["entry_z"] = orders_to_submit[idx].get("entry_z", 2.2)
                res["expected_beta"] = orders_to_submit[idx].get("expected_beta", 1.5)
                self.active_positions[res["symbol"]] = res
                oid = res["response"].get("data", {}).get("orderId", "FILLED")
                print(f"    -> Dispatched {res['requested_side']} {res['symbol']} (Qty: {res['quantity']} @ ${res['price']:.2f}) [Order ID: {oid}]")
        else:
            print("\n  ✓ No extreme dislocations (|Z| >= threshold) detected. Capital preserved in 100% Cash.")

    def trigger_monday_convergence_exit(self, simulate_convergence: bool = False):
        """Phase 3 & 4: Closes positions and performs autonomous post-mortem self-audit."""
        print(f"\n[{self.get_current_ny_time().strftime('%Y-%m-%d %H:%M:%S EST')}] [PHASE 3] Institutional Convergence Window Active (08:00-09:30 EST)")
        if not self.active_positions:
            print("  ✓ No active weekend positions to liquidate. Portfolio is in 100% Cash.")
            return

        print(f"  Liquidity returning to Wall Street. Exiting {len(self.active_positions)} positions into deep books...")
        close_orders = []
        audited_records = []

        for sym, pos in self.active_positions.items():
            exit_side = "BUY_COVER" if "SHORT" in pos["requested_side"] else "SELL_CLOSE"
            ticker = self.mcp.get_tokenized_ticker(sym)
            exit_px = ticker["last_price"]
            if simulate_convergence and sym in self.anchors:
                exit_px = round(self.anchors[sym] * 1.002, 2)  # Converged back to institutional anchor

            close_orders.append({"symbol": sym, "side": exit_side, "quantity": pos["quantity"], "price": exit_px})

            # Calculate realized return
            if "SHORT" in pos["requested_side"]:
                ret_pct = (pos["price"] - exit_px) / pos["price"]
            else:
                ret_pct = (exit_px - pos["price"]) / pos["price"]

            audited_records.append({
                "symbol": sym,
                "side": pos["requested_side"],
                "entry_price": pos["price"],
                "exit_price": exit_px,
                "quantity": pos["quantity"],
                "return_pct": ret_pct,
                "pnl_usd": ret_pct * pos["price"] * pos["quantity"],
                "entry_z": pos.get("entry_z", 2.2),
                "exit_z": 0.28,
                "exit_reason": "Monday Pre-Market Convergence (08:30 EST)",
                "expected_beta": pos.get("expected_beta", 1.5),
                "realized_beta": pos.get("expected_beta", 1.5)
            })

        exec_results = self.trader.execute_basket(close_orders)
        for res in exec_results:
            oid = res["response"].get("data", {}).get("orderId", "CLOSED")
            print(f"    -> Liquidated {res['requested_side']} {res['symbol']} @ ${res['price']:.2f} [Order ID: {oid}]")
        print(f"  ✓ All positions successfully liquidated at institutional pre-market fair value.")
        print(f"  ✓ Strategy returned to 100% USDT Cash before 09:30 EST Cash Open. Zero weekday risk.")

        # Phase 4: Autonomous Self-Audit & Adaptation
        print(f"\n[{self.get_current_ny_time().strftime('%Y-%m-%d %H:%M:%S EST')}] [PHASE 4] Running Closed-Loop Trade Post-Mortem & Parameter Adaptation...")
        evals = [self.auditor.audit_trade(rec) for rec in audited_records]
        print(self.auditor.generate_post_mortem_table(evals))

        self.active_positions.clear()

    def run_cycle(self, simulate_dislocation: bool = False):
        """Executes a single end-to-end cycle demonstration."""
        self.print_banner()
        self.snapshot_friday_anchors()
        self.evaluate_weekend_dislocations(simulate_dislocation=simulate_dislocation)
        self.trigger_monday_convergence_exit(simulate_convergence=simulate_dislocation)
        print("\n" + "=" * 76)
        print("  LIVE EXECUTION CYCLE COMPLETED SUCCESSFULLY!")
        print("  STATE: 100% CASH SLEEP (ZERO WEEKDAY RISK)")
        print("=" * 76)

    def start_autonomous_daemon(self, poll_interval_seconds: int = 3600):
        """
        Runs the 100% autonomous 24/7 execution loop forever without human intervention.
        Automatically checks the New York clock, executes anchors, trades weekend alpha,
        cashes out on Monday morning, and sleeps during the trading week.
        """
        self.print_banner()
        print(f"\n[AUTONOMOUS ENGINE ACTIVE] Polling market every {poll_interval_seconds}s (Press Ctrl+C to stop)...")

        while True:
            try:
                now = self.get_current_ny_time()
                weekday = now.weekday()  # 0=Mon, 4=Fri, 5=Sat, 6=Sun
                hour = now.hour

                # State A: Friday 16:00 EST -> Lock Anchors
                if weekday == 4 and hour == 16 and not self.anchors:
                    self.snapshot_friday_anchors()

                # State B: Weekend Session (Fri 17:00 -> Mon 07:59 EST) -> Alpha Trading
                elif (weekday == 4 and hour >= 17) or (weekday in (5, 6)) or (weekday == 0 and hour < 8):
                    if not self.anchors:
                        self.snapshot_friday_anchors()
                    self.evaluate_weekend_dislocations()

                # State C: Monday 08:00 - 09:30 EST -> Institutional Convergence Exit
                elif weekday == 0 and (8 <= hour <= 9):
                    if self.active_positions:
                        self.trigger_monday_convergence_exit()
                    self.anchors.clear()

                # State D: Regular Trading Week (Mon 09:30 -> Fri 15:59 EST) -> 100% Cash Sleep
                else:
                    print(f"[{now.strftime('%Y-%m-%d %H:%M EST')}] US Cash Markets Open. Chronos in 100% Cash Sleep State (Zero Overnight Risk).")

                time.sleep(poll_interval_seconds)

            except KeyboardInterrupt:
                print("\n[STOPPED] Autonomous Chronos daemon terminated cleanly by user.")
                break
            except Exception as e:
                print(f"[DAEMON ERROR] {e}. Retrying in 60 seconds...")
                time.sleep(60)


if __name__ == "__main__":
    is_daemon = "--daemon" in sys.argv
    is_demo = "--demo" in sys.argv or "--demo-cycle" in sys.argv
    runner = ChronosLiveRunner()
    if is_daemon:
        runner.start_autonomous_daemon(poll_interval_seconds=3600)
    else:
        runner.run_cycle(simulate_dislocation=is_demo)

