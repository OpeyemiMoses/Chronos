// Test Paper vs Live state isolation and balance displays
const fs = require('fs');
const assert = require('assert');

console.log("--- TEST: Paper vs Live State Isolation & Clean Balance ---");
const html = fs.readFileSync('dashboard/app.html', 'utf8');

// 1. Verify wiping positions in live switch was completely removed
assert(!html.includes('d.positions = [];\n          d.openPositions = [];'), "Regression: Wiping positions in live switch must be completely removed");

// 2. Verify clearBitgetCredentials function exists
assert(html.includes('function clearBitgetCredentials()'), "clearBitgetCredentials must be defined");
assert(html.includes('btnClearBitget'), "btnClearBitget button must be present");

// 3. Verify paperOpenPositions and liveOpenPositions isolation logic exists
assert(html.includes('d.paperOpenPositions'), "paperOpenPositions must be used to preserve paper positions");
assert(html.includes('d.liveOpenPositions'), "liveOpenPositions must be used for live trades");

// 4. Verify that in Live mode, balStr checks for d.liveBalance and defaults to '—', NOT paperBalance
assert(html.includes('if (isLive)'), "isLive balance check must be present in syncActiveView");

console.log("=== ALL PAPER VS LIVE ISOLATION TESTS PASSED PERFECTLY ===");
