# Chronos — Bitget AI Base Camp Hackathon S2 Official Submission Guide

> **Important Notice for Submitting Teams:**
> The hackathon rules permit submitting to **up to two different themes** as independent entries using separate Google Form submissions (keeping the same Bitget UID).
> Below are the ready-to-use, question-by-question submission dossiers for **Track 2 (Agentic Trading)** and **Track 1 (Alpha Factory)**.
>
> **Submission Portal (Google Form):** [https://forms.gle/GyWZCMCPocgJdJon6](https://forms.gle/GyWZCMCPocgJdJon6)  
> **Submission Deadline:** September 27, 2026 (UTC+8)

---

# SUBMISSION 1: Track 2 — Agentic Trading

* **Competition Track (Q9):** `Agentic Trading`
* **Competition Sub-Theme (Q10):** `Market Sentiment Agent` *(or `Cross-Asset Execution Agent` / `Open Theme`)*
* **Project Name (Q11):** `Chronos: Autonomous 24/7 Weekend Dislocation Agent for Bitget Tokenized Equities`
* **One-Line Summary (Q12, max 140 chars):**  
  `Autonomous agent exploiting 24/7 weekend price dislocations in Bitget rTokens via statistical z-scores, LLM reasoning, & stress tests.` *(131 chars)*

---

### Q13: Project Description (Parts 1 to 5)

#### Part 1 · Thesis (Core Hypothesis & Strategy Design)
* **The Structural Inefficiency:** Traditional US equity markets close Friday at 4:00 PM EST and reopen Monday at 9:30 AM EST. However, macro news, earnings developments, and geopolitical shocks continue uninterrupted throughout the weekend. On Bitget, tokenized US equities (rTokens / USDT-Futures such as `NVDAUSDT`, `TSLAUSDT`, `COINUSDT`, `MSTRUSDT`) trade 24/7. 
* **The Core Hypothesis:** Without the continuous high-volume institutional liquidity of the primary exchanges, weekend rToken markets experience retail-dominated emotional dislocations. When an asset dislocates by $|Z| \ge 1.50\sigma$ away from its Friday settlement anchor, there is a strong statistical tendency for mean-reversion as global market makers position ahead of Monday's cash open.
* **Autonomous Decision & Risk Architecture:**
  1. **Anchor Calibration:** Chronos freezes Friday 4:00 PM closing settlement as the benchmark anchor price.
  2. **Live Perception:** Streams 24/7 live order book depth and spot prices from Bitget (`/api/market-prices`) every 3.5s.
  3. **Noise Band Filter:** Assets drifting $< 2.0\%$ or $|Z| < 1.50\sigma$ are strictly **BLOCKED** to protect capital against taker fee drag ($0.06\%$) and spread slippage.
  4. **Deterministic Scenario Stress Testing:** Evaluates 6 forward-looking price shock scenarios (Full Reversion, 60% Convergence, Flat Stall, Adverse $+2\%$, Blow-off $+4\%$, Tail Shock $+8\%$) calibrated to asset-specific beta.
  5. **Autonomous Order Routing:** Generates plain-English trade reasoning and executes risk-managed positions directly to the user's isolated wallet.
  6. **Post-Mortem Audits:** Records immutable trade post-mortems in local storage memory to prevent repeat loss patterns.

#### Part 2 · Target User & Product Value
* **Target Audience:** Crypto-native prop traders, quantitative retail investors, and automated fund managers seeking uncorrelated alpha during traditional market downtime (Friday 4 PM – Monday 9:30 AM EST).
* **Capital Profile & Risk Appetite:** $5,000 to $100,000 USDT capital allocation per account, with a strict 5% risk cap per trade and a hard maximum of 5 active weekend positions.
* **Unmet Need:** Manual weekend monitoring of 7+ tokenized stocks across 65 non-stop hours is physically exhausting and prone to emotional FOMO. Chronos provides an autonomous agent that never sleeps, enforcing institutional risk discipline and mathematical edge without human fatigue.

#### Part 3 · Validation Data & Key Metrics
* **Empirical 90-Day Continuous Evaluation (June – September 2026):**
  - **Dataset:** 90 daily candlestick records pulled directly from Bitget USDT-Futures (`NVDAUSDT`, `TSLAUSDT`, `COINUSDT`, etc.).
  - **Total Executed Trades:** **151 Trades** across 7 tokenized US assets.
  - **Overall Win Rate:** **51.0%** across the entire portfolio; **65.0% on rCOIN** and **56.5% on rNVDA**.
  - **Portfolio Profit Factor:** **1.42** (Gross Profit: $3,328.08 USDT, Gross Loss: $2,336.88 USDT).
  - **Net Cumulative Return:** **+1.98%** on $50,000 paper capital (+$991.20 USDT net profit).
  - **Maximum Drawdown:** **-1.36%** (-$682.79 USDT peak-to-trough), proving extraordinary capital preservation.
  - **Sharpe Ratio (Annualized):** **1.74** | **Sortino Ratio:** **3.25** (downside risk heavily constrained).
  - **Fee Accounting:** Every single metric incorporates full Bitget taker fee friction of **0.06% per side** ($453.00 USDT total taker fees deducted).
  - **Distribution Targets:** Targeting 250 active Bitget wallet connections and $1.5M monthly traded volume within 60 days of Bitget Playbook listing.

#### Part 4 · Progress
* **Built & Production-Ready:**
  - Full live Bitget futures ticker integration with automatic caching and retry (`/api/market-prices`).
  - Empirical backtest API endpoint (`/api/backtest-results`) serving 90-day candlestick performance profiles.
  - Interactive Unified Trading Terminal (`dashboard/app.html`) with dynamic real-time price selector cards, order book depth charts, and scenario stress tester.
  - Authentic Web3 RainbowKit / wagmi wallet connectivity with 100% isolated multi-user state.
  - Complete automated test suite: 12 passing isolation and execution guard tests (`node test_wallet_isolation.js`).
* **Frameworks, Models & APIs Used:**
  - **Bitget APIs:** Bitget Mix Market API v2 (USDT-Futures candles and tickers).
  - **LLM Engine:** Alibaba Cloud Qwen (`qwen3.8-max` via Bitget Hackathon endpoint `https://hackathon.bitgetops.com/v1`) for autonomous trading-signal reasoning, plain-English chain-of-thought, and post-trade audit analysis.
  - **Frontend:** Pure high-performance Vanilla JS and CSS for zero-latency execution.

#### Part 5 · View on AI Trading
* Agentic Trading must transcend "chatbots that trade." An LLM should never be allowed to execute orders unconstrained. Chronos demonstrates the optimal paradigm: **LLM for reasoning, synthesis, and narrative explanation + deterministic mathematical code for risk gates, stress tests, and sizing limits.**

---

### Q14: Submission Material Links
```text
Project Demo URL: https://chronos-production-a1e4.up.railway.app/terminal
Public GitHub Repository: https://github.com/OpeyemiMoses/Chronos
Paper Trading Logs (CSV): https://github.com/OpeyemiMoses/Chronos/blob/main/data/paper_trading_logs.csv
Paper Trading Logs (JSON): https://github.com/OpeyemiMoses/Chronos/blob/main/data/paper_trading_logs.json
Paper Trading Quantitative Report: https://github.com/OpeyemiMoses/Chronos/blob/main/docs/PAPER_TRADING_REPORT.md
Backtest Engine Script: https://github.com/OpeyemiMoses/Chronos/blob/main/scripts/run_real_backtest.py
Demo Video Link: [Insert your 2-3 minute YouTube or X video link]
```

### Q15: Role of the LLM / AI in Your Project
```text
In Chronos, the LLM (Alibaba Cloud Qwen qwen3.8-max) acts as the autonomous perception, thesis generation, and post-trade audit engine. Specifically:
1. Signal Reasoning: Ingests real-time Bitget order book metrics, Friday anchor deviation, and retail sentiment indicators to synthesize a structured, plain-English trade thesis.
2. Risk Validation: Explains the statistical rationale behind the 6 forward-looking deterministic stress scenarios.
3. Post-Mortem Audits: Upon trade settlement, analyzes slippage, hold duration, and reversion efficacy to generate an audit report stored in the wallet memory to optimize future execution.
```

---

# SUBMISSION 2: Track 1 — Alpha Factory

* **Competition Track (Q9):** `Alpha Factory`
* **Competition Sub-Theme (Q10):** `After-Hours Information Pricing` *(or `rToken Factor Strategies` / `Arbitrage`)*
* **Project Name (Q11):** `Chronos-Alpha: Statistical Mean-Reversion & Weekend Dispersion Alpha Engine for US rTokens`
* **One-Line Summary (Q12, max 140 chars):**  
  `Verifiable quant alpha strategy capturing weekend mispricings in tokenized US equities using rolling z-scores and beta-adjusted mean reversion.` *(139 chars)*

---

### Q13: Project Description (Parts 1 to 5)

#### Part 1 · Thesis (Alpha Source & Signal Logic)
* **Alpha Source:** The strategy monetizes liquidity premiums and retail overreaction in 24/7 tokenized US equities during US exchange closure (Friday 20:00 UTC to Sunday 22:00 UTC).
* **Signal Mathematical Specification:**
  - Anchor Price $P_{\text{anchor}} = P_{\text{close, Fri}}$
  - Continuous Drift: $\Delta(t) = \frac{P_{\text{spot}}(t) - P_{\text{anchor}}}{P_{\text{anchor}}}$
  - Statistical Dispersion: $Z(t) = \frac{P_{\text{spot}}(t) - \mu_{20}}{\sigma_{20}}$
  - Sizing & Direction:
    $$\text{Signal} = \begin{cases} \text{SHORT}, & \text{if } Z(t) \ge +1.50\sigma \text{ and } \Delta(t) \ge +2.0\% \\ \text{LONG}, & \text{if } Z(t) \le -1.50\sigma \text{ and } \Delta(t) \le -2.0\% \\ \text{HOLD CASH (NOISE BAND)}, & \text{otherwise} \end{cases}$$
* **Execution & Friction Sinks:** Orders execute as limit orders near mid-price with a conservative taker fee penalty ($0.06\%$) and a strict $3.5\%$ stop-loss.

#### Part 2 · Target User & Product Value
* **Target Audience:** Quantitative funds, crypto market makers, and systematic retail investors deploying algorithmic capital into tokenized Real World Assets (RWAs).
* **Value Proposition:** Uncorrelated alpha stream that produces its highest Sharpe ratio during periods when conventional equity strategies generate zero returns (weekends and market holidays).

#### Part 3 · Validation Data & Key Metrics
* **90-Day Empirical Continuous Backtest (Bitget USDT-Futures):**
  - **In-Sample Period (60 Days):** Win rate 53.2%, Profit Factor 1.58, Sharpe 1.92.
  - **Out-of-Sample Period (30 Days):** Win rate 48.6%, Profit Factor 1.31, Sharpe 1.48 (Minimal decay: OS Sharpe $> 0.77 \times$ IS Sharpe, well above the $0.5\times$ alert threshold).
  - **Token Highlights:**
    - `rCOIN`: 65.0% win rate, 3.68 profit factor, +$992.33 net contribution.
    - `rNVDA`: 56.5% win rate, 2.41 profit factor, +$303.15 net contribution.
  - **Portfolio Drawdown:** Capped at -1.36% across 151 trade cycles.
  - **Friction Accounting:** Deducts $453.00 USDT in exchange taker fees.

#### Part 4 · Progress
* Fully implemented python backtest engine (`scripts/run_real_backtest.py`), automated paper trading execution logger (`scripts/generate_paper_trading_records.py`), and real-time Bitget market gateway (`server.py`).

#### Part 5 · View on AI Trading
* AI is most effective in quantitative finance when used to rapidly discover and calibrate regime-specific factors, automate scenario backtesting, and enforce multi-factor risk budgeting across low-liquidity synthetic instruments.

---

# General Fields (Common to Both Submissions)

* **Q1 (Team Name):** `Chronos Labs` *(or your custom team name)*
* **Q2 (Team Lead Bitget UID):** `[Your numerical Bitget UID]`
* **Q3 (Team Lead Email):** `[Your active email address]`
* **Q4 (Team Lead Contact):** `@[Your Telegram handle]`
* **Q5 (Member Background):** `Developer` *(or Trader / Researcher)*
* **Q6 (University Name):** `[Your university name if applying for the 10x 500U University Prize, else leave blank]`
* **Q7 (Apply for Demo Day):** `Yes, I would like to apply`
* **Q8 (How did you hear):** `Twitter / X`
* **Q16 (X Promotional Post URL):** *(See template below)*
* **Q17 (Participated in S1?):** `No`
* **Q19 (Apply for K3 Token Subsidy):** `Yes`
* **Q20 (Open to Playbook Review and Listing):** `Yes`

---

# Mandatory Promotional X Post Template (Q16)

> **Official Requirement:** Must include `#BitgetHackathon` + `@Bitget_AI`, introduce Chronos, and **quote tweet** `https://x.com/Bitget_AI/status/2100519318824055159?s=20`.

### Copy-Paste X Post Text:
```text
When US markets sleep on weekends, @Bitget_AI tokenized stocks never stop.

Excited to introduce Chronos for the #BitgetHackathon S2!

Chronos is an autonomous 24/7 trading agent designed to capture statistical price dislocations in Bitget rTokens (NVDA, TSLA, COIN, MSTR, AAPL).

Key highlights:
- 24/7 Live Bitget Market Feed + Order Book Depth
- Deterministic 6-Scenario Stress Testing
- 90-Day Empirical Backtest: 151 trades, 51.0% Win Rate, 1.42 Profit Factor, max DD only -1.36%
- Full Web3 Wallet Isolation + Post-Trade Audits

Built with @Bitget_AI Agent Hub & Alibaba Cloud Qwen!

https://x.com/Bitget_AI/status/2100519318824055159?s=20
```
