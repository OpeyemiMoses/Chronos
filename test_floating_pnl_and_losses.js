// Test for Realistic Floating PnL, Early Close Loss/Profit, and Settlement
const fs = require('fs');

const storage = {};
global.localStorage = {
  getItem: (k) => storage[k] || null,
  setItem: (k, v) => { storage[k] = String(v); },
  removeItem: (k) => { delete storage[k]; },
  clear: () => { for (let k in storage) delete storage[k]; }
};

const elements = {};
function createMockEl(id) {
  const el = {
    id: id,
    textContent: '',
    innerHTML: '',
    style: {},
    classList: {
      add: () => {},
      remove: () => {},
      contains: () => false
    },
    addEventListener: () => {},
    removeEventListener: () => {},
    setAttribute: (k, v) => { el[k] = v; },
    getAttribute: (k) => el[k] || null,
    querySelector: () => createMockEl('sub_' + Math.random()),
    querySelectorAll: () => [],
    appendChild: function(c) { this.children = this.children || []; this.children.push(c); },
    removeChild: () => {},
    children: [],
    scrollTop: 0,
    scrollHeight: 100
  };
  return el;
}

global.document = {
  addEventListener: () => {},
  removeEventListener: () => {},
  querySelectorAll: () => [],
  querySelector: () => null,
  getElementById: (id) => {
    if (!elements[id]) elements[id] = createMockEl(id);
    return elements[id];
  },
  createElement: (t) => createMockEl('tag_' + Math.random())
};

global.window = {
  ethereum: null,
  addEventListener: () => {},
  removeEventListener: () => {},
  location: { href: '' },
  showToast: (t, m, type) => console.log(`[TOAST: ${type}] ${t}: ${m}`)
};
global.showToast = global.window.showToast;

const html = fs.readFileSync('dashboard/app.html', 'utf8');
const scriptMatches = html.match(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi);
let targetScript = '';
for (const s of scriptMatches) {
  if (s.includes('ChronosWalletStore')) {
    targetScript = s.replace(/<script[\s\S]*?>/i, '').replace(/<\/script>/i, '');
    break;
  }
}

const runner = new Function('window', 'document', 'localStorage', targetScript);
runner(global.window, global.document, global.localStorage);

const ChronosWalletStore = global.window.ChronosWalletStore;
const markets = global.window.markets;
const triggerInstantAgentTrade = global.window.triggerInstantAgentTrade;
const settleActivePosition = global.window.settleActivePosition;
const settleMondayMarketOpen = global.window.settleMondayMarketOpen;
const renderActivePositions = global.window.renderActivePositions;

console.log('--- TEST 1: Open trade and verify initial floating PnL is NOT free profit ---');
const testWallet = '0x9999999999999999999999999999999999999999';
ChronosWalletStore.connect(testWallet);
markets['rNVDA'].spot_price = 132.80;

triggerInstantAgentTrade();
let d = ChronosWalletStore.getCurrentData();
console.log('Open position count:', d.openPositions.length);
const pos = d.openPositions[0];
console.log('Position Symbol:', pos.symbol, 'Side:', pos.side, 'Entry Price:', pos.entry_price);

renderActivePositions();
const orderBookHtml = elements['orderBookContainer'].innerHTML;
if (orderBookHtml.includes('EST. PROFIT')) {
  console.error('FAIL: Position card should NOT use "EST. PROFIT" label');
  process.exit(1);
}
if (!orderBookHtml.includes('FLOATING PnL')) {
  console.error('FAIL: Position card must display "FLOATING PnL"');
  process.exit(1);
}
console.log('Confirmed: Card displays FLOATING PnL instead of EST. PROFIT');

console.log('--- TEST 2: Adverse Price Move (Short loses when spot price increases) ---');
// For a SHORT position entered at 132.80, if price moves UP to 134.50, trade must be in LOSS!
markets['rNVDA'].spot_price = 134.50;
renderActivePositions();

const orderBookLossHtml = elements['orderBookContainer'].innerHTML;
console.log('Simulated Adverse Price: $134.50 (vs Entry: $132.80 for SHORT)');
if (!orderBookLossHtml.includes('var(--color-red)')) {
  console.error('FAIL: Adverse move must render floating PnL in RED');
  process.exit(1);
}
console.log('Confirmed: Adverse market move renders floating loss in red');

console.log('--- TEST 3: Close Position Early at Adverse Price (Audited Loss) ---');
const initialBalance = d.paperBalance;
console.log('Wallet balance before early close:', initialBalance);
settleActivePosition(pos.id);

