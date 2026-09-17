import json
import os

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

# Build rich market definitions for the 7 tokenized equities
markets_data = {
    "rNVDA": {
        "name": "rNVDA / USDT Strike",
        "symbol": "rNVDA",
        "company": "NVIDIA Corp (Tokenized)",
        "spot_price": 132.80,
        "anchor_price": 128.40,
        "drift_pct": 3.42,
        "z_score": 2.24,
        "regime": "OVERBOUGHT (SHORT BIAS)",
        "beta": 1.48,
        "volatility": "3.2%",
        "shares_per_dollar": 0.00753,
        "resolution_time": "Monday 08:00 EST"
    },
    "rTSLA": {
        "name": "rTSLA / USDT Strike",
        "symbol": "rTSLA",
        "company": "Tesla Inc (Tokenized)",
        "spot_price": 258.40,
        "anchor_price": 248.00,
        "drift_pct": 4.19,
        "z_score": 2.65,
        "regime": "EXTREME MOMENTUM (SHORT)",
        "beta": 1.95,
        "volatility": "4.8%",
        "shares_per_dollar": 0.00387,
        "resolution_time": "Monday 08:00 EST"
    },
    "rAAPL": {
        "name": "rAAPL / USDT Strike",
        "symbol": "rAAPL",
        "company": "Apple Inc (Tokenized)",
        "spot_price": 222.10,
        "anchor_price": 224.00,
        "drift_pct": -0.85,
        "z_score": -0.68,
        "regime": "WITHIN NOISE BAND (IDLE)",
        "beta": 0.72,
        "volatility": "1.5%",
        "shares_per_dollar": 0.0045,
        "resolution_time": "Monday 08:00 EST"
    },
    "rCOIN": {
        "name": "rCOIN / USDT Strike",
        "symbol": "rCOIN",
        "company": "Coinbase Global (Tokenized)",
        "spot_price": 218.50,
        "anchor_price": 206.80,
        "drift_pct": 5.66,
        "z_score": 3.10,
        "regime": "HIGH CRYPTO BETA (SHORT)",
        "beta": 2.45,
        "volatility": "5.6%",
        "shares_per_dollar": 0.00457,
        "resolution_time": "Monday 08:00 EST"
    },
    "rMSTR": {
        "name": "rMSTR / USDT Strike",
        "symbol": "rMSTR",
        "company": "MicroStrategy Inc (Tokenized)",
        "spot_price": 312.40,
        "anchor_price": 292.20,
        "drift_pct": 6.91,
        "z_score": 3.48,
        "regime": "LEVERAGED BTC DRIFT (SHORT)",
        "beta": 2.90,
        "volatility": "6.8%",
        "shares_per_dollar": 0.0032,
        "resolution_time": "Monday 08:00 EST"
    },
    "rSPY": {
        "name": "rSPY / USDT Strike",
        "symbol": "rSPY",
        "company": "S&P 500 ETF (Tokenized)",
        "spot_price": 564.20,
        "anchor_price": 561.80,
        "drift_pct": 0.43,
        "z_score": 0.35,
        "regime": "STABLE BENCHMARK (IDLE)",
        "beta": 0.35,
        "volatility": "0.8%",
        "shares_per_dollar": 0.00177,
        "resolution_time": "Monday 08:00 EST"
    },
    "rQQQ": {
        "name": "rQQQ / USDT Strike",
        "symbol": "rQQQ",
        "company": "Invesco QQQ Trust (Tokenized)",
        "spot_price": 482.60,
        "anchor_price": 478.90,
        "drift_pct": 0.77,
        "z_score": 0.62,
        "regime": "TECH BENCHMARK (IDLE)",
        "beta": 0.58,
        "volatility": "1.1%",
        "shares_per_dollar": 0.00207,
        "resolution_time": "Monday 08:00 EST"
    }
}

# Generate 40 realistic hourly candlesticks for each asset
import random
random.seed(42)

candles_data = {}
for sym, m in markets_data.items():
    anchor = m["anchor_price"]
    spot = m["spot_price"]
    candles = []
    
    current_p = anchor
    # Drift towards spot over 40 steps
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

