// Offline tests for the Polymarket US module. Canned replies follow the shapes in docs.polymarket.us.
//   node --test polymarket/paperbot/*.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { DEFAULTS, loadCredentials, parseArgs, report, riskCheck, scan, settle, sideBooks, signHeaders, usFee } from './us.mjs';
import { readLedger } from './paperbot.mjs';

const NOW = Date.parse('2026-10-21T23:00:00Z');
const at = (mins) => new Date(NOW + mins * 60000).toISOString();
const px = (v) => ({ value: String(v), currency: 'USD' });
const sides = (a, b) => [{ long: true, description: a, team: { name: a }, price: '0.5' }, { long: false, description: b, team: { name: b }, price: '0.5' }];
const mkt = (slug, mins, extra = {}) => ({ slug, question: `${slug}?`, marketType: 'moneyline', status: 'MARKET_STATUS_OPEN',
  gameStartTime: at(mins), marketSides: sides('Home', 'Away'), feeCoefficient: 0.0695, orderPriceMinTickSize: 0.01, minimumTradeQty: 1, ...extra });
const MARKETS = [
  mkt('aec-nba-fav-long', 30), // long side 0.95 ask
  mkt('aec-nba-fav-short', 40), // YES bid 0.04 -> NO ask 0.96
  mkt('aec-nba-coinflip', 30),
  mkt('aec-nba-late', 400),
  mkt('aec-nba-spread-x', 30),
];
const BOOKS = {
  'aec-nba-fav-long': { bids: [{ px: px(0.94), qty: '5000' }], offers: [{ px: px(0.95), qty: '5000' }] },
  'aec-nba-fav-short': { bids: [{ px: px(0.04), qty: '5000' }], offers: [{ px: px(0.05), qty: '5000' }] },
  'aec-nba-coinflip': { bids: [{ px: px(0.49), qty: '5000' }], offers: [{ px: px(0.51), qty: '5000' }] },
};
let resolved = {}; let calls = []; let balance = 100; let orders = [];
globalThis.fetch = async (u, init = {}) => {
  const url = new URL(u); const method = init.method || 'GET'; calls.push({ host: url.hostname, method, path: url.pathname, headers: init.headers });
  const ok = (body) => ({ ok: true, status: 200, text: async () => JSON.stringify(body) });
  if (url.hostname === 'gateway.polymarket.us') {
    if (url.pathname === '/v1/markets' && url.searchParams.get('slug')) {
      const s = url.searchParams.get('slug'); const m = MARKETS.find((x) => x.slug === s);
      return ok({ markets: [resolved[s] ? { ...m, status: 'MARKET_STATUS_RESOLVED', marketSides: resolved[s] } : m] });
    }
    if (url.pathname === '/v1/markets') return ok({ markets: Number(url.searchParams.get('offset')) ? [] : MARKETS });
    const m = url.pathname.match(/^\/v1\/markets\/(.+)\/book$/);
    if (m) return ok({ marketData: BOOKS[decodeURIComponent(m[1])] || { bids: [], offers: [] } });
  }
  if (url.hostname === 'api.polymarket.us') {
    if (url.pathname === '/v1/account/balances') return ok({ balances: [{ currency: 'USD', buyingPower: balance }] });
    if (url.pathname === '/v1/orders' && method === 'POST') {
      const b = JSON.parse(init.body); orders.push(b);
      return ok({ id: `o${orders.length}`, executions: [{ order: { state: 'ORDER_STATE_FILLED', cumQuantity: b.quantity,
        avgPx: px(b.price.value), commissionNotionalTotalCollected: px(0.02) } }] });
    }
  }
  return { ok: false, status: 404, text: async () => 'not found' };
};

const { privateKey, publicKey } = crypto.generateKeyPairSync('ed25519');
const seed = privateKey.export({ format: 'der', type: 'pkcs8' }).subarray(-32);
const CREDS = { keyId: 'kid', secretKey: Buffer.concat([seed, Buffer.alloc(32)]).toString('base64') };
const tmp = (extra = {}) => ({ ...DEFAULTS, data: fs.mkdtempSync(path.join(os.tmpdir(), 'pmus-')), ...extra });
const quiet = () => {};
const reset = () => { resolved = {}; calls = []; balance = 100; orders = []; };

test('signature verifies with the matching public key', () => {
  const h = signHeaders(CREDS, 'POST', '/v1/orders', 1700000000000);
  assert.equal(h['X-PM-Access-Key'], 'kid'); assert.equal(h['X-PM-Timestamp'], '1700000000000');
  assert.ok(crypto.verify(null, Buffer.from('1700000000000POST/v1/orders'), publicKey, Buffer.from(h['X-PM-Signature'], 'base64')));
});

test('short side is priced from the YES bids', () => {
  const b = sideBooks(BOOKS['aec-nba-fav-short']);
  assert.ok(Math.abs(b.short.ask - 0.96) < 1e-9); assert.ok(Math.abs(b.long.ask - 0.05) < 1e-9); assert.ok(Math.abs(b.spread - 0.01) < 1e-9);
});

