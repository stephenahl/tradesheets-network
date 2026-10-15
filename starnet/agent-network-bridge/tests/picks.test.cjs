'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { readPicks, _internals } = require('../lib/picks.cjs');

const board = {
  researched_at: '2026-10-15T19:30Z',
  legs: [
    { id: 'a-ml', label: 'A wins', market_slug: 'g1', outcome: 'A', prob: 0.60, ask_at_research: 0.55, bid_at_research: 0.54, liquidity_at_research: 9000, starts_utc: '2030-01-01T00:00:00Z' },
    { id: 'a-sp', label: 'A -2.5', market_slug: 'g1-sp', outcome: 'A', prob: 0.52, ask_at_research: 0.48, bid_at_research: 0.47, liquidity_at_research: 9000, starts_utc: '2030-01-01T00:00:00Z' },
    { id: 'x', label: 'X wins', market_slug: 'g2', outcome: 'X', prob: 0.40, ask_at_research: 0.30, bid_at_research: 0.20, liquidity_at_research: 9000, starts_utc: '2030-01-01T00:00:00Z' },
    { id: 'old', label: 'Started', market_slug: 'g3', outcome: 'Y', prob: 0.9, ask_at_research: 0.5, bid_at_research: 0.49, liquidity_at_research: 9000, starts_utc: '2020-01-01T00:00:00Z' },
  ],
  lifts: { 'a-ml|a-sp': 1.6 },
};

test('flags value, wide spreads and started games; correlation is priced, not counted as edge', async () => {
  const r = await readPicks({ board, now: Date.parse('2026-10-15T20:00:00Z') });
  const by = Object.fromEntries(r.legs.map((l) => [l.id, l]));
  assert.equal(by['a-ml'].value, true);
  assert.equal(by.x.value, false); assert.equal(by.x.flag, 'wide spread');
  assert.equal(by.old.value, false); assert.equal(by.old.flag, 'started');
  assert.equal(r.combos.length, 1);
  const c = r.combos[0];
  // EV must equal what the two legs' own edges give (0.60/0.55 * 0.52/0.48 / haircut), not the lift's 1.6x.
  const expected = (0.60 / 0.55) * (0.52 / 0.48) / 1.04 - 1;
  assert.ok(Math.abs(c.ev - expected) < 0.01, `ev ${c.ev} vs ${expected}`);
});

test('outcome index 1 mirrors the quote, closed markets return null', () => {
  const m = { outcomes: '["A","B"]', bestBid: 0.58, bestAsk: 0.60, liquidityNum: 1000 };
  assert.deepEqual(_internals.priceFromMarket(m, 'B'), { ask: 0.42, bid: 0.4, liquidity: 1000, live: false, score: null });
  assert.equal(_internals.priceFromMarket({ ...m, closed: true }, 'A'), null);
});

test('live mode uses fetched prices and falls back to research prices on errors', async () => {
  const fetchImpl = async (url) => url.includes('g1-sp') ? { ok: false, status: 403 }
    : { ok: true, json: async () => [{ outcomes: '["A","B"]', bestBid: 0.49, bestAsk: 0.50, liquidityNum: 5000 }] };
  const r = await readPicks({ board, live: true, fetchImpl, now: Date.parse('2026-10-15T20:00:00Z') });
  const by = Object.fromEntries(r.legs.map((l) => [l.id, l]));
  assert.equal(by['a-ml'].ask, 0.5); assert.equal(by['a-ml'].price_source, 'live');
  assert.equal(by['a-sp'].ask, 0.48); assert.equal(by['a-sp'].price_source, 'research');
  assert.ok(r.errors.some((e) => e.startsWith('a-sp')));
});

test('reads the newest board from a clone, and says so when there is none', async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'picks-'));
  assert.equal((await readPicks({ root })).available, false);
  const dir = path.join(root, 'polymarket', 'scanner', 'boards'); fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, '2026-10-14.json'), JSON.stringify({ legs: [] }));
  fs.writeFileSync(path.join(dir, '2026-10-15.json'), JSON.stringify(board));
  const r = await readPicks({ root, now: 0 });
  assert.equal(r.board, '2026-10-15.json'); assert.equal(r.legs.length, 4);
});
