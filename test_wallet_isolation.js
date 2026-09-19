// Simulation test for Chronos Wallet Isolation & Dynamic Metrics
const fs = require('fs');

// Mock localStorage
const storage = {};
global.localStorage = {
  getItem: (k) => storage[k] || null,
  setItem: (k, v) => { storage[k] = String(v); },
  removeItem: (k) => { delete storage[k]; },
  clear: () => { for (let k in storage) delete storage[k]; }
};

// Mock document
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
    addEventListener: (evt, cb) => {},
    removeEventListener: (evt, cb) => {},
    setAttribute: (k, v) => { el[k] = v; },
    getAttribute: (k) => el[k] || null,
    removeAttribute: (k) => { delete el[k]; },
    querySelector: (sel) => createMockEl('sub_' + Math.random()),
    querySelectorAll: (sel) => [],
    appendChild: function(child) {
      this.children = this.children || [];
      this.children.push(child);
    },
    removeChild: function(child) {
      this.children = this.children || [];
      const idx = this.children.indexOf(child);
      if (idx !== -1) this.children.splice(idx, 1);
    },
    children: [],
    scrollTop: 0,
    scrollHeight: 100
  };
  return el;
}

global.document = {
  addEventListener: (event, cb) => {},
  removeEventListener: (event, cb) => {},
  querySelectorAll: (selector) => [],
  querySelector: (selector) => null,
  getElementById: (id) => {
    if (!elements[id]) {
      elements[id] = createMockEl(id);
    }
    return elements[id];
  },
  createElement: (tag) => {
    return createMockEl('tag_' + Math.random());
  }
};

global.window = {
  ethereum: null,
  addEventListener: (event, cb) => {},
  removeEventListener: (event, cb) => {},
  location: { href: '' },
  showToast: (t, m, type) => console.log(`[TOAST: ${type}] ${t}: ${m}`)
};
global.showToast = global.window.showToast;

// Read the app.html file and extract JS from the main script
const html = fs.readFileSync('dashboard/app.html', 'utf8');

// Find the script containing ChronosWalletStore
const scriptMatches = html.match(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi);
let targetScript = '';
for (const s of scriptMatches) {
  if (s.includes('ChronosWalletStore')) {
    targetScript = s.replace(/<script[\s\S]*?>/i, '').replace(/<\/script>/i, '');
    break;
  }
}

if (!targetScript) {
  console.error('FAIL: Could not find ChronosWalletStore script');
  process.exit(1);
}

// Execute the script in an isolated Function scope
try {
  const runner = new Function('window', 'document', 'localStorage', targetScript);
  runner(global.window, global.document, global.localStorage);
} catch (e) {
  console.error('FAIL during script eval:', e);
  process.exit(1);
}

const ChronosWalletStore = global.window.ChronosWalletStore;
const triggerInstantAgentTrade = global.window.triggerInstantAgentTrade;
const settleMondayMarketOpen = global.window.settleMondayMarketOpen;

console.log('--- TEST 1: Initial State Disconnected ---');
console.log('Connected Wallet:', ChronosWalletStore.currentAddress);
console.log('Overview Balance Text:', elements['overviewPortfolioVal']?.textContent);
console.log('Overview Settled Count:', elements['overviewSettledCount']?.textContent);
console.log('Overview Cumulative Return:', elements['overviewCumulativeReturn']?.textContent);
console.log('Sidebar Trades Badge:', elements['sidebarTradesBadge']?.textContent);

if (elements['overviewPortfolioVal']?.textContent !== '—') {
  console.error('FAIL: overviewPortfolioVal should be — when disconnected');
  process.exit(1);
}

console.log('--- TEST 2: Connect Fresh Wallet 0xAlice... ---');
const aliceAddr = '0x1111111111111111111111111111111111111111';
ChronosWalletStore.connect(aliceAddr);
const aliceData = ChronosWalletStore.getCurrentData();
console.log('Alice address:', ChronosWalletStore.currentAddress);
console.log('Alice trades length:', aliceData.trades.length);
console.log('Alice audits length:', aliceData.audits.length);
console.log('Alice openPositions length:', aliceData.openPositions.length);
console.log('Alice Balance:', elements['overviewPortfolioVal']?.textContent);
console.log('Alice Cumulative Return:', elements['overviewCumulativeReturn']?.textContent);

if (aliceData.trades.length !== 0 || aliceData.audits.length !== 0) {
  console.error('FAIL: Fresh wallet Alice should have 0 trades and 0 audits');
  process.exit(1);
}

console.log('--- TEST 3: Deploy Instant Opportunistic Trade for Alice ---');
triggerInstantAgentTrade();
const aliceAfterTrade = ChronosWalletStore.getCurrentData();
console.log('Alice openPositions count:', aliceAfterTrade.openPositions.length);
console.log('Alice trade symbol:', aliceAfterTrade.openPositions[0]?.symbol);
console.log('Alice trade side:', aliceAfterTrade.openPositions[0]?.side);
console.log('Portfolio Quota Badge:', elements['portfolioQuotaBadge']?.textContent);
console.log('Portfolio Available Slots:', elements['portfolioAvailableSlots']?.textContent);

