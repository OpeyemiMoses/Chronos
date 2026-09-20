"""
Chronos // Live Trading Backend Server
Flask API that bridges the dashboard frontend to the Bitget API.
Handles authentication, order execution, position management, and balance sync.

Usage:
    python3 server.py          # Starts on http://localhost:8899
    TRADING_MODE=LIVE python3 server.py   # Enable live trading
"""

import json
import logging
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from src.bitget_live_trader import BitgetLiveTrader

# =========================================================================
# APP SETUP
# =========================================================================

app = Flask(__name__, static_folder="dashboard", static_url_path="")
CORS(app, resources={r"/*": {
    "origins": "*",
    "allow_headers": [
        "Content-Type",
        "Authorization",
        "X-Bitget-Api-Key",
        "X-Bitget-Key",
        "X-Bitget-Api-Secret",
        "X-Bitget-Secret",
        "X-Bitget-Passphrase",
        "X-Trading-Mode"
    ]
}})

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger("Chronos.Server")

# Initialize default trader (reads from .env)
trader = BitgetLiveTrader()

logger.info(f"Default Trading Mode: {trader.trading_mode}")
logger.info(f"Default Live Trading: {'ENABLED' if trader.is_live else 'DISABLED (Paper Mode)'}")
if trader.is_live:
    logger.info(f"Default Server API Key: {trader.api_key[:8]}...{trader.api_key[-4:]}")


def get_trader_for_request(req) -> BitgetLiveTrader:
    """
    Returns an authenticated BitgetLiveTrader for the active request.
    If the client provided their own Bitget API keys (via request headers or JSON body),
    it dynamically instantiates a trader using their credentials.
    Otherwise, it falls back to the server's default trader from .env.
    """
    user_key = (
        req.headers.get("X-Bitget-Api-Key")
        or req.headers.get("X-Bitget-Key")
        or ""
    ).strip()
    user_secret = (
        req.headers.get("X-Bitget-Api-Secret")
        or req.headers.get("X-Bitget-Secret")
        or ""
    ).strip()
    user_passphrase = (
        req.headers.get("X-Bitget-Passphrase")
        or ""
    ).strip()
    user_mode = (
        req.headers.get("X-Trading-Mode")
        or ""
    ).strip().upper()

    # Also inspect JSON payload if present
    if req.is_json:
        data = req.get_json(silent=True) or {}
        gw = data.get("gateway") or {}
        if isinstance(gw, dict):
            user_key = user_key or (gw.get("apiKey") or "").strip()
            user_secret = user_secret or (gw.get("apiSecret") or "").strip()
            user_passphrase = user_passphrase or (gw.get("passphrase") or "").strip()
            user_mode = user_mode or (gw.get("mode") or "").strip().upper()

    # If the user provided all 3 Bitget credentials, use their credentials directly
    if user_key and user_secret and user_passphrase:
        masked = f"{user_key[:4]}...{user_key[-4:]}" if len(user_key) > 8 else "***"
        logger.info(f"[CLIENT GATEWAY] Executing request with user-provided Bitget Key: {masked} (Mode: LIVE)")
        return BitgetLiveTrader(
            api_key=user_key,
            api_secret=user_secret,
            passphrase=user_passphrase,
            trading_mode="LIVE"
        )

    # Fallback to server default trader from .env
    return trader


# =========================================================================
# STATIC FILE SERVING
# =========================================================================

@app.route("/")
def serve_landing():
    """Serve the landing page."""
    return send_from_directory("dashboard", "index.html")


@app.route("/terminal")
@app.route("/app")
def serve_terminal():
    """Serve the trading terminal."""
    return send_from_directory("dashboard", "app.html")


@app.route("/docs")
def serve_docs():
    """Serve the documentation."""
    return send_from_directory("dashboard", "docs.html")


@app.route("/help")
def serve_help():
    """Serve the help page."""
    return send_from_directory("dashboard", "help.html")


# =========================================================================
# API: CONNECTION STATUS
# =========================================================================

@app.route("/api/status", methods=["GET"])
def api_status():
    """
    Returns current connection status, trading mode, and auth health.
    The dashboard calls this on autopilot activation to verify connectivity.
    Supports user-supplied credentials via request headers or query.
    """
    active_trader = get_trader_for_request(request)
    result = active_trader.test_connection()
    result["trading_mode"] = active_trader.trading_mode
    return jsonify(result)


# =========================================================================
# API: ACCOUNT BALANCE
# =========================================================================

@app.route("/api/balance", methods=["GET"])
def api_balance():
    """
    Returns account balance (live from Bitget or simulated paper balance).
    Dashboard syncs this periodically to show real balance.
    Supports user-supplied credentials via request headers.
    """
    active_trader = get_trader_for_request(request)
    resp = active_trader.get_account_balance()

    if resp.get("code") == "00000":
        # Parse balance from response
        data = resp.get("data", [])
        usdt_balance = 0.0
        if isinstance(data, list):
            for asset in data:
                if asset.get("marginCoin") == "USDT" or asset.get("coin") == "USDT":
                    usdt_balance = float(asset.get("available", asset.get("crossedMaxAvailable", "0")))
                    break
            if not usdt_balance and data:
                # Fallback: take first item's available
                usdt_balance = float(data[0].get("available", "0"))
        elif isinstance(data, dict):
            usdt_balance = float(data.get("available", data.get("totalEquity", "0")))

        return jsonify({
            "status": "ok",
            "trading_mode": active_trader.trading_mode,
            "balance_usdt": usdt_balance,
            "raw": resp
        })
    else:
        return jsonify({
            "status": "error",
            "trading_mode": active_trader.trading_mode,
            "message": resp.get("msg", "Failed to fetch balance"),
            "error_code": resp.get("code"),
            "balance_usdt": active_trader._paper_balance if not active_trader.is_live else 0
        }), 400


