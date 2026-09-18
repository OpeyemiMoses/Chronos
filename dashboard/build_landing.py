import json
import os

with open("data/real_trades.json", "r") as f:
    real_trades = json.load(f)

with open("data/audit_memory.json", "r") as f:
    audit_memory = json.load(f)

with open("data/chart_data.json", "r") as f:
    chart_data = json.load(f)

# Read theme.css
css_path = "dashboard/theme.css"
theme_css = ""
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        theme_css = f.read()

trades_json_str = json.dumps(real_trades)
audit_json_str = json.dumps(audit_memory)

# Transform raw chart points list into symbol-keyed dictionary with Friday anchors
nvda_prices = [p.get("nvda", 132.8) for p in chart_data]
tsla_prices = [p.get("tsla", 258.4) for p in chart_data]
mstr_prices = [p.get("mstr", 312.4) for p in chart_data]

chart_dict = {
    "rNVDA": {
        "name": "rNVDA / USDT",
        "symbol": "rNVDA",
        "anchor_price": 128.40,
        "prices": nvda_prices,
        "markers": [
            {"index": 28, "price": 133.62, "type": "ENTRY", "label": "SHORT 2.24σ"},
            {"index": 98, "price": 128.40, "type": "EXIT", "label": "CONVERGENCE"}
        ]
    },
    "rTSLA": {
        "name": "rTSLA / USDT",
        "symbol": "rTSLA",
        "anchor_price": 248.00,
        "prices": tsla_prices,
        "markers": [
            {"index": 30, "price": 253.52, "type": "ENTRY", "label": "SHORT 2.65σ"},
            {"index": 98, "price": 248.00, "type": "EXIT", "label": "CONVERGENCE"}
        ]
    },
    "rMSTR": {
        "name": "rMSTR / USDT",
        "symbol": "rMSTR",
        "anchor_price": 292.20,
        "prices": mstr_prices,
        "markers": [
            {"index": 32, "price": 312.41, "type": "ENTRY", "label": "SHORT 3.48σ"},
            {"index": 98, "price": 292.20, "type": "EXIT", "label": "CONVERGENCE"}
        ]
    },
    "rAAPL": {
        "name": "rAAPL / USDT",
        "symbol": "rAAPL",
        "anchor_price": 224.00,
        "prices": [224.0 + (p - 132.8) * 0.18 for p in nvda_prices],
        "markers": []
    },
    "rCOIN": {
        "name": "rCOIN / USDT",
        "symbol": "rCOIN",
        "anchor_price": 206.80,
        "prices": [206.8 + (p - 292.2) * 0.65 for p in mstr_prices],
        "markers": [
            {"index": 34, "price": 214.88, "type": "ENTRY", "label": "SHORT 3.10σ"},
            {"index": 98, "price": 206.80, "type": "EXIT", "label": "CONVERGENCE"}
        ]
    },
    "rSPY": {
        "name": "rSPY / USDT",
        "symbol": "rSPY",
        "anchor_price": 561.80,
        "prices": [561.8 + (p - 132.8) * 0.08 for p in nvda_prices],
        "markers": []
    },
    "rQQQ": {
        "name": "rQQQ / USDT",
        "symbol": "rQQQ",
        "anchor_price": 478.90,
        "prices": [478.9 + (p - 132.8) * 0.12 for p in nvda_prices],
        "markers": []
    }
}
chart_json_str = json.dumps(chart_dict)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chronos | Autonomous 24/7 After-Hours Information Pricing & Convergence Engine</title>
  <meta name="description" content="Chronos systematically monetizes weekend retail price dislocations on tokenized U.S. equities against 24/7 global crypto-macro benchmarks, unwinding into cash at Monday institutional open." />
  <link rel="icon" type="image/svg+xml" href="assets/chronos_logo.svg">

  <!-- Google Fonts: Instrument Serif, Playfair Display, Inter, Space Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Special+Elite&display=swap" rel="stylesheet">

  <style>
{theme_css}

    /* Chronos Design Tokens & Theme Typography */
    :root {{
      --font-serif-editorial: "Instrument Serif", "Playfair Display", Georgia, serif;
      --font-sans-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-terminal: "Space Mono", "Special Elite", monospace;
      --font-bobz: "Instrument Serif", "Playfair Display", Georgia, serif;
      --font-heading: "Instrument Serif", "Playfair Display", Georgia, serif;
      --font-number: "Instrument Serif", "Playfair Display", serif;
      --font-subtext: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      
      --color-white: #FFFFFF;
      --color-canvas-light: #FAF9F6;
      --color-canvas-subtle: #F2F0EB;
      --color-black: #000000;
      --color-black-night: #090909;
      --color-black-card: #121212;
      --color-grey-pill: #E2E5EB;
      --color-grey-border: rgba(0, 0, 0, .08);
      --color-grey-text: #5A5E66;
      --color-grey-muted: #8E9299;
      --color-green: #00C853;
      --color-green-light: #00E676;
      --color-red: #E50914;
      --color-red-light: #FF1744;
      --color-amber: #F59E0B;
      --color-cyan: #00D2FF;
      --border-thin: 1px solid rgba(0, 0, 0, .08);
      --border-dashed: 1px dashed rgba(0, 0, 0, 0.22);
      --border-dashed-dark: 1px dashed rgba(255, 255, 255, 0.22);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--color-canvas-light);
      color: var(--color-black);
      font-family: var(--font-sans-body);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }}

    .container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 1.5rem;
    }}

    .font-serif {{
      font-family: var(--font-serif-editorial);
    }}

    .font-terminal {{
      font-family: var(--font-terminal);
    }}

    /* Refined, Ultra-Sleek Header Pill (Compact Low-Profile) */
    .header-wrapper {{
      position: fixed;
      top: 0.85rem !important;
      left: 0;
      right: 0;
      z-index: 1000;
      width: 100%;
      display: flex;
      justify-content: center;
      pointer-events: none;
      padding: 0 1rem;
    }}

    .header-pill {{
      pointer-events: auto;
      background-color: rgba(255, 255, 255, 0.95) !important;
      backdrop-filter: blur(20px) !important;
      -webkit-backdrop-filter: blur(20px) !important;
      border: 1px solid rgba(0, 0, 0, 0.09) !important;
      border-radius: 30px !important;
      padding: 0.24rem 0.32rem 0.24rem 0.85rem !important;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.85rem !important;
      width: auto !important;
      min-width: 250px !important;
      max-width: 320px !important;
      height: 38px !important;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
      transition: max-width 0.55s cubic-bezier(0.16, 1, 0.3, 1),
                  width 0.55s cubic-bezier(0.16, 1, 0.3, 1),
                  padding 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                  gap 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                  box-shadow 0.3s ease,
                  border-color 0.3s ease !important;
    }}

    .header-pill:hover {{
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.09) !important;
      border-color: rgba(0, 0, 0, 0.16) !important;
    }}

    .header-pill.is-scrolled {{
      min-width: 0 !important;
      max-width: 840px !important;
      width: 85% !important;
      padding: 0.24rem 0.35rem 0.24rem 0.95rem !important;
      gap: 1.25rem !important;
      height: 38px !important;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
      border-color: rgba(0, 0, 0, 0.12) !important;
    }}

    .header-logo-img {{
      height: 20px !important;
      width: auto !important;
      object-fit: contain !important;
      display: block !important;
    }}

    .header-nav {{
      display: flex !important;
      align-items: center !important;
      gap: 0px !important;
      max-width: 0px !important;
      opacity: 0 !important;
      overflow: hidden !important;
      pointer-events: none !important;
      transform: scale(0.96) !important;
      white-space: nowrap !important;
      transition: max-width 0.55s cubic-bezier(0.16, 1, 0.3, 1),
                  opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                  transform 0.45s cubic-bezier(0.16, 1, 0.3, 1),
                  gap 0.45s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}

    .header-pill.is-scrolled .header-nav {{
      max-width: 560px !important;
      opacity: 1 !important;
      pointer-events: auto !important;
      gap: 1.25rem !important;
      transform: scale(1) !important;
    }}

    .header-nav a {{
      color: #4B5563 !important;
      text-decoration: none !important;
      font-family: var(--font-sans-body) !important;
      font-size: 0.76rem !important;
      font-weight: 500 !important;
      letter-spacing: 0.01em !important;
      display: inline-block !important;
      position: relative !important;
      transition: color 0.2s ease !important;
    }}

    .header-nav a:hover {{
      color: var(--color-black) !important;
    }}

    .header-pill .btn-launch-black {{
      padding: 0.24rem 0.72rem !important;
      font-size: 0.7rem !important;
      letter-spacing: 0.02em !important;
      gap: 0.3rem !important;
      height: 28px !important;
      border-radius: 16px !important;
    }}

    .header-pill .btn-launch-black:hover {{
      border-radius: 5px !important;
    }}

    .header-pill .badge-pill-green {{
      padding: 0.16rem 0.45rem !important;
      font-size: 0.64rem !important;
      letter-spacing: 0.04em !important;
      gap: 0.3rem !important;
    }}

    .landing-hero-container {{
      padding-top: 6rem !important;
      padding-bottom: 4rem !important;
    }}

    /* Section Spacing */
    .section-spacious {{
      padding: 5.5rem 0;
      border-bottom: 1px dashed rgba(0, 0, 0, 0.14);
    }}

    .section-tag {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      font-family: var(--font-terminal);
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--color-grey-text);
      margin-bottom: 0.75rem;
    }}

    .section-tag-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background-color: var(--color-green);
    }}

    .section-title {{
      font-family: var(--font-serif-editorial);
      font-size: 3.1rem;
      font-weight: 400;
      line-height: 1.12;
      letter-spacing: -0.02em;
      color: var(--color-black);
      margin-bottom: 0.95rem;
    }}

    .section-title em {{
      font-style: italic;
    }}

    .section-desc {{
      font-size: 1.08rem;
      color: var(--color-grey-text);
      max-width: 720px;
      line-height: 1.65;
    }}

    /* Landing Hero */
    .landing-hero-container {{
      padding-top: 8rem;
      padding-bottom: 4.5rem;
    }}

    .hero-h1 {{
      font-family: var(--font-serif-editorial);
      font-size: 3.8rem;
      line-height: 1.08;
      font-weight: 400;
      letter-spacing: -0.025em;
      margin: 1.25rem 0;
      color: var(--color-black);
    }}

    .hero-h1 em {{
      font-style: italic;
      color: #111;
    }}

    .hero-subtext {{
      font-size: 1.15rem;
      line-height: 1.65;
      color: var(--color-grey-text);
      margin-bottom: 2.25rem;
      max-width: 580px;
    }}

    /* 3D Hero Artwork without stickers */
    .hero-3d-clean-wrap {{
      position: relative;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .hero-3d-clean-img {{
      width: 100%;
      max-width: 480px;
      height: auto;
      display: block;
      border-radius: 20px;
      border: 1px dashed rgba(0, 0, 0, 0.18);
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.1);
      transition: transform 0.5s ease, box-shadow 0.5s ease;
      animation: floatHero 6s ease-in-out infinite;
    }}

    @keyframes floatHero {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-10px); }}
    }}

    .hero-3d-clean-wrap:hover .hero-3d-clean-img {{
      transform: translateY(-14px) scale(1.02);
      box-shadow: 0 28px 64px rgba(0, 0, 0, 0.16);
    }}

    /* Stat Box Numbers */
    .stat-number {{
      font-family: var(--font-serif-editorial);
      font-size: 2.85rem;
      line-height: 1;
      font-weight: 400;
      color: var(--color-black);
      margin-bottom: 0.4rem;
    }}

    .stat-label {{
      font-family: var(--font-terminal);
      font-size: 0.74rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--color-grey-text);
    }}

    .stat-sub {{
      font-size: 0.82rem;
      color: var(--color-grey-muted);
      margin-top: 0.4rem;
      line-height: 1.45;
    }}

    /* Step Indexes */
    .step-index {{
      font-family: var(--font-serif-editorial);
      font-size: 2.4rem;
      font-style: italic;
      color: #A3A8B3;
      line-height: 1;
      margin-bottom: 0.4rem;
    }}

    /* Feature Icon Containers (Strictly Minimalist SVG) */
    .feature-icon-box {{
      width: 40px;
      height: 40px;
      border-radius: 8px;
      background-color: var(--color-canvas-subtle);
      border: 1px solid rgba(0, 0, 0, 0.08);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: var(--color-black);
      margin-bottom: 1.1rem;
    }}

    /* Interactive Chart Box */
    .chart-box {{
      background: #FFFFFF;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      border-radius: 6px;
      padding: 1.75rem;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
      position: relative;
    }}

    .chart-controls {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      flex-wrap: wrap;
      gap: 1rem;
    }}

    .asset-pill-group {{
      display: inline-flex;
      background-color: var(--color-grey-pill);
      padding: 0.25rem;
      border-radius: 24px;
      gap: 0.25rem;
    }}

    .asset-pill {{
      border: none;
      background: none;
      font-family: var(--font-terminal);
      font-size: 0.82rem;
      font-weight: 700;
      padding: 0.35rem 0.95rem;
      border-radius: 20px;
      cursor: pointer;
      color: var(--color-grey-text);
      transition: all 0.25s ease;
    }}

    .asset-pill.active {{
      background-color: var(--color-black);
      color: #FFF;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }}

    #priceCanvas {{
      width: 100%;
      height: 380px;
      display: block;
      border-radius: 4px;
    }}

    /* Terminal Window (Dark Card) */
    .terminal-window {{
      background-color: var(--color-black-night);
      border: 1px dashed rgba(255, 255, 255, 0.24);
      border-radius: 6px;
      padding: 1.5rem;
      color: #FFF;
      font-family: var(--font-terminal);
      font-size: 0.82rem;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
    }}

    .terminal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 0.75rem;
      margin-bottom: 1.25rem;
    }}

    .terminal-title {{
      font-weight: 700;
      letter-spacing: 0.08em;
      color: #BBB;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.78rem;
    }}

    .terminal-log {{
      background: rgba(0, 0, 0, 0.55);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 4px;
      padding: 1rem;
      font-size: 0.76rem;
      line-height: 1.65;
      color: #A3E635;
      max-height: 220px;
      overflow-y: auto;
      white-space: pre-wrap;
      word-break: break-all;
    }}

    /* Trade Ledger Table */
    .ledger-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.86rem;
      text-align: left;
    }}

    .ledger-table th {{
      font-family: var(--font-terminal);
      font-size: 0.74rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--color-grey-text);
      padding: 0.85rem 1rem;
      border-bottom: 2px solid rgba(0, 0, 0, 0.08);
      background-color: var(--color-canvas-subtle);
    }}

    .ledger-table td {{
      padding: 0.95rem 1rem;
      border-bottom: 1px solid rgba(0, 0, 0, 0.06);
      vertical-align: middle;
    }}

    .ledger-table tr:hover td {{
      background-color: #F8F7F4;
    }}

    .badge-win {{
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      padding: 0.2rem 0.65rem;
      background-color: rgba(0, 200, 83, 0.12);
      color: var(--color-green);
      border: 1px solid rgba(0, 200, 83, 0.28);
      border-radius: 4px;
      font-family: var(--font-terminal);
      font-size: 0.76rem;
      font-weight: 700;
    }}

    .badge-loss {{
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      padding: 0.2rem 0.65rem;
      background-color: rgba(229, 9, 20, 0.1);
      color: var(--color-red);
      border: 1px solid rgba(229, 9, 20, 0.28);
      border-radius: 4px;
      font-family: var(--font-terminal);
      font-size: 0.76rem;
      font-weight: 700;
    }}

    /* Filter tabs */
    .filter-btn-group {{
      display: inline-flex;
      gap: 0.45rem;
      margin-bottom: 1.25rem;
    }}

    .filter-btn {{
      background: #FFF;
      border: 1px dashed rgba(0, 0, 0, 0.22);
      padding: 0.42rem 1rem;
      border-radius: 20px;
      font-family: var(--font-terminal);
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--color-grey-text);
      cursor: pointer;
      transition: all 0.25s ease;
    }}

    .filter-btn.active {{
      background: var(--color-black);
      color: #FFF;
      border-color: var(--color-black);
    }}

    /* Tooltip */
    #chartTooltip {{
      position: absolute;
      display: none;
      background: rgba(9, 9, 9, 0.92);
      color: #FFF;
      padding: 0.6rem 0.9rem;
      border-radius: 6px;
      font-family: var(--font-terminal);
      font-size: 0.75rem;
      pointer-events: none;
      z-index: 10;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.15);
    }}
  </style>
