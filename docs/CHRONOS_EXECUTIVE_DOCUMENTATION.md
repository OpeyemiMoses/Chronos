# Chronos — Master Project Documentation

---

## 1. Description

**Chronos** is an autonomous quantitative trading agent and unified execution terminal designed to capture 24/7 weekend price dislocations across tokenized U.S. equities (rTokens on Bitget) and harvest alpha upon Monday morning institutional liquidity return.

Traditional financial markets operate on legacy schedules, closing every Friday at 4:00 PM EST. However, tokenized stocks trade 24/7 on Web3 rails. Chronos connects these two worlds. It treats the 65-hour weekend closure of Wall Street as a systematic dislocation factory, using a dual-engine architecture:

* **The Quantitative Risk Shield:** High-frequency statistical Z-score algorithms and deterministic 6-scenario stress models that filter market noise and strictly enforce capital preservation.
* **The Cognitive AI Brain:** Alibaba Cloud Qwen (`qwen3.8-max`), which evaluates live order book depth, momentum exhaustion, and market sentiment to generate plain-English trade theses and post-mortem diagnostic audits.

The terminal features real-time Bitget market streaming, live mark-to-market floating P&L, isolated multi-user Web3 wallet connectivity, and automated Monday pre-market position unwinding into 100% USDT cash.

---

## 2. Problem

### The 65-Hour Liquidity Void
Every week at 4:00 PM EST on Friday, the New York Stock Exchange and NASDAQ close. For **65 consecutive hours**—from Friday evening until Monday at 9:30 AM EST—the world’s primary stock markets are completely dark. Over a year, traditional equities are closed for more than **4,000 hours**, nearly half the calendar.

### The 24/7 Web3 Reality & Order Book Fragility
Macro events, geopolitical developments, regulatory announcements, and earnings leaks continue to happen over the weekend. On Bitget, tokenized U.S. equities (`NVDAUSDT`, `TSLAUSDT`, `COINUSDT`, `MSTRUSDT`, `AAPLUSDT`, `QQQUSDT`, `SPYUSDT`) trade continuously 24/7/365.

However, during the weekend:
1. **Institutional Market Makers Are Offline:** Designated broker-dealers, high-frequency liquidity providers, and cash clearinghouses are closed.
2. **Thin, Retail-Dominated Order Books:** Without institutional depth, weekend books are shallow and susceptible to speculative hysteria.
3. **Severe Price Dislocations:** Retail traders aggressively bid up or dump tokenized stocks based on rumors and emotion, creating massive artificial premiums or discounts away from the true fundamental closing value.
4. **The Human Dilemma:** Manual traders cannot monitor 7+ continuous order books across 65 hours without sleep. They suffer from fatigue, emotional bias, poor risk sizing, and high execution slippage.

---

## 3. Solution

Chronos monetizes this structural inefficiency through a systematic, 4-phase operational lifecycle:

```
[Friday 16:00 EST]          [Weekend 24/7]           [Weekend Signal]          [Monday 08:00 EST]        [Monday 09:30 EST]
Anchor Lock Consensus  ──>  24/7 Bitget Stream   ──>  |Z| >= 1.50σ Clearance ──>  Pre-Market Harvest  ──>  Flat Cash Sleep
(Freeze Stock Prices)       (Detect Retail Drift)     (Stress Test & Qwen)       (Exit Into Deep Liq)     (100% USDT Cash)
```

1. **Locks the Institutional Consensus Anchor:** At 16:00 EST on Friday, Chronos takes an immutable snapshot of official institutional closing settlement prices across all target assets ($P_{\text{anchor}}$).
2. **Streams 24/7 Live Bitget Telemetry:** Every 3.5 seconds, the backend polls Bitget’s live USDT-Futures ticker and depth APIs to track spot prices, bid/ask depth, and rolling 20-day volatility standard deviations.
3. **Enforces the Algorithmic Noise Band:** To prevent capital bleed from taker fees (0.06%) and slippage, assets drifting under 2.0% or within 1.5 standard deviations are flagged as noise and strictly blocked from order routing.
4. **Dual-Layer Evaluation:** When an asset exceeds the threshold (e.g. `rNVDA` drifting +2.3% at $Z = 1.52\sigma$):
   * **Deterministic Stress Engine:** Simulates 6 forward-looking price shock scenarios against empirical beta, verifying risk/reward asymmetry.
   * **Qwen AI Reasoning:** Synthesizes order flow dynamics into a verifiable trade thesis.
5. **Pre-Market Institutional Liquidity Harvest:** When institutional liquidity returns Monday morning (08:00–09:30 EST), retail premiums collapse back toward the Friday anchor. Chronos executes limit/market orders to close positions into this returning deep liquidity.
6. **Flat Cash Posture (Zero Weekday Exposure):** 100% of open contracts are closed into liquid USDT before 9:30 AM EST, completely bypassing normal weekday market risk.

---

## 4. Why It Was Built

