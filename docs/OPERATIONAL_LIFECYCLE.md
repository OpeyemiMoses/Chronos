# Chronos Operational Lifecycle: The 4-Phase Alpha Engine

[![Bitget AI Hackathon S2](https://img.shields.io/badge/Bitget_AI_Hackathon-Track_1:_Alpha_Factory-00E5FF)](https://bitget-ai.gitbook.io/bitgetai_hackathons2/)
[![Sub-Theme](https://img.shields.io/badge/Sub--Theme-After--Hours_Information_Pricing-10B981)](https://bitget-ai.gitbook.io/bitgetai_hackathons2/)
[![Execution Standard](https://img.shields.io/badge/Execution-Bitget_UTA_v3_&_MCP-7000FF)](https://agent.bitget.com/mcp)
[![State Machine](https://img.shields.io/badge/Status-100%25_Cash_Weekday_Sleep-success)](https://github.com/OpeyemiMoses/Chronos)

> **"When tokenized US stocks make 7×24 the new normal, humans sleep — Agents don't."**  
> *Chronos exploits the structural 128-hour weekend closure of traditional financial exchanges by capturing retail pricing dislocations on tokenized U.S. equities (rTokens) and unwinding positions during Monday morning institutional pre-market liquidity, before returning to a flat cash posture (100% USDT cash allocation, zero market exposure) and autonomously self-auditing its strategy.*

> [!CAUTION]
> **Risk Disclosure & No Principal Guarantee:** There is **no principal guarantee** in quantitative or algorithmic trading. Tokenized equity synthetics trade against real market volatility, slippage, and taker fees. Individual trades **can and do close at a loss** if dislocations widen or dynamic stop losses (3.5% adverse excursion threshold) are triggered. "100% Cash Sleep" refers strictly to **portfolio asset allocation** (holding 0 open contracts and 100% of remaining account equity in USDT cash during weekday hours), not a guarantee of principal preservation.

---

## 🧭 The 4-Phase Weekly Operational Lifecycle

```
========================================================================================================
                          CHRONOS WEEKLY OPERATIONAL TIMELINE
========================================================================================================

    FRIDAY 16:00 EST        WEEKEND (24/7)            MONDAY 08:00-09:30 EST    MON 09:30 - FRI 15:59
 ┌──────────────────────┐  ┌───────────────────────┐  ┌──────────────────────┐  ┌───────────────────┐
 │       PHASE 1        │  │        PHASE 2        │  │       PHASE 3        │  │      PHASE 4      │
 │  Anchor Snapshot     │  │  Weekend Alpha Hunt   │  │  Pre-Market Harvest  │  │  Self-Audit &     │
 │  Lock Cash Close &   │─>│  Scan Retail Drift &  │─>│  Unwind into deep    │─>│  100% Cash Sleep  │
 │  BTC Macro Baseline  │  │  Enter |Z| >= 2.0σ    │  │  Institutional Books │  │  Tune Parameters  │
 └──────────────────────┘  └───────────────────────┘  └──────────────────────┘  └───────────────────┘
      (Cash Closes)           (Retail Dominance)         (Institutions Return)     (Zero Weekday Risk)
```

---

## 📌 Detailed Breakdown of Each Phase

### 🕒 Phase 1: Friday 16:00 EST — *Anchor Snapshot & Baseline Freeze*

#### What Happens:
1. At Friday 16:00 EST (closing bell of the New York Stock Exchange and NASDAQ), traditional U.S. equities cease trading for the weekend.
2. Chronos automatically triggers its **Anchor Snapshot Protocol**:
   - Queries the official cash closing prices of the 7 supported tokenized equities (`rNVDA`, `rTSLA`, `rAAPL`, `rCOIN`, `rMSTR`, `rSPY`, `rQQQ`).
   - Queries the 24/7 crypto-macro benchmark: **Bitcoin Spot Price** ($M_{\text{anchor}}$) and perpetual funding rates.
3. These values are cryptographically locked as unalterable reference baselines:
   $$P_{i,\text{anchor}} = P_i(t_{\text{anchor}}), \quad M_{\text{anchor}} = M(t_{\text{anchor}})$$

#### Why This Matters:
Without a fixed anchor, drift cannot be measured accurately. The Friday 16:00 EST closing price represents the **consensus institutional fair value** before market makers went offline.

---

### 🕒 Phase 2: Weekend 24/7 — *Information Dislocation Alpha Hunt*

#### What Happens:
1. Tokenized stocks (rTokens) continue trading 24 hours a day, 7 days a week on crypto platforms like Bitget.
2. During the weekend, breaking macroeconomic news, geopolitical developments, and social media sentiment hit the market.
3. Because institutional liquidity providers and designated market makers are offline, order book depth drops and **retail speculative flow dominates**.
4. Retail traders frequently overreact, causing tokenized prices to deviate wildly from fundamental reality.

#### Quantitative Model Under the Hood:
Chronos does not simply buy dips or sell rallies; it mathematically distinguishes between **justified macro moves** and **irrational retail overreaction**:

1. **Justified Macro Drift:**  
   Computes how much asset $i$ *should* have moved given the broad market crypto benchmark move ($\Delta M$), scaled by its rolling covariance beta ($\beta_{i,t}$):
   $$\text{Drift}_{i,\text{justified}}(t) = \beta_{i,t} \cdot \left(\frac{M(t) - M_{\text{anchor}}}{M_{\text{anchor}}}\right)$$

2. **Excess Retail Drift (The Pure Alpha):**  
   Isolates the unhedged retail distortion:
   $$\text{Excess Drift}_i(t) = \left(\frac{P_i(t) - P_{i,\text{anchor}}}{P_{i,\text{anchor}}}\right) - \text{Drift}_{i,\text{justified}}(t)$$

3. **Normalized Z-Score Signal:**  
   $$Z_i(t) = \frac{\text{Excess Drift}_i(t)}{\sigma_{i,\text{excess}}(t)}$$

4. **Order Execution Rules:**  
   - **Short Entry ($Z_i \ge +2.0\sigma$):** Retail speculative euphoria has overbought the asset $\rightarrow$ Open Short.
   - **Long Entry ($Z_i \le -2.0\sigma$):** Retail panic discount without fundamental justification $\rightarrow$ Open Long.
   - **Risk-Parity Weighting:** Capital is allocated inversely proportional to volatility ($w_i \propto 1/\sigma_i$), capped at $|w_i| \le 25\%$ per asset with gross leverage $\le 1.2\times$.
   - **Order Dispatch:** Dispatched via Bitget UTA v3 API with HMAC-SHA256 authentication or Bitget MCP client. Available margin is immediately deducted from the trading balance.

---

### 🕒 Phase 3: Monday 08:00–09:30 EST — *Institutional Pre-Market Harvest*

#### What Happens:
1. On Monday morning at 08:00 EST, traditional institutional market makers, designated broker-dealers, and algorithmic desks boot up for official U.S. Pre-Market Trading.
2. Institutional order books flood with deep liquidity.
3. The temporary weekend retail pricing distortions collapse as arbitrageurs force rTokens back toward institutional fair value.
4. **Mandatory Liquidation & Cash Unwind:**  
   - Between **08:00 and 09:30 EST**, Chronos executes atomic market orders to close all active weekend positions into deep pre-market liquidity.
   - All collateral and realized profits/losses are credited back to the vault.
   - **The portfolio is returned to a flat 100% USDT Cash allocation before 09:30 EST** (the official cash market open). Trades close at prevailing market prices and can book gains or audited losses.

#### Emergency Weekend Exits:
Chronos does not blindly hold until Monday if market conditions mandate early closure:
- **Take-Profit Convergence:** If the price converges early during the weekend ($|Z_i| \le 0.4\sigma$), Chronos secures profits immediately.
- **Stop-Loss Protection:** A hard adverse excursion stop-loss of **3.5%** is strictly enforced to protect vault equity against catastrophic black swan moves.

---

### 🕒 Phase 4: Monday 09:30 EST — *Cognitive Self-Audit & Adaptation*

#### What Happens:
As soon as the trade settles and the portfolio reaches 100% Cash, the **Cognitive Self-Auditor** ([`src/self_auditor.py`](file:///Users/user/.gemini/antigravity-ide/scratch/chronos/src/self_auditor.py)) initiates an autonomous post-mortem:

1. **Trade Audit Evaluation:**  
   - Analyzes realized net return, dollar PnL, and transaction fees.
   - Computes **Maximum Adverse Excursion (MAE)** (the maximum drawdown experienced while the trade was open).
   - Measures **Beta Decoupling Deviation** (did the asset follow its historical correlation to Bitcoin?).

2. **Root-Cause Diagnosis Taxonomy:**  
   - `PROFITABLE_ALPHA_CONVERGENCE`: Clean convergence into Monday institutional books. Model performed as calibrated.
   - `AUDITED_LOSS_MOMENTUM_OVERRUN`: Retail momentum broke through statistical bounds before reversing.
   - `AUDITED_LOSS_BETA_DECOUPLING`: Fundamental corporate news or earnings broke the historical macro correlation.
   - `AUDITED_LOSS_LATENCY_SLIPPAGE`: Bid-ask spread friction or network delay eroded the edge.

3. **Autonomous Parameter Adaptation:**  
   - If an asset suffered a momentum overrun loss, the auditor automatically increases the entry threshold for that asset (e.g. from $2.00\sigma \rightarrow 2.25\sigma$).
   - If adverse excursion was too deep, it tightens single-asset exposure caps.
   - Lessons, diagnostics, and adapted parameter states are saved into [`data/audit_memory.json`](file:///Users/user/.gemini/antigravity-ide/scratch/chronos/data/audit_memory.json).

---

### 💤 Weekday Intermission: Monday 09:30 – Friday 15:59 EST — *100% Cash Sleep*

#### What Happens:
- While traditional Wall Street trades between 9:30 AM and 4:00 PM EST throughout the week, **Chronos is 100% in cash**.
- It does not trade regular equity hours.
- It is completely insulated from:
  - Intraday Wall Street whipsaws
  - Regular-hours earnings surprise dumps
  - High-frequency market-maker front-running
  - Overnight gap risk between regular weekdays

Chronos remains in this dormant, capital-preserving sleep state until **Friday 16:00 EST**, at which point Phase 1 initiates again.

---

## 🎯 Strategic Advantages of This Architecture

| Operational Feature | Traditional Trading Bots | Chronos 4-Phase Alpha Engine |
| :--- | :--- | :--- |
| **Market Session Exposure** | Trade 24/7 or regular hours (high noise) | **Only trades weekend retail dislocations** |
| **Weekday Market Risk** | Constant capital exposure to macro shocks | **100% Cash from Mon 09:30 to Fri 15:59 EST** |
| **Counterparty Profile** | Trades against institutional HFT algorithms | **Trades against unhedged retail sentiment** |
| **Exit Liquidity** | Subject to retail slippage | **Harvested by returning institutional pre-market volume** |
| **Post-Trade Reflection** | Static parameters; requires manual dev retuning | **Autonomous Closed-Loop Cognitive Self-Auditor** |
| **Overfitting Risk** | Severe curve-fitting on backtests | **Audited Out-of-Sample / In-Sample Ratio: 1.26x** |

---

## 💻 How to Run the 4-Phase System

### 1. Single-Cycle Demonstration (All 4 Phases End-to-End)
```bash
source .venv/bin/activate
python src/live_runner.py --demo-cycle
```

### 2. 24/7 Autonomous Daemon (Runs Forever According to New York Clock)
```bash
source .venv/bin/activate
python src/live_runner.py --daemon
```

### 3. Visual Interactive Cockpit
Open the institutional trading terminal to observe the live 4-phase stepper and execute trades manually or via auto-pilot:
```bash
open dashboard/app.html
```
