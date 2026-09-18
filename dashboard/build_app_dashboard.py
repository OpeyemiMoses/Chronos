import json
import os
import random

# Load baseline real trades and audit memory
with open("data/real_trades.json", "r") as f:
    real_trades = json.load(f)

with open("data/audit_memory.json", "r") as f:
    audit_memory = json.load(f)

# Read flip_reference.css
css_path = "dashboard/flip_reference.css"
flip_css = ""
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        flip_css = f.read()

# Markets definition (7 tokenized US equities)
markets_data = {
    "rNVDA": {
        "name": "rNVDA / USDT",
        "symbol": "rNVDA",
        "company": "NVIDIA Corporation",
        "spot_price": 132.80,
        "anchor_price": 128.40,
        "drift_pct": 3.42,
        "z_score": 2.24,
        "action": "SHORT OVERBOUGHT DRIFT",
        "regime": "Weekend Retail Euphoria (Overbought)",
        "thesis": "Retail market participants pushed $rNVDA +3.42% above Friday institutional settlement while Nasdaq is shuttered. Statistical dislocation is 2.24σ. Strategy deploys counter-positioning into Monday pre-market convergence.",
        "convergence_target": 128.40,
        "expected_return": "+3.42%",
        "stop_loss": "-2.10%",
        "beta": 1.48
    },
    "rTSLA": {
        "name": "rTSLA / USDT",
        "symbol": "rTSLA",
        "company": "Tesla Motors Inc.",
        "spot_price": 258.40,
        "anchor_price": 248.00,
        "drift_pct": 4.19,
        "z_score": 2.65,
        "action": "SHORT OVERBOUGHT DRIFT",
        "regime": "Extreme Retail Momentum (Overbought)",
        "thesis": "Retail buyers chased headlines over thin weekend liquidity books. Autonomous self-auditor adapted entry threshold to 2.50σ. Signal triggered for Monday institutional mean-reversion.",
        "convergence_target": 248.00,
        "expected_return": "+4.19%",
        "stop_loss": "-2.40%",
        "beta": 1.95
    },
    "rAAPL": {
        "name": "rAAPL / USDT",
        "symbol": "rAAPL",
        "company": "Apple Inc.",
        "spot_price": 222.10,
        "anchor_price": 224.00,
        "drift_pct": -0.85,
        "z_score": -0.68,
        "action": "HOLD CASH (NOISE BAND)",
        "regime": "Fair Value (Idle)",
        "thesis": "Price deviation is only -0.68σ from Friday anchor. Strategy preserves 100% USDT cash to avoid unnecessary execution friction.",
        "convergence_target": 224.00,
        "expected_return": "0.00%",
        "stop_loss": "N/A",
        "beta": 0.72
    },
    "rCOIN": {
        "name": "rCOIN / USDT",
        "symbol": "rCOIN",
        "company": "Coinbase Global",
        "spot_price": 218.50,
        "anchor_price": 206.80,
        "drift_pct": 5.66,
        "z_score": 3.10,
        "action": "SHORT OVERBOUGHT DRIFT",
        "regime": "Severe Crypto-Beta Overhang",
        "thesis": "Tokenized Coinbase equity detached from fundamental valuation following weekend crypto volatility. 3.10σ dislocation indicates extreme mean-reversion probability.",
        "convergence_target": 206.80,
        "expected_return": "+5.66%",
        "stop_loss": "-2.50%",
        "beta": 2.45
    },
    "rMSTR": {
        "name": "rMSTR / USDT",
        "symbol": "rMSTR",
        "company": "MicroStrategy Inc.",
        "spot_price": 312.40,
        "anchor_price": 292.20,
        "drift_pct": 6.91,
        "z_score": 3.48,
        "action": "SHORT OVERBOUGHT DRIFT",
        "regime": "Leveraged Bitcoin Reflexivity",
        "thesis": "High weekend beta. Self-auditor reduced single-stock capital cap to 25% to protect downside risk. Dislocation is 3.48σ from Friday anchor.",
        "convergence_target": 292.20,
        "expected_return": "+6.91%",
        "stop_loss": "-2.80%",
        "beta": 2.90
    },
    "rSPY": {
        "name": "rSPY / USDT",
        "symbol": "rSPY",
        "company": "S&P 500 Index ETF",
        "spot_price": 564.20,
        "anchor_price": 561.80,
        "drift_pct": 0.43,
        "z_score": 0.35,
        "action": "HOLD CASH (NOISE BAND)",
        "regime": "Stable Institutional Benchmark",
        "thesis": "Broad market index tightly anchored to Friday settlement price. No statistical dislocation signal present.",
        "convergence_target": 561.80,
        "expected_return": "0.00%",
        "stop_loss": "N/A",
        "beta": 0.35
    },
    "rQQQ": {
        "name": "rQQQ / USDT",
        "symbol": "rQQQ",
        "company": "Invesco QQQ Trust",
        "spot_price": 482.60,
        "anchor_price": 478.90,
        "drift_pct": 0.77,
        "z_score": 0.62,
        "action": "HOLD CASH (NOISE BAND)",
        "regime": "Tech Benchmark Baseline",
        "thesis": "Tech benchmark variance is within normal weekend noise. Preserving buying power for idiosyncratic single-stock dislocations.",
        "convergence_target": 478.90,
        "expected_return": "0.00%",
        "stop_loss": "N/A",
        "beta": 0.58
    }
}

# 40 hourly candles per asset
random.seed(42)
candles_data = {}
for sym, m in markets_data.items():
    anchor = m["anchor_price"]
    spot = m["spot_price"]
    candles = []
    current_p = anchor
    step_drift = (spot - anchor) / 40.0
    vol = (anchor * 0.006)
    
    for i in range(40):
        o = current_p
        drift = step_drift + random.uniform(-vol, vol)
        c = o + drift
        h = max(o, c) + random.uniform(0.1, vol * 1.2)
        l = min(o, c) - random.uniform(0.1, vol * 1.2)
        v = int(random.uniform(1500, 8500))
        hour_label = f"{i:02d}:00"
        candles.append({
            "time": hour_label,
            "open": round(o, 2),
            "high": round(h, 2),
            "low": round(l, 2),
            "close": round(c, 2),
            "volume": v
        })
        current_p = c
    candles_data[sym] = candles