1. **Capitalizing on the 24/7 RWA Paradigm Shift:** Tokenized Real-World Assets are the multi-trillion-dollar future of global finance. When traditional markets sleep while tokenized markets trade, a structural information pricing asymmetry is born. Chronos was built to capture this asymmetry systematically.
2. **Uncorrelated Statistical Alpha:** Traditional trading strategies (momentum chasing, trend following, long-only equities) are crowded and tied to market direction. Chronos generates returns **strictly during market downtime**, producing an alpha stream uncorrelated with standard equity beta.
3. **Institutional AI Defensibility:** Most "AI trading bots" are naive prompt wrappers that hallucinate trades and blow up on market impact. Chronos demonstrates the correct institutional framework: **an LLM for contextual reasoning and qualitative explanation + deterministic mathematical code for risk gates, stress tests, and sizing limits.**
4. **Tireless, Emotionless Execution:** Machines do not get tired, panic, or FOMO. Chronos provides continuous, disciplined risk management across all 65 weekend hours without human fatigue.

---

## 5. Who It Is Built For

* **Quantitative & Systematic Traders:** Traders seeking market-neutral statistical mean-reversion strategies with audited metrics (1.42 profit factor, 1.74 Sharpe, -1.36% max drawdown) and zero curve-fitting decay.
* **Stablecoin & Yield Allocators:** Web3 users holding idle USDT who want active, market-neutral returns generated from real-world equity dislocations without taking directional crypto market risk.
* **Prop Trading Desks & Family Offices:** Professional entities seeking an automated weekend alpha overlay that operates exclusively while traditional venues are closed and sits in 100% cash during the week.
* **Bitget Ecosystem & Playbook Users:** Retail and institutional traders on Bitget who can subscribe to or deploy Chronos directly through **Bitget Playbook** for automated revenue-sharing execution.

---

## 6. Core Primitives

Chronos is founded on six mathematical and architectural primitives:

### Primitive 1: The Friday Consensus Settlement Anchor ($P_{\text{anchor}}$)
Freezes the official Friday 16:00 EST closing settlement price as the structural fair-value baseline:
$$P_{\text{anchor}} = P_{\text{close, Fri 16:00 EST}}$$
All weekend movements are measured as relative drift against this consensus:
$$\text{Drift}(t) = \frac{P_{\text{spot}}(t) - P_{\text{anchor}}}{P_{\text{anchor}}}$$

### Primitive 2: Statistical Dispersion & Rolling Z-Score ($Z$)
Normalizes price deviations against 20-day historical volatility ($\sigma_{20}$) and mean price ($\mu_{20}$):
$$Z(t) = \frac{P_{\text{spot}}(t) - \mu_{20}}{\sigma_{20}}$$
* $|Z| < 1.50\sigma$: Normal random fluctuation $\rightarrow$ **Blocked**.
* $|Z| \ge 1.50\sigma$: Statistically significant dislocation $\rightarrow$ **Cleared for Stress Testing**.

### Primitive 3: The Algorithmic Noise Band (Capital Shield)
Protects capital from fee erosion by enforcing an explicit entry barrier:
$$\text{Execution Status} = \begin{cases} \text{CLEARED}, & \text{if } |Z| \ge 1.50\sigma \text{ AND } |\text{Drift}| \ge 2.0\% \\ \text{BLOCKED (NOISE BAND)}, & \text{otherwise} \end{cases}$$
Assets inside the Noise Band (like Tesla and MicroStrategy when flat) are scored 10/100 and held in cash, eliminating unnecessary taker fee churn ($0.06\%$) and spread slippage.

### Primitive 4: Deterministic 6-Scenario Forward Stress Matrix
Simulates 6 forward outcomes calibrated to the asset’s empirical volatility beta ($\beta_i$):
1. **Full Reversion:** 100% convergence to Friday anchor.
2. **Partial Convergence (60%):** 60% gap closure.
3. **Flat Stall:** Price remains pinned at current spot until Monday morning.
4. **Adverse Shock (+2%):** Additional +2% momentum move against the position.
5. **Blow-Off (+4%):** Severe +4% retail momentum spike.
6. **Tail Shock (+8%):** Black-swan gap event against the trade.
* Enforces a hard **3.50% dynamic stop-loss**. If downside tail risk violates the safety margin, the order is halted.

### Primitive 5: Hybrid AI Architecture (Qwen LLM + Hard Deterministic Rules)
* **Perception & Thesis Engine:** Alibaba Cloud Qwen (`qwen3.8-max`) ingests order book imbalance, beta volatility, and retail sentiment to produce a structured, plain-English trade thesis and explain risk metrics.
* **Execution & Safety Layer:** Deterministic Python/JS code manages wallet balances, enforces a 25% single-asset capital cap, limits concurrent positions to max 5, and routes orders.

### Primitive 6: Web3 Isolated Wallet State
Built with custom RainbowKit connectors, ensuring complete isolation across connected addresses:
* Wallets (`0xAlice`, `0xBob`) each maintain private, segregated local storage stores.
* Disconnecting a wallet immediately wipes the UI to a secure baseline.
* Zero cross-contamination of trade quotas, margin balances, or audit histories.

---

### Empirical Validation Summary (90-Day Continuous Evaluation)
* **Dataset:** 90 continuous daily candlestick records from Bitget USDT-Futures.
* **Executed Trades:** 151 real trade cycles.
* **Overall Win Rate:** 51.0% (65.0% on Coinbase, 56.5% on NVIDIA).
* **Portfolio Profit Factor:** 1.42 (Gross Profit: $3,328.08 USDT, Gross Loss: $2,336.88 USDT).
* **Maximum Drawdown:** Capped at -1.36% (-$682.79 USDT).
* **Sharpe Ratio:** 1.74 | **Sortino Ratio:** 3.25.
* **Fee Model:** 0.06% exchange taker fee deducted on every entry and exit.
