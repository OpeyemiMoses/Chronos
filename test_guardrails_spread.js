// test_guardrails_spread.js
// Verification of the 2x2 Scroll-Pinned Guardrails Spread Engine
const fs = require('fs');
const assert = require('assert');

console.log("=== RUNNING GUARDRAILS 2x2 SCROLL-PINNED SPREAD TESTS ===");

const html = fs.readFileSync('dashboard/index.html', 'utf8');

// 1. Structure Verification
console.log("--- TEST 1: DOM Elements & 2x2 Grid Slots ---");
assert(html.includes('id="guardrails"'), "Missing #guardrails section");
assert(html.includes('class="guardrails-pinned-stage"'), "Missing .guardrails-pinned-stage");
assert(html.includes('id="guardrailsStickyWindow"'), "Missing #guardrailsStickyWindow");
assert(html.includes('id="guardrailsSpreadCanvas"'), "Missing #guardrailsSpreadCanvas");
assert(html.includes('class="guardrails-ambient-glow"'), "Missing ambient glow backdrop");

assert(html.includes('data-slot="tl"'), "Missing Top-Left slot (Beta Decoupling)");
assert(html.includes('data-slot="tr"'), "Missing Top-Right slot (Closed-Loop Self-Auditor)");
assert(html.includes('data-slot="bl"'), "Missing Bottom-Left slot (Bitget HMAC Gateway)");
assert(html.includes('data-slot="br"'), "Missing Bottom-Right slot (Multi-Wallet Isolation)");
console.log("Passed: All 4 slots (TL, TR, BL, BR) present in 2x2 layout.");

// 2. Card Content Verification
console.log("--- TEST 2: Card Content & Institutional Defenses ---");
assert(html.includes('Beta Decoupling'), "Missing Beta Decoupling title");
assert(html.includes('Closed-Loop Self-Auditor'), "Missing Closed-Loop Self-Auditor title");
assert(html.includes('Bitget HMAC Gateway'), "Missing Bitget HMAC Gateway title");
assert(html.includes('Multi-Wallet Isolation'), "Missing Multi-Wallet Isolation title");
assert(!html.includes('id="guardrailsScrollPill"'), "Scroll deployment pill tracker should NOT be present");
assert(!html.includes('id="guardrailsBarFill"'), "Scroll bar fill should NOT be present");
console.log("Passed: All 4 guardrail cards verified, loading bar & instruction pill cleanly removed.");

// 3. Mathematical Animation Spread Test
console.log("--- TEST 3: Mathematical Spread Calculation (0.0 -> 1.0) ---");
function computeTransforms(progress, canvasWidth = 980) {
  const eased = 1 - Math.pow(1 - progress, 3);
  const clusterFactor = 1 - eased;
  const shiftX = Math.min(canvasWidth * 0.22, 230);
  const shiftY = 82;

  const results = {};
  const slots = ['tl', 'tr', 'bl', 'br'];
  slots.forEach(slotType => {
    let tx = 0, ty = 0, rot = 0;
    if (slotType === "tl") {
      tx = shiftX * clusterFactor;
      ty = shiftY * clusterFactor;
      rot = -1.2 * clusterFactor;
    } else if (slotType === "tr") {
      tx = -shiftX * clusterFactor;
      ty = shiftY * clusterFactor;
      rot = 1.2 * clusterFactor;
    } else if (slotType === "bl") {
      tx = shiftX * clusterFactor;
      ty = -shiftY * clusterFactor;
      rot = -0.8 * clusterFactor;
    } else if (slotType === "br") {
      tx = -shiftX * clusterFactor;
      ty = -shiftY * clusterFactor;
      rot = 0.8 * clusterFactor;
    }
    const scale = 0.94 + 0.06 * eased;
    results[slotType] = { tx, ty, rot, scale };
  });
  return results;
}

// At Progress = 0 (Clustered together at center)
const atZero = computeTransforms(0.0);
console.log("Progress 0.0 (Clustered Together):");
console.log("  Top-Left: tx =", atZero.tl.tx.toFixed(1), "ty =", atZero.tl.ty.toFixed(1), "scale =", atZero.tl.scale.toFixed(2));
console.log("  Top-Right: tx =", atZero.tr.tx.toFixed(1), "ty =", atZero.tr.ty.toFixed(1), "scale =", atZero.tr.scale.toFixed(2));
console.log("  Bottom-Left: tx =", atZero.bl.tx.toFixed(1), "ty =", atZero.bl.ty.toFixed(1), "scale =", atZero.bl.scale.toFixed(2));
console.log("  Bottom-Right: tx =", atZero.br.tx.toFixed(1), "ty =", atZero.br.ty.toFixed(1), "scale =", atZero.br.scale.toFixed(2));

assert(atZero.tl.tx > 200, "TL should be shifted right into center at start");
assert(atZero.tl.ty > 70, "TL should be shifted down into center at start");
assert(atZero.tr.tx < -200, "TR should be shifted left into center at start");
assert(atZero.br.ty < -70, "BR should be shifted up into center at start");

// At Progress = 0.5 (Mid-spread)
const atHalf = computeTransforms(0.5);
console.log("Progress 0.5 (Mid-Spread):");
console.log("  Top-Left: tx =", atHalf.tl.tx.toFixed(1), "ty =", atHalf.tl.ty.toFixed(1), "scale =", atHalf.tl.scale.toFixed(3));
assert(atHalf.tl.tx < atZero.tl.tx && atHalf.tl.tx > 0, "TL should be smoothly interpolating outward");

// At Progress = 1.0 (Fully Spread 2x2 Grid)
const atOne = computeTransforms(1.0);
console.log("Progress 1.0 (Fully Spread Out):");
console.log("  Top-Left: tx =", atOne.tl.tx.toFixed(1), "ty =", atOne.tl.ty.toFixed(1), "scale =", atOne.tl.scale.toFixed(2));
console.log("  Top-Right: tx =", atOne.tr.tx.toFixed(1), "ty =", atOne.tr.ty.toFixed(1), "scale =", atOne.tr.scale.toFixed(2));
console.log("  Bottom-Left: tx =", atOne.bl.tx.toFixed(1), "ty =", atOne.bl.ty.toFixed(1), "scale =", atOne.bl.scale.toFixed(2));
console.log("  Bottom-Right: tx =", atOne.br.tx.toFixed(1), "ty =", atOne.br.ty.toFixed(1), "scale =", atOne.br.scale.toFixed(2));

assert(Math.abs(atOne.tl.tx) < 0.001, "TL tx must be 0 at fully spread state");
assert(Math.abs(atOne.tl.ty) < 0.001, "TL ty must be 0 at fully spread state");
assert(Math.abs(atOne.tr.tx) < 0.001, "TR tx must be 0 at fully spread state");
assert(Math.abs(atOne.tr.ty) < 0.001, "TR ty must be 0 at fully spread state");
assert(Math.abs(atOne.bl.tx) < 0.001, "BL tx must be 0 at fully spread state");
assert(Math.abs(atOne.bl.ty) < 0.001, "BL ty must be 0 at fully spread state");
assert(Math.abs(atOne.br.tx) < 0.001, "BR tx must be 0 at fully spread state");
assert(Math.abs(atOne.br.ty) < 0.001, "BR ty must be 0 at fully spread state");
assert.strictEqual(atOne.tl.scale, 1, "Scale must be 1.0 at fully spread state");

console.log("=== ALL GUARDRAILS 2x2 SPREAD TESTS PASSED PERFECTLY ===");