# =========================================================================
# API: PLACE TRADE
# =========================================================================

@app.route("/api/trade", methods=["POST"])
def api_trade():
    """
    Places a trade order on Bitget.
    Supports user-supplied credentials via request headers or JSON payload.
    
    Expected JSON body:
    {
        "symbol": "rNVDA",
        "side": "SHORT" or "LONG",
        "collateral": 2500,
        "entry_price": 135.50,
        "order_type": "market"  (optional, defaults to "market")
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON body provided"}), 400

    active_trader = get_trader_for_request(request)

    symbol = data.get("symbol")
    side = data.get("side", "").upper()
    collateral = float(data.get("collateral", 0))
    entry_price = float(data.get("entry_price", 0))
    order_type = data.get("order_type", "market")

    if not symbol or not side or collateral <= 0:
        return jsonify({"status": "error", "message": "Missing required fields: symbol, side, collateral"}), 400

    # Calculate position size from collateral and price
    if entry_price > 0:
        size = round(collateral / entry_price, 4)
    else:
        size = collateral  # Fallback: use collateral as size directly

    # Map side to Bitget format
    bitget_side = "sell" if side in ("SHORT", "SELL") else "buy"
    trade_side = "open"

    logger.info(f"[TRADE REQUEST] {side} {symbol} | Collateral: ${collateral} | Size: {size} | Mode: {active_trader.trading_mode}")

    resp = active_trader.place_order(
        symbol=symbol,
        side=bitget_side,
        trade_side=trade_side,
        size=size,
        price=entry_price if order_type == "limit" else None,
        order_type=order_type
    )

    if resp.get("code") == "00000":
        order_data = resp.get("data", {})
        logger.info(f"[TRADE SUCCESS] Order ID: {order_data.get('orderId')} | {side} {symbol}")
        return jsonify({
            "status": "ok",
            "trading_mode": active_trader.trading_mode,
            "order_id": order_data.get("orderId"),
            "symbol": symbol,
            "side": side,
            "size": size,
            "collateral": collateral,
            "order_type": order_type,
            "is_paper": not active_trader.is_live,
            "raw": resp
        })
    else:
        logger.error(f"[TRADE FAILED] {resp.get('msg')} | {side} {symbol}")
        return jsonify({
            "status": "error",
            "trading_mode": active_trader.trading_mode,
            "message": resp.get("msg", "Order placement failed"),
            "error_code": resp.get("code"),
            "symbol": symbol,
            "is_paper": not active_trader.is_live
        }), 400


# =========================================================================
# API: OPEN POSITIONS
# =========================================================================

@app.route("/api/positions", methods=["GET"])
def api_positions():
    """Returns all open futures positions from Bitget (supports user credentials)."""
    active_trader = get_trader_for_request(request)
    resp = active_trader.get_open_positions()

    if resp.get("code") == "00000":
        positions = resp.get("data") or []
        return jsonify({
            "status": "ok",
            "trading_mode": active_trader.trading_mode,
            "positions": positions,
            "count": len(positions)
        })
    else:
        return jsonify({
            "status": "error",
            "trading_mode": active_trader.trading_mode,
            "message": resp.get("msg"),
            "error_code": resp.get("code")
        }), 400


# =========================================================================
# API: CLOSE POSITION
# =========================================================================

@app.route("/api/close", methods=["POST"])
def api_close():
    """
    Closes an open position on Bitget (supports user credentials).
    
    Expected JSON body:
    {
        "symbol": "rNVDA",
        "side": "SHORT" or "LONG"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON body provided"}), 400

    active_trader = get_trader_for_request(request)

    symbol = data.get("symbol")
    side = data.get("side", "")

    if not symbol:
        return jsonify({"status": "error", "message": "Missing required field: symbol"}), 400

    logger.info(f"[CLOSE REQUEST] Closing {side} position on {symbol} | Mode: {active_trader.trading_mode}")

    resp = active_trader.close_position(symbol, side)

    if resp.get("code") == "00000":
        logger.info(f"[CLOSE SUCCESS] {symbol} position closed")
        return jsonify({
            "status": "ok",
            "trading_mode": active_trader.trading_mode,
            "symbol": symbol,
            "raw": resp
        })
    else:
        return jsonify({
            "status": "error",
            "trading_mode": active_trader.trading_mode,
            "message": resp.get("msg"),
            "error_code": resp.get("code")
        }), 400


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8899"))
    print("\n" + "=" * 68)
    print("  CHRONOS // LIVE TRADING SERVER")
    print("=" * 68)
    print(f"  Mode:     {trader.trading_mode}")
    print(f"  Live:     {'YES — REAL TRADES ENABLED' if trader.is_live else 'NO — Paper/Simulation Only'}")
    print(f"  Server:   http://localhost:{port}")
    print(f"  Terminal: http://localhost:{port}/terminal")
    print("=" * 68 + "\n")

    app.run(host="0.0.0.0", port=port, debug=False)
