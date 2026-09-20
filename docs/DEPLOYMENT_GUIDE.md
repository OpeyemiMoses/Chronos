# 🚀 Chronos — Deployment Guide (Railway & Vercel)

Chronos is production-ready for deployment to cloud platforms. You have two primary deployment architectures:

* **Option 1 (Recommended — 1-Click All-in-One):** Deploy full-stack on **Railway**. Railway runs the Python backend (`server.py`), live Bitget ticker streams, and serves the Web3 terminal directly on a public HTTPS domain.
* **Option 2 (Decoupled):** Deploy the **Python API Backend on Railway** and the **Terminal Frontend on Vercel**.

---

## Option 1: 1-Click Full-Stack Deployment on Railway (Recommended)

Because Chronos uses a lightweight Flask server that serves both the API endpoints (`/api/market-prices`, `/api/qwen/thesis`, `/api/trade`) and the trading UI (`/terminal`), Railway can host the entire system under a single domain in under 3 minutes.

### Step-by-Step Instructions:

1. **Log in to Railway:**
   * Go to [railway.app](https://railway.app) and sign in with your GitHub account.

2. **Create New Project:**
   * Click **"+ New Project"** in the top-right corner.
   * Select **"Deploy from GitHub repo"**.
   * Choose your repository: **`OpeyemiMoses/Chronos`**.

3. **Configure Settings (Automatic):**
   * Railway automatically detects `requirements.txt`, `Procfile`, and `railway.toml`.
   * It will automatically set:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python server.py`
     - **Healthcheck Path:** `/api/status`

4. **Set Environment Variables:**
   * In your Railway dashboard, click on your project service $\rightarrow$ **"Variables"** tab.
   * Add the following (optional but recommended):
     ```env
     PORT=8899
     TRADING_MODE=PAPER
     BITGET_API_KEY=your_bitget_api_key_here
     BITGET_API_SECRET=your_bitget_secret_here
     BITGET_PASSPHRASE=your_bitget_passphrase_here
     BITGET_QWEN_API_KEY=your_qwen_key_here
     ```
   *(Note: Even with no Bitget credentials entered, Chronos defaults to safe PAPER trading mode and streams live public market prices from Bitget without any API keys).*

5. **Generate Public Domain:**
   * Go to the **"Settings"** tab $\rightarrow$ **"Networking"** section.
   * Click **"Generate Domain"** (e.g. `chronos-production.up.railway.app`).

6. **Verify Deployment:**
   * Visit: `https://your-domain.up.railway.app/terminal`
   * Your terminal is now live on the internet with 24/7 Bitget ticker updates, Qwen reasoning, and Web3 wallet connectivity!

---

## Option 2: Deploy Frontend on Vercel

If you prefer having your frontend hosted on Vercel’s global Edge CDN:

### Step 1: Deploy Backend to Railway (per Option 1 above)
Get your live backend URL from Railway (e.g., `https://chronos-backend.up.railway.app`).

### Step 2: Configure Vercel Proxy in `vercel.json`
Update `vercel.json` to proxy API requests directly to your live Railway backend URL:

```json
{
  "version": 2,
  "cleanUrls": true,
  "rewrites": [
    { "source": "/api/:match*", "destination": "https://your-railway-backend.up.railway.app/api/:match*" },
    { "source": "/", "destination": "/dashboard/index.html" },
    { "source": "/terminal", "destination": "/dashboard/app.html" },
    { "source": "/docs", "destination": "/dashboard/docs.html" },
    { "source": "/help", "destination": "/dashboard/help.html" },
    { "source": "/assets/:match*", "destination": "/dashboard/assets/:match*" }
  ]
}
```

### Step 3: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in.
2. Click **"Add New..."** $\rightarrow$ **"Project"**.
3. Import your GitHub repository: **`OpeyemiMoses/Chronos`**.
4. In Project Settings:
   - **Framework Preset:** `Other`
   - **Root Directory:** `./`
   - **Build & Output Settings:** Leave default (Vercel automatically detects `vercel.json`).
5. Click **"Deploy"**.

Your Vercel deployment will be live at `https://chronos.vercel.app/terminal`!

---

## Verification Checklist After Deployment

Once deployed, verify that the following endpoints return `HTTP 200 OK`:

1. **Terminal UI:** `https://your-domain/terminal` (Loads the interactive trading terminal)
2. **Live Bitget Prices:** `https://your-domain/api/market-prices` (Returns JSON with 7 live token prices)
3. **Qwen AI Reasoning:** `https://your-domain/api/qwen/thesis?symbol=rNVDA` (Returns plain-English thesis)
4. **Empirical Backtest Data:** `https://your-domain/api/backtest-results` (Returns 90-day backtest JSON)
5. **System Health:** `https://your-domain/api/status` (Returns `status: ok`)