if (aliceAfterTrade.openPositions.length !== 1) {
  console.error('FAIL: Alice should have 1 open trade');
  process.exit(1);
}
if (elements['portfolioQuotaBadge']?.textContent !== '1 / 5 Active') {
  console.error('FAIL: portfolioQuotaBadge should be 1 / 5 Active');
  process.exit(1);
}

console.log('--- TEST 4: Settle Monday Market Open for Alice ---');
settleMondayMarketOpen();
const aliceAfterSettle = ChronosWalletStore.getCurrentData();
console.log('Alice openPositions count after settle:', aliceAfterSettle.openPositions.length);
console.log('Alice settled trades count:', aliceAfterSettle.trades.length);
console.log('Alice settled audits count:', aliceAfterSettle.audits.length);
console.log('Overview Settled Count:', elements['overviewSettledCount']?.textContent);
console.log('Overview Cumulative Return:', elements['overviewCumulativeReturn']?.textContent);
console.log('Portfolio Quota Badge:', elements['portfolioQuotaBadge']?.textContent);

if (aliceAfterSettle.openPositions.length !== 0) {
  console.error('FAIL: Open positions should be 0 after settlement');
  process.exit(1);
}
if (aliceAfterSettle.trades.length !== 1) {
  console.error('FAIL: Alice should have exactly 1 settled trade in ledger');
  process.exit(1);
}
if (elements['portfolioQuotaBadge']?.textContent !== '0 / 5 Active') {
  console.error('FAIL: portfolioQuotaBadge should be 0 / 5 Active');
  process.exit(1);
}

console.log('--- TEST 5: Connect Fresh Wallet 0xBob... (Isolation Check) ---');
const bobAddr = '0x2222222222222222222222222222222222222222';
ChronosWalletStore.connect(bobAddr);
const bobData = ChronosWalletStore.getCurrentData();
console.log('Bob address:', ChronosWalletStore.currentAddress);
console.log('Bob trades length:', bobData.trades.length);
console.log('Bob audits length:', bobData.audits.length);
console.log('Bob openPositions length:', bobData.openPositions.length);
console.log('Bob Settled Count in DOM:', elements['overviewSettledCount']?.textContent);

if (bobData.trades.length !== 0 || bobData.audits.length !== 0 || bobData.openPositions.length !== 0) {
  console.error('FAIL: Bob must have 0 trades, 0 audits, 0 openPositions');
  process.exit(1);
}
if (elements['overviewSettledCount']?.textContent !== '0 Settled Trades') {
  console.error('FAIL: Overview settled count for Bob should be 0 Settled Trades');
  process.exit(1);
}

console.log('--- TEST 6: Reconnect Alice (Persistence Check) ---');
ChronosWalletStore.connect(aliceAddr);
const aliceReloaded = ChronosWalletStore.getCurrentData();
console.log('Alice reloaded trades length:', aliceReloaded.trades.length);
console.log('Alice reloaded audits length:', aliceReloaded.audits.length);
console.log('Overview Settled Count for Alice:', elements['overviewSettledCount']?.textContent);

if (aliceReloaded.trades.length !== 1) {
  console.error('FAIL: Alice must retain her 1 settled trade');
  process.exit(1);
}
if (elements['overviewSettledCount']?.textContent !== '1 Settled Trade') {
  console.error('FAIL: Overview settled count for Alice should be 1 Settled Trade');
  process.exit(1);
}

console.log('--- TEST 7: Disconnect Wallet ---');
ChronosWalletStore.disconnect();
console.log('Disconnected Connected Wallet:', ChronosWalletStore.currentAddress);
console.log('Disconnected Balance Text:', elements['overviewPortfolioVal']?.textContent);
console.log('Disconnected Cumulative Return:', elements['overviewCumulativeReturn']?.textContent);

if (elements['overviewPortfolioVal']?.textContent !== '—') {
  console.error('FAIL: Disconnected overviewPortfolioVal should be —');
  process.exit(1);
}

console.log('--- TEST 8: Check for Absence of Historical Strategy Benchmark & Overview Ledger ---');
if (html.includes('Historical Strategy Benchmark')) {
  console.error('FAIL: Historical Strategy Benchmark should be removed from all screens');
  process.exit(1);
}
if (html.includes('overviewLedgerTableBody')) {
  console.error('FAIL: overviewLedgerTableBody should not exist on Overview page');
  process.exit(1);
}
console.log('Confirmed: 0 instances of Historical Strategy Benchmark, 0 overview ledger duplicate');

console.log('--- TEST 9: Customize Autonomous Agent Settings in Settings View ---');
ChronosWalletStore.connect(aliceAddr);
const saveAgentSettings = global.window.saveAgentSettings;
const verifyStrategyClearance = global.window.verifyStrategyClearance;
const clearLedgerHistory = global.window.clearLedgerHistory;