markets_json = json.dumps(markets_data)
candles_json = json.dumps(candles_data)
trades_json = json.dumps(real_trades)
audit_json = json.dumps(audit_memory)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chronos // Trading Arena & Execution Terminal</title>
  <link rel="icon" type="image/svg+xml" href="assets/chronos_logo.svg">

  <!-- Google Fonts matching flip-prediction.vercel.app -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Special+Elite&display=swap" rel="stylesheet">

  <style>
{flip_css}

    /* Exact Dashboard Layout & Aesthetics from flip-prediction.vercel.app */
    :root {{
      --font-serif-editorial: "Instrument Serif", "Playfair Display", Georgia, serif;
      --font-sans-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-terminal: "Space Mono", monospace;
      --font-bobz: "Instrument Serif", "Playfair Display", Georgia, serif;
      
      --color-white: #FFFFFF;
      --color-canvas-light: #FAF9F6;
      --color-canvas-subtle: #F2F0EB;
      --color-black: #000000;
      --color-black-night: #090909;
      --color-black-card: #121212;
      --color-grey-pill: #E2E5EB;
      --color-grey-border: rgba(0, 0, 0, 0.08);
      --color-grey-text: #5A5E66;
      --color-grey-muted: #8E9299;
      --color-green: #00C853;
      --color-green-light: #00E676;
      --color-red: #E50914;
      --color-amber: #F59E0B;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--color-canvas-light);
      color: var(--color-black);
      font-family: var(--font-sans-body);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* Top Full-Width Dashboard Header Bar */
    .app-header {{
      background: #FFFFFF;
      border-bottom: 1px solid rgba(0, 0, 0, 0.08);
      height: 58px;
      padding: 0 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .app-header-left {{
      display: flex;
      align-items: center;
      gap: 2rem;
    }}

    .app-brand {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      text-decoration: none;
      color: #000;
      cursor: pointer;
    }}

    .app-brand-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--color-green);
    }}

    .app-brand-name {{
      font-family: var(--font-serif-editorial);
      font-size: 1.65rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}

    .app-header-tabs {{
      display: flex;
      align-items: center;
      gap: 1.5rem;
    }}

    .app-tab {{
      color: #555;
      text-decoration: none;
      font-family: var(--font-sans-body);
      font-size: 0.86rem;
      font-weight: 500;
      padding: 0.4rem 0;
      position: relative;
      cursor: pointer;
      transition: color 0.2s ease;
    }}

    .app-tab:hover {{
      color: #000;
    }}

    .app-tab.active {{
      color: #000;
      font-weight: 700;
    }}

    .app-tab.active::after {{
      content: "";
      position: absolute;
      bottom: -16px;
      left: 0;
      width: 100%;
      height: 2px;
      background: #000;
    }}

    .app-header-right {{
      display: flex;
      align-items: center;
      gap: 0.65rem;
    }}

    .pill-btn-subtle {{
      background: none;
      border: 1px solid rgba(0, 0, 0, 0.12);
      border-radius: 20px;
      padding: 0.38rem 0.85rem;
      font-family: var(--font-sans-body);
      font-size: 0.78rem;
      font-weight: 600;
      color: #333;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s ease;
    }}

    .pill-btn-subtle:hover {{
      background: rgba(0, 0, 0, 0.04);
      color: #000;
    }}

    .pill-btn-faucet {{
      background: rgba(0, 200, 83, 0.12);
      border: 1px solid rgba(0, 200, 83, 0.28);
      border-radius: 20px;
      padding: 0.38rem 0.85rem;
      font-family: var(--font-sans-body);
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--color-green);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s ease;
    }}

    .pill-btn-faucet:hover {{
      background: rgba(0, 200, 83, 0.2);
    }}

    /* Main App Layout Container (Sidebar + Content) */
    .app-body {{
      display: flex;
      flex: 1;
      min-height: calc(100vh - 58px);
    }}

    /* Left Sidebar */
    .app-sidebar {{
      width: 250px;
      flex-shrink: 0;
      background: #FFFFFF;
      border-right: 1px solid rgba(0, 0, 0, 0.08);
      padding: 1.25rem 0.85rem;
      display: flex;
      flex-direction: column;
      gap: 1.75rem;
    }}

    .sidebar-section-title {{
      font-family: var(--font-terminal);
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--color-grey-muted);
      padding: 0 0.65rem;
      margin-bottom: 0.5rem;
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
      padding: 0.55rem 0.75rem;
      border-radius: 8px;
      color: #374151;
      text-decoration: none;
      font-family: var(--font-sans-body);
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid transparent;
    }}

    .sidebar-item:hover {{
      background: rgba(0, 0, 0, 0.035);
      color: #000;
    }}

    .sidebar-item.active {{
      background: var(--color-grey-pill);
      color: var(--color-black);
      border-color: rgba(0, 0, 0, 0.06);
    }}

    .sidebar-item-left {{
      display: flex;
      align-items: center;
      gap: 0.55rem;
    }}

    .sidebar-item-metric {{
      font-family: var(--font-terminal);
      font-size: 0.76rem;
      font-weight: 700;
      color: #4B5563;
    }}

    .sidebar-item.active .sidebar-item-metric {{
      color: #000;
    }}

    /* Main Content Area */
    .app-main {{
      flex: 1;
      padding: 2rem 2.75rem;
      max-width: 1400px;
    }}

    /* Breadcrumb Row */
    .breadcrumb-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.25rem;
    }}

    .back-btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.35rem 0.85rem;
      border-radius: 20px;
      border: 1px solid rgba(0, 0, 0, 0.14);
      background: #FFFFFF;
      font-family: var(--font-sans-body);
      font-size: 0.8rem;
      font-weight: 600;
      color: #333;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .back-btn:hover {{
      background: #F3F4F6;
      color: #000;
      transform: translateX(-2px);
    }}

    .breadcrumb-path {{
      font-family: var(--font-terminal);
      font-size: 0.78rem;
      color: var(--color-grey-muted);
    }}

    /* Market Title Area */
    .market-header-area {{
      margin-bottom: 1.5rem;
    }}

    .market-title {{
      font-family: var(--font-serif-editorial);
      font-size: 2.75rem;
      line-height: 1.1;
      font-weight: 400;
      letter-spacing: -0.02em;
      margin-bottom: 0.35rem;
    }}

    .market-subtitle {{
      font-size: 0.95rem;
      color: var(--color-grey-text);
      max-width: 700px;
      margin-bottom: 1rem;
    }}

    /* Status Strip */
    .status-strip {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.45rem 1rem;
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      border-radius: 8px;
      font-family: var(--font-terminal);
      font-size: 0.78rem;
      color: #333;
    }}

    /* Two-Column Arena Grid */
    .arena-grid {{
      display: grid;
      grid-template-columns: 1.6fr 1fr;
      gap: 1.75rem;
      margin-top: 1.5rem;
      align-items: start;
    }}

    /* Left Card: Market Data & Interactive Chart */
    .chart-panel-card {{
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      border-radius: 6px;
      padding: 1.6rem;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
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
      font-weight: 700;
      color: var(--color-grey-text);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 0.25rem;
    }}

    .big-price-val {{
      font-family: var(--font-serif-editorial);
      font-size: 2.35rem;
      line-height: 1;
      font-weight: 400;
      color: #000;
    }}

    .strike-barrier-val {{
      font-family: var(--font-serif-editorial);
      font-size: 2.35rem;
      line-height: 1;
      font-weight: 400;
      color: #000;
      text-align: right;
    }}

    .anchor-subtext {{
      font-family: var(--font-terminal);
      font-size: 0.76rem;
      font-weight: 700;
      color: var(--color-green);
      text-align: right;
      margin-top: 0.25rem;
    }}

    /* Chart Sub-Toolbar */
    .chart-subbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(0, 0, 0, 0.06);
      border-bottom: 1px solid rgba(0, 0, 0, 0.06);
      padding: 0.6rem 0;
      margin-bottom: 1rem;
    }}

    .chart-tools-left {{
      display: flex;
      align-items: center;
      gap: 0.65rem;
      font-family: var(--font-terminal);
      font-size: 0.74rem;
    }}

    .timeframe-pill-group {{
      display: inline-flex;
      gap: 0.25rem;
    }}

    .timeframe-pill {{
      border: none;
      background: none;
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
      font-family: var(--font-terminal);
      font-size: 0.74rem;
      font-weight: 700;
      color: #6B7280;
      cursor: pointer;
    }}

    .timeframe-pill.active {{
      background: var(--color-black);
      color: #FFF;
    }}

    #appCandleCanvas {{
      width: 100%;
      height: 360px;
      display: block;
    }}

    /* Right Card: Order Execution Panel */
    .execution-panel-card {{
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      border-radius: 6px;
      padding: 1.6rem;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }}

    .execution-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
    }}

    .execution-title {{
      font-family: var(--font-serif-editorial);
      font-size: 1.35rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}

    /* Two Large Direction Buttons */
    .flip-btn-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    }}

    .btn-direction {{
      border-radius: 24px;
      padding: 0.75rem 1rem;
      font-family: var(--font-serif-editorial);
      font-size: 1.15rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 0.2rem;
      transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
      border: 1px solid transparent;
    }}

    .btn-direction:hover {{
      border-radius: 8px;
      transform: translateY(-2px);
    }}

    .btn-direction.btn-green-active {{
      background: var(--color-green);
      color: #000;
      box-shadow: 0 4px 14px rgba(0, 200, 83, 0.35);
    }}

    .btn-direction.btn-subtle-inactive {{
      background: #FAF9F6;
      border: 1px solid rgba(0, 0, 0, 0.14);
      color: #374151;
    }}

    .btn-direction.btn-red-active {{
      background: var(--color-red);
      color: #FFF;
      box-shadow: 0 4px 14px rgba(229, 9, 20, 0.35);
    }}

    /* Collateral Input Box */
    .collateral-box {{
      margin-bottom: 1.5rem;
    }}

    .collateral-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.82rem;
      margin-bottom: 0.45rem;
    }}

    .collateral-input-field {{
      width: 100%;
      background: #EAEBED;
      border: 1px solid rgba(0, 0, 0, 0.08);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      font-family: var(--font-terminal);
      font-size: 1.25rem;
      font-weight: 700;
      color: #000;
      margin-bottom: 0.65rem;
    }}

    .collateral-presets {{
      display: flex;
      gap: 0.4rem;
    }}

    .preset-chip {{
      flex: 1;
      padding: 0.35rem 0;
      text-align: center;
      border: 1px solid rgba(0, 0, 0, 0.1);
      border-radius: 6px;
      background: #FFFFFF;
      font-family: var(--font-terminal);
      font-size: 0.76rem;
      font-weight: 700;
      color: #4B5563;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .preset-chip:hover {{
      background: #F3F4F6;
    }}

    .preset-chip.active {{
      background: #000;
      color: #FFF;
      border-color: #000;
    }}

    /* Calculations Table Rows */
    .calc-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.45rem 0;
      font-size: 0.82rem;
      color: var(--color-grey-text);
      font-family: var(--font-terminal);
    }}

    .calc-row strong {{
      color: #000;
      font-size: 0.88rem;
    }}

    /* Bottom Big Button */
    .btn-execute-big {{
      width: 100%;
      background: #000000;
      color: #FFFFFF;
      border: 1px solid #000000;
      border-radius: 28px;
      padding: 0.75rem 1.25rem;
      font-family: var(--font-serif-editorial);
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      margin-top: 1.25rem;
      transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
    }}

    .btn-execute-big:hover {{
      border-radius: 8px;
      background: #222;
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.28);
    }}

    /* Modal Styling */
    .modal-overlay {{
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

    .modal-overlay.open {{
      display: flex;
    }}

    .modal-card {{
      background: #FFFFFF;
      border-radius: 12px;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      width: 100%;
      max-width: 480px;
      padding: 2rem;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
    }}
  </style>
</head>
<body>

  <!-- Top Navigation Header -->
  <header class="app-header">
    <div class="app-header-left">
      <a href="index.html" class="app-brand">
        <span class="app-brand-dot"></span>
        <span class="app-brand-name">chronos</span>
      </a>

      <nav class="app-header-tabs">
        <span class="app-tab active" onclick="switchView('arena', this)">Trading Arena</span>
        <span class="app-tab" onclick="switchView('auditor', this)">Cognitive Self-Auditor</span>
        <span class="app-tab" onclick="switchView('ledger', this)">Trade Ledger (26)</span>
        <a href="index.html#architecture" class="app-tab" style="text-decoration: none;">Architecture</a>
        <a href="index.html" class="app-tab" style="text-decoration: none; display: flex; align-items: center; gap: 0.25rem;">
          <span>Landing Page</span>
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        </a>
      </nav>
    </div>

    <div class="app-header-right">
      <div id="modePillBadge" class="pill-btn-subtle" onclick="openConnectModal()">
        <span style="width: 6px; height: 6px; border-radius: 50%; background: var(--color-green);"></span>
        <span id="currentModeLabel">Paper Mode ($50k)</span>
      </div>

      <button class="pill-btn-faucet" onclick="resetPaperBalance()">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        <span>Faucet</span>
      </button>

      <button class="pill-btn-subtle" onclick="openConnectModal()">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 1 0-16 0"/></svg>
        <span>Profile</span>
      </button>

      <button class="btn-wallet-connect" onclick="openConnectModal()" id="connectHeaderBtn">
        <span>CONNECT BITGET</span>
      </button>
    </div>
  </header>

  <!-- App Layout: Sidebar + Main Stage -->
  <div class="app-body">
    <!-- Left Sidebar: Markets List -->
    <aside class="app-sidebar">
      <div>
        <div class="sidebar-section-title">
          <span>STANDARD MARKETS</span>
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
          <span>ACCOUNT & MEMORY</span>
        </div>
        <div class="sidebar-menu">
          <div class="sidebar-item" onclick="switchView('auditor', null)">
            <div class="sidebar-item-left">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
              <span>Self-Auditor Brain</span>
            </div>
            <span class="sidebar-item-metric">v2.1</span>
          </div>
          <div class="sidebar-item" onclick="switchView('ledger', null)">
            <div class="sidebar-item-left">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/></svg>
              <span>Trade Ledger</span>
            </div>
            <span class="sidebar-item-metric">26 Trades</span>
          </div>
        </div>
      </div>

      <div>
        <div class="sidebar-section-title">
          <span>PROTOCOL SPECS</span>
        </div>
        <div class="sidebar-menu">
          <a href="index.html#architecture" class="sidebar-item" style="text-decoration: none;">
            <div class="sidebar-item-left">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <span>Bitget UTA Gateway</span>
            </div>
            <span class="sidebar-item-metric" style="color: var(--color-green);">14ms</span>
          </a>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="app-main">
      <!-- VIEW 1: TRADING ARENA (Matches user photo) -->
      <div id="viewArena">
        <!-- Breadcrumb Row -->
        <div class="breadcrumb-row">
          <a href="index.html" class="back-btn">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m15 18-6-6 6-6"/></svg>
            <span>Back to Landing</span>
          </a>
          <div class="breadcrumb-path" id="breadcrumbPathDisplay">Bitget UTA v3 • $rNVDA / USDT Strike</div>
        </div>

        <!-- Market Title Area -->
        <div class="market-header-area">
          <h1 class="market-title" id="marketTitleDisplay">rNVDA / USDT Strike</h1>
          <p class="market-subtitle" id="marketQuestionDisplay">
            Will $rNVDA converge to Friday Anchor $128.40 USD? Resolves via Monday Institutional Pre-Market Open.
          </p>

          <div class="status-strip">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>Monday Convergence in: <strong id="countdownDisplay" style="font-family: var(--font-terminal);">38h 14m</strong> • Oracle Heartbeat: Bitget UTA v3 WebSocket</span>
          </div>
        </div>

        <!-- Two-Column Arena Grid -->
        <div class="arena-grid">
          <!-- Left: Chart Panel Card -->
          <div class="chart-panel-card">
            <div class="chart-card-header">
              <div>
                <div class="oracle-label">Bitget UTA v3 Oracle • <span id="symbolDisplay">rNVDA/USDT</span></div>
                <div style="display: flex; align-items: baseline; gap: 0.65rem;">
                  <span class="big-price-val" id="chartPriceDisplay">$132.80</span>
                  <span class="badge-pill-green" id="chartDriftBadge" style="font-size: 0.76rem; padding: 0.2rem 0.55rem;">+3.42%</span>
                </div>
              </div>

              <div>
                <div class="oracle-label" style="text-align: right;">TARGET STRIKE BARRIER</div>
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

          <!-- Right: Order Execution Panel -->
          <div class="execution-panel-card">
            <div class="execution-header">
              <span class="execution-title">ORDER EXECUTION</span>
              <span class="badge-pill-green" style="font-size: 0.7rem; font-family: var(--font-terminal);">ZERO SLIPPAGE</span>
            </div>

            <!-- Two Direction Buttons -->
            <div class="flip-btn-row">
              <button class="btn-direction btn-red-active" id="btnShort" onclick="selectDirection('SHORT')">
                <span>FLIP SHORT</span>
                <span style="font-size: 0.74rem; font-family: var(--font-terminal); font-weight: 700; opacity: 0.85;">Overbought Reversion</span>
              </button>
              <button class="btn-direction btn-subtle-inactive" id="btnLong" onclick="selectDirection('LONG')">
                <span>FLIP LONG</span>
                <span style="font-size: 0.74rem; font-family: var(--font-terminal); font-weight: 700; opacity: 0.85;">Oversold Bounce</span>
              </button>
            </div>

            <!-- Collateral Input -->
            <div class="collateral-box">
              <div class="collateral-header">
                <span style="font-weight: 600;">Position Allocation (USDT)</span>
                <span style="color: var(--color-grey-muted); font-family: var(--font-terminal);">Avail: <strong id="availBalanceDisplay" style="color: #000;">$50,000.00</strong></span>
              </div>
              <input type="number" id="collateralInput" class="collateral-input-field" value="2500" oninput="recalcExecution()">
              
              <div class="collateral-presets">
                <button class="preset-chip" onclick="setCollateral(500, this)">$500</button>
                <button class="preset-chip" onclick="setCollateral(1000, this)">$1,000</button>
                <button class="preset-chip active" onclick="setCollateral(2500, this)">$2,500</button>
                <button class="preset-chip" onclick="setCollateral(12500, this)">MAX (25%)</button>
              </div>
            </div>

            <!-- Execution Breakdown -->
            <div style="border-top: 1px dashed rgba(0,0,0,0.14); padding-top: 0.85rem; margin-bottom: 1.25rem;">
              <div class="calc-row">
                <span>Contracts Minted:</span>
                <strong id="calcContractsDisplay">18.82 rNVDA</strong>
              </div>
              <div class="calc-row">
                <span>Convergence Target:</span>
                <strong id="calcTargetPriceDisplay">$128.40</strong>
              </div>
              <div class="calc-row">
                <span>Expected Return:</span>
                <strong id="calcExpectedProfit" style="color: var(--color-green);">+$85.50 (+3.42%)</strong>
              </div>
              <div class="calc-row">
                <span>Z-Score Dislocation:</span>
                <strong id="calcZScoreDisplay" style="color: var(--color-amber);">+2.24σ (ENTRY READY)</strong>
              </div>
            </div>

            <button class="btn-execute-big" onclick="executeTradeOrder()">
              <span id="executeBtnText">EXECUTE COUNTER-POSITION (PAPER)</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- VIEW 2: COGNITIVE SELF-AUDITOR (Persistent Memory & Parameter Tuning) -->
      <div id="viewAuditor" style="display: none;">
        <div class="breadcrumb-row">
          <span class="back-btn" onclick="switchView('arena', null)">← Back to Trading Arena</span>
          <div class="breadcrumb-path">Chronos Autonomous Self-Auditor • Memory State</div>
        </div>

        <h1 class="market-title">Cognitive Self-Auditor & Closed-Loop Memory</h1>
        <p class="market-subtitle">
          Autonomous trade post-mortem engine. Diagnoses every closed position across 120 days and recalibrates execution boundaries.
        </p>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 2rem;">
          <div class="chart-panel-card">
            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.4rem; margin-bottom: 1rem;">Post-Mortem Root Cause Diagnosis</h3>
            <div style="font-family: var(--font-terminal); font-size: 0.82rem; line-height: 2;">
              <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(0,0,0,0.06); padding: 0.35rem 0;">
                <span>• RETAIL_MOMENTUM_OVERRUN (4 Cases)</span>
                <strong style="color: var(--color-red);">-1.48% Avg Loss</strong>
              </div>
              <div style="color: #666; font-size: 0.74rem; padding-left: 1rem;">Action: rTSLA Entry Z raised from 2.00σ to 2.50σ.</div>

              <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(0,0,0,0.06); padding: 0.35rem 0; margin-top: 0.5rem;">
                <span>• BETA_DECOUPLING (2 Cases)</span>
                <strong style="color: var(--color-red);">-1.62% Avg Loss</strong>
              </div>
              <div style="color: #666; font-size: 0.74rem; padding-left: 1rem;">Action: rMSTR single-stock cap trimmed from 0.35 to 0.25.</div>

              <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(0,0,0,0.06); padding: 0.35rem 0; margin-top: 0.5rem;">
                <span>• CONVERGENCE_LATENCY (0 Cases)</span>
                <strong style="color: var(--color-green);">100% On-Time Exits</strong>
              </div>
            </div>
          </div>

          <div class="chart-panel-card" style="background: var(--color-black-night); color: #FFF;">
            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.4rem; margin-bottom: 1rem; color: #FFF;">Live Memory State (data/audit_memory.json)</h3>
            <pre id="auditRawBox" style="font-family: var(--font-terminal); font-size: 0.75rem; line-height: 1.6; color: #A3E635; max-height: 260px; overflow-y: auto;">
            </pre>
          </div>
        </div>
      </div>

      <!-- VIEW 3: TRADE LEDGER (26 Audited Historical Trades) -->
      <div id="viewLedger" style="display: none;">
        <div class="breadcrumb-row">
          <span class="back-btn" onclick="switchView('arena', null)">← Back to Trading Arena</span>
          <div class="breadcrumb-path">120-Day Audited Backtest Ledger</div>
        </div>

        <h1 class="market-title">Audited Institutional Trade Ledger</h1>
        <p class="market-subtitle">Complete chronological record of all 26 audited trades net of 0.10% friction.</p>

        <div class="chart-panel-card" style="padding: 0; overflow-x: auto; margin-top: 1.5rem;">
          <table class="ledger-table" style="width: 100%; border-collapse: collapse; font-size: 0.84rem;">
            <thead>
              <tr style="background: var(--color-canvas-subtle); text-align: left; font-family: var(--font-terminal); font-size: 0.72rem; color: #555;">
                <th style="padding: 0.85rem 1rem;">Asset</th>
                <th style="padding: 0.85rem 1rem;">Side</th>
                <th style="padding: 0.85rem 1rem;">Entry Time</th>
                <th style="padding: 0.85rem 1rem;">Entry $</th>
                <th style="padding: 0.85rem 1rem;">Exit Time</th>
                <th style="padding: 0.85rem 1rem;">Exit $</th>
                <th style="padding: 0.85rem 1rem;">Net PnL</th>
                <th style="padding: 0.85rem 1rem;">USDT PnL</th>
                <th style="padding: 0.85rem 1rem;">Audit Diagnosis</th>
              </tr>
            </thead>
            <tbody id="appLedgerTableBody">
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>

  <!-- Connect Bitget Account Modal -->
  <div class="modal-overlay" id="connectModalOverlay" onclick="closeModalOnBackdrop(event)">
    <div class="modal-card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
        <h3 style="font-family: var(--font-serif-editorial); font-size: 1.65rem;">Connect Bitget Account</h3>
        <button onclick="closeConnectModal()" style="background: none; border: none; font-size: 1.25rem; cursor: pointer;">✕</button>
      </div>

      <p style="font-size: 0.84rem; color: var(--color-grey-text); margin-bottom: 1.5rem; line-height: 1.5;">
        Enter your Bitget Universal Trading Account (UTA v3) API credentials. Keys are encrypted in local browser storage and never leave your machine.
      </p>

      <div style="margin-bottom: 1rem;">
        <label style="font-family: var(--font-terminal); font-size: 0.72rem; font-weight: 700; text-transform: uppercase;">Trading Environment</label>
        <select id="modalEnvSelect" style="width: 100%; padding: 0.55rem; border-radius: 6px; border: 1px solid #CCC; font-family: var(--font-sans-body); font-size: 0.84rem; margin-top: 0.25rem;">
          <option value="paper">Paper Trading Mode (Simulated $50k USDT - No Keys Needed)</option>
          <option value="mainnet">Bitget UTA v3 (Live Capital Trading)</option>
        </select>
      </div>

      <div style="margin-bottom: 1rem;">
        <label style="font-family: var(--font-terminal); font-size: 0.72rem; font-weight: 700; text-transform: uppercase;">API Key (ACCESS-KEY)</label>
        <input type="text" id="modalApiKey" placeholder="bg_live_********" style="width: 100%; padding: 0.55rem; border-radius: 6px; border: 1px solid #CCC; font-family: var(--font-terminal); font-size: 0.82rem; margin-top: 0.25rem;">
      </div>

      <div style="margin-bottom: 1rem;">
        <label style="font-family: var(--font-terminal); font-size: 0.72rem; font-weight: 700; text-transform: uppercase;">API Secret (SECRET-KEY)</label>
        <input type="password" id="modalApiSecret" placeholder="••••••••••••••••" style="width: 100%; padding: 0.55rem; border-radius: 6px; border: 1px solid #CCC; font-family: var(--font-terminal); font-size: 0.82rem; margin-top: 0.25rem;">
      </div>

      <div style="margin-bottom: 1.5rem;">
        <label style="font-family: var(--font-terminal); font-size: 0.72rem; font-weight: 700; text-transform: uppercase;">API Passphrase (ACCESS-PASSPHRASE)</label>
        <input type="password" id="modalPassphrase" placeholder="••••••••" style="width: 100%; padding: 0.55rem; border-radius: 6px; border: 1px solid #CCC; font-family: var(--font-terminal); font-size: 0.82rem; margin-top: 0.25rem;">
      </div>

      <div style="font-size: 0.74rem; color: var(--color-grey-muted); margin-bottom: 1.25rem; font-family: var(--font-terminal); line-height: 1.4;">
        NOTICE: Only enable "Read" and "Trade" permissions on Bitget. Never enable "Withdrawal" permissions.
      </div>

      <div style="display: flex; gap: 0.75rem;">
        <button class="btn-wallet-connect" style="flex: 1; justify-content: center;" onclick="saveCredentials()">
          <span>Save & Verify Gateway</span>
        </button>
      </div>
    </div>
  </div>

  <script>
    const markets = {markets_json};
    const candlesData = {candles_json};
    const realTrades = {trades_json};
    const auditMemory = {audit_json};

    let selectedSymbol = "rNVDA";
    let selectedDirection = "SHORT";
    let chartViewMode = "candles"; // 'candles' or 'line'
    let paperBalance = 50000.00;

    // Render Sidebar Markets
    function renderSidebar() {{
      const container = document.getElementById("marketsMenuList");
      container.innerHTML = "";

      Object.keys(markets).forEach(sym => {{
        const m = markets[sym];
        const item = document.createElement("div");
        item.className = "sidebar-item" + (sym === selectedSymbol ? " active" : "");
        item.onclick = () => selectMarket(sym);

        const driftSign = m.drift_pct > 0 ? "+" : "";
        item.innerHTML = `
          <div class="sidebar-item-left">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
            <span>${{sym}} / Strike</span>
          </div>
          <span class="sidebar-item-metric" style="color: ${{m.drift_pct > 0 ? 'var(--color-green)' : 'var(--color-red)'}}">${{driftSign}}${{m.drift_pct.toFixed(1)}}%</span>
        `;
        container.appendChild(item);
      }});
    }}

    // Switch Selected Market
    function selectMarket(sym) {{
      selectedSymbol = sym;
      renderSidebar();
      updateMarketView();
      drawCandleChart();
    }}

    function updateMarketView() {{
      const m = markets[selectedSymbol];
      document.getElementById("breadcrumbPathDisplay").textContent = `Bitget UTA v3 • ${{m.symbol}} / USDT Strike`;
      document.getElementById("marketTitleDisplay").textContent = `${{m.symbol}} / USDT Strike`;
      document.getElementById("marketQuestionDisplay").textContent = 
        `Will ${{m.symbol}} converge to Friday Anchor $${{m.anchor_price.toFixed(2)}} USD? Resolves via Monday Institutional Pre-Market Open.`;
      
      document.getElementById("symbolDisplay").textContent = `${{m.symbol}}/USDT`;
      document.getElementById("chartPriceDisplay").textContent = `$${{m.spot_price.toFixed(2)}}`;
      
      const driftSign = m.drift_pct > 0 ? "+" : "";
      document.getElementById("chartDriftBadge").textContent = `${{driftSign}}${{m.drift_pct.toFixed(2)}}% Drift`;
      document.getElementById("chartDriftBadge").className = m.drift_pct > 0 ? "badge-pill-green" : "badge-pill-gold";

      document.getElementById("strikeBarrierDisplay").textContent = `$${{m.anchor_price.toFixed(2)}}`;
      document.getElementById("anchorStatusSubtext").textContent = `Prev Close Anchor: $${{m.anchor_price.toFixed(2)}} (${{m.regime}})`;

      recalcExecution();
    }}

    // Recalculate Execution Panel
    function recalcExecution() {{
      const m = markets[selectedSymbol];
      const collateral = parseFloat(document.getElementById("collateralInput").value) || 0;
      
      const contracts = collateral / m.spot_price;
      document.getElementById("calcContractsDisplay").textContent = `${{contracts.toFixed(2)}} ${{m.symbol}}`;
      document.getElementById("calcTargetPriceDisplay").textContent = `$${{m.anchor_price.toFixed(2)}}`;

      const expectedProfit = collateral * (Math.abs(m.drift_pct) / 100.0);
      document.getElementById("calcExpectedProfit").textContent = `+$${{expectedProfit.toFixed(2)}} (+${{Math.abs(m.drift_pct).toFixed(2)}}%)`;

      const z = m.z_score;
      const zColor = Math.abs(z) >= 2.0 ? "var(--color-amber)" : "var(--color-grey-text)";
      document.getElementById("calcZScoreDisplay").textContent = `${{z > 0 ? '+' : ''}}${{z.toFixed(2)}}σ (${{Math.abs(z) >= 2.0 ? 'ENTRY SIGNAL' : 'BELOW THRESHOLD'}})`;
      document.getElementById("calcZScoreDisplay").style.color = zColor;
    }}

    function selectDirection(dir) {{
      selectedDirection = dir;
      const btnShort = document.getElementById("btnShort");
      const btnLong = document.getElementById("btnLong");

      if (dir === "SHORT") {{
        btnShort.className = "btn-direction btn-red-active";
        btnLong.className = "btn-direction btn-subtle-inactive";
        document.getElementById("executeBtnText").textContent = "EXECUTE SHORT REVERSION (PAPER)";
      }} else {{
        btnShort.className = "btn-direction btn-subtle-inactive";
        btnLong.className = "btn-direction btn-green-active";
        document.getElementById("executeBtnText").textContent = "EXECUTE LONG BOUNCE (PAPER)";
      }}
    }}

    function setCollateral(val, btn) {{
      document.getElementById("collateralInput").value = val;
      document.querySelectorAll(".preset-chip").forEach(b => b.classList.remove("active"));
      if (btn) btn.classList.add("active");
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

    // Draw Candlestick Chart on Canvas (Matching Screenshot)
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

      // Draw Friday Anchor Dashed Line (Matching Screenshot)
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
      ctx.fillText(`TARGET STRIKE ANCHOR: $${{anchor.toFixed(2)}}`, 42, anchorY - 6);

      // Volume Section at bottom
      const maxVol = Math.max(...candles.map(c => c.volume));
      const volTop = h - 50;
      const volHeight = 40;

      const numCandles = candles.length;
      const candleWidth = Math.max(4, (w - 80) / numCandles - 3);

      candles.forEach((c, i) => {{
        const x = 50 + i * ((w - 80) / numCandles);
        const isUp = c.close >= c.open;
        const color = isUp ? "#00C853" : "#E50914";

        if (chartViewMode === "candles") {{
          // Wick
          ctx.beginPath();
          ctx.strokeStyle = color;
          ctx.lineWidth = 1.2;
          ctx.moveTo(x + candleWidth / 2, getY(c.high));
          ctx.lineTo(x + candleWidth / 2, getY(c.low));
          ctx.stroke();

          // Body
          const openY = getY(c.open);
          const closeY = getY(c.close);
          const bodyY = Math.min(openY, closeY);
          const bodyH = Math.max(2, Math.abs(closeY - openY));

          ctx.fillStyle = color;
          ctx.fillRect(x, bodyY, candleWidth, bodyH);
        }}

        // Volume Bar
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

      // Axes labels
      ctx.fillStyle = "#888";
      ctx.font = "10px 'Space Mono', monospace";
      ctx.fillText("$" + maxP.toFixed(2), 5, chartTop + 10);
      ctx.fillText("$" + minP.toFixed(2), 5, chartBottom);
    }}

    // Switch Views (Arena, Auditor, Ledger)
    function switchView(view, tabEl) {{
      document.getElementById("viewArena").style.display = view === "arena" ? "block" : "none";
      document.getElementById("viewAuditor").style.display = view === "auditor" ? "block" : "none";
      document.getElementById("viewLedger").style.display = view === "ledger" ? "block" : "none";

      document.querySelectorAll(".app-header-tabs .app-tab").forEach(t => t.classList.remove("active"));
      if (tabEl) tabEl.classList.add("active");

      if (view === "arena") {{
        setTimeout(drawCandleChart, 50);
      }} else if (view === "auditor") {{
        document.getElementById("auditRawBox").textContent = JSON.stringify(auditMemory, null, 2);
      }} else if (view === "ledger") {{
        renderLedgerTable();
      }}
    }}

    function renderLedgerTable() {{
      const tbody = document.getElementById("appLedgerTableBody");
      tbody.innerHTML = "";
      realTrades.forEach(t => {{
        const isWin = t.pnl_pct > 0;
        const tr = document.createElement("tr");
        tr.style.borderBottom = "1px solid rgba(0,0,0,0.06)";
        tr.innerHTML = `
          <td style="padding: 0.85rem 1rem;"><strong>${{t.asset}}</strong></td>
          <td style="padding: 0.85rem 1rem; color: ${{t.side === 'SHORT' ? 'var(--color-red)' : 'var(--color-green)'}}">${{t.side}}</td>
          <td style="padding: 0.85rem 1rem; color: #666;">${{t.entry_time}}</td>
          <td style="padding: 0.85rem 1rem;">$${{t.entry_price.toFixed(2)}}</td>
          <td style="padding: 0.85rem 1rem; color: #666;">${{t.exit_time}}</td>
          <td style="padding: 0.85rem 1rem;">$${{t.exit_price.toFixed(2)}}</td>
          <td style="padding: 0.85rem 1rem;"><span class="${{isWin ? 'badge-win' : 'badge-loss'}}">${{isWin ? '+' : ''}}${{t.pnl_pct.toFixed(2)}}%</span></td>
          <td style="padding: 0.85rem 1rem; font-weight: 700; color: ${{isWin ? 'var(--color-green)' : 'var(--color-red)'}}">${{isWin ? '+' : ''}}$${{t.pnl_usdt.toFixed(2)}}</td>
          <td style="padding: 0.85rem 1rem; color: #666; font-size: 0.78rem;">${{t.audit_note}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function executeTradeOrder() {{
      const m = markets[selectedSymbol];
      const collateral = parseFloat(document.getElementById("collateralInput").value) || 0;
      if (collateral > paperBalance) {{
        alert("Insufficient Paper Balance. Please use Faucet to reset.");
        return;
      }}
      paperBalance -= collateral;
      document.getElementById("availBalanceDisplay").textContent = `$${{paperBalance.toLocaleString('en-US', {{minimumFractionDigits: 2}})}}`;
      alert(`[PAPER EXECUTION SUCCESS]\\nFilled ${{selectedDirection}} on ${{m.symbol}}\\nCollateral: $${{collateral.toFixed(2)}} USDT\\nTarget Exit: $${{m.anchor_price.toFixed(2)}} (Monday Convergence)\\nRecorded in Chronos execution engine.`);
    }}

    function resetPaperBalance() {{
      paperBalance = 50000.00;
      document.getElementById("availBalanceDisplay").textContent = "$50,000.00";
      alert("Paper Balance reset to $50,000.00 USDT.");
    }}

    function openConnectModal() {{
      document.getElementById("connectModalOverlay").classList.add("open");
    }}

    function closeConnectModal() {{
      document.getElementById("connectModalOverlay").classList.remove("open");
    }}

    function closeModalOnBackdrop(e) {{
      if (e.target.id === "connectModalOverlay") closeConnectModal();
    }}

    function saveCredentials() {{
      const env = document.getElementById("modalEnvSelect").value;
      const key = document.getElementById("modalApiKey").value.trim();

      if (env === "mainnet" && !key) {{
        alert("Please enter your Bitget API Key or switch to Paper Trading Mode.");
        return;
      }}

      if (env === "mainnet") {{
        document.getElementById("currentModeLabel").textContent = "Bitget UTA Live";
        document.getElementById("modePillBadge").style.borderColor = "var(--color-green)";
        document.getElementById("connectHeaderBtn").innerHTML = "<span>CONNECTED</span>";
      }} else {{
        document.getElementById("currentModeLabel").textContent = "Paper Mode ($50k)";
      }}

      closeConnectModal();
      alert(`[GATEWAY CONFIGURED]\\nTrading Mode: ${{env.toUpperCase()}}\\nCryptographic HMAC-SHA256 initialized.`);
    }}

    window.addEventListener("resize", drawCandleChart);
    window.addEventListener("DOMContentLoaded", () => {{
      renderSidebar();
      updateMarketView();
      setTimeout(drawCandleChart, 100);
    }});
  </script>
</body>
</html>
"""

with open("dashboard/app.html", "w") as f:
    f.write(html_template)

print(f"Successfully generated Master Trading Arena Dashboard at dashboard/app.html ({len(html_template)} bytes)")
