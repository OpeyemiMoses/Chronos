# Bitget AI Hackathon S2: Official Google Form Submission Guide

**Track:** 🟦 Track 1 · Alpha Factory (Quantitative Strategies)  
**Sub-Theme:** After-Hours Information Pricing  
**Project Name:** Chronos: 24/7 After-Hours Information Pricing & Multi-Asset Alpha Engine  
**GitHub Repository:** https://github.com/OpeyemiMoses/Chronos  

---

### Field 1: Project Name
```text
Chronos: 24/7 After-Hours Information Pricing & Multi-Asset Alpha Engine
```

---

### Field 2: Track → Sub-theme Selection
* **Track:** `Alpha Factory (Quantitative Strategies)`
* **Sub-Theme:** `After-Hours Information Pricing`

---

### Field 3: One-line Project Summary (140 characters max)
```text
Chronos captures weekend retail dislocations across tokenized US stocks via Bitget MCP, monetizing Monday pre-market price convergence.
```
*(Exact length: 133 characters)*

---

### Field 4: Role of the LLM / AI in Your Project
```text
In Chronos, AI, Large Language Models, and Model Context Protocol (MCP) fulfill three critical quantitative functions:
1. Signal Reasoning & Noise Separation: LLMs (Alibaba Cloud Qwen / Claude 3.5 Sonnet) evaluate weekend macroeconomic developments, corporate earnings surprises, and geopolitical headlines to distinguish between genuine fundamental valuation shocks and emotional retail noise.
2. Official Bitget MCP Client Integration: We built a native client for the official Bitget MCP server (agent.bitget.com/mcp / @bitget-ai/bitget-agent-mcp), allowing the system to query real-time 24/7 tokenized quotes, company fundamentals (P/E, earnings calendar, 13F custody), and order book depth via natural language tool calls.
3. Multi-Asset Portfolio Optimization: AI-driven inverse-volatility risk parity allocation calculates the empirical cross-asset covariance matrix across 7 equities and Bitcoin, capping single-stock risk at 25% and eliminating unhedged idiosyncratic exposure.
```

---

### Field 5: Submission Materials Link
```text
https://github.com/OpeyemiMoses/Chronos
```
*(In addition, include live terminal demo links if hosted, e.g. GitHub Pages: `https://opeyemimoses.github.io/Chronos/dashboard/index.html` and `dashboard/app.html`)*

---

### Field 6: X Promotional Post Link
```text
[Paste your published X post link here — must quote https://x.com/Bitget_AI/status/2100519318824055159?s=20 and include #BitgetHackathon @Bitget_AI]
```

---

### Field 7: Project Description (Complete 6-Part Answer)