elements['settingsAgentMaxTradesInput'] = { value: '3' };
elements['settingsAgentCollateralInput'] = { value: '1500' };

saveAgentSettings();
const aliceUpdatedCfg = ChronosWalletStore.getCurrentData();
console.log('Alice maxTrades:', aliceUpdatedCfg.agentConfig.maxTrades);
console.log('Alice collateralPerTrade:', aliceUpdatedCfg.agentConfig.collateralPerTrade);

if (aliceUpdatedCfg.agentConfig.maxTrades !== 3 || aliceUpdatedCfg.agentConfig.collateralPerTrade !== 1500) {
  console.error('FAIL: Custom agent configuration was not saved properly');
  process.exit(1);
}

console.log('Sidebar badge for 3 trades:', elements['sidebarTradesBadge']?.textContent);
console.log('Overview cap badge for 3 trades:', elements['overviewWeekendCapBadge']?.textContent);
console.log('Sidebar nav text for 3 trades:', elements['sidebarTradesNavText']?.textContent);
console.log('Trades page title for 3 trades:', elements['tradesPageTitle']?.textContent);

if (elements['overviewWeekendCapBadge']?.textContent !== 'WEEKEND CAP: 3 TRADES') {
  console.error('FAIL: overviewWeekendCapBadge should be WEEKEND CAP: 3 TRADES, got:', elements['overviewWeekendCapBadge']?.textContent);
  process.exit(1);
}
if (elements['sidebarTradesBadge']?.textContent !== '0/3') {
  console.error('FAIL: sidebarTradesBadge should be 0/3, got:', elements['sidebarTradesBadge']?.textContent);
  process.exit(1);
}
if (elements['sidebarTradesNavText']?.textContent !== '3-Trade Strategy') {
  console.error('FAIL: sidebarTradesNavText should be 3-Trade Strategy, got:', elements['sidebarTradesNavText']?.textContent);
  process.exit(1);
}
if (elements['tradesPageTitle']?.textContent !== 'Active 3-Trade Weekend Portfolio') {
  console.error('FAIL: tradesPageTitle should be Active 3-Trade Weekend Portfolio, got:', elements['tradesPageTitle']?.textContent);
  process.exit(1);
}

console.log('--- TEST 10: Strategy Clearance Engine Test ---');
const clearanceResult = verifyStrategyClearance('rNVDA');
console.log('rNVDA Strategy Clearance:', clearanceResult.cleared, clearanceResult.reason);
if (!clearanceResult.cleared) {
  console.error('FAIL: rNVDA should clear strategy rules on fresh state');
  process.exit(1);
}
if (clearanceResult.collateral !== 1500) {
  console.error('FAIL: Clearance should use custom configured collateral of 1500');
  process.exit(1);
}

console.log('--- TEST 11: Clear Ledger Functionality ---');
console.log('Alice trades before clear:', ChronosWalletStore.getCurrentData().trades.length);
clearLedgerHistory();
console.log('Alice trades after clear:', ChronosWalletStore.getCurrentData().trades.length);
if (ChronosWalletStore.getCurrentData().trades.length !== 0) {
  console.error('FAIL: clearLedgerHistory should wipe ledger to 0 trades');
  process.exit(1);
}

console.log('--- TEST 12: Disconnected Trade Guard Verification ---');
ChronosWalletStore.disconnect();
console.log('Connected Wallet after disconnect:', ChronosWalletStore.currentAddress);
if (ChronosWalletStore.currentAddress !== null) {
  console.error('FAIL: Wallet should be null when disconnected');
  process.exit(1);
}

// Attempt to execute opportunistic trade while disconnected
const executeOpportunisticTrade = global.window.executeOpportunisticTrade;
const runAutonomousAgentTick = global.window.runAutonomousAgentTick;
const toggleAutoPilot = global.window.toggleAutoPilot;

executeOpportunisticTrade('rTSLA');
runAutonomousAgentTick();
toggleAutoPilot();

// Check that orderBookContainer is clean and reflects disconnected state
const orderBookHtml = elements['orderBookContainer']?.innerHTML || '';
console.log('Order book contains No Wallet Connected:', orderBookHtml.includes('No Wallet Connected'));
if (!orderBookHtml.includes('No Wallet Connected')) {
  console.error('FAIL: Order book container should display "No Wallet Connected" when disconnected');
  process.exit(1);
}

// Check auto-pilot status
console.log('Auto pilot badge:', elements['autoPilotModeBadge']?.textContent);
if (!elements['autoPilotModeBadge']?.textContent.includes('NO WALLET')) {
  console.error('FAIL: Auto-pilot badge should show STANDBY (NO WALLET)');
  process.exit(1);
}

console.log('=== ALL 12 ISOLATION, AGENT SETTINGS, CLEARANCE & DISCONNECTED GUARD TESTS PASSED PERFECTLY ===');
process.exit(0);