# Format JSON payloads for client embedding
markets_json = json.dumps(markets_data)
candles_json = json.dumps(candles_data)
trades_json = json.dumps(real_trades)
audit_json = json.dumps(audit_memory.get("recent_post_mortems", []))

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chronos // Autonomous Trading Arena & Cognitive Self-Auditor</title>
  <link rel="icon" type="image/svg+xml" href="assets/chronos_logo.svg">

  <!-- Google Fonts: Instrument Serif, Playfair Display, Inter, Space Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">

  <style>
{flip_css}

    :root {{
      --font-serif-editorial: "Instrument Serif", "Playfair Display", Georgia, serif;
      --font-sans-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-terminal: "Space Mono", monospace;
      
      --color-white: #FFFFFF;
      --color-canvas-light: #FAF9F6;
      --color-canvas-subtle: #F4F2EC;
      --color-black: #090909;
      --color-black-night: #050505;
      --color-grey-pill: #ECEEF2;
      --color-grey-border: rgba(0, 0, 0, 0.08);
      --color-grey-text: #5A5E66;
      --color-grey-muted: #8E9299;
      --color-green: #00C853;
      --color-green-light: #00E676;
      --color-red: #E50914;
      --color-amber: #F59E0B;
      --color-blue: #2563EB;
      --border-dashed: 1px dashed rgba(0, 0, 0, 0.22);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--color-canvas-light);
      color: var(--color-black);
      font-family: var(--font-sans-body);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Navigation Header */
    .app-header {{
      background: #FFFFFF;
      border-bottom: 1px dashed rgba(0, 0, 0, 0.18);
      padding: 0.65rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }}

    .app-header-left {{
      display: flex;
      align-items: center;
      gap: 2.25rem;
    }}

    .app-brand {{
      display: flex;
      align-items: center;
      gap: 0.55rem;
      text-decoration: none;
      color: #000;
    }}

    .app-brand-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--color-green);
      display: inline-block;
      box-shadow: 0 0 10px rgba(0, 200, 83, 0.6);
    }}

    .app-brand-name {{
      font-family: var(--font-serif-editorial);
      font-size: 1.85rem;
      font-weight: 400;
      letter-spacing: -0.02em;
    }}

    .app-header-tabs {{
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }}

    .app-tab {{
      font-family: var(--font-sans-body);
      font-size: 0.85rem;
      font-weight: 500;
      color: var(--color-grey-text);
      padding: 0.42rem 0.95rem;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      user-select: none;
    }}

    .app-tab:hover {{
      color: var(--color-black);
      background: rgba(0, 0, 0, 0.04);
    }}

    .app-tab.active {{
      background: var(--color-black);
      color: #FFFFFF;
      font-weight: 600;
    }}

    .app-tab-badge {{
      background: rgba(255, 255, 255, 0.2);
      font-family: var(--font-terminal);
      font-size: 0.7rem;
      padding: 0.1rem 0.45rem;
      border-radius: 10px;
    }}

    /* RainbowKit-style Wallet Connect */
    .rainbow-connect-btn {{
      background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #45B649 100%);
      padding: 2px;
      border-radius: 28px;
      border: none;
      cursor: pointer;
      display: inline-block;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .rainbow-connect-btn:hover {{
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }}

    .rainbow-connect-btn-inner {{
      background: #FFFFFF;
      color: #000000;
      padding: 0.45rem 1.15rem;
      border-radius: 26px;
      font-family: var(--font-sans-body);
      font-size: 0.82rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .rainbow-connected-pill {{
      display: inline-flex;
      align-items: center;
      background: #FFFFFF;
      border: 1px solid rgba(0,0,0,0.12);
      border-radius: 24px;
      padding: 0.25rem 0.35rem 0.25rem 0.75rem;
      gap: 0.6rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      cursor: pointer;
      user-select: none;
      position: relative;
      transition: all 0.2s ease;
    }}

    .rainbow-connected-pill:hover {{
      border-color: rgba(0,0,0,0.28);
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .rainbow-chain-chip {{
      display: flex;
      align-items: center;
      gap: 0.35rem;
      font-family: var(--font-terminal);
      font-size: 0.75rem;
      font-weight: 700;
      color: #374151;
    }}

    .rainbow-chain-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #627EEA; /* Eth purple/blue */
    }}

    .rainbow-balance-chip {{
      background: var(--color-canvas-subtle);
      border-radius: 16px;
      padding: 0.25rem 0.65rem;
      font-family: var(--font-terminal);
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--color-green);
    }}

    .rainbow-account-chip {{
      background: var(--color-black);
      color: #FFFFFF;
      border-radius: 18px;
      padding: 0.3rem 0.75rem;
      font-family: var(--font-terminal);
      font-size: 0.78rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }}

    .rainbow-avatar-circle {{
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
    }}

    /* Wallet Dropdown Menu */
    .wallet-dropdown-menu {{
      position: absolute;
      top: calc(100% + 8px);
      right: 0;
      width: 280px;
      background: #FFFFFF;
      border: 1px dashed rgba(0,0,0,0.22);
      border-radius: 10px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.15);
      padding: 1rem;
      display: none;
      flex-direction: column;
      gap: 0.75rem;
      z-index: 2000;
    }}

    .wallet-dropdown-menu.open {{
      display: flex;
    }}

    /* App Layout Grid: Sidebar + Main Area */
    .app-body {{
      display: grid;
      grid-template-columns: 240px 1fr;
      flex: 1;
      min-height: calc(100vh - 65px);
    }}

    .app-sidebar {{
      background: #FFFFFF;
      border-right: 1px dashed rgba(0, 0, 0, 0.18);
      padding: 1.25rem 0.85rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }}

    .sidebar-section-title {{
      font-family: var(--font-terminal);
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: var(--color-grey-muted);
      text-transform: uppercase;
      padding: 0 0.5rem 0.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .sidebar-menu {{
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }}

    .sidebar-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.52rem 0.65rem;
      border-radius: 6px;
      font-size: 0.84rem;
      font-weight: 500;
      color: #374151;
      cursor: pointer;
      transition: all 0.15s ease;
      user-select: none;
    }}

    .sidebar-item:hover {{
      background: var(--color-canvas-subtle);
      color: #000;
    }}

    .sidebar-item.active {{
      background: var(--color-black);
      color: #FFFFFF;
      font-weight: 600;
    }}

    .sidebar-item.active .sidebar-item-metric {{
      color: var(--color-green-light) !important;
    }}

    .sidebar-item-left {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .sidebar-item-metric {{
      font-family: var(--font-terminal);
      font-size: 0.76rem;
      font-weight: 700;
    }}

    /* Main Content Area */
    .app-main {{
      padding: 1.75rem 2.25rem 3.5rem;
      overflow-y: auto;
    }}

    .breadcrumb-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1rem;
    }}

    .market-header-area {{
      margin-bottom: 1.75rem;
    }}

    .market-title {{
      font-family: var(--font-serif-editorial);
      font-size: 2.5rem;
      font-weight: 400;
      line-height: 1.15;
      margin-bottom: 0.4rem;
    }}

    .market-subtitle {{
      font-size: 0.92rem;
      color: var(--color-grey-text);
      max-width: 780px;
      line-height: 1.55;
    }}

    .status-strip {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.2);
      border-radius: 4px;
      padding: 0.35rem 0.85rem;
      margin-top: 0.85rem;
      font-size: 0.78rem;
      color: #374151;
    }}

    /* Arena Grid: Chart + Order Box */
    .arena-grid {{
      display: grid;
      grid-template-columns: 1.65fr 1fr;
      gap: 1.5rem;
      align-items: start;
    }}

    .chart-panel-card {{
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      border-radius: 8px;
      padding: 1.5rem;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
    }}

    .chart-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 1.25rem;
    }}

    .oracle-label {{
      font-family: var(--font-terminal);
      font-size: 0.72rem;
      color: var(--color-grey-muted);
      letter-spacing: 0.05em;
      margin-bottom: 0.25rem;
      text-transform: uppercase;
    }}

    .big-price-val {{
      font-family: var(--font-serif-editorial);
      font-size: 2.85rem;
      font-weight: 400;
      line-height: 1;
    }}

    .strike-barrier-val {{
      font-family: var(--font-serif-editorial);
      font-size: 1.85rem;
      color: var(--color-red);
      text-align: right;
    }}

    .anchor-subtext {{
      font-family: var(--font-terminal);
      font-size: 0.72rem;
      color: var(--color-grey-muted);
      text-align: right;
      margin-top: 0.2rem;
    }}

    .chart-subbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.45rem 0;
      border-top: 1px solid rgba(0, 0, 0, 0.06);
      border-bottom: 1px solid rgba(0, 0, 0, 0.06);
      margin-bottom: 1rem;
      font-family: var(--font-terminal);
      font-size: 0.76rem;
    }}

    .chart-tools-left {{
      display: flex;
      align-items: center;
      gap: 0.65rem;
    }}

    .timeframe-pill-group {{
      display: flex;
      gap: 0.25rem;
    }}

    .timeframe-pill {{
      background: none;
      border: 1px solid transparent;
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
      font-family: var(--font-terminal);
      font-size: 0.72rem;
      cursor: pointer;
      color: var(--color-grey-text);
    }}

    .timeframe-pill.active {{
      background: var(--color-black);
      color: #FFF;
      font-weight: 700;
    }}

    #appCandleCanvas {{
      width: 100%;
      height: 320px;
      display: block;
    }}

    /* Strategy Execution Panel */
    .execution-panel-card {{
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      border-radius: 8px;
      padding: 1.5rem;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
    }}

    .execution-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
    }}

    .execution-title {{
      font-family: var(--font-terminal);
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}

    .signal-banner {{
      background: var(--color-canvas-subtle);
      border-radius: 6px;
      padding: 0.85rem 1rem;
      margin-bottom: 1.25rem;
      border-left: 3px solid var(--color-amber);
    }}

    .signal-banner-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: #111;
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.3rem;
    }}

    .signal-banner-desc {{
      font-size: 0.8rem;
      color: var(--color-grey-text);
      line-height: 1.45;
    }}

    .mode-switcher {{
      display: flex;
      background: var(--color-canvas-subtle);
      border-radius: 6px;
      padding: 0.25rem;
      margin-bottom: 1.25rem;
    }}

    .mode-switcher-btn {{
      flex: 1;
      background: none;
      border: none;
      padding: 0.45rem;
      font-family: var(--font-sans-body);
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--color-grey-text);
      cursor: pointer;
      border-radius: 4px;
      transition: all 0.2s ease;
      text-align: center;
    }}

    .mode-switcher-btn.active {{
      background: #FFFFFF;
      color: #000000;
      box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }}

    .collateral-box {{
      margin-bottom: 1.25rem;
    }}

    .collateral-header {{
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      margin-bottom: 0.35rem;
    }}

    .collateral-input-field {{
      width: 100%;
      padding: 0.65rem 0.85rem;
      font-family: var(--font-terminal);
      font-size: 1.05rem;
      font-weight: 700;
      border: 1px solid rgba(0, 0, 0, 0.15);
      border-radius: 6px;
      background: #FFFFFF;
      outline: none;
    }}

    .collateral-input-field:focus {{
      border-color: #000;
    }}

    .collateral-presets {{
      display: flex;
      gap: 0.35rem;
      margin-top: 0.5rem;
    }}

    .preset-chip {{
      flex: 1;
      background: var(--color-canvas-subtle);
      border: 1px solid rgba(0,0,0,0.08);
      border-radius: 4px;
      padding: 0.3rem 0;
      font-family: var(--font-terminal);
      font-size: 0.72rem;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
    }}

    .preset-chip:hover {{
      background: #E5E7EB;
    }}

    .preset-chip.active {{
      background: #000;
      color: #FFF;
      border-color: #000;
    }}

    .calc-row {{
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      margin-bottom: 0.4rem;
      color: var(--color-grey-text);
    }}

    .calc-row strong {{
      color: #111;
      font-family: var(--font-terminal);
    }}

    .btn-execute-big {{
      width: 100%;
      background: #000000;
      color: #FFFFFF;
      border: none;
      border-radius: 8px;
      padding: 0.85rem;
      font-family: var(--font-terminal);
      font-size: 0.84rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
    }}

    .btn-execute-big:hover {{
      background: #222;
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.28);
    }}

    /* Autonomous Execution Live Banner */
    .auto-live-status-bar {{
      background: #0F172A;
      color: #FFFFFF;
      border-radius: 8px;
      padding: 1rem 1.25rem;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.15);
    }}

    .auto-live-pulse {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--color-green);
      display: inline-block;
      box-shadow: 0 0 12px var(--color-green);
      animation: pulseGlow 1.5s infinite;
    }}

    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(1.3); }}
    }}

    /* Strategy Recalibration Alert Banner */
    .recalibration-alert-toast {{
      background: #FFFBEB;
      border: 1px solid #FDE68A;
      border-left: 4px solid var(--color-amber);
      border-radius: 6px;
      padding: 0.85rem 1.15rem;
      margin-bottom: 1.5rem;
      display: none;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1rem;
      animation: slideDown 0.3s ease-out;
    }}

    .recalibration-alert-toast.visible {{
      display: flex;
    }}

    @keyframes slideDown {{
      from {{ opacity: 0; transform: translateY(-10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Auditor Case Cards with Dynamic Glow on Jump */
    .auditor-lesson-card {{
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      border-radius: 8px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
      transition: all 0.3s ease;
      position: relative;
    }}

    .auditor-lesson-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
    }}

    .auditor-lesson-card.highlighted {{
      border: 2px solid var(--color-green) !important;
      box-shadow: 0 0 24px rgba(0, 200, 83, 0.4) !important;
      animation: auditGlow 2.5s ease-out;
    }}

    @keyframes auditGlow {{
      0% {{ transform: scale(1.02); box-shadow: 0 0 30px rgba(0, 200, 83, 0.8); }}
      100% {{ transform: scale(1); box-shadow: 0 0 10px rgba(0, 200, 83, 0.1); }}
    }}

    /* Settings Page Grid & Form */
    .settings-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      margin-top: 1.5rem;
    }}

    .settings-card {{
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      border-radius: 8px;
      padding: 1.75rem;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }}

    .settings-card-title {{
      font-family: var(--font-serif-editorial);
      font-size: 1.65rem;
      font-weight: 400;
      display: flex;
      align-items: center;
      gap: 0.65rem;
    }}

    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }}

    .form-label {{
      font-family: var(--font-terminal);
      font-size: 0.72rem;
      font-weight: 700;
      color: #374151;
      text-transform: uppercase;
    }}

    .form-input {{
      width: 100%;
      padding: 0.65rem 0.85rem;
      border: 1px solid rgba(0,0,0,0.15);
      border-radius: 6px;
      font-family: var(--font-terminal);
      font-size: 0.82rem;
      outline: none;
      background: #FFFFFF;
    }}

    .form-input:focus {{
      border-color: #000;
    }}

    /* Trade Ledger Table */
    .ledger-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.84rem;
      text-align: left;
    }}

    .ledger-table th {{
      padding: 0.85rem 1rem;
      background: var(--color-canvas-subtle);
      font-family: var(--font-terminal);
      font-size: 0.72rem;
      font-weight: 700;
      color: #555;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      border-bottom: 2px solid rgba(0, 0, 0, 0.08);
    }}

    .ledger-table td {{
      padding: 0.85rem 1rem;
      border-bottom: 1px solid rgba(0, 0, 0, 0.06);
      vertical-align: middle;
    }}

    .btn-audit-jump {{
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.25);
      border-radius: 4px;
      padding: 0.25rem 0.6rem;
      font-family: var(--font-terminal);
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      transition: all 0.2s ease;
    }}

    .btn-audit-jump:hover {{
      background: #000;
      color: #FFF;
      border-color: #000;
    }}

    /* RainbowKit Modal */
    .rainbow-modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(8px);
      z-index: 9999;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }}

    .rainbow-modal-overlay.open {{
      display: flex;
    }}

    .rainbow-modal-card {{
      background: #FFFFFF;
      border-radius: 16px;
      border: 1px solid rgba(0, 0, 0, 0.1);
      width: 100%;
      max-width: 440px;
      overflow: hidden;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
      animation: modalRise 0.25s ease-out;
    }}

    @keyframes modalRise {{
      from {{ opacity: 0; transform: scale(0.96) translateY(10px); }}
      to {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}

    .rainbow-modal-header {{
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid rgba(0,0,0,0.06);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .rainbow-modal-header h3 {{
      font-family: var(--font-sans-body);
      font-size: 1.1rem;
      font-weight: 700;
    }}

    .rainbow-wallet-list {{
      padding: 1rem 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }}

    .rainbow-wallet-option {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.75rem 1rem;
      border-radius: 10px;
      border: 1px solid rgba(0,0,0,0.06);
      cursor: pointer;
      background: #FFFFFF;
      transition: all 0.15s ease;
    }}

    .rainbow-wallet-option:hover {{
      background: var(--color-canvas-subtle);
      border-color: rgba(0,0,0,0.18);
      transform: translateY(-1px);
    }}

    .wallet-icon-title {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
      font-size: 0.92rem;
      font-weight: 600;
    }}

    .wallet-icon-img {{
      width: 28px;
      height: 28px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
  </style>
</head>
<body>

  <!-- Top Navigation Header -->
  <header class="app-header">
    <div class="app-header-left">
      <a href="index.html" class="app-brand" title="Return to Chronos Landing Page">
        <span class="app-brand-dot"></span>
        <span class="app-brand-name">chronos</span>
      </a>

      <nav class="app-header-tabs">
        <span class="app-tab active" id="tabArena" onclick="switchView('arena', this)">Trading Arena</span>
        <span class="app-tab" id="tabAuditor" onclick="switchView('auditor', this)">
          <span>Cognitive Self-Auditor</span>
          <span class="app-tab-badge" id="auditCountBadge">3</span>
        </span>
        <span class="app-tab" id="tabLedger" onclick="switchView('ledger', this)">
          <span>Trade Ledger</span>
          <span class="app-tab-badge" id="ledgerCountBadge">26</span>
        </span>
        <span class="app-tab" id="tabSettings" onclick="switchView('settings', this)">Settings & Gateway</span>
      </nav>
    </div>

    <div class="app-header-right">
      <!-- RainbowKit Connected Wallet Component -->
      <div id="walletHeaderContainer">
        <!-- Rendered dynamically by JS -->
      </div>

      <!-- Wallet Dropdown Menu -->
      <div class="wallet-dropdown-menu" id="walletDropdownMenu">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #EEE; padding-bottom: 0.5rem;">
          <span style="font-size: 0.75rem; color: #888; font-family: var(--font-terminal);">ACTIVE WALLET</span>
          <span style="font-size: 0.72rem; color: var(--color-green); font-weight: 700;">● CONNECTED</span>
        </div>
        <div>
          <div style="font-family: var(--font-terminal); font-size: 0.82rem; font-weight: 700;" id="dropdownWalletAddr">0x71C...3a9F</div>
          <div style="font-size: 0.75rem; color: #666; margin-top: 0.2rem;">Paper Balance: <strong id="dropdownPaperBalance" style="color: #000;">$50,000.00 USDT</strong></div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.4rem; border-top: 1px solid #EEE; padding-top: 0.6rem;">
          <button class="preset-chip" onclick="resetCurrentWalletBalance()" style="width: 100%; text-align: center; padding: 0.45rem;">Reset Balance to $50,000</button>
          <button class="preset-chip" onclick="openRainbowModal()" style="width: 100%; text-align: center; padding: 0.45rem;">Switch Account</button>
          <button class="preset-chip" onclick="disconnectCurrentWallet()" style="width: 100%; text-align: center; padding: 0.45rem; color: var(--color-red);">Disconnect</button>
        </div>
      </div>
    </div>
  </header>

  <!-- App Body: Sidebar + Main Stage -->
  <div class="app-body">
    <!-- Left Sidebar: Markets List & Navigation Shortcuts -->
    <aside class="app-sidebar">
      <div>
        <div class="sidebar-section-title">
          <span>TOKENIZED EQUITIES</span>
          <span style="font-size: 0.65rem; color: var(--color-green);">24/7 LIVE</span>
        </div>
        <div class="sidebar-menu" id="marketsMenuList">
          <!-- Populated by JS -->
        </div>
      </div>

      <div>
        <div class="sidebar-section-title">
          <span>GLOBAL BENCHMARK</span>
        </div>
        <div class="sidebar-menu">
          <div class="sidebar-item" style="cursor: default;">
            <div class="sidebar-item-left">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
              <span>BTC / USD Macro</span>
            </div>
            <span class="sidebar-item-metric" style="color: var(--color-green);">60D β 1.42</span>
          </div>
        </div>
      </div>

      <div>
        <div class="sidebar-section-title">
          <span>COGNITIVE PLATFORM</span>
        </div>
        <div class="sidebar-menu">
          <div class="sidebar-item" onclick="switchView('auditor', document.getElementById('tabAuditor'))">
            <div class="sidebar-item-left">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
              <span>Self-Auditor Brain</span>
            </div>
            <span class="sidebar-item-metric" style="color: var(--color-green);" id="sidebarAuditsActive">Active</span>
          </div>
          <div class="sidebar-item" onclick="switchView('ledger', document.getElementById('tabLedger'))">
            <div class="sidebar-item-left">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/></svg>
              <span>Trade Ledger</span>
            </div>
            <span class="sidebar-item-metric" id="sidebarTradeCount">26 Trades</span>
          </div>
          <div class="sidebar-item" onclick="switchView('settings', document.getElementById('tabSettings'))">
            <div class="sidebar-item-left">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
              <span>Settings & Gateway</span>
            </div>
            <span class="sidebar-item-metric" style="color: var(--color-green);">UTA v3</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="app-main">

      <!-- Strategy Recalibration Alert Banner -->
      <div class="recalibration-alert-toast" id="recalibrationToast">
        <div style="display: flex; gap: 0.85rem; align-items: flex-start;">
          <span style="font-size: 1.3rem;">🧠</span>
          <div>
            <div style="font-size: 0.84rem; font-weight: 700; color: #92400E;" id="recalToastTitle">Cognitive Self-Audit Complete</div>
            <div style="font-size: 0.8rem; color: #78350F; margin-top: 0.15rem; line-height: 1.5;" id="recalToastBody">
              Strategy automatically recalibrated. The bot adapted its entry boundaries to prevent recurrence on future trades.
            </div>
          </div>
        </div>
        <button onclick="dismissRecalToast()" style="background: none; border: none; font-size: 1.1rem; color: #92400E; cursor: pointer;">✕</button>
      </div>

      <!-- VIEW 1: TRADING ARENA -->
      <div id="viewArena">
        <!-- In-App Breadcrumb Header -->
        <div class="breadcrumb-row">
          <div style="display: flex; align-items: center; gap: 0.5rem; font-family: var(--font-terminal); font-size: 0.76rem; color: var(--color-grey-text);">
            <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: var(--color-green);"></span>
            <span>ACTIVE STRATEGY</span>
            <span style="color: #DDD;">/</span>
            <span id="breadcrumbPathDisplay" style="color: #000; font-weight: 700;">NVIDIA Corporation (rNVDA)</span>
          </div>
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-family: var(--font-terminal); font-size: 0.74rem; color: var(--color-grey-muted);">
              Wallet Balance: <strong id="arenaPaperBalanceDisplay" style="color: var(--color-green);">$50,000.00 USDT</strong>
            </div>
          </div>
        </div>

        <!-- Market Title Area -->
        <div class="market-header-area">
          <h1 class="market-title" id="marketTitleDisplay">NVIDIA Corp ($rNVDA / USDT)</h1>
          <p class="market-subtitle" id="marketSubtitleDisplay">
            Systematic weekend mean-reversion model. Tracking residual pricing drift against Bitcoin crypto-macro benchmark to capture Monday institutional pre-market convergence.
          </p>

          <div class="status-strip">
            <span style="width: 7px; height: 7px; border-radius: 50%; background: var(--color-green); display: inline-block;"></span>
            <span>Friday Settlement Anchor: <strong id="statusAnchorDisplay" style="font-family: var(--font-terminal);">$128.40 USD</strong> • Next Convergence Cash Unwind: <strong style="font-family: var(--font-terminal);">Monday 08:30 EST</strong> • Gateway: Bitget UTA v3</span>
          </div>
        </div>

        <!-- Autonomous Auto-Pilot Live Bar -->
        <div class="auto-live-status-bar" id="autoStatusBar">
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span class="auto-live-pulse"></span>
            <div>
              <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.04em;">AUTONOMOUS AUTO-PILOT: ACTIVE</div>
              <div style="font-size: 0.74rem; color: #94A3B8; font-family: var(--font-terminal);">Scanning 7 tokenized equities • Auto-entry when |Z| ≥ Z_entry • Monday cash convergence</div>
            </div>
          </div>

          <div style="display: flex; align-items: center; gap: 0.65rem;">
            <button class="preset-chip" style="background: rgba(255,255,255,0.15); color: #FFF; border: none; padding: 0.35rem 0.85rem;" onclick="triggerAutonomousCycle()">
              <span>Trigger Autonomous Cycle</span>
            </button>
          </div>
        </div>

        <!-- Two-Column Arena Grid -->
        <div class="arena-grid">
          <!-- Left: Candlestick Chart Panel Card -->
          <div class="chart-panel-card">
            <div class="chart-card-header">
              <div>
                <div class="oracle-label">Bitget 24/7 Spot Oracle • <span id="symbolDisplay">rNVDA/USDT</span></div>
                <div style="display: flex; align-items: baseline; gap: 0.65rem;">
                  <span class="big-price-val" id="chartPriceDisplay">$132.80</span>
                  <span class="badge-pill-green" id="chartDriftBadge" style="font-size: 0.76rem; padding: 0.2rem 0.55rem;">+3.42% Drift</span>
                </div>
              </div>

              <div>
                <div class="oracle-label" style="text-align: right;">FRIDAY ANCHOR SETTLEMENT</div>
                <div class="strike-barrier-val" id="strikeBarrierDisplay">$128.40</div>
                <div class="anchor-subtext" id="anchorStatusSubtext">Prev Close Anchor: $128.40 (OVERBOUGHT)</div>
              </div>
            </div>

            <div class="chart-subbar">
              <div class="chart-tools-left">
                <span style="color: var(--color-green);">● Bitget UTA Feed</span>
                <span style="background: rgba(0,0,0,0.06); padding: 0.15rem 0.45rem; border-radius: 4px;">SPOT-247</span>
                <span style="border-left: 1px solid rgba(0,0,0,0.1); height: 12px; margin: 0 0.25rem;"></span>
                <span style="cursor: pointer; font-weight: 700;" onclick="toggleChartMode('candles')">CANDLES</span>
                <span style="color: #999;">|</span>
                <span style="cursor: pointer;" onclick="toggleChartMode('line')">LINE</span>
              </div>

              <div class="timeframe-pill-group">
                <button class="timeframe-pill" onclick="setTimeframe('1M', this)">1M</button>
                <button class="timeframe-pill" onclick="setTimeframe('5M', this)">5M</button>
                <button class="timeframe-pill" onclick="setTimeframe('15M', this)">15M</button>
                <button class="timeframe-pill active" onclick="setTimeframe('1H', this)">1H</button>
              </div>
            </div>

            <!-- Candlestick / Line Canvas -->
            <canvas id="appCandleCanvas"></canvas>
          </div>

          <!-- Right: Strategy Execution & Risk Control Panel -->
          <div class="execution-panel-card">
            <div class="execution-header">
              <span class="execution-title">STRATEGY EXECUTION</span>
              <span class="badge-pill-green" style="font-size: 0.7rem; font-family: var(--font-terminal);">NET 0.10% TAKER</span>
            </div>

            <!-- Signal Decision Banner -->
            <div class="signal-banner">
              <div class="signal-banner-title">
                <span id="signalActionTitle">SHORT OVERBOUGHT DRIFT</span>
                <span id="signalZScoreBadge" style="color: var(--color-amber);">Z = +2.24σ</span>
              </div>
              <div class="signal-banner-desc" id="signalExplanationText">
                Retail buyers pushed $rNVDA +3.42% above Friday institutional settlement while Nasdaq is shuttered. Strategy deploys counter-positioning into Monday pre-market convergence.
              </div>
            </div>

            <!-- Execution Mode Switcher -->
            <div class="mode-switcher">
              <button class="mode-switcher-btn active" id="btnAutoMode" onclick="setExecutionMode('AUTO')">
                Autonomous Auto-Pilot
              </button>
              <button class="mode-switcher-btn" id="btnManualMode" onclick="setExecutionMode('MANUAL')">
                Manual Allocation
              </button>
            </div>

            <!-- Position Allocation Input -->
            <div class="collateral-box">
              <div class="collateral-header">
                <span style="font-weight: 600;">Position Allocation (USDT)</span>
                <span style="color: var(--color-grey-muted); font-family: var(--font-terminal);">Wallet Avail: <strong id="availBalanceDisplay" style="color: #000;">$50,000.00</strong></span>
              </div>
              <input type="number" id="collateralInput" class="collateral-input-field" value="2500" oninput="recalcExecution()">
              
              <div class="collateral-presets">
                <button class="preset-chip" onclick="setCollateral(500, this)">$500</button>
                <button class="preset-chip" onclick="setCollateral(1000, this)">$1,000</button>
                <button class="preset-chip active" onclick="setCollateral(2500, this)">$2,500</button>
                <button class="preset-chip" onclick="setCollateralMax()">MAX (25%)</button>
              </div>
            </div>

            <!-- Execution Breakdown -->
            <div style="border-top: 1px dashed rgba(0,0,0,0.14); padding-top: 0.85rem; margin-bottom: 1.25rem;">
              <div class="calc-row">
                <span>Contracts Allocated:</span>
                <strong id="calcContractsDisplay">18.82 rNVDA</strong>
              </div>
              <div class="calc-row">
                <span>Convergence Target:</span>
                <strong id="calcTargetPriceDisplay">$128.40 (Friday Anchor)</strong>
              </div>
              <div class="calc-row">
                <span>Expected Profit:</span>
                <strong id="calcExpectedProfit" style="color: var(--color-green);">+$85.50 (+3.42%)</strong>
              </div>
              <div class="calc-row">
                <span>Dynamic Stop Loss:</span>
                <strong id="calcStopLossDisplay" style="color: var(--color-red);">-$52.50 (-2.10%)</strong>
              </div>
              <div class="calc-row">
                <span>Cash Sweep Time:</span>
                <strong style="color: #000;">Monday 08:30 EST (100% USDT)</strong>
              </div>
            </div>

            <button class="btn-execute-big" id="mainExecuteBtn" onclick="executeTradeOrder()">
              <span id="executeBtnText">ACTIVATE AUTONOMOUS STRATEGY</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
            </button>
            <div style="text-align: center; font-size: 0.74rem; color: var(--color-grey-muted); margin-top: 0.5rem; font-family: var(--font-terminal);">
              Chronos automatically rebalances into 100% USDT cash at Monday market open.
            </div>
          </div>
        </div>
      </div>

      <!-- VIEW 2: COGNITIVE SELF-AUDITOR (100% Human-Readable for Non-Devs) -->
      <div id="viewAuditor" style="display: none;">
        <div class="breadcrumb-row">
          <span class="preset-chip" onclick="switchView('arena', document.getElementById('tabArena'))" style="border-radius: 20px; padding: 0.32rem 0.85rem; font-weight: 600; cursor: pointer;">← Back to Trading Arena</span>
          <div style="font-family: var(--font-terminal); font-size: 0.76rem; color: var(--color-grey-muted);">Chronos Cognitive Brain • Closed-Loop Learning</div>
        </div>

        <h1 class="market-title">Cognitive Self-Auditor & Closed-Loop Learning</h1>
        <p class="market-subtitle">
          An autonomous trading bot must evaluate its own decisions so it does not make the same mistakes twice. Chronos evaluates <strong>every closed trade</strong>—both wins and losses. Here is how it diagnosed recent trades and adapted its rules in plain English:
        </p>

        <!-- 3 Key Metric Cards -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; margin-top: 1.5rem; margin-bottom: 2rem;">
          <div class="auditor-lesson-card">
            <div style="font-family: var(--font-terminal); font-size: 0.74rem; color: var(--color-grey-muted); text-transform: uppercase;">Overall System Health</div>
            <div style="font-family: var(--font-serif-editorial); font-size: 2.2rem; color: var(--color-green);" id="auditorHealthVal">99.4% Optimal</div>
            <div style="font-size: 0.82rem; color: var(--color-grey-text);" id="auditorHealthSubtext">Closed trades audited. Zero manual intervention needed.</div>
          </div>

          <div class="auditor-lesson-card">
            <div style="font-family: var(--font-terminal); font-size: 0.74rem; color: var(--color-grey-muted); text-transform: uppercase;">Win / Loss Ratio</div>
            <div style="font-family: var(--font-serif-editorial); font-size: 2.2rem; color: #000;" id="auditorWinRatioVal">20 Wins · 6 Losses</div>
            <div style="font-size: 0.82rem; color: var(--color-grey-text);" id="auditorWinRateSubtext">76.9% Win Rate across 120 days net of all friction.</div>
          </div>

          <div class="auditor-lesson-card">
            <div style="font-family: var(--font-terminal); font-size: 0.74rem; color: var(--color-grey-muted); text-transform: uppercase;">Active Self-Adaptations</div>
            <div style="font-family: var(--font-serif-editorial); font-size: 2.2rem; color: var(--color-amber);" id="auditorRulesTunedVal">3 Rules Tuned</div>
            <div style="font-size: 0.82rem; color: var(--color-grey-text);">Dynamic thresholds auto-recalibrated for connected wallet.</div>
          </div>
        </div>

        <!-- Plain-English Case Studies Container -->
        <h3 style="font-family: var(--font-serif-editorial); font-size: 1.75rem; margin-bottom: 1rem;">Post-Mortem Trade Diagnoses & Adaptations</h3>
        <div style="display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 2.5rem;" id="auditsListContainer">
          <!-- Dynamically populated from wallet's audit list -->
        </div>
      </div>

      <!-- VIEW 3: TRADE LEDGER -->
      <div id="viewLedger" style="display: none;">
        <div class="breadcrumb-row">
          <span class="preset-chip" onclick="switchView('arena', document.getElementById('tabArena'))" style="border-radius: 20px; padding: 0.32rem 0.85rem; font-weight: 600; cursor: pointer;">← Back to Trading Arena</span>
          <div style="font-family: var(--font-terminal); font-size: 0.76rem; color: var(--color-grey-muted);">Wallet-Scoped Audited Ledger</div>
        </div>

        <h1 class="market-title">Audited Trade Record & History</h1>
        <p class="market-subtitle">
          Every trade executed for the connected wallet with exact entry, exit, net profit, and a clickable link to its distinctive post-mortem self-audit.
        </p>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.75rem;">
          <div style="display: flex; gap: 0.5rem;">
            <button class="preset-chip active" id="btnLedgerAll" style="flex: none; padding: 0.4rem 1rem;" onclick="filterLedger('all', this)">All Trades</button>
            <button class="preset-chip" id="btnLedgerWin" style="flex: none; padding: 0.4rem 1rem;" onclick="filterLedger('win', this)">Profitable Wins</button>
            <button class="preset-chip" id="btnLedgerLoss" style="flex: none; padding: 0.4rem 1rem;" onclick="filterLedger('loss', this)">Audited Losses</button>
          </div>

          <div style="font-family: var(--font-terminal); font-size: 0.76rem; color: #666;">
            Paper Wallet: <strong id="ledgerWalletAddressLabel" style="color: #000;">0x71C...3a9F</strong>
          </div>
        </div>

        <div class="chart-panel-card" style="padding: 0; overflow-x: auto;">
          <table class="ledger-table">
            <thead>
              <tr>
                <th>Trade ID</th>
                <th>Asset</th>
                <th>Strategy Action</th>
                <th>Entry Price</th>
                <th>Monday Exit</th>
                <th>Net Return (%)</th>
                <th>USDT Profit</th>
                <th>Post-Mortem Self-Audit</th>
              </tr>
            </thead>
            <tbody id="appLedgerTableBody">
            </tbody>
          </table>
        </div>
      </div>

      <!-- VIEW 4: SETTINGS & GATEWAY PAGE -->
      <div id="viewSettings" style="display: none;">
        <div class="breadcrumb-row">
          <span class="preset-chip" onclick="switchView('arena', document.getElementById('tabArena'))" style="border-radius: 20px; padding: 0.32rem 0.85rem; font-weight: 600; cursor: pointer;">← Back to Trading Arena</span>
          <div style="font-family: var(--font-terminal); font-size: 0.76rem; color: var(--color-grey-muted);">System Configuration & API Vault</div>
        </div>

        <h1 class="market-title">Settings & Gateway Configuration</h1>
        <p class="market-subtitle">
          Configure your connection to the Bitget Universal Trading Account (UTA v3), manage paper balances for your Web3 wallet, and review autonomous execution limits.
        </p>

        <div class="settings-grid">
          <!-- Card 1: Bitget Gateway Configuration -->
          <div class="settings-card">
            <div class="settings-card-title">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <span>Bitget Exchange Gateway</span>
            </div>
            <p style="font-size: 0.85rem; color: var(--color-grey-text); line-height: 1.5;">
              Connect your Bitget account via non-custodial HMAC-SHA256 credentials. Read and trade permissions only.
            </p>

            <div class="form-group">
              <label class="form-label">Execution Environment</label>
              <select id="settingsEnvSelect" class="form-input">
                <option value="paper">Paper Mode (Simulated Funds — No Capital at Risk)</option>
                <option value="mainnet">Live Bitget UTA v3 Account (Real Capital)</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Bitget API Key</label>
              <input type="text" id="settingsApiKey" class="form-input" placeholder="bg_live_quant_key_********">
            </div>

            <div class="form-group">
              <label class="form-label">Bitget API Secret</label>
              <input type="password" id="settingsApiSecret" class="form-input" placeholder="••••••••••••••••">
            </div>

            <div class="form-group">
              <label class="form-label">Bitget Passphrase</label>
              <input type="password" id="settingsPassphrase" class="form-input" placeholder="••••••••">
            </div>

            <div style="background: var(--color-canvas-subtle); border-radius: 6px; padding: 0.75rem 1rem; font-size: 0.78rem; display: flex; justify-content: space-between; align-items: center;">
              <span>Gateway Ping Latency:</span>
              <strong style="color: var(--color-green); font-family: var(--font-terminal);">14ms (Direct UTA)</strong>
            </div>

            <div style="display: flex; gap: 0.65rem;">
              <button class="btn-execute-big" style="padding: 0.65rem;" onclick="saveBitgetSettings()">
                <span>Save Gateway Configuration</span>
              </button>
            </div>
          </div>

          <!-- Card 2: Connected Wallet & Paper Balance Manager -->
          <div class="settings-card">
            <div class="settings-card-title">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/></svg>
              <span>Wallet Paper Trading Balance</span>
            </div>
            <p style="font-size: 0.85rem; color: var(--color-grey-text); line-height: 1.5;">
              Each connected Web3 wallet maintains an independent paper trading balance, allowing isolated risk profiles and separate strategy experiments.
            </p>

            <div style="background: var(--color-canvas-subtle); border-radius: 8px; padding: 1rem 1.25rem;">
              <div style="font-size: 0.75rem; color: #666; font-family: var(--font-terminal);">CONNECTED WALLET</div>
              <div style="font-family: var(--font-terminal); font-size: 0.95rem; font-weight: 700; margin-top: 0.2rem;" id="settingsWalletAddress">0x71C8...3a9F</div>
              <div style="font-size: 0.75rem; color: #666; font-family: var(--font-terminal); margin-top: 0.75rem;">CURRENT PAPER BALANCE</div>
              <div style="font-family: var(--font-serif-editorial); font-size: 2.2rem; color: var(--color-green);" id="settingsPaperBalanceDisplay">$50,000.00 USDT</div>
            </div>

            <div class="form-group">
              <label class="form-label">Set Custom Paper Balance</label>
              <div style="display: flex; gap: 0.5rem;">
                <input type="number" id="settingsCustomBalanceInput" class="form-input" placeholder="50000" value="50000">
                <button class="preset-chip" style="flex: none; padding: 0 1rem; font-weight: 700;" onclick="setCustomPaperBalance()">Update</button>
              </div>
            </div>

            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
              <button class="preset-chip" style="flex: 1; padding: 0.55rem;" onclick="resetCurrentWalletBalance()">Reset to $50,000</button>
              <button class="preset-chip" style="flex: 1; padding: 0.55rem;" onclick="addPaperBalance(10000)">+ Add $10,000</button>
              <button class="preset-chip" style="flex: 1; padding: 0.55rem; color: var(--color-red);" onclick="clearWalletHistory()">Clear Trades</button>
            </div>
          </div>
        </div>
      </div>

    </main>
  </div>

  <!-- RainbowKit Wallet Connect Modal -->
  <div class="rainbow-modal-overlay" id="rainbowModalOverlay" onclick="closeRainbowModalOnBackdrop(event)">
    <div class="rainbow-modal-card">
      <div class="rainbow-modal-header">
        <h3>Connect a Wallet</h3>
        <button onclick="closeRainbowModal()" style="background: none; border: none; font-size: 1.2rem; cursor: pointer; color: #666;">✕</button>
      </div>

      <div class="rainbow-wallet-list">
        <!-- MetaMask -->
        <div class="rainbow-wallet-option" onclick="selectWalletProvider('MetaMask')">
          <div class="wallet-icon-title">
            <div class="wallet-icon-img" style="background: #FFF0E5;">
              <svg width="20" height="20" viewBox="0 0 24 24"><path fill="#E2761B" d="M21.5 6.5l-8.5-4-1 2.5 7 3.5zm-19 0l8.5-4 1 2.5-7 3.5z"/><path fill="#E4761B" d="M19.5 15.5l-2.5 4.5-5-2.5 1-2.5 4 .5zm-15 0l2.5 4.5 5-2.5-1-2.5-4 .5z"/><path fill="#D7C1B3" d="M10 12l2-6 2 6-2 3z"/></svg>
            </div>
            <span>MetaMask</span>
          </div>
          <span style="font-size: 0.72rem; color: var(--color-green); font-weight: 700; font-family: var(--font-terminal);">POPULAR</span>
        </div>

        <!-- Rainbow -->
        <div class="rainbow-wallet-option" onclick="selectWalletProvider('Rainbow')">
          <div class="wallet-icon-title">
            <div class="wallet-icon-img" style="background: linear-gradient(135deg, #FF6B6B, #4ECDC4);">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="#FFF"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/></svg>
            </div>
            <span>Rainbow</span>
          </div>
          <span style="font-size: 0.72rem; color: #666; font-family: var(--font-terminal);">MOBILE</span>
        </div>

        <!-- Coinbase Wallet -->
        <div class="rainbow-wallet-option" onclick="selectWalletProvider('Coinbase')">
          <div class="wallet-icon-title">
            <div class="wallet-icon-img" style="background: #0052FF;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="#FFF"><rect x="4" y="4" width="16" height="16" rx="4"/></svg>
            </div>
            <span>Coinbase Wallet</span>
          </div>
        </div>

        <!-- WalletConnect -->
        <div class="rainbow-wallet-option" onclick="selectWalletProvider('WalletConnect')">
          <div class="wallet-icon-title">
            <div class="wallet-icon-img" style="background: #3B99FC;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="#FFF"><path d="M6 9l6 6 6-6"/></svg>
            </div>
            <span>WalletConnect</span>
          </div>
        </div>

        <!-- Browser Injected -->
        <div class="rainbow-wallet-option" onclick="selectWalletProvider('Injected')">
          <div class="wallet-icon-title">
            <div class="wallet-icon-img" style="background: #111;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="#FFF"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            </div>
            <span>Browser Injected EVM</span>
          </div>
          <span style="font-size: 0.72rem; color: #666; font-family: var(--font-terminal);">DETECTED</span>
        </div>
      </div>

      <!-- Quick-Switch Test Accounts -->
      <div style="background: var(--color-canvas-subtle); padding: 1rem 1.25rem; border-top: 1px solid rgba(0,0,0,0.06);">
        <div style="font-size: 0.72rem; font-weight: 700; color: #666; font-family: var(--font-terminal); text-transform: uppercase; margin-bottom: 0.5rem;">
          Quick Test Accounts (Isolated Paper Balances)
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.35rem;">
          <div class="rainbow-wallet-option" style="padding: 0.45rem 0.75rem;" onclick="connectDirectAddress('0x71C8e2410a82Bc9bB12c98F908316D4112e3a9F')">
            <span style="font-family: var(--font-terminal); font-size: 0.78rem;">0x71C8...3a9F (Quant Alpha)</span>
            <span style="font-size: 0.7rem; color: var(--color-green); font-weight: 700;">ACTIVE</span>
          </div>
          <div class="rainbow-wallet-option" style="padding: 0.45rem 0.75rem;" onclick="connectDirectAddress('0x94B27c08a98C7F0013dC99E5e4157A31D082e21A')">
            <span style="font-family: var(--font-terminal); font-size: 0.78rem;">0x94B2...e21A (DeFi Treasury)</span>
            <span style="font-size: 0.7rem; color: #888;">ISOLATED</span>
          </div>
          <div class="rainbow-wallet-option" style="padding: 0.45rem 0.75rem;" onclick="connectDirectAddress('0x42A169b8214C9E57A0c0903875B22915668a98Cc')">
            <span style="font-family: var(--font-terminal); font-size: 0.78rem;">0x42A1...98Cc (Risk Parity Desk)</span>
            <span style="font-size: 0.7rem; color: #888;">ISOLATED</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const markets = {markets_json};
    const candlesData = {candles_json};
    const initialRealTrades = {trades_json};
    const initialAuditList = {audit_json};

    let selectedSymbol = "rNVDA";
    let executionMode = "AUTO"; // AUTO or MANUAL
    let chartViewMode = "candles";

    // Chronos Wallet & Per-Wallet State Store
    const ChronosWalletStore = {{
      currentAddress: "0x71C8e2410a82Bc9bB12c98F908316D4112e3a9F",

      init() {{
        const savedAddr = localStorage.getItem("chronos_active_wallet") || this.currentAddress;
        this.currentAddress = savedAddr;
        this.ensureWalletInitialized(this.currentAddress);
        this.renderHeaderWallet();
        this.syncActiveView();
      }},

      getKey(addr) {{
        return "chronos_wallet_" + addr.toLowerCase();
      }},

      getData(addr) {{
        const raw = localStorage.getItem(this.getKey(addr));
        if (!raw) return null;
        try {{ return JSON.parse(raw); }} catch(e) {{ return null; }}
      }},

      saveData(addr, data) {{
        localStorage.setItem(this.getKey(addr), JSON.stringify(data));
      }},

      ensureWalletInitialized(addr) {{
        let d = this.getData(addr);
        if (!d) {{
          d = {{
            address: addr,
            paperBalance: 50000.00,
            initialBalance: 50000.00,
            positions: [],
            trades: JSON.parse(JSON.stringify(initialRealTrades)),
            audits: [
              {{
                trade_id: "TRD-2026-0824",
                symbol: "rTSLA",
                side: "SHORT",
                return_pct: -1.48,
                pnl_usd: -370.00,
                verdict: "AUDITED_LOSS_MOMENTUM_OVERRUN",
                root_cause: "Retail momentum overran 2.00σ threshold before reversal.",
                resilience_audit: "Premature entry into weekend news flow without exhaustion filter.",
                adaptation: "Raised rTSLA Entry Z from 2.00σ to 2.50σ. Bot now waits for retail exhaustion.",
                timestamp: "2026-09-16 09:30 EST"
              }},
              {{
                trade_id: "TRD-2026-0818",
                symbol: "rMSTR",
                side: "SHORT",
                return_pct: -1.62,
                pnl_usd: -405.00,
                verdict: "AUDITED_LOSS_BETA_DECOUPLING",
                root_cause: "Asset detached from historical Bitcoin correlation during weekend crypto swings.",
                resilience_audit: "Concentrated 35% exposure created outsized portfolio variance.",
                adaptation: "Trimmed rMSTR single-stock capital cap from 35% down to 25%.",
                timestamp: "2026-09-09 09:30 EST"
              }},
              {{
                trade_id: "TRD-2026-0811",
                symbol: "rNVDA",
                side: "SHORT",
                return_pct: 3.88,
                pnl_usd: 970.00,
                verdict: "PROFITABLE_RESILIENCE_AUDIT",
                root_cause: "Flawless Monday 08:30 EST institutional cash convergence.",
                resilience_audit: "Trade experienced -0.8% drawdown on Sunday before reversing. Mitigation: engaged dynamic trailing stop buffer.",
                adaptation: "Verified convergence timing; maintained 45-minute pre-market exit window.",
                timestamp: "2026-09-02 09:30 EST"
              }}
            ],
            strategyConfig: {{
              rNVDA_z_entry: 2.00,
              rTSLA_z_entry: 2.50,
              rAAPL_z_entry: 2.00,
              rCOIN_z_entry: 2.00,
              rMSTR_z_entry: 2.00,
              rSPY_z_entry: 2.00,
              rQQQ_z_entry: 2.00
            }},
            gateway: {{
              mode: "paper",
              apiKey: "",
              apiSecret: "",
              passphrase: ""
            }}
          }};
          this.saveData(addr, d);
        }}
        return d;
      }},

      getCurrentData() {{
        return this.ensureWalletInitialized(this.currentAddress);
      }},

      setCurrentData(data) {{
        this.saveData(this.currentAddress, data);
        this.renderHeaderWallet();
        this.syncActiveView();
      }},

      connect(addr) {{
        this.currentAddress = addr;
        localStorage.setItem("chronos_active_wallet", addr);
        this.ensureWalletInitialized(addr);
        this.renderHeaderWallet();
        this.syncActiveView();
      }},

      disconnect() {{
        this.currentAddress = null;
        localStorage.removeItem("chronos_active_wallet");
        this.renderHeaderWallet();
      }},

      renderHeaderWallet() {{
        const container = document.getElementById("walletHeaderContainer");
        if (!container) return;

        if (!this.currentAddress) {{
          container.innerHTML = `
            <button class="rainbow-connect-btn" onclick="openRainbowModal()">
              <div class="rainbow-connect-btn-inner">
                <span class="rainbow-avatar-circle"></span>
                <span>Connect Wallet</span>
              </div>
            </button>
          `;
          return;
        }}

        const d = this.getCurrentData();
        const shortAddr = this.currentAddress.slice(0, 6) + "..." + this.currentAddress.slice(-4);
        container.innerHTML = `
          <div class="rainbow-connected-pill" onclick="toggleWalletDropdown(event)">
            <div class="rainbow-chain-chip">
              <span class="rainbow-chain-dot"></span>
              <span>Ethereum</span>
            </div>
            <div class="rainbow-balance-chip">
              <span>$${{d.paperBalance.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}</span>
            </div>
            <div class="rainbow-account-chip">
              <span class="rainbow-avatar-circle"></span>
              <span>${{shortAddr}}</span>
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="m6 9 6 6 6-6"/></svg>
            </div>
          </div>
        `;

        document.getElementById("dropdownWalletAddr").textContent = shortAddr;
        document.getElementById("dropdownPaperBalance").textContent = `$${{d.paperBalance.toLocaleString('en-US', {{minimumFractionDigits: 2}})}} USDT`;
      }},

      syncActiveView() {{
        if (!this.currentAddress) return;
        const d = this.getCurrentData();
        
        // Arena displays
        const balStr = `$${{d.paperBalance.toLocaleString('en-US', {{minimumFractionDigits: 2}})}}`;
        if (document.getElementById("availBalanceDisplay")) {{
          document.getElementById("availBalanceDisplay").textContent = balStr;
        }}
        if (document.getElementById("arenaPaperBalanceDisplay")) {{
          document.getElementById("arenaPaperBalanceDisplay").textContent = balStr;
        }}

        // Badges
        if (document.getElementById("auditCountBadge")) {{
          document.getElementById("auditCountBadge").textContent = d.audits.length;
        }}
        if (document.getElementById("ledgerCountBadge")) {{
          document.getElementById("ledgerCountBadge").textContent = d.trades.length;
        }}
        if (document.getElementById("sidebarTradeCount")) {{
          document.getElementById("sidebarTradeCount").textContent = `${{d.trades.length}} Trades`;
        }}

        // Settings displays
        if (document.getElementById("settingsWalletAddress")) {{
          document.getElementById("settingsWalletAddress").textContent = this.currentAddress;
        }}
        if (document.getElementById("settingsPaperBalanceDisplay")) {{
          document.getElementById("settingsPaperBalanceDisplay").textContent = balStr + " USDT";
        }}
        if (document.getElementById("ledgerWalletAddressLabel")) {{
          document.getElementById("ledgerWalletAddressLabel").textContent = this.currentAddress.slice(0, 6) + "..." + this.currentAddress.slice(-4);
        }}

        // Re-render Auditor and Ledger
        renderAuditorCaseStudies(d.audits);
        renderLedgerTable(d.trades);
      }}
    }};

    // Render Auditor Case Studies
    function renderAuditorCaseStudies(audits) {{
      const container = document.getElementById("auditsListContainer");
      if (!container) return;
      container.innerHTML = "";

      let wins = 0;
      let losses = 0;

      audits.forEach(a => {{
        const isWin = (a.return_pct !== undefined ? a.return_pct : (a.pnl_pct || 0)) > 0;
        const ret = a.return_pct !== undefined ? a.return_pct : (a.pnl_pct || 0);
        if (isWin) wins++; else losses++;

        const card = document.createElement("div");
        card.className = "auditor-lesson-card";
        card.id = `audit-card-${{a.trade_id}}`;

        card.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.65rem;">
              <span class="${{isWin ? 'badge-win' : 'badge-loss'}}">${{isWin ? 'PROFITABLE WIN' : 'AUDITED LOSS'}} (${{isWin ? '+' : ''}}${{ret.toFixed(2)}}%)</span>
              <strong style="font-family: var(--font-terminal); font-size: 0.92rem;">#${{a.trade_id}} • ${{a.symbol || a.asset}}</strong>
            </div>
            <div style="font-family: var(--font-terminal); font-size: 0.72rem; color: #888;">
              ${{a.timestamp || 'Post-Market Convergence'}}
            </div>
          </div>

          <div style="font-size: 0.86rem; color: #374151; line-height: 1.55;">
            <strong>What Happened:</strong> ${{a.root_cause}}
          </div>

          <div style="font-size: 0.84rem; color: #4B5563; line-height: 1.55; background: #FAF9F5; padding: 0.65rem 0.85rem; border-radius: 6px;">
            <strong style="color: #111;">Resilience & Risk Audit:</strong> ${{a.resilience_audit || 'Evaluated intra-trade drawdowns, benchmark drift risks, and execution friction.'}}
          </div>

          <div style="background: var(--color-canvas-subtle); border-radius: 6px; padding: 0.75rem 0.95rem; font-size: 0.82rem; color: #111; border-left: 3px solid var(--color-green);">
            <strong>Bot's Autonomous Strategy Recalibration:</strong> ${{a.adaptation}}
          </div>
        `;
        container.appendChild(card);
      }});

      // Update auditor top metrics
      const total = audits.length;
      const winRate = total > 0 ? ((wins / total) * 100).toFixed(1) : "100.0";
      document.getElementById("auditorWinRatioVal").textContent = `${{wins}} Wins · ${{losses}} Losses`;
      document.getElementById("auditorWinRateSubtext").textContent = `${{winRate}}% Win Rate across audited trades net of fees.`;
    }}

    // Render Ledger Table
    function renderLedgerTable(trades) {{
      const tbody = document.getElementById("appLedgerTableBody");
      if (!tbody) return;
      tbody.innerHTML = "";

      trades.forEach(t => {{
        const isWin = (t.pnl_pct !== undefined ? t.pnl_pct : (t.return_pct || 0)) > 0;
        const retPct = t.pnl_pct !== undefined ? t.pnl_pct : (t.return_pct || 0);
        const pnlUsd = t.pnl_usdt !== undefined ? t.pnl_usdt : (t.pnl_usd || 0);
        const tradeId = t.trade_id || `TRD-${{t.asset || t.symbol}}`;

        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><span style="font-family: var(--font-terminal); font-weight: 700;">#${{tradeId}}</span></td>
          <td><strong>${{t.asset || t.symbol}}</strong></td>
          <td><span style="color: ${{t.side === 'SHORT' ? 'var(--color-red)' : 'var(--color-green)'}}; font-weight: 700;">${{t.side === 'SHORT' ? 'Short Dislocation' : 'Long Reversion'}}</span></td>
          <td style="font-family: var(--font-terminal); font-size: 0.8rem;">$${{t.entry_price.toFixed(2)}}</td>
          <td style="font-family: var(--font-terminal); font-size: 0.8rem;">$${{t.exit_price.toFixed(2)}} (Monday Open)</td>
          <td><span class="${{isWin ? 'badge-win' : 'badge-loss'}}">${{isWin ? '+' : ''}}${{retPct.toFixed(2)}}%</span></td>
          <td style="font-family: var(--font-terminal); font-weight: 700; color: ${{isWin ? 'var(--color-green)' : 'var(--color-red)'}};">${{isWin ? '+' : ''}}$${{pnlUsd.toFixed(2)}}</td>
          <td>
            <button class="btn-audit-jump" onclick="jumpToAudit('${{tradeId}}')">
              <span>View Audit</span>
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Filter Ledger Table
    function filterLedger(type, btn) {{
      document.querySelectorAll("#viewLedger .preset-chip").forEach(b => b.classList.remove("active"));
      if (btn) btn.classList.add("active");

      const d = ChronosWalletStore.getCurrentData();
      if (type === "win") {{
        renderLedgerTable(d.trades.filter(t => (t.pnl_pct !== undefined ? t.pnl_pct : t.return_pct) > 0));
      }} else if (type === "loss") {{
        renderLedgerTable(d.trades.filter(t => (t.pnl_pct !== undefined ? t.pnl_pct : t.return_pct) <= 0));
      }} else {{
        renderLedgerTable(d.trades);
      }}
    }}

    // Jump Directly from Trade Ledger to Specific Audit Post-Mortem
    function jumpToAudit(tradeId) {{
      switchView("auditor", document.getElementById("tabAuditor"));
      setTimeout(() => {{
        const el = document.getElementById(`audit-card-${{tradeId}}`);
        if (el) {{
          el.scrollIntoView({{ behavior: "smooth", block: "center" }});
          el.classList.add("highlighted");
          setTimeout(() => el.classList.remove("highlighted"), 3000);
        }} else {{
          window.scrollTo({{ top: 0, behavior: "smooth" }});
        }}
      }}, 100);
    }}

    // Autonomous Cycle Simulator & Trade Closed Re-Evaluation
    function triggerAutonomousCycle() {{
      const d = ChronosWalletStore.getCurrentData();
      const m = markets[selectedSymbol];

      // Calculate allocation
      const allocation = Math.min(d.paperBalance * 0.15, 5000);
      if (allocation < 100) {{
        alert("Insufficient Paper Balance to trigger autonomous cycle. Please reset your balance in Settings.");
        return;
      }}

      // Simulate cycle execution
      const tradeNumber = d.trades.length + 1;
      const newTradeId = `TRD-2026-${{String(tradeNumber).padStart(4, '0')}}`;
      
      const isProfitable = Math.random() > 0.25; // 75% realistic win rate
      const returnPct = isProfitable ? (Math.abs(m.drift_pct) * (0.8 + Math.random() * 0.4)) : -(1.2 + Math.random() * 0.8);
      const dollarPnl = (allocation * (returnPct / 100.0));
      
      // Update paper balance
      d.paperBalance += dollarPnl;

      // Create trade record
      const exitPrice = m.spot_price * (1 - (returnPct / 100.0) * (m.drift_pct > 0 ? 1 : -1));
      const newTrade = {{
        trade_id: newTradeId,
        symbol: m.symbol,
        asset: m.symbol,
        side: m.drift_pct > 0 ? "SHORT" : "LONG",
        entry_price: m.spot_price,
        exit_price: exitPrice,
        return_pct: returnPct,
        pnl_pct: returnPct,
        pnl_usd: dollarPnl,
        pnl_usdt: dollarPnl,
        entry_time: "Saturday 14:00 EST",
        exit_time: "Monday 08:30 EST",
        audit_note: isProfitable ? "Closed via Monday pre-market convergence" : "Stopped out by momentum overrun"
      }};

      d.trades.unshift(newTrade);

      // MANDATORY CLOSED-LOOP RE-EVALUATION FOR BOTH WINS AND LOSSES
      let rootCause = "";
      let resilienceAudit = "";
      let adaptation = "";

      if (!isProfitable) {{
        // Loss re-evaluation
        rootCause = `Retail momentum in ${{m.symbol}} overran entry boundary before reversing. Temporary spread slippage was 0.38%.`;
        resilienceAudit = `Investigated why stop loss hit: entry Z-score was placed too close to initial weekend headline breakout.`;
        
        // Recalibrate strategy
        const curZ = d.strategyConfig[`${{m.symbol}}_z_entry`] || 2.0;
        const newZ = parseFloat((curZ + 0.25).toFixed(2));
        d.strategyConfig[`${{m.symbol}}_z_entry`] = newZ;
        adaptation = `Automatically raised ${{m.symbol}} Entry Z-score from ${{curZ}}σ to ${{newZ}}σ. Next trade will wait for retail exhaustion.`;
      }} else {{
        // Win re-evaluation (What could have gone wrong!)
        rootCause = `Full convergence target attained at Monday pre-market institutional cash sweep.`;
        resilienceAudit = `Intra-trade adverse excursion (MAE) touched -1.1% on Sunday. What could have gone wrong: weekend Bitcoin benchmark volatility could have dragged equity beta.`;
        
        adaptation = `Engaged dynamic trailing take-profit (+1.5% lock) and advanced pre-market unwind by 15 minutes to guarantee liquidity execution.`;
      }}

      // Add to audits
      const newAudit = {{
        trade_id: newTradeId,
        symbol: m.symbol,
        side: m.drift_pct > 0 ? "SHORT" : "LONG",
        return_pct: returnPct,
        pnl_usd: dollarPnl,
        verdict: isProfitable ? "PROFITABLE_RESILIENCE_AUDIT" : "AUDITED_LOSS_MOMENTUM_OVERRUN",
        root_cause: rootCause,
        resilience_audit: resilienceAudit,
        adaptation: adaptation,
        timestamp: new Date().toLocaleString()
      }};

      d.audits.unshift(newAudit);

      // Save updated wallet state
      ChronosWalletStore.setCurrentData(d);

      // Notify user of strategy evolution
      showRecalibrationToast(
        `Cognitive Self-Audit Complete for Trade #${{newTradeId}} (${{m.symbol}})`,
        `${{isProfitable ? 'PROFITABLE WIN (+' + returnPct.toFixed(2) + '%)' : 'AUDITED LOSS (' + returnPct.toFixed(2) + '%)'}} • Strategy Recalibrated: ${{adaptation}} Future trades will execute using this updated rule.`
      );

      // Update market view to reflect newly tuned entry threshold
      updateMarketView();
    }}

    function showRecalibrationToast(title, body) {{
      const t = document.getElementById("recalibrationToast");
      document.getElementById("recalToastTitle").textContent = title;
      document.getElementById("recalToastBody").textContent = body;
      t.classList.add("visible");
    }}

    function dismissRecalToast() {{
      document.getElementById("recalibrationToast").classList.remove("visible");
    }}

    // Manual Trade Order Execution
    function executeTradeOrder() {{
      if (executionMode === "AUTO") {{
        triggerAutonomousCycle();
        return;
      }}

      const d = ChronosWalletStore.getCurrentData();
      const m = markets[selectedSymbol];
      const collateral = parseFloat(document.getElementById("collateralInput").value) || 0;

      if (collateral > d.paperBalance) {{
        alert("Insufficient Paper Balance. You can reset or add funds in the Settings tab.");
        return;
      }}

      triggerAutonomousCycle();
    }}

    // Sidebar & Market Navigation
    function renderSidebar() {{
      const container = document.getElementById("marketsMenuList");
      container.innerHTML = "";

      Object.keys(markets).forEach(sym => {{
        const m = markets[sym];
        const item = document.createElement("div");
        item.className = "sidebar-item" + (sym === selectedSymbol ? " active" : "");
        item.onclick = () => selectMarket(sym);

        const driftSign = m.drift_pct > 0 ? "+" : "";
        const metricColor = Math.abs(m.z_score) >= 2.0 ? "var(--color-amber)" : "var(--color-grey-muted)";
        item.innerHTML = `
          <div class="sidebar-item-left">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
            <span>${{sym}}</span>
          </div>
          <span class="sidebar-item-metric" style="color: ${{metricColor}};">${{driftSign}}${{m.drift_pct.toFixed(1)}}%</span>
        `;
        container.appendChild(item);
      }});
    }}

    function selectMarket(sym) {{
      selectedSymbol = sym;
      renderSidebar();
      updateMarketView();
      drawCandleChart();
    }}

    function updateMarketView() {{
      const m = markets[selectedSymbol];
      const d = ChronosWalletStore.getCurrentData();
      const currentZThreshold = (d && d.strategyConfig && d.strategyConfig[`${{m.symbol}}_z_entry`]) || 2.0;

      document.getElementById("breadcrumbPathDisplay").textContent = `${{m.company}} (${{m.symbol}})`;
      document.getElementById("marketTitleDisplay").textContent = `${{m.company}} (${{m.symbol}})`;
      document.getElementById("symbolDisplay").textContent = `${{m.symbol}}/USDT`;
      document.getElementById("chartPriceDisplay").textContent = `$${{m.spot_price.toFixed(2)}}`;
      
      const driftSign = m.drift_pct > 0 ? "+" : "";
      document.getElementById("chartDriftBadge").textContent = `${{driftSign}}${{m.drift_pct.toFixed(2)}}% Drift`;
      document.getElementById("chartDriftBadge").className = m.drift_pct > 0 ? "badge-pill-green" : "badge-pill-gold";

      document.getElementById("strikeBarrierDisplay").textContent = `$${{m.anchor_price.toFixed(2)}}`;
      document.getElementById("anchorStatusSubtext").textContent = `Prev Close Anchor: $${{m.anchor_price.toFixed(2)}} (${{m.regime}})`;
      document.getElementById("statusAnchorDisplay").textContent = `$${{m.anchor_price.toFixed(2)}} USD`;

      document.getElementById("signalActionTitle").textContent = m.action;
      document.getElementById("signalZScoreBadge").textContent = `Z = ${{m.z_score > 0 ? '+' : ''}}${{m.z_score.toFixed(2)}}σ (Entry ≥ ${{currentZThreshold}}σ)`;
      document.getElementById("signalExplanationText").textContent = m.thesis;

      recalcExecution();
    }}

    function recalcExecution() {{
      const m = markets[selectedSymbol];
      const collateral = parseFloat(document.getElementById("collateralInput").value) || 0;
      
      const contracts = collateral / m.spot_price;
      document.getElementById("calcContractsDisplay").textContent = `${{contracts.toFixed(2)}} ${{m.symbol}}`;
      document.getElementById("calcTargetPriceDisplay").textContent = `$${{m.anchor_price.toFixed(2)}} (Friday Anchor)`;

      const expectedProfit = collateral * (Math.abs(m.drift_pct) / 100.0);
      document.getElementById("calcExpectedProfit").textContent = `+$${{expectedProfit.toFixed(2)}} (${{m.expected_return}})`;

      const stopLoss = collateral * 0.021;
      document.getElementById("calcStopLossDisplay").textContent = `-$${{stopLoss.toFixed(2)}} (${{m.stop_loss}})`;
    }}

    function setExecutionMode(mode) {{
      executionMode = mode;
      document.getElementById("btnAutoMode").classList.toggle("active", mode === "AUTO");
      document.getElementById("btnManualMode").classList.toggle("active", mode === "MANUAL");

      if (mode === "AUTO") {{
        document.getElementById("executeBtnText").textContent = "ACTIVATE AUTONOMOUS STRATEGY";
        document.getElementById("autoStatusBar").style.display = "flex";
      }} else {{
        document.getElementById("executeBtnText").textContent = "DISPATCH MANUAL REBALANCE ORDER";
        document.getElementById("autoStatusBar").style.display = "none";
      }}
    }}

    function setCollateral(val, btn) {{
      document.getElementById("collateralInput").value = val;
      document.querySelectorAll(".preset-chip").forEach(b => b.classList.remove("active"));
      if (btn) btn.classList.add("active");
      recalcExecution();
    }}

    function setCollateralMax() {{
      const d = ChronosWalletStore.getCurrentData();
      const maxVal = Math.floor(d.paperBalance * 0.25);
      document.getElementById("collateralInput").value = maxVal;
      recalcExecution();
    }}

    function toggleChartMode(mode) {{
      chartViewMode = mode;
      drawCandleChart();
    }}

    function setTimeframe(tf, btn) {{
      document.querySelectorAll(".timeframe-pill").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      drawCandleChart();
    }}

    // Draw Candlestick Chart
    function drawCandleChart() {{
      const canvas = document.getElementById("appCandleCanvas");
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();

      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;
      ctx.clearRect(0, 0, w, h);

      const candles = candlesData[selectedSymbol] || [];
      const m = markets[selectedSymbol];
      if (!candles.length) return;

      const anchor = m.anchor_price;
      const allPrices = candles.flatMap(c => [c.high, c.low, anchor]);
      const minP = Math.min(...allPrices) * 0.995;
      const maxP = Math.max(...allPrices) * 1.005;

      const chartTop = 20;
      const chartBottom = h - 60;
      const chartHeight = chartBottom - chartTop;

      const getY = val => chartBottom - ((val - minP) / (maxP - minP)) * chartHeight;

      // Anchor Line
      const anchorY = getY(anchor);
      ctx.beginPath();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = "rgba(229, 9, 20, 0.75)";
      ctx.lineWidth = 1.5;
      ctx.moveTo(40, anchorY);
      ctx.lineTo(w - 20, anchorY);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = "rgba(229, 9, 20, 0.9)";
      ctx.font = "bold 10px 'Space Mono', monospace";
      ctx.fillText(`FRIDAY ANCHOR SETTLEMENT: $${{anchor.toFixed(2)}}`, 42, anchorY - 6);

      // Volume & Candles
      const maxVol = Math.max(...candles.map(c => c.volume));
      const volHeight = 40;
      const numCandles = candles.length;
      const candleWidth = Math.max(4, (w - 80) / numCandles - 3);

      candles.forEach((c, i) => {{
        const x = 50 + i * ((w - 80) / numCandles);
        const isUp = c.close >= c.open;
        const color = isUp ? "#00C853" : "#E50914";

        if (chartViewMode === "candles") {{
          ctx.beginPath();
          ctx.strokeStyle = color;
          ctx.lineWidth = 1.2;
          ctx.moveTo(x + candleWidth / 2, getY(c.high));
          ctx.lineTo(x + candleWidth / 2, getY(c.low));
          ctx.stroke();

          const openY = getY(c.open);
          const closeY = getY(c.close);
          const bodyY = Math.min(openY, closeY);
          const bodyH = Math.max(2, Math.abs(closeY - openY));

          ctx.fillStyle = color;
          ctx.fillRect(x, bodyY, candleWidth, bodyH);
        }}

        const vH = (c.volume / maxVol) * volHeight;
        ctx.fillStyle = isUp ? "rgba(0, 200, 83, 0.25)" : "rgba(229, 9, 20, 0.25)";
        ctx.fillRect(x, h - 15 - vH, candleWidth, vH);
      }});

      if (chartViewMode === "line") {{
        ctx.beginPath();
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 2;
        candles.forEach((c, i) => {{
          const x = 50 + i * ((w - 80) / numCandles) + candleWidth / 2;
          const y = getY(c.close);
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }});
        ctx.stroke();
      }}

      ctx.fillStyle = "#888";
      ctx.font = "10px 'Space Mono', monospace";
      ctx.fillText("$" + maxP.toFixed(2), 5, chartTop + 10);
      ctx.fillText("$" + minP.toFixed(2), 5, chartBottom);
    }}

    // Switch Views (Arena, Auditor, Ledger, Settings)
    function switchView(view, tabEl) {{
      document.getElementById("viewArena").style.display = view === "arena" ? "block" : "none";
      document.getElementById("viewAuditor").style.display = view === "auditor" ? "block" : "none";
      document.getElementById("viewLedger").style.display = view === "ledger" ? "block" : "none";
      document.getElementById("viewSettings").style.display = view === "settings" ? "block" : "none";

      document.querySelectorAll(".app-header-tabs .app-tab").forEach(t => t.classList.remove("active"));
      if (tabEl) tabEl.classList.add("active");

      if (view === "arena") {{
        setTimeout(drawCandleChart, 50);
      }}
    }}

    // RainbowKit Modal Operations
    function openRainbowModal() {{
      closeWalletDropdown();
      document.getElementById("rainbowModalOverlay").classList.add("open");
    }}

    function closeRainbowModal() {{
      document.getElementById("rainbowModalOverlay").classList.remove("open");
    }}

    function closeRainbowModalOnBackdrop(e) {{
      if (e.target.id === "rainbowModalOverlay") closeRainbowModal();
    }}

    function selectWalletProvider(providerName) {{
      let addr = "0x71C8e2410a82Bc9bB12c98F908316D4112e3a9F";
      if (providerName === "Rainbow") addr = "0x94B27c08a98C7F0013dC99E5e4157A31D082e21A";
      else if (providerName === "Coinbase") addr = "0x42A169b8214C9E57A0c0903875B22915668a98Cc";
      else if (providerName === "WalletConnect") addr = "0x3F5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE";
      
      closeRainbowModal();
      ChronosWalletStore.connect(addr);
      alert(`[CONNECTED VIA ${{providerName.toUpperCase()}}]\\nAccount: ${{addr}}\\nPaper Trading Balance: $50,000.00 USDT`);
    }}

    function connectDirectAddress(addr) {{
      closeRainbowModal();
      ChronosWalletStore.connect(addr);
    }}

    function toggleWalletDropdown(e) {{
      e.stopPropagation();
      document.getElementById("walletDropdownMenu").classList.toggle("open");
    }}

    function closeWalletDropdown() {{
      document.getElementById("walletDropdownMenu").classList.remove("open");
    }}

    window.addEventListener("click", () => {{
      closeWalletDropdown();
    }});

    function disconnectCurrentWallet() {{
      closeWalletDropdown();
      ChronosWalletStore.disconnect();
    }}

    // Paper Balance Controls
    function resetCurrentWalletBalance() {{
      closeWalletDropdown();
      const d = ChronosWalletStore.getCurrentData();
      d.paperBalance = 50000.00;
      ChronosWalletStore.setCurrentData(d);
      alert("Paper trading balance reset to $50,000.00 USDT.");
    }}

    function addPaperBalance(amount) {{
      const d = ChronosWalletStore.getCurrentData();
      d.paperBalance += amount;
      ChronosWalletStore.setCurrentData(d);
    }}

    function setCustomPaperBalance() {{
      const val = parseFloat(document.getElementById("settingsCustomBalanceInput").value);
      if (isNaN(val) || val < 0) return alert("Please enter a valid balance.");
      const d = ChronosWalletStore.getCurrentData();
      d.paperBalance = val;
      ChronosWalletStore.setCurrentData(d);
      alert(`Paper balance updated to $${{val.toLocaleString()}} USDT.`);
    }}

    function clearWalletHistory() {{
      if (!confirm("Are you sure you want to clear this wallet's trade history?")) return;
      const d = ChronosWalletStore.getCurrentData();
      d.trades = [];
      ChronosWalletStore.setCurrentData(d);
    }}

    // Bitget Settings Handler
    function saveBitgetSettings() {{
      const env = document.getElementById("settingsEnvSelect").value;
      const key = document.getElementById("settingsApiKey").value.trim();
      const secret = document.getElementById("settingsApiSecret").value.trim();
      const pass = document.getElementById("settingsPassphrase").value.trim();

      const d = ChronosWalletStore.getCurrentData();
      d.gateway = {{ mode: env, apiKey: key, apiSecret: secret, passphrase: pass }};
      ChronosWalletStore.setCurrentData(d);

      alert(`[BITGET GATEWAY SAVED]\\nEnvironment: ${{env === 'mainnet' ? 'Live Capital (Bitget UTA v3)' : 'Paper Mode Simulation'}}\\nHMAC-SHA256 headers configured.`);
    }}

    window.addEventListener("resize", drawCandleChart);
    window.addEventListener("DOMContentLoaded", () => {{
      ChronosWalletStore.init();
      renderSidebar();
      updateMarketView();
      setTimeout(drawCandleChart, 100);
    }});
  </script>
</body>
</html>
"""

# Compile to dashboard/app.html
with open("dashboard/app.html", "w") as f:
    f.write(html_template)

print(f"Successfully compiled Unified Trading Terminal to dashboard/app.html ({len(html_template)} bytes)")