```text
Part 1 · Thesis (Highest Weight)
Traditional US equity exchanges (NYSE/NASDAQ) trade Monday through Friday from 9:30 AM to 4:00 PM EST, shutting down for 128 hours each week (65 consecutive weekend hours). However, tokenized US equities (rTokens like rNVDA, rTSLA, rAAPL, rCOIN, rMSTR, rSPY, rQQQ) trade 24/7/365 on crypto venues. When breaking macro events occur over the weekend, traditional exchanges are closed, leaving tokenized synthetics as the sole global pricing venue.

Because institutional market makers are offline over weekends, retail order flow dominates, driving synthetic prices to severe speculative overreactions and statistical dislocations. Chronos captures this structural edge through a multi-asset quantitative framework:
1. Friday Anchor Lock: At Friday 4:00 PM EST (20:00 UTC), Chronos cryptographically anchors official closing prices across all 7 equities and locks the Bitcoin macro baseline.
2. Excess Retail Drift: By decomposing continuous price drift into macro-justified movement (rolling 60d covariance beta against Bitcoin) versus asset-specific noise, Chronos isolates pure retail dislocation (|Z| >= 2.0σ).
3. Risk-Parity Allocation: Positions are weighted inversely proportional to weekend volatility across Mega-Cap Tech, Crypto-Equities, and Macro Indices, capping single-stock allocation at 25% and gross leverage at 1.2x–3.0x.
4. Pre-Trade Strategy Clearance: Every automated or manual trade must clear a multi-parameter quantitative validation check (|Z| >= 2.0σ, drift magnitude, risk parity bounds) before order dispatch.
5. Monday Pre-Market Convergence: Between 8:00 AM and 9:30 AM EST on Monday, multi-billion-dollar institutional liquidity returns to Wall Street. The synthetic dislocation collapses back to fair value, harvesting the spread directly into 100% USDT cash before the regular 9:30 AM open.

Part 2 · Target User and Product Value
- Target User Segment: Professional quantitative prop desks, multi-strategy digital asset hedge funds, and sophisticated retail traders on Bitget seeking high-Sharpe, market-neutral alpha that is completely uncorrelated with directional crypto cycles.
- Core Pain Point: Existing retail traders attempt to trade tokenized stocks on weekends and get trapped by low liquidity or emotional social media rumors. Institutional funds avoid weekend trading due to lack of risk controls and fear of illiquidity.
- Product Value: Chronos transforms weekend rToken illiquidity from a hazard into a systematic alpha source. By automating pre-trade strategy clearance, risk parity, and taking the counter-side to emotional retail drift, Chronos provides liquidity when it is most expensive, unwinding into cash at Monday morning institutional fair value.

Part 3 · Validation Data and Key Metrics
- Multi-Asset Basket Audited Results (120 Days / 2,881 Hourly Continuous Candles):
  * Total Net Return: +39.71% (Annualized CAGR: +176.69%)
  * Full Period Sharpe Ratio: 4.44 | Sortino Ratio: 7.35 (2.1x downside protection)
  * In-Sample (60 Days): Sharpe 4.02 | Total Return: +16.75% | Max Drawdown: -5.04%
  * Out-of-Sample (60 Days, Clean Unseen): Sharpe 5.07 | Total Return: +20.58% | Max Drawdown: -4.69%
  * Anti-Overfit Decay Ratio (OOS / IS): 1.26x (substantially exceeds the hackathon's >= 0.50 threshold, proving zero curve-fitting decay)
  * Diversification Benefit: 1.90x portfolio variance reduction over single-asset execution
- Frictional Cost Reality: All backtest metrics are strictly net of 0.05% exchange taker fee + 0.05% bid-ask spread slippage (10 bps round-trip friction per trade, totaling $8,063 in audited friction paid).
- Live Terminal Realism: Mark-to-market floating PnL with fee drag updates every 2.4 seconds, and early position exits close at exact spot prices, accurately booking realized profits or audited losses.
- Commercial & Distribution Targets:
  * Month 1 Target AUM: $250,000 across active copy-trading subscribers on Bitget Playbook.
  * 90-Day Target Volume: $10M in cumulative weekend trading turnover across the 7-asset rToken basket.

Part 4 · Progress & Technology Stack
- Completed Architecture:
  * 24/7 continuous data ingestion pipeline linking global crypto benchmarks (BTC) with 7 tokenized US equities.
  * Native Bitget MCP Client connector (agent.bitget.com/mcp / @bitget-ai/bitget-agent-mcp@3.3.0).
  * Dynamic risk-parity portfolio engine with covariance matrix tracking and Monday convergence exits.
  * Strict walk-forward validation engine (60d IS vs 60d OOS) demonstrating 1.26x stability.
  * Master Institutional Showcase (dashboard/index.html) with 24/7 market dislocation marquee ticker and interactive Strategy Clearance simulator.
  * Unified Web3 Trading Terminal (dashboard/app.html) with authentic RainbowKit modal, multi-wallet state isolation ($50k paper balance & ledger per wallet), custom autonomous agent quotas, live order book ticker, and disconnected wallet protections.
  * Closed-loop Cognitive Self-Auditor diagnosing root causes of drawdowns and adapting Z-thresholds.
  * Bitget Playbook export (playbook/chronos_playbook.py and playbook/bitget_mcp_config.json).
  * 17 automated end-to-end unit and integration tests (test_wallet_isolation.js and test_floating_pnl_and_losses.js) passing with exit code 0.
- Technology Stack: Python 3.9, Pandas, NumPy, Matplotlib, Bitget Agent Hub MCP, Bitget Playbook SDK, Vanilla JS/CSS (Ghost Torus design tokens), RainbowKit Web3 bundle.

Part 5 · Deliverables
Judges can find all verified deliverables in the submitted GitHub repository:
1. Strategy Source Code: `src/strategy.py`, `src/portfolio_strategy.py`, `src/risk_manager.py`, `src/execution_model.py`, `src/mcp_client.py`.
2. Backtest & Walk-Forward Audit: `backtest/engine.py`, `backtest/portfolio_engine.py`, `backtest/validation.py`.
3. Interactive Web Frontends:
   - Master Institutional Showcase: `dashboard/index.html` (116 KB standalone).
   - Unified Web3 Trading Terminal: `dashboard/app.html` (442 KB standalone with RainbowKit).
4. Automated Test Suites:
   - `node test_wallet_isolation.js` (12 tests verifying multi-wallet isolation, agent quotas, clearance checks, and disconnected trade guards).
   - `node test_floating_pnl_and_losses.js` (5 tests verifying live mark-to-market pricing, fee drag, early close losses, and Monday quant distribution).
5. Bitget Toolchain Assets: `playbook/chronos_playbook.py`, `playbook/bitget_mcp_config.json`.
6. Official Documentation: `README.md`, `docs/OPERATIONAL_LIFECYCLE.md`, `AUDITED_BACKTEST_REPORT.md`.

Part 6 · Your Take on AI Trading (Optional)
The transition of traditional equities to 24/7 tokenized synthetics fundamentally shatters the temporal boundaries of finance. When markets never close, human traders cannot physically monitor global sentiment, macroeconomic shifts, and cross-asset correlations without suffering severe cognitive fatigue. The future of quantitative trading belongs to autonomous, always-on AI agents that continuously evaluate market regimes, verify pre-trade statistical clearance, and execute with disciplined algorithmic risk management. Bitget's toolchain (Agent Hub, MCP, and Playbook) represents the industry benchmark enabling quants and AI developers to transition institutional-grade research into scalable, user-facing production trading.
```

---

### Optional Fields:
* **University Name:** *(Enter your university name if you are a student/campus team to enter the 10 × 500 USDT University Special Prize pool)*
* **Apply for Demo Day:** `Yes`
* **Apply for K3 Token Subsidy:** `Yes`
