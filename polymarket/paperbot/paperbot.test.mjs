// Offline tests: Polymarket is replaced by canned responses shaped like the real gamma/clob replies.
//   node --test polymarket/paperbot/
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { DEFAULTS, feeFor, getJson, parseGameStart, readLedger, report, scan, settle, simulateBuy } from './paperbot.mjs';

const NOW = Date.parse('2026-10-20T18:00:00Z');
const gameAt = (mins) => new Date(NOW + mins * 60000).toISOString().replace('T', ' ').replace(/\.\d+Z$/, '+00');
const market = (id, slug, prices, mins, extra = {}) => ({
  id, slug, question: `Q ${slug}`, outcomes: '["Yes", "No"]', outcomePrices: JSON.stringify(prices.map(String)),
  clobTokenIds: JSON.stringify([`${id}-yes`, `${id}-no`]), gameStartTime: gameAt(mins), closed: false,
  sportsMarketType: 'moneyline', feesEnabled: true, feeSchedule: { exponent: 1, rate: 0.05, takerOnly: true }, ...extra,
});
const BOOKS = {
  // in band, tight, deep: should be bought
  '1-yes': { bids: [{ price: '0.93', size: '5000' }], asks: [{ price: '0.95', size: '3' }, { price: '0.94', size: '5000' }] },
  // spread too wide
  '2-no': { bids: [{ price: '0.90', size: '100' }], asks: [{ price: '0.93', size: '100' }] },
  // too thin for $10
  '3-yes': { bids: [{ price: '0.94', size: '100' }], asks: [{ price: '0.95', size: '2' }] },
};
const MARKETS = [
  market('1', 'nba-a-b', [0.935, 0.065], 30),
  market('2', 'nfl-c-d', [0.08, 0.92], 45),
  market('3', 'mlb-e-f', [0.945, 0.055], 20),
  market('4', 'nhl-g-h', [0.95, 0.05], 300), // starts too late
  market('5', 'nba-spread-x', [0.95, 0.05], 30), // a spread market slug
  market('6', 'tennis-i-j', [0.60, 0.40], 30), // not a deep favourite
  market('7', 'usl1-k-l-2026-08-01-k', [0.95, 0.05], 30), // stale listing: slug date months before the game time
];
let settledPrices = null;
let calls = [];
globalThis.fetch = async (u, init) => {
  const url = new URL(u); calls.push({ url: url.href, method: init?.method });
  let body;
  if (url.hostname === 'gamma-api.polymarket.com' && url.pathname === '/markets') body = MARKETS;
  else if (url.hostname === 'gamma-api.polymarket.com' && url.pathname.startsWith('/markets/'))
    body = { ...MARKETS.find((m) => m.id === url.pathname.split('/')[2]), ...(settledPrices || {}) };
  else if (url.hostname === 'clob.polymarket.com' && url.pathname === '/book') body = BOOKS[url.searchParams.get('token_id')] || { bids: [], asks: [] };
  else return { ok: false, status: 404 };
  return { ok: true, status: 200, json: async () => body };
};

const tmp = () => ({ ...DEFAULTS, data: fs.mkdtempSync(path.join(os.tmpdir(), 'paperbot-')) });
const quiet = () => {};

test('parses gamma game times', () => {
  assert.equal(parseGameStart('2026-10-20 19:00:00+00'), Date.parse('2026-10-20T19:00:00Z'));
  assert.equal(parseGameStart(null), null);
});

test('fee follows the docs formula, rounded to 5 dp', () => {
  assert.equal(feeFor(100, 0.95, 0.05), 0.2375);
});

test('book walk fills cheapest first and refuses thin books', () => {
  const f = simulateBuy([{ price: '0.95', size: '100' }, { price: '0.94', size: '5' }], 10, 0.99);
  assert.ok(Math.abs(f.cost - 10) < 1e-3);
  assert.ok(f.avgPrice > 0.94 && f.avgPrice < 0.95);
  assert.equal(simulateBuy([{ price: '0.95', size: '2' }], 10, 0.99), null);
  assert.equal(simulateBuy([{ price: '0.995', size: '1000' }], 10, 0.99), null);
});

test('only GETs the two allowed Polymarket hosts', async () => {
  await assert.rejects(getJson('https://example.com/x'), /blocked host/);
  await assert.rejects(getJson('http://gamma-api.polymarket.com/markets'), /blocked host/);
});

test('scan -> settle -> report', async () => {
  const o = tmp(); calls = [];
  const r = await scan(o, NOW, quiet);
  assert.deepEqual(r.entries.map((e) => e.market_id), ['1']);
  assert.equal(r.markets, 4); // late start, spread slug and stale listing filtered out
  assert.ok(calls.every((c) => c.method === 'GET'));
  const [row] = readLedger(o);
  assert.equal(row.outcome, 'Yes'); assert.equal(row.best_ask, '0.94'); assert.equal(row.status, 'open');
  assert.ok(Math.abs(Number(row.cost) - 10) < 1e-3);

  // a second scan never buys the same market twice
  assert.equal((await scan(o, NOW, quiet)).entries.length, 0);

  // not settled while the market is open
  assert.equal(await settle(o, NOW, quiet), 0);
  settledPrices = { closed: true, outcomePrices: '["1", "0"]' };
  assert.equal(await settle(o, NOW + 3 * 3600e3, quiet), 1);
  const [done] = readLedger(o);
  assert.equal(done.status, 'won');
  assert.ok(Math.abs(Number(done.pnl) - (Number(done.shares) - Number(done.cost) - Number(done.fee))) < 1e-3);
  const rep = report(o, quiet);
  assert.equal(rep.settled, 1); assert.equal(rep.wins, 1); assert.ok(rep.pnl > 0);
  settledPrices = null;
});

test('dry scan records nothing', async () => {
  const o = { ...tmp(), dry: true };
  const r = await scan(o, NOW, quiet);
  assert.equal(r.entries.length, 1);
  assert.equal(readLedger(o).length, 0);
});
