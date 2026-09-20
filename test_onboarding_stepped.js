// test_onboarding_stepped.js
const fs = require('fs');
const assert = require('assert');

console.log("=== RUNNING ONBOARDING STEPPED LAYOUT TESTS ===");

const html = fs.readFileSync('dashboard/index.html', 'utf8');

// 1. Structure Verification
assert(html.includes('class="onboarding-stepped-stage"'), "Missing .onboarding-stepped-stage");
assert(html.includes('class="onboarding-card-wrap step-left"'), "Missing .step-left card wrap");
assert(html.includes('class="onboarding-card-wrap step-center"'), "Missing .step-center card wrap");
assert(html.includes('class="onboarding-card-wrap step-right"'), "Missing .step-right card wrap");

// 2. Center Prominence
assert(html.includes('onboarding-card-prominent'), "Missing .onboarding-card-prominent on center card");

// 3. Card Content & Stagger Indices
assert(html.includes('Launch Trading Vault'), "Missing Step 1 title");
assert(html.includes('Monitor Weekend Drift'), "Missing Step 2 title");
assert(html.includes('Connect Bitget UTA v3'), "Missing Step 3 title");

assert(html.includes('data-stagger-index="0"'), "Missing stagger index 0");
assert(html.includes('data-stagger-index="1"'), "Missing stagger index 1");
assert(html.includes('data-stagger-index="2"'), "Missing stagger index 2");

console.log("=== ALL ONBOARDING STEPPED TESTS PASSED PERFECTLY ===");
