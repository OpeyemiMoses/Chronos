"""
Chronos // Bitget Connection & Authentication Diagnostic Test
Verifies API credentials, HMAC-SHA256 signature generator, network reachability,
and live account synchronization with Bitget UTA v3.
"""

import os
import sys
import time
import json
import base64
import hmac
import hashlib
import socket
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

def print_header(title):
    print("\n" + "=" * 76)
    print(f"  {title}")
    print("=" * 76)

def run_diagnostic():
    print_header("CHRONOS // BITGET LIVE INTEGRATION DIAGNOSTIC")

    # 1. Inspect Environment Variables
    print("\n[Step 1] Loading Credentials from .env:")
    api_key = os.getenv("BITGET_API_KEY", "").strip()
    api_secret = os.getenv("BITGET_API_SECRET", "").strip()
    passphrase = os.getenv("BITGET_PASSPHRASE", "").strip()
    base_url = os.getenv("BITGET_REST_URL", "https://api.bitget.com").strip()
    trading_mode = os.getenv("TRADING_MODE", "PAPER").strip()

    if not api_key or not api_secret or not passphrase:
        print("   Incomplete credentials in .env!")
        print(f"     BITGET_API_KEY: {'[SET]' if api_key else '[MISSING]'}")
        print(f"     BITGET_API_SECRET: {'[SET]' if api_secret else '[MISSING]'}")
        print(f"     BITGET_PASSPHRASE: {'[SET]' if passphrase else '[MISSING]'}")
        return

    masked_key = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
    print(f"   BITGET_API_KEY:      {masked_key} (length: {len(api_key)} chars)")
    print(f"   BITGET_API_SECRET:   {'*' * 12}...{api_secret[-4:]} (length: {len(api_secret)} chars)")
    print(f"   BITGET_PASSPHRASE:   {'*' * len(passphrase)} (length: {len(passphrase)} chars)")
    print(f"   BITGET_REST_URL:     {base_url}")
    print(f"   CURRENT TRADING_MODE: {trading_mode}")

    # 2. Test Cryptographic HMAC-SHA256 Signature Generation
    print("\n[Step 2] Testing HMAC-SHA256 Authentication Signature:")
    sample_timestamp = str(int(time.time() * 1000))
    sample_path = "/api/v3/account/assets"
    prehash = sample_timestamp + "GET" + sample_path
    sig = base64.b64encode(
        hmac.new(api_secret.encode("utf-8"), prehash.encode("utf-8"), hashlib.sha256).digest()
    ).decode("utf-8")
    print(f"   Pre-hash Payload: {sample_timestamp}GET{sample_path}")
    print(f"   Generated Sig:   {sig[:16]}... (valid base64 hash)")

    # 3. Network DNS & TCP Route
    print("\n[Step 3] Checking Network Route to api.bitget.com:")
    hostname = base_url.replace("https://", "").replace("http://", "").split("/")[0]
    try:
        ip = socket.gethostbyname(hostname)
        print(f"   DNS Resolution: {hostname} -> {ip}")
        s = socket.create_connection((ip, 443), timeout=4)
        print(f"   TCP Port 443:  Connected successfully")
        s.close()
    except Exception as e:
        print(f"   TCP Connection Failed: {e}")
        return

    # 4. Live TLS Handshake & API Request
    print("\n[Step 4] Dispatching Authenticated Request to Bitget UTA v3:")
    # Generate FRESH timestamp and signature right before the request
    live_timestamp = str(int(time.time() * 1000))
    live_path = "/api/v3/account/assets"
    live_prehash = live_timestamp + "GET" + live_path
    live_sig = base64.b64encode(
        hmac.new(api_secret.encode("utf-8"), live_prehash.encode("utf-8"), hashlib.sha256).digest()
    ).decode("utf-8")
    print(f"  → Timestamp: {live_timestamp}")
    print(f"  → Pre-hash:  {live_timestamp}GET{live_path}")
    headers = {
        "ACCESS-KEY": api_key,
        "ACCESS-SIGN": live_sig,
        "ACCESS-TIMESTAMP": live_timestamp,
        "ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json",
        "locale": "en-US",
        "User-Agent": "Chronos-Quant-Engine/2.0"
    }
    api_url = f"{base_url}/api/v3/account/assets"
    print(f"  → URL: {api_url}")
    req = urllib.request.Request(api_url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print("   HTTP Response Received from Bitget API:")
            print(f"    Code: {data.get('code')}")
            print(f"    Message: {data.get('msg')}")
            if data.get("data"):
                print(f"    Account Data: {json.dumps(data.get('data'), indent=2)}")
            if data.get("code") == "00000":
                print("\n   SUCCESS: Bitget API credentials are fully valid and operational!")
            else:
                print(f"\n  ️ BITGET RESPONSE CODE: {data.get('code')} - {data.get('msg')}")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"  ️ Bitget API Returned HTTP {e.code}:")
        print(f"    {err_msg}")
        try:
            err_json = json.loads(err_msg)
            if err_json.get("code") == "40017":
                print("    -> Note: API key signature error. Verify passphrase or API secret.")
            elif err_json.get("code") == "40014":
                print("    -> Note: Invalid API key. Check key string.")
        except Exception:
            pass
    except Exception as e:
        err_str = str(e)
        print(f"  ️ Network TLS Handshake: {err_str}")
        if "timed out" in err_str.lower() or "handshake" in err_str.lower():
            print("\n  ℹ️ REGIONAL NETWORK DIAGNOSIS:")
            print("     Your TCP packet reached Bitget, but the TLS handshake timed out.")
            print("     This typically happens on telecommunication networks in Nigeria or")
            print("     jurisdictions where crypto domains (bitget.com) are SNI-blocked by ISPs.")
            print("     -> FIX: Turn on a VPN (e.g., Cloudflare WARP 1.1.1.1, ProtonVPN, or any VPN)")
            print("        to encrypt the TLS SNI and connect directly to Bitget.")

    # 5. Chronos BitgetLiveTrader Class Test
    print("\n[Step 5] Testing Chronos BitgetLiveTrader Class (src/bitget_live_trader.py):")
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from src.bitget_live_trader import BitgetLiveTrader

    # Paper mode test
    paper_trader = BitgetLiveTrader(trading_mode="PAPER")
    paper_bal = paper_trader.get_account_balance()
    print(f"   PAPER Mode Balance: ${paper_bal['data'][0]['available']} USDT (Isolated Sandbox)")

    # Order simulation test
    paper_order = paper_trader.place_order(
        symbol="rNVDA",
        side="sell",
        trade_side="open",
        size=10.0,
        price=132.80,
        order_type="market"
    )
    print(f"   PAPER Order Simulation: Order ID {paper_order['data']['orderId']} ({paper_order['data']['mode']})")

    print("\n" + "=" * 76)
    print("  DIAGNOSTIC COMPLETED")
    print("=" * 76)

if __name__ == "__main__":
    run_diagnostic()