d = ChronosWalletStore.getCurrentData();
console.log('Wallet balance after early close:', d.paperBalance);
console.log('Trades length:', d.trades.length);
const closedTrade = d.trades[0];
console.log('Closed Trade Return %:', closedTrade.return_pct, 'PnL USD:', closedTrade.pnl_usd);
console.log('Closed Trade Note:', closedTrade.audit_note);

if (closedTrade.pnl_usd >= 0 || closedTrade.return_pct >= 0) {
  console.error('FAIL: Closing early at adverse price should result in a LOSS!');
  process.exit(1);
}
console.log('Confirmed: Early close at adverse price successfully settled as an AUDITED LOSS!');

console.log('--- TEST 4: Favorable Price Move (Short gains when spot price drops) ---');
markets['rNVDA'].spot_price = 132.80;
triggerInstantAgentTrade();
d = ChronosWalletStore.getCurrentData();
const pos2 = d.openPositions[0];

// Price drops to 132.00 (favorable for SHORT)
markets['rNVDA'].spot_price = 132.00;
renderActivePositions();
settleActivePosition(pos2.id);

d = ChronosWalletStore.getCurrentData();
const winTrade = d.trades[0];
console.log('Favorable Trade Return %:', winTrade.return_pct, 'PnL USD:', winTrade.pnl_usd);
console.log('Favorable Trade Note:', winTrade.audit_note);

if (winTrade.pnl_usd <= 0 || winTrade.return_pct <= 0) {
  console.error('FAIL: Closing early after favorable drop should result in a profit');
  process.exit(1);
}
console.log('Confirmed: Early close after favorable drop settled with legitimate profit!');

console.log('--- TEST 5: Monday Market Settlement Distribution (Wins AND Losses) ---');
// Simulate the Ornstein-Uhlenbeck weekend ticker by explicitly setting spot_price
// to both favorable (price dropped → SHORT profit) and adverse (price rose → SHORT loss) levels.
// This proves settlement is based on actual live price at settlement time, NOT random wins.
let totalSettledWins = 0;
let totalSettledLosses = 0;

const ENTRY_PRICE = 132.80;
// Alternate between adverse and favorable spot prices across 15 cycles
const mondaySpotPrices = [
  134.50, // adverse (SHORT loss: price rose from 132.80)
  130.20, // favorable (SHORT win: price fell toward anchor)
  135.10, // adverse
  129.80, // favorable
  133.90, // adverse
  128.50, // favorable (near anchor)
  134.20, // adverse
  131.00, // favorable
  136.00, // adverse
  130.60, // favorable
  133.10, // adverse
  129.40, // favorable
  134.80, // adverse
  131.50, // favorable
  133.40  // adverse
];

for (let cycle = 0; cycle < 15; cycle++) {
  // Set the market spot_price to simulate where price is on Monday morning
  markets['rNVDA'].spot_price = mondaySpotPrices[cycle];

  d.openPositions = [{
    id: `POS-CYCLE-${cycle}`,
    symbol: 'rNVDA',
    side: 'SHORT',
    entry_price: ENTRY_PRICE,
    target_price: 128.40,
    collateral: 2500,
    contracts: '18.82',
    entry_time: '14:00',
    status: 'ACTIVE'
  }];
  ChronosWalletStore.setCurrentData(d);
  settleMondayMarketOpen();
  d = ChronosWalletStore.getCurrentData();
  const latestTrade = d.trades[0];
  const expectedWin = mondaySpotPrices[cycle] < ENTRY_PRICE; // SHORT profits when price drops
  const actualWin = latestTrade.pnl_usd > 0;

  // Verify each trade settled correctly based on the spot price
  if (actualWin !== expectedWin) {
    console.error(`FAIL: Cycle ${cycle}: spot=$${mondaySpotPrices[cycle]}, entry=$${ENTRY_PRICE}, expected ${expectedWin ? 'WIN' : 'LOSS'} but got ${actualWin ? 'WIN' : 'LOSS'}. PnL: $${latestTrade.pnl_usd}`);
    process.exit(1);
  }

  if (latestTrade.pnl_usd > 0) totalSettledWins++;
  else totalSettledLosses++;
}

console.log(`Settlement distribution across 15 cycles: ${totalSettledWins} Wins, ${totalSettledLosses} Losses`);
if (totalSettledWins === 0 || totalSettledLosses === 0) {
  console.error('FAIL: Settlement must include BOTH wins and losses, not 100% wins or 100% losses!');
  process.exit(1);
}
console.log('Confirmed: Monday settlement realistically uses actual live spot_price — wins and losses determined by real market position!');

console.log('=== ALL REALISTIC PRICING & LOSS TESTS PASSED PERFECTLY ===');
process.exit(0);