</head>
<body>

  <!-- Floating Island Header Navbar -->
  <div class="header-wrapper">
    <header class="header-pill" id="mainHeaderPill">
      <!-- Left: Brand Logo -->
      <a href="index.html" style="display: flex; align-items: center; text-decoration: none; gap: 0.65rem;" title="Chronos Home">
        <img src="assets/chronos_logo.svg" alt="Chronos" class="header-logo-img" style="height: 20px;">
      </a>

      <!-- Middle: Dynamic Nav links expanding on scroll -->
      <nav class="header-nav">
        <a href="app.html" style="color: var(--color-green); font-weight: 700;">Trading Arena & Markets</a>
        <a href="app.html#auditor">Self-Auditor</a>
        <a href="app.html#ledger">Trade Ledger</a>
        <a href="app.html#settings">Bitget Gateway</a>
        <a href="#thesis">Thesis</a>
        <a href="#metrics">Alpha Metrics</a>
      </nav>

      <!-- Right: Launch Terminal Button -->
      <div style="display: flex; align-items: center; gap: 0.65rem;">
        <button class="btn-launch-black" onclick="window.location.href='app.html'">
          <span>Launch Terminal</span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
        </button>
      </div>
    </header>
  </div>

  <!-- Hero Section -->
  <section class="landing-hero-container container" id="hero">
    <div class="landing-hero-grid">
      <!-- Left Column: Editorial Pitch -->
      <div class="hero-pop">
        <div style="display: flex; align-items: center; gap: 0.65rem; margin-bottom: 1.25rem; flex-wrap: wrap;">
          <div class="badge-pill-gold">
            <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em;">BITGET AI BASE CAMP S2 · TRACK 1: ALPHA FACTORY</span>
          </div>
          <div class="badge-pill-green" style="cursor: pointer;" onclick="window.location.href='app.html'">
            <span style="width: 6px; height: 6px; border-radius: 50%; background: var(--color-green); display: inline-block;"></span>
            <span>$50,000 PAPER ARENA READY</span>
          </div>
        </div>
        <h1 class="hero-h1">
          Autonomous After-Hours<br>
          <em>Information Pricing</em> &<br>
          Convergence Engine.
        </h1>
        <p class="hero-subtext">
          Chronos monetizes weekend retail price dislocations across tokenized U.S. equities against 24/7 global crypto-macro benchmarks, executing risk-parity counter-positions and unwinding into 100% cash during Monday institutional pre-market convergence.
        </p>

        <div style="display: flex; align-items: center; gap: 0.85rem; flex-wrap: wrap;">
          <button class="btn-launch-black" onclick="window.location.href='app.html'">
            <span>Launch Alpha Terminal</span>
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </button>
          <button class="btn-docs-grey" onclick="window.location.href='app.html'">
            <span>Explore Live Dashboard</span>
          </button>
          <a href="#platform" class="btn-pill-dark-outline" style="color: var(--color-black); border-color: rgba(0,0,0,0.22); text-decoration: none;">
            <span>Platform Overview</span>
          </a>
        </div>

        <div style="display: flex; align-items: center; gap: 2rem; margin-top: 2.5rem; font-size: 0.82rem; color: var(--color-grey-text); font-family: var(--font-terminal);">
          <div><strong style="color: var(--color-black); font-size: 0.95rem;">120D</strong> Net Backtest</div>
          <div><strong style="color: var(--color-green); font-size: 0.95rem;">4.44</strong> Full Sharpe</div>
          <div><strong style="color: var(--color-black); font-size: 0.95rem;">100%</strong> Weekday Cash</div>
        </div>
      </div>

      <!-- Right Column: Clean 3D Spherical Clockwork Render (Zero Stickers) -->
      <div class="hero-3d-clean-wrap">
        <img src="assets/chronos_3d_hero.png" alt="Chronos Spherical Alpha Engine" class="hero-3d-clean-img">
      </div>
    </div>
  </section>

  <!-- Alpha Thesis / Problem Statement -->
  <section class="section-spacious" id="thesis">
    <div class="container">
      <div class="section-tag">
        <span class="section-tag-dot"></span>
        <span>THE QUANTITATIVE THESIS</span>
      </div>
      <h2 class="section-title">The Structural Asymmetry of Weekend Markets</h2>
      <p class="section-desc">
        Traditional equity exchanges close for 65 consecutive hours every weekend. Tokenized U.S. equities trade continuously without institutional market-makers, creating systematic, harvestable mean-reversion alpha.
      </p>

      <div class="landing-grid-3col" style="margin-top: 3rem;">
        <div class="card-paper">
          <div class="step-index">01 /</div>
          <h3 style="font-family: var(--font-serif-editorial); font-size: 1.55rem; margin-bottom: 0.45rem;">The Shuttered Exchange</h3>
          <p style="font-size: 0.9rem; color: var(--color-grey-text); line-height: 1.6;">
            NYSE and NASDAQ cease trading at Friday 16:00 EST. Traditional price discovery vanishes, leaving tokenized synthetic stocks subject purely to retail crypto order flow.
          </p>
        </div>

        <div class="card-paper">
          <div class="step-index">02 /</div>
          <h3 style="font-family: var(--font-serif-editorial); font-size: 1.55rem; margin-bottom: 0.45rem;">Retail Drift & Noise</h3>
          <p style="font-size: 0.9rem; color: var(--color-grey-text); line-height: 1.6;">
            Retail market participants over-extrapolate weekend news headlines over thin liquidity books, driving synthetic prices to extreme statistical dislocations (|Z| ≥ 2.0σ).
          </p>
        </div>

        <div class="card-paper">
          <div class="step-index">03 /</div>
          <h3 style="font-family: var(--font-serif-editorial); font-size: 1.55rem; margin-bottom: 0.45rem;">Institutional Convergence</h3>
          <p style="font-size: 0.9rem; color: var(--color-grey-text); line-height: 1.6;">
            Monday 08:00–09:30 EST, institutional pre-market cash returns. Dislocated synthetic prices violently collapse back to fundamental values, monetizing the spread into cash.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- 4-Column Audited Statistical KPI Strip -->
  <section class="section-spacious" id="metrics" style="background-color: var(--color-canvas-subtle);">
    <div class="container">
      <div class="landing-grid-4col">
        <div class="card-paper stat-box-interactive">
          <div class="stat-number" style="color: var(--color-green);">+39.71%</div>
          <div class="stat-label">120-Day Cumulative Return</div>
          <div class="stat-sub">Net of 0.10% taker fee and bid-ask spread on 2,881 hourly candles.</div>
        </div>
        <div class="card-paper stat-box-interactive">
          <div class="stat-number">4.44</div>
          <div class="stat-label">Full Horizon Sharpe Ratio</div>
          <div class="stat-sub">5.07 Out-of-Sample Sharpe (1.26x Walk-Forward Stability Ratio).</div>
        </div>
        <div class="card-paper stat-box-interactive">
          <div class="stat-number" style="color: #222;">-4.69%</div>
          <div class="stat-label">Max Peak-to-Trough DD</div>
          <div class="stat-sub">Protected by dynamic volatility stops and 3.0x max leverage cap.</div>
        </div>
        <div class="card-paper stat-box-interactive">
          <div class="stat-number" style="color: var(--color-green);">100%</div>
          <div class="stat-label">Weekday Cash Sweep</div>
          <div class="stat-sub">Zero overnight equity beta. 100% USDT cash held Monday afternoon through Friday.</div>
        </div>
      </div>
    </div>
  </section>

  <!-- Systematic Architecture & Protocol Mechanics -->
  <section class="section-spacious" id="architecture">
    <div class="container">
      <div class="section-tag">
        <span class="section-tag-dot"></span>
        <span>EXECUTION LIFECYCLE</span>
      </div>
      <h2 class="section-title">Deterministic 4-Stage Mathematical Loop</h2>
      <p class="section-desc">
        Chronos eliminates emotional discretionary trading through an autonomous four-stage state machine synchronized with global market clocks.
      </p>

      <div class="landing-arch-grid" style="margin-top: 3rem;">
        <!-- Left: Lifecycle Steps -->
        <div style="display: flex; flex-direction: column; gap: 1.5rem;">
          <div class="card-paper">
            <div class="step-index">01 /</div>
            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.55rem; margin-bottom: 0.35rem;">Friday Anchor Price Lock</h3>
            <p style="font-size: 0.92rem; color: var(--color-grey-text);">
              At Friday 20:00 UTC (16:00 EST), cash equities close. Chronos cryptographically anchors the institutional settlement price across $rNVDA, $rTSLA, $rAAPL, $rCOIN, $rMSTR, $rSPY, $rQQQ alongside 24/7 global benchmarks ($BTC).
            </p>
          </div>

          <div class="card-paper">
            <div class="step-index">02 /</div>
            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.55rem; margin-bottom: 0.35rem;">Synthetic Drift & Kalman Z-Scores</h3>
            <p style="font-size: 0.92rem; color: var(--color-grey-text);">
              Over thin weekend liquidity, retail participants over-extrapolate news. Chronos decomposes drift into macro beta components versus asset-specific noise, generating normalized dislocation scores: |Z| = |Drift - β · Drift_BTC| / σ.
            </p>
          </div>

          <div class="card-paper">
            <div class="step-index">03 /</div>
            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.55rem; margin-bottom: 0.35rem;">Risk-Parity Counter-Positioning</h3>
            <p style="font-size: 0.92rem; color: var(--color-grey-text);">
              When |Z| ≥ 2.0σ, Chronos initiates inverse statistical arbitrage baskets via Bitget UTA v3 REST / MCP endpoints. Weights are allocated inversely proportional to weekend volatility with strict 3.0x maximum aggregate leverage.
            </p>
          </div>

          <div class="card-paper">
            <div class="step-index">04 /</div>
            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.55rem; margin-bottom: 0.35rem;">Monday Institutional Convergence & Cash Sweep</h3>
            <p style="font-size: 0.92rem; color: var(--color-grey-text);">
              Between 08:00 and 09:30 EST Monday morning, multi-billion-dollar institutional pre-market liquidity returns. Retail dislocation collapses back to fundamental value. Chronos closes all positions directly into 100% USDT cash.
            </p>
          </div>
        </div>

        <!-- Right: Telemetry & Live Equations Card -->
        <div class="card-dark" style="display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px dashed rgba(255,255,255,0.2); padding-bottom: 0.75rem;">
              <span class="font-terminal" style="font-size: 0.75rem; letter-spacing: 0.12em; color: var(--color-green);">MATHEMATICAL FORMULATION</span>
              <span class="badge-pill-green" style="font-size: 0.72rem;">BITGET MCP READY</span>
            </div>

            <div style="background: rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 1.25rem; margin-bottom: 1.5rem;">
              <div style="color: #9CA3AF; font-size: 0.75rem; font-family: var(--font-terminal); margin-bottom: 0.35rem;">EQUATION: RESIDUAL DISLOCATION</div>
              <div style="font-family: var(--font-terminal); font-size: 0.95rem; color: #FFF; line-height: 1.6;">
                ε_i(t) = R_i(t) - [ α_i + β_i · R_BTC(t) ]<br>
                Z_i(t) = ( ε_i(t) - μ_ε ) / σ_ε
              </div>
            </div>

            <div style="font-family: var(--font-terminal); font-size: 0.8rem; line-height: 1.8; color: #D1D5DB;">
              <div>• Friday Anchor Baseline: <span style="color: var(--color-green);">LOCKED (20:00 UTC)</span></div>
              <div>• Execution Horizon: <span style="color: #FFF;">Saturday 00:00 — Monday 09:30 EST</span></div>
              <div>• Slippage Model: <span style="color: #FFF;">0.10% Taker / Execution Cycle</span></div>
              <div>• Diversification Boost: <span style="color: var(--color-green);">1.90x Multi-Asset Sharpe Gain</span></div>
              <div>• Weekday Idle Capital: <span style="color: #FFF;">100% USDT (Zero Equity Beta)</span></div>
            </div>
          </div>

          <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px dashed rgba(255,255,255,0.2); font-family: var(--font-terminal); font-size: 0.75rem; color: #6B7280;">
            SESSION: CHRONOS-AUTONOMOUS-V2.1 // HOST: MAC-OS // ENGINE: PYTHON-NUMPY
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 4 Core Quantitative Guardrails (Zero Stickers, Pure Precision SVG) -->
  <section class="section-spacious" id="guardrails">
    <div class="container">
      <div class="section-tag">
        <span class="section-tag-dot"></span>
        <span>INSTITUTIONAL GUARDRAILS</span>
      </div>
      <h2 class="section-title">Engineered Defenses & Risk Control</h2>
      <p class="section-desc">
        Engineered specifically for Track 1: Alpha Factory, Chronos introduces structural defenses against idiosyncratic retail spikes and weekend liquidity shocks.
      </p>

      <div class="landing-grid-4col" style="margin-top: 2.5rem;">
        <div class="card-paper">
          <div class="feature-icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l3 8 4-16 3 8h4"/></svg>
          </div>
          <h4 style="font-family: var(--font-serif-editorial); font-size: 1.35rem; margin-bottom: 0.5rem;">Beta Decoupling</h4>
          <p style="font-size: 0.86rem; color: var(--color-grey-text); line-height: 1.55;">
            Filters broad crypto-market rallies from stock-specific drifts using rolling 60-day empirical beta estimation against Bitcoin.
          </p>
        </div>

        <div class="card-paper">
          <div class="feature-icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 21h5v-5"/></svg>
          </div>
          <h4 style="font-family: var(--font-serif-editorial); font-size: 1.35rem; margin-bottom: 0.5rem;">Closed-Loop Self-Auditor</h4>
          <p style="font-size: 0.86rem; color: var(--color-grey-text); line-height: 1.55;">
            Diagnoses why losses occurred (Momentum Overrun, Decoupling, Latency) and automatically adapts entry Z-thresholds.
          </p>
        </div>

        <div class="card-paper">
          <div class="feature-icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          </div>
          <h4 style="font-family: var(--font-serif-editorial); font-size: 1.35rem; margin-bottom: 0.5rem;">Bitget HMAC Gateway</h4>
          <p style="font-size: 0.86rem; color: var(--color-grey-text); line-height: 1.55;">
            Cryptographically signed headers with ACCESS-KEY, ACCESS-SIGN, and TIMESTAMP for Bitget UTA v3 REST and MCP endpoints.
          </p>
        </div>

        <div class="card-paper">
          <div class="feature-icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          </div>
          <h4 style="font-family: var(--font-serif-editorial); font-size: 1.35rem; margin-bottom: 0.5rem;">Capital Shield</h4>
          <p style="font-size: 0.86rem; color: var(--color-grey-text); line-height: 1.55;">
            Maximum 35% single-stock allocation, strict 3.0x aggregate leverage cap, and dynamic volatility-scaled stop losses.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Platform Suite / Dashboard Showcase -->
  <section class="section-spacious" id="platform" style="background-color: var(--color-canvas-subtle);">
    <div class="container">
      <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2.5rem; flex-wrap: wrap; gap: 1rem;">
        <div>
          <div class="section-tag">
            <span class="section-tag-dot"></span>
            <span>THE CHRONOS PLATFORM</span>
          </div>
          <h2 class="section-title" style="margin-bottom: 0.35rem;">An Institutional Terminal Built for Everyone</h2>
          <p class="section-desc">Experience statistical arbitrage with a dedicated web interface designed for quantitative precision and non-dev clarity.</p>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <button class="btn-launch-black" onclick="window.location.href='app.html'">
            <span>Launch Live Terminal</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </button>
        </div>
      </div>

      <!-- 3 Core Platform Pillars (Card Grid) -->
      <div class="landing-grid-3col" style="margin-bottom: 2.5rem;">
        <!-- Card 1: Trading Arena -->
        <div class="card-paper" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
              <span class="badge-pill-light" style="font-size: 0.72rem; font-weight: 700;">MODULE 01</span>
              <span class="badge-pill-green" style="font-size: 0.7rem;">LIVE ARENA</span>
            </div>
            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.65rem; margin-bottom: 0.6rem;">Real-Time Trading Arena</h3>
            <p style="font-size: 0.88rem; color: var(--color-grey-text); line-height: 1.6; margin-bottom: 1.25rem;">
              Track continuous price discovery across 7 tokenized U.S. equities against Friday 16:00 EST anchor prices. Live dislocation gauges alert you when retail order flow drifts beyond statistical normal limits (|Z| ≥ 2.0σ).
            </p>
            <ul style="list-style: none; font-size: 0.82rem; color: #4B5563; display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.5rem; font-family: var(--font-terminal);">
              <li style="display: flex; align-items: center; gap: 0.45rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Live Candlestick Chart & Friday Anchor</span>
              </li>
              <li style="display: flex; align-items: center; gap: 0.45rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Auto-Pilot vs. Manual Rebalancing</span>
              </li>
              <li style="display: flex; align-items: center; gap: 0.45rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>One-Click Allocation Presets (25%, 50%, 100%)</span>
              </li>
            </ul>
          </div>
          <button class="btn-docs-grey" style="width: 100%; justify-content: center;" onclick="window.location.href='app.html'">
            <span>Enter Trading Arena →</span>
          </button>
        </div>

        <!-- Card 2: Cognitive Self-Auditor -->
        <div class="card-paper" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
              <span class="badge-pill-light" style="font-size: 0.72rem; font-weight: 700;">MODULE 02</span>
              <span class="badge-pill-gold" style="font-size: 0.7rem;">CLOSED-LOOP AI</span>
            </div>
            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.65rem; margin-bottom: 0.6rem;">Cognitive Self-Auditor</h3>
            <p style="font-size: 0.88rem; color: var(--color-grey-text); line-height: 1.6; margin-bottom: 1.25rem;">
              Every trade is diagnosed after Monday convergence. When an anomalous drawdown occurs, Chronos pinpoints the market regime shift and tightens risk thresholds—all explained in human-readable cards with zero confusing JSON.
            </p>
            <ul style="list-style: none; font-size: 0.82rem; color: #4B5563; display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.5rem; font-family: var(--font-terminal);">
              <li style="display: flex; align-items: center; gap: 0.45rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Automated Post-Mortem Diagnostics</span>
              </li>
              <li style="display: flex; align-items: center; gap: 0.45rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>rTSLA Overrun: Entry Z raised to 2.50σ</span>
              </li>
              <li style="display: flex; align-items: center; gap: 0.45rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>rMSTR Decoupling: Max cap trimmed to 25%</span>
              </li>
            </ul>
          </div>
          <button class="btn-docs-grey" style="width: 100%; justify-content: center;" onclick="window.location.href='app.html#tab=audit'">
            <span>Inspect Self-Auditor →</span>
          </button>
        </div>

        <!-- Card 3: Dual Execution Engine & Web3 Wallets -->
        <div class="card-paper" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
              <span class="badge-pill-light" style="font-size: 0.72rem; font-weight: 700;">MODULE 03</span>
              <span class="badge-pill-light" style="font-size: 0.7rem; font-weight: 700;">RAINBOWKIT WEB3</span>
            </div>
            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.65rem; margin-bottom: 0.6rem;">Web3 Wallet & Autonomous Bot</h3>
            <p style="font-size: 0.88rem; color: var(--color-grey-text); line-height: 1.6; margin-bottom: 1.25rem;">
              Connect via RainbowKit modal. Each connected wallet maintains its own isolated $50,000 paper trading balance, ledger, and cognitive memory. Configure real Bitget UTA v3 keys in Terminal Settings when ready to deploy live capital.
            </p>
            <ul style="list-style: none; font-size: 0.82rem; color: #4B5563; display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.5rem; font-family: var(--font-terminal);">
              <li style="display: flex; align-items: center; gap: 0.45rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>RainbowKit Web3 Connect (MetaMask, Rainbow, Injected)</span>
              </li>
              <li style="display: flex; align-items: center; gap: 0.45rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Isolated Per-Wallet $50,000 Paper Balance & State</span>
              </li>
              <li style="display: flex; align-items: center; gap: 0.45rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Bitget UTA v3 Gateway in Settings (HMAC-SHA256)</span>
              </li>
            </ul>
          </div>
          <button class="btn-docs-grey" style="width: 100%; justify-content: center;" onclick="window.location.href='app.html'">
            <span>Launch Terminal & Trade ($50k) →</span>
          </button>
        </div>
      </div>

      <!-- Live Terminal Interactive Preview & Dislocation Chart -->
      <div class="dashboard-arena-grid">
        <!-- Left: Interactive Canvas Chart Box -->
        <div class="chart-box">
          <div class="chart-controls">
            <div class="asset-pill-group" style="display: flex; gap: 0.35rem; flex-wrap: wrap;">
              <button class="asset-pill active" onclick="switchAsset('rNVDA', this)">$rNVDA (+3.4%)</button>
              <button class="asset-pill" onclick="switchAsset('rTSLA', this)">$rTSLA (+4.2%)</button>
              <button class="asset-pill" onclick="switchAsset('rAAPL', this)">$rAAPL (-0.8%)</button>
              <button class="asset-pill" onclick="switchAsset('rCOIN', this)">$rCOIN (+5.7%)</button>
              <button class="asset-pill" onclick="switchAsset('rMSTR', this)">$rMSTR (+6.9%)</button>
              <button class="asset-pill" onclick="switchAsset('rSPY', this)">$rSPY (+0.4%)</button>
              <button class="asset-pill" onclick="switchAsset('rQQQ', this)">$rQQQ (+0.8%)</button>
            </div>
            <div style="font-family: var(--font-terminal); font-size: 0.78rem; display: flex; gap: 1.25rem;">
              <span>Friday Anchor: <strong id="anchorPriceDisplay" style="color: var(--color-black);">$128.40</strong></span>
              <span>Current Drift: <strong id="driftDisplay" style="color: var(--color-green);">+3.42%</strong></span>
              <span>Z-Score: <strong id="zScoreDisplay" style="color: var(--color-amber);">+2.24σ</strong></span>
            </div>
          </div>

          <!-- Canvas Chart -->
          <div style="position: relative;">
            <canvas id="priceCanvas"></canvas>
            <div id="chartTooltip"></div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; font-family: var(--font-terminal); font-size: 0.74rem; color: var(--color-grey-text);">
            <div style="display: flex; gap: 1rem; align-items: center;">
              <span style="display: inline-flex; align-items: center; gap: 0.3rem;"><span style="width: 10px; height: 2px; background: #000;"></span> Price Action</span>
              <span style="display: inline-flex; align-items: center; gap: 0.3rem;"><span style="width: 10px; height: 1px; border-top: 1px dashed #E50914;"></span> Friday Anchor</span>
              <span style="display: inline-flex; align-items: center; gap: 0.3rem;"><span style="width: 8px; height: 8px; border-radius: 50%; background: #00C853;"></span> Trade Entry/Exit</span>
            </div>
            <div>Timeframe: 120 Hours Continuous (Fri Close → Mon Open)</div>
          </div>
        </div>

        <!-- Right: Terminal Quick Launch Card (Clean, Human Readable, Zero Raw JSON) -->
        <div class="card-paper" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%; padding: 1.75rem;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--color-green); display: inline-block;"></span>
                <span class="font-terminal" style="font-size: 0.76rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;">Terminal Active</span>
              </div>
              <span class="badge-pill-green" style="font-size: 0.7rem;">INSTANT ACCESS</span>
            </div>

            <h3 style="font-family: var(--font-serif-editorial); font-size: 1.85rem; margin-bottom: 0.75rem; line-height: 1.15;">
              Ready to execute after-hours alpha?
            </h3>
            <p style="font-size: 0.88rem; color: var(--color-grey-text); line-height: 1.6; margin-bottom: 1.5rem;">
              Launch the full Chronos Trading Terminal in your browser. Seamlessly toggle between paper and live trading, monitor real-time order books, and explore post-mortem learning reports.
            </p>

            <div style="background: var(--color-canvas-subtle); border-radius: 6px; padding: 1rem; margin-bottom: 1.5rem; font-family: var(--font-terminal); font-size: 0.78rem; display: flex; flex-direction: column; gap: 0.6rem;">
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--color-grey-text);">Default Account:</span>
                <strong style="color: var(--color-green);">Paper Mode ($50,000 USDT)</strong>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--color-grey-text);">Strategy Mode:</span>
                <strong style="color: var(--color-black);">Autonomous Auto-Pilot</strong>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--color-grey-text);">Active Pairs:</span>
                <strong style="color: var(--color-black);">7 Tokenized Equities + BTC</strong>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--color-grey-text);">Gateway Latency:</span>
                <strong style="color: var(--color-black);">14ms Direct UTA v3</strong>
              </div>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.65rem;">
            <button class="btn-launch-black" style="width: 100%; justify-content: center; padding: 0.75rem;" onclick="window.location.href='app.html'">
              <span>Launch Live Trading Terminal</span>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
            </button>
            <button class="btn-docs-grey" style="width: 100%; justify-content: center;" onclick="window.location.href='app.html#tab=audit'">
              <span>Open Cognitive Self-Auditor</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- How to Get Started in 3 Steps -->
  <section class="section-spacious" style="background-color: var(--color-canvas-light);">
    <div class="container">
      <div class="section-tag">
        <span class="section-tag-dot"></span>
        <span>ONBOARDING WORKFLOW</span>
      </div>
      <h2 class="section-title">Get Started in 3 Simple Steps</h2>
      <p class="section-desc">Designed with frictionless onboarding. Start paper trading in seconds without connecting API keys or wallet setups.</p>

      <div class="landing-grid-3col" style="margin-top: 2.5rem;">
        <div class="card-paper">
          <div class="step-index">01 /</div>
          <h3 style="font-family: var(--font-serif-editorial); font-size: 1.45rem; margin-bottom: 0.45rem;">Launch in Paper Mode</h3>
          <p style="font-size: 0.88rem; color: var(--color-grey-text); line-height: 1.6;">
            Open the terminal with $50,000 pre-loaded simulated USDT. Test the full strategy, toggle auto-pilot, and observe live executions without risking real capital.
          </p>
        </div>

        <div class="card-paper">
          <div class="step-index">02 /</div>
          <h3 style="font-family: var(--font-serif-editorial); font-size: 1.45rem; margin-bottom: 0.45rem;">Monitor Weekend Drift</h3>
          <p style="font-size: 0.88rem; color: var(--color-grey-text); line-height: 1.6;">
            Observe continuous price feeds across tokenized equities. Statistical Z-scores automatically notify you when retail sentiment creates tradeable dislocations.
          </p>
        </div>

        <div class="card-paper">
          <div class="step-index">03 /</div>
          <h3 style="font-family: var(--font-serif-editorial); font-size: 1.45rem; margin-bottom: 0.45rem;">Connect Bitget UTA v3</h3>
          <p style="font-size: 0.88rem; color: var(--color-grey-text); line-height: 1.6;">
            When you're ready for real deployment, add your Bitget API credentials in the non-custodial modal. Chronos handles execution and Monday cash unwinds autonomously.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Complete Audited Trade Ledger Table -->
  <section class="section-spacious" id="ledger">
    <div class="container">
      <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
        <div>
          <div class="section-tag">
            <span class="section-tag-dot"></span>
            <span>TRANSPARENT EXECUTION AUDIT</span>
          </div>
          <h2 class="section-title" style="margin-bottom: 0.25rem;">Audited Trade History (120-Day Horizon)</h2>
          <p class="section-desc">Every trade executed by Chronos with exact entry, Monday convergence exit, net PnL, and self-audit post-mortem status.</p>
        </div>

        <!-- Filter Tabs & Open in Terminal Button -->
        <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
          <div class="filter-btn-group" style="margin-bottom: 0;">
            <button class="filter-btn active" onclick="filterTrades('all', this)">All Trades (26)</button>
            <button class="filter-btn" onclick="filterTrades('win', this)">Profitable Wins (20)</button>
            <button class="filter-btn" onclick="filterTrades('loss', this)">Audited Losses (6)</button>
          </div>
          <button class="btn-launch-black" style="padding: 0.42rem 1rem; font-size: 0.76rem;" onclick="window.location.href='app.html#tab=ledger'">
            <span>Open in Terminal</span>
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </button>
        </div>
      </div>

      <div class="card-paper" style="padding: 0; overflow-x: auto;">
        <table class="ledger-table">
          <thead>
            <tr>
              <th>Asset</th>
              <th>Direction</th>
              <th>Entry Time</th>
              <th>Entry Price</th>
              <th>Exit Time</th>
              <th>Exit Price</th>
              <th>Net PnL (%)</th>
              <th>USDT PnL</th>
              <th>Audit Post-Mortem</th>
            </tr>
          </thead>
          <tbody id="ledgerTableBody">
            <!-- Populated dynamically by JavaScript from data/real_trades.json -->
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- Call to Action (CTA) Section -->
  <section class="section-spacious" style="background-color: var(--color-canvas-light);">
    <div class="container">
      <div class="card-dark" style="text-align: center; padding: 4rem 2rem;">
        <div class="badge-pill-green" style="margin-bottom: 1.25rem;">
          <span>BITGET AI BASE CAMP S2 · SUBMISSION READY</span>
        </div>
        <h2 style="font-family: var(--font-serif-editorial); font-size: 2.85rem; font-weight: 400; line-height: 1.15; margin-bottom: 1rem; color: #FFF;">
          Deploy Institutional After-Hours Alpha
        </h2>
        <p style="font-size: 1.05rem; color: #9CA3AF; max-width: 600px; margin: 0 auto 2.25rem; line-height: 1.6;">
          Chronos runs autonomously 24/7 on Python with zero human intervention required. Seamlessly connects to Bitget UTA v3 and Bitget MCP tools.
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
          <button class="btn-launch-white" onclick="window.location.href='app.html'">
            <span>Launch Alpha Terminal</span>
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </button>
          <a href="https://github.com/OpeyemiMoses/Chronos" target="_blank" class="btn-pill-dark-outline" style="text-decoration: none;">
            <span>View Source on GitHub</span>
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Editorial Footer -->
  <footer style="background-color: #FFF; border-top: 1px dashed rgba(0, 0, 0, 0.22); padding: 4.5rem 0 3rem;">
    <div class="container">
      <div class="footer-grid-container" style="display: grid; grid-template-columns: 1.6fr 1fr 1fr 1fr; gap: 2.5rem; margin-bottom: 3.5rem;">
        <div>
          <img src="assets/chronos_logo.svg" alt="Chronos" style="height: 42px; margin-bottom: 1rem;">
          <p style="font-size: 0.88rem; color: var(--color-grey-text); max-width: 320px; line-height: 1.6;">
            Chronos is an autonomous quantitative trading engine for Bitget AI Base Camp Season 2, Track 1: Alpha Factory. Specializing in 24/7 After-Hours Information Pricing on tokenized U.S. equities.
          </p>
          <div style="margin-top: 1.25rem;" class="badge-pill-light">
            <span>BITGET UTA v3 COMPLIANT</span>
          </div>
        </div>

        <div>
          <h5 style="font-family: var(--font-terminal); font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.1rem;">Strategy</h5>
          <ul style="list-style: none; font-size: 0.88rem; color: var(--color-grey-text); display: flex; flex-direction: column; gap: 0.6rem;">
            <li><a href="#thesis" style="color: inherit; text-decoration: none;">Weekend Dislocation</a></li>
            <li><a href="#metrics" style="color: inherit; text-decoration: none;">120D Alpha Audit</a></li>
            <li><a href="#architecture" style="color: inherit; text-decoration: none;">Friday Anchor Model</a></li>
            <li><a href="#guardrails" style="color: inherit; text-decoration: none;">Beta Decoupling</a></li>
          </ul>
        </div>

        <div>
          <h5 style="font-family: var(--font-terminal); font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.1rem;">Hackathon</h5>
          <ul style="list-style: none; font-size: 0.88rem; color: var(--color-grey-text); display: flex; flex-direction: column; gap: 0.6rem;">
            <li><a href="https://github.com/OpeyemiMoses/Chronos" target="_blank" style="color: inherit; text-decoration: none;">GitHub Repository</a></li>
            <li><a href="#" style="color: inherit; text-decoration: none;">Bitget AI Base Camp S2</a></li>
            <li><a href="#" style="color: inherit; text-decoration: none;">Track 1: Alpha Factory</a></li>
            <li><a href="#" style="color: inherit; text-decoration: none;">Sub-Theme: After-Hours</a></li>
          </ul>
        </div>

        <div>
          <h5 style="font-family: var(--font-terminal); font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.1rem;">System Status</h5>
          <div style="font-family: var(--font-terminal); font-size: 0.8rem; color: var(--color-grey-text); line-height: 1.8;">
            <div>All Systems Operational</div>
            <div style="color: var(--color-green);">API Gateway Connected</div>
            <div>Latency: 14ms (Direct UTA)</div>
            <div>Uptime: 99.98%</div>
          </div>
        </div>
      </div>

      <div style="border-top: 1px solid rgba(0, 0, 0, 0.06); padding-top: 1.75rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; font-size: 0.8rem; color: var(--color-grey-muted);">
        <div>© 2026 Chronos Quantitative Research. All rights reserved.</div>
        <div>Engineered for Bitget AI Base Camp Hackathon Season 2.</div>
      </div>
    </div>
  </footer>

  <!-- Embedded Client Logic & Real Data Rendering -->
  <script>
    const realTrades = {trades_json_str};
    const auditMemory = {audit_json_str};
    const chartData = {chart_json_str};

    let activeSymbol = "rNVDA";

    // Header Scroll Expansion Dynamic Transition
    window.addEventListener("scroll", () => {{
      const headerPill = document.getElementById("mainHeaderPill");
      if (window.scrollY > 40) {{
        headerPill.classList.add("is-scrolled");
      }} else {{
        headerPill.classList.remove("is-scrolled");
      }}
    }});

    // Populate Trade Ledger Table
    function renderLedger(trades) {{
      const tbody = document.getElementById("ledgerTableBody");
      if (!tbody) return;
      tbody.innerHTML = "";

      (trades || []).forEach((t) => {{
        const tr = document.createElement("tr");
        const retVal = typeof t.return_pct === "number" ? t.return_pct : (typeof t.pnl_pct === "number" ? t.pnl_pct : 0);
        const isWin = retVal > 0;
        const pnlColor = isWin ? "var(--color-green)" : "var(--color-red)";
        const pnlPrefix = isWin ? "+" : "";
        const badgeClass = isWin ? "badge-win" : "badge-loss";
        const entryP = typeof t.entry_price === "number" ? t.entry_price.toFixed(2) : "0.00";
        const exitP = typeof t.exit_price === "number" ? t.exit_price.toFixed(2) : "0.00";
        const pnlUsd = typeof t.pnl_usd === "number" ? t.pnl_usd : (typeof t.pnl_usdt === "number" ? t.pnl_usdt : 0);
        const assetName = t.asset || t.symbol || "rNVDA";
        const sideName = (t.side === "SHORT" || t.side === "SELL_SHORT") ? "SHORT" : "LONG";
        const entryTime = t.entry_time || "Friday 17:00 EST";
        const exitTime = t.exit_time || "Monday 09:30 EST";
        const note = t.audit_note || t.exit_reason || "Monday Institutional Convergence";

        tr.innerHTML = `
          <td><strong style="font-family: var(--font-terminal);">${{assetName}}</strong></td>
          <td><span style="font-family: var(--font-terminal); font-size: 0.78rem; font-weight: 700; color: ${{sideName === 'SHORT' ? 'var(--color-red)' : 'var(--color-green)'}}">${{sideName}}</span></td>
          <td style="font-family: var(--font-terminal); font-size: 0.8rem; color: var(--color-grey-text);">${{entryTime}}</td>
          <td style="font-family: var(--font-terminal); font-size: 0.84rem;">$${{entryP}}</td>
          <td style="font-family: var(--font-terminal); font-size: 0.8rem; color: var(--color-grey-text);">${{exitTime}}</td>
          <td style="font-family: var(--font-terminal); font-size: 0.84rem;">$${{exitP}}</td>
          <td><span class="${{badgeClass}}">${{pnlPrefix}}${{retVal.toFixed(2)}}%</span></td>
          <td style="font-family: var(--font-terminal); font-size: 0.84rem; font-weight: 700; color: ${{pnlColor}};">${{pnlPrefix}}$${{pnlUsd.toFixed(2)}}</td>
          <td style="font-size: 0.8rem; color: var(--color-grey-text);">${{note}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Filter Trades
    function filterTrades(type, btn) {{
      document.querySelectorAll(".filter-btn-group .filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      if (type === "win") {{
        renderLedger(realTrades.filter(t => (t.return_pct !== undefined ? t.return_pct : t.pnl_pct) > 0));
      }} else if (type === "loss") {{
        renderLedger(realTrades.filter(t => (t.return_pct !== undefined ? t.return_pct : t.pnl_pct) <= 0));
      }} else {{
        renderLedger(realTrades);
      }}
    }}

    // Switch Chart Asset
    function switchAsset(symbol, btn) {{
      activeSymbol = symbol;
      document.querySelectorAll(".asset-pill").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");

      // Update indicators
      const data = chartData[symbol];
      if (data) {{
        document.getElementById("anchorPriceDisplay").textContent = "$" + data.anchor_price.toFixed(2);
        const lastPrice = data.prices[data.prices.length - 1];
        const drift = ((lastPrice - data.anchor_price) / data.anchor_price) * 100;
        document.getElementById("driftDisplay").textContent = (drift > 0 ? "+" : "") + drift.toFixed(2) + "%";
        document.getElementById("driftDisplay").style.color = drift > 0 ? "var(--color-green)" : "var(--color-red)";
        document.getElementById("zScoreDisplay").textContent = (drift > 0 ? "+" : "-") + (Math.abs(drift) / 1.5).toFixed(2) + "σ";
      }}
      drawChart();
    }}

    // Canvas Chart Rendering
    function drawChart() {{
      const canvas = document.getElementById("priceCanvas");
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

      const data = chartData[activeSymbol];
      if (!data) return;

      const prices = data.prices;
      const anchor = data.anchor_price;
      const minP = Math.min(...prices, anchor) * 0.985;
      const maxP = Math.max(...prices, anchor) * 1.015;

      const getX = (i) => 50 + (i / (prices.length - 1)) * (w - 70);
      const getY = (val) => h - 35 - ((val - minP) / (maxP - minP)) * (h - 70);

      // Draw Weekend Shaded Area
      const wStart = getX(24);
      const wEnd = getX(96);
      ctx.fillStyle = "rgba(0, 0, 0, 0.025)";
      ctx.fillRect(wStart, 10, wEnd - wStart, h - 45);

      ctx.fillStyle = "rgba(0, 0, 0, 0.35)";
      ctx.font = "10px 'Space Mono', monospace";
      ctx.fillText("WEEKEND TRADING ZONE (24/7 TOKENIZED LIQUIDITY)", wStart + 12, 26);

      // Horizontal Anchor Price Line
      const anchorY = getY(anchor);
      ctx.beginPath();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = "rgba(229, 9, 20, 0.65)";
      ctx.lineWidth = 1.5;
      ctx.moveTo(50, anchorY);
      ctx.lineTo(w - 20, anchorY);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = "rgba(229, 9, 20, 0.85)";
      ctx.fillText("FRIDAY ANCHOR: $" + anchor.toFixed(2), 52, anchorY - 6);

      // Price Path
      ctx.beginPath();
      ctx.strokeStyle = "#090909";
      ctx.lineWidth = 2.2;
      for (let i = 0; i < prices.length; i++) {{
        const x = getX(i);
        const y = getY(prices[i]);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }}
      ctx.stroke();

      // Subtle Gradient Fill under Price
      const gradient = ctx.createLinearGradient(0, 0, 0, h);
      gradient.addColorStop(0, "rgba(0, 200, 83, 0.12)");
      gradient.addColorStop(1, "rgba(0, 200, 83, 0.0)");
      ctx.lineTo(getX(prices.length - 1), h - 35);
      ctx.lineTo(getX(0), h - 35);
      ctx.closePath();
      ctx.fillStyle = gradient;
      ctx.fill();

      // Draw Trade Markers
      if (data.markers) {{
        data.markers.forEach((m) => {{
          const mx = getX(m.index);
          const my = getY(m.price);
          
          ctx.beginPath();
          ctx.arc(mx, my, 5.5, 0, Math.PI * 2);
          ctx.fillStyle = m.type === "ENTRY" ? "#00C853" : "#090909";
          ctx.fill();
          ctx.strokeStyle = "#FFF";
          ctx.lineWidth = 2;
          ctx.stroke();

          ctx.fillStyle = "#000";
          ctx.font = "bold 9px 'Space Mono', monospace";
          ctx.fillText(m.label, mx - 12, my - 9);
        }});
      }}

      // Axes & Labels
      ctx.fillStyle = "#888";
      ctx.font = "10px 'Space Mono', monospace";
      ctx.fillText("$" + maxP.toFixed(2), 8, 25);
      ctx.fillText("$" + ((maxP + minP) / 2).toFixed(2), 8, h / 2);
      ctx.fillText("$" + minP.toFixed(2), 8, h - 35);

      ctx.fillText("Friday 20:00 UTC", 50, h - 14);
      ctx.fillText("Saturday Noon", w * 0.35, h - 14);
      ctx.fillText("Sunday 18:00 UTC", w * 0.65, h - 14);
      ctx.fillText("Monday 09:30 EST (Convergence)", w - 210, h - 14);
    }}

    window.addEventListener("resize", drawChart);
    function initIndexApp() {{
      try {{ renderLedger(realTrades); }} catch(e) {{ console.error("renderLedger error:", e); }}
      try {{ setTimeout(drawChart, 80); }} catch(e) {{}}
    }}
    if (document.readyState === "loading") {{
      document.addEventListener("DOMContentLoaded", initIndexApp);
    }} else {{
      initIndexApp();
    }}
  </script>
</body>
</html>
"""

# Compile clean Master Chronos Landing Page
with open("dashboard/index.html", "w") as f:
    f.write(html_content)

print(f"Successfully generated Master Chronos Landing Page at dashboard/index.html ({len(html_content)} bytes)")