test('US fee formula, rounded to cents', () => { assert.equal(usFee(100, 0.95, 0.0695), 0.33); });

test('live needs all three limits', () => {
  assert.throws(() => parseArgs(['run', '--live', '--max-trade', '5']), /needs/);
  assert.throws(() => parseArgs(['run', '--live', '--max-trade', '60', '--daily-loss', '15', '--bankroll', '50']), /exceed/);
  assert.equal(parseArgs(['run', '--live', '--max-trade', '5', '--daily-loss', '15', '--bankroll', '50']).o.live, true);
});

test('credentials file must be private', () => {
  const d = fs.mkdtempSync(path.join(os.tmpdir(), 'cred-')); const f = path.join(d, 'c.json');
  fs.writeFileSync(f, JSON.stringify(CREDS)); fs.chmodSync(f, 0o644);
  if (process.platform !== 'win32') assert.throws(() => loadCredentials(f), /chmod 600/);
  fs.chmodSync(f, 0o600); assert.equal(loadCredentials(f).keyId, 'kid');
  assert.equal(loadCredentials(path.join(d, 'missing.json')), null);
});

test('paper scan buys both favourites, never calls the trading API', async () => {
  reset(); const o = tmp();
  const r = await scan(o, NOW, quiet);
  assert.deepEqual(r.entries.map((e) => [e.slug, e.side]), [['aec-nba-fav-long', 'long'], ['aec-nba-fav-short', 'short']]);
  assert.equal(r.markets, 3);
  assert.ok(calls.every((c) => c.host === 'gateway.polymarket.us' && c.method === 'GET'));
  resolved['aec-nba-fav-long'] = [{ long: true, price: '1' }, { long: false, price: '0' }];
  resolved['aec-nba-fav-short'] = [{ long: true, price: '1' }, { long: false, price: '0' }];
  assert.equal(await settle(o, NOW + 4 * 3600e3, quiet), 2);
  const rows = readLedger(o, 'us-ledger.csv');
  assert.deepEqual(rows.map((x) => x.status), ['won', 'lost']);
  const rep = report(o, quiet); assert.equal(rep.paper.settled, 2); assert.equal(rep.live, undefined);
});

test('live scan places capped, automated IOC orders and respects limits', async () => {
  reset(); const o = tmp(parseArgs(['scan', '--live', '--max-trade', '5', '--daily-loss', '15', '--bankroll', '8']).o);
  o.data = tmp().data;
  const r = await scan(o, NOW, quiet, CREDS);
  // $5 max per trade: the first fills; the second would take the bankroll past $8, so it is blocked
  assert.equal(orders.length, 1);
  const [ord] = orders;
  assert.equal(ord.intent, 'ORDER_INTENT_BUY_LONG'); assert.equal(ord.tif, 'TIME_IN_FORCE_IMMEDIATE_OR_CANCEL');
  assert.equal(ord.manualOrderIndicator, 'MANUAL_ORDER_INDICATOR_AUTOMATIC'); assert.equal(ord.quantity, 5);
  assert.ok(Number(ord.price.value) * ord.quantity <= 5);
  assert.ok(r.skipped.some((s) => /bankroll limit/.test(s)));
  const order = calls.find((c) => c.path === '/v1/orders');
  assert.ok(order.headers['X-PM-Signature'] && order.headers['X-PM-Access-Key'] === 'kid');
  const [row] = readLedger(o, 'us-ledger.csv'); assert.equal(row.mode, 'live'); assert.equal(row.order_state, 'ORDER_STATE_FILLED');
});

test('short-side live order sends the YES price', async () => {
  reset(); const o = { ...tmp(), live: true, maxTrade: 5, dailyLoss: 15, bankroll: 50 };
  await scan(o, NOW, quiet, CREDS);
  const short = orders.find((x) => x.intent === 'ORDER_INTENT_BUY_SHORT');
  assert.ok(short); assert.equal(short.price.value, '0.0300'); // NO limit 0.97 -> YES 0.03
  const row = readLedger(o, 'us-ledger.csv').find((x) => x.side === 'short');
  assert.ok(Number(row.avg_price) > 0.9);
});

test('STOP file, daily loss and low balance block live orders', async () => {
  reset(); const o = { ...tmp(), live: true, maxTrade: 5, dailyLoss: 15, bankroll: 50 };
  fs.mkdirSync(o.data, { recursive: true }); fs.writeFileSync(path.join(o.data, 'STOP'), '');
  let r = await scan(o, NOW, quiet, CREDS); assert.equal(orders.length, 0); assert.ok(r.skipped.every((s) => /STOP|no side/.test(s)));
  fs.rmSync(path.join(o.data, 'STOP'));
  assert.match(riskCheck([{ mode: 'live', status: 'lost', settled_at: new Date(NOW).toISOString(), pnl: '-15', cost: '5' }], o, 5, NOW), /daily loss/);
  balance = 1; r = await scan(o, NOW, quiet, CREDS); assert.equal(orders.length, 0); assert.ok(r.skipped.some((s) => /buying power/.test(s)));
});
