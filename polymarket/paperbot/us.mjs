#!/usr/bin/env node
// PaperBot for Polymarket US (the venue Stephen can use). Same strategy H2 as paperbot.mjs:
// buy a sports favourite priced 90-99c shortly before the game starts, hold to settlement.
//
// Paper by default. Live orders only when ALL of these hold (Stephen's decision, 2026-10-21):
//   - run with --live plus all three limits: --max-trade <$>, --daily-loss <$>, --bankroll <$>
//   - Stephen's own API key file exists (~/.polymarket-us/credentials.json, which he creates;
//     Claude never opens it). Override the location with PM_US_CREDENTIALS.
//   - no STOP file in the data folder (touch data/STOP to halt new live orders at once)
//   - the account balance can be read and covers the order
//
//   node polymarket/paperbot/us.mjs scan|settle|report|run            # paper
//   node polymarket/paperbot/us.mjs run --live --max-trade 5 --daily-loss 15 --bankroll 50
//   options: --stake 10 (paper size)  --min-price 0.90  --max-price 0.99  --max-spread 0.015
//            --window-min 15  --window-max 60  --every 5  --data <dir>  --dry
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readLedger, simulateBuy, writeLedger } from './paperbot.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const GATEWAY = 'https://gateway.polymarket.us'; // public market data
const API = 'https://api.polymarket.us'; // signed: balances and orders
const ALLOWED = { 'gateway.polymarket.us': ['GET'], 'api.polymarket.us': ['GET', 'POST'] };
const LEDGER = 'us-ledger.csv';
const EXCLUDE = ['-spread-', '-over-', '-under-', '-total-', '-handicap-', '-pt5'];
const DEFAULT_FEE = 0.0695; // Polymarket US taker coefficient (docs.polymarket.us/fees), used if a market lacks feeCoefficient

export const DEFAULTS = {
  stake: 10, minPrice: 0.90, maxPrice: 0.99, maxSpread: 0.015, windowMin: 15, windowMax: 60, every: 5,
  data: path.join(HERE, 'data'), dry: false, live: false, maxTrade: null, dailyLoss: null, bankroll: null,
  credentials: process.env.PM_US_CREDENTIALS || path.join(os.homedir(), '.polymarket-us', 'credentials.json'),
};

const COLUMNS = ['entered_at', 'mode', 'slug', 'question', 'side', 'team', 'game_start', 'minutes_to_start',
  'best_bid', 'best_ask', 'spread', 'shares', 'avg_price', 'cost', 'fee', 'order_id', 'order_state',
  'status', 'settled_at', 'payout', 'pnl'];

// ---------- network ----------
async function request(url, { method = 'GET', body, headers = {} } = {}) {
  const u = new URL(url);
  if (u.protocol !== 'https:' || !(ALLOWED[u.hostname] || []).includes(method)) throw new Error(`blocked: ${method} ${u.hostname}`);
  const res = await fetch(u, { method, headers: { accept: 'application/json', ...(body ? { 'content-type': 'application/json' } : {}), ...headers },
    body: body ? JSON.stringify(body) : undefined, signal: AbortSignal.timeout(20000) });
  const text = await res.text();
  if (!res.ok) throw new Error(`${method} ${u.hostname}${u.pathname} -> HTTP ${res.status} ${text.slice(0, 200)}`);
  return text ? JSON.parse(text) : {};
}
export const gateway = (p) => request(`${GATEWAY}${p}`);

// Ed25519 over `${timestampMs}${METHOD}${path}`; the secret is base64 and its first 32 bytes are the seed.
export function signHeaders(creds, method, pathOnly, now = Date.now()) {
  const seed = Buffer.from(creds.secretKey, 'base64').subarray(0, 32);
  if (seed.length !== 32) throw new Error('secret key is not a base64 Ed25519 key');
  const key = crypto.createPrivateKey({ key: Buffer.concat([Buffer.from('302e020100300506032b657004220420', 'hex'), seed]), format: 'der', type: 'pkcs8' });
  const ts = String(now);
  return { 'X-PM-Access-Key': creds.keyId, 'X-PM-Timestamp': ts,
    'X-PM-Signature': crypto.sign(null, Buffer.from(`${ts}${method}${pathOnly}`), key).toString('base64') };
}
const signed = (creds, method, p, body) => request(`${API}${p}`, { method, body, headers: signHeaders(creds, method, p) });

export function loadCredentials(file) {
  if (!fs.existsSync(file)) return null;
  const st = fs.statSync(file);
  if (process.platform !== 'win32' && (st.mode & 0o077)) throw new Error(`${file} is readable by other users; run: chmod 600 "${file}"`);
  const c = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!c.keyId || !c.secretKey) throw new Error(`${file} needs "keyId" and "secretKey"`);
  return c;
}

// ---------- market helpers ----------
const num = (a) => (a == null ? null : Number(typeof a === 'object' ? a.value : a));
const isMoneyline = (m) => m.marketType === 'moneyline' || m.sportsMarketType === 'moneyline' || m.sportsMarketTypeV2 === 'SPORTS_MARKET_TYPE_MONEYLINE';
export const usFee = (shares, p, coef) => Math.round(shares * coef * p * (1 - p) * 100) / 100;

// The book is quoted for the long (YES) side. Buying the short side means taking the YES bids at 1 - price.
export function sideBooks(book) {
  const bids = (book.bids || []).map((b) => ({ price: num(b.px), size: Number(b.qty) })).filter((b) => b.price > 0 && b.size > 0);
  const offers = (book.offers || []).map((b) => ({ price: num(b.px), size: Number(b.qty) })).filter((b) => b.price > 0 && b.size > 0);
  const bid = bids.length ? Math.max(...bids.map((b) => b.price)) : null;
  const ask = offers.length ? Math.min(...offers.map((b) => b.price)) : null;
  return {
    spread: bid != null && ask != null ? ask - bid : null,
    long: { bid, ask, asks: offers },
    short: { bid: ask == null ? null : 1 - ask, ask: bid == null ? null : 1 - bid, asks: bids.map((b) => ({ price: 1 - b.price, size: b.size })) },
  };
}

async function upcoming(now, o) {
  const out = [];
  // page until an empty page: the server may return fewer than `limit` per page
  for (let offset = 0, pages = 0; pages < 200; pages++) {
    const page = (await gateway(`/v1/markets?active=true&closed=false&marketTypes=moneyline&limit=100&offset=${offset}`)).markets || [];
    if (!page.length) break;
    out.push(...page); offset += page.length;
  }
  return out.filter((m) => {
    const start = Date.parse(m.gameStartTime || '');
    const mins = (start - now) / 60000;
    return Number.isFinite(start) && isMoneyline(m) && mins >= o.windowMin && mins <= o.windowMax
      && (!m.status || m.status === 'MARKET_STATUS_OPEN') && (m.marketSides || []).length === 2
      && !EXCLUDE.some((x) => String(m.slug || '').includes(x));
  });
}

// ---------- live risk checks ----------
const utcDay = (t) => new Date(t).toISOString().slice(0, 10);
export function riskCheck(rows, o, cost, now = Date.now()) {
  if (fs.existsSync(path.join(o.data, 'STOP'))) return 'STOP file present';
  const live = rows.filter((r) => r.mode === 'live');
  const today = live.filter((r) => r.settled_at && utcDay(r.settled_at) === utcDay(now)).reduce((s, r) => s + Number(r.pnl || 0), 0);
  if (today <= -o.dailyLoss) return `daily loss limit hit ($${(-today).toFixed(2)} lost today)`;
  const openCost = live.filter((r) => r.status === 'open').reduce((s, r) => s + Number(r.cost || 0), 0);
  const realised = live.filter((r) => r.status !== 'open').reduce((s, r) => s + Number(r.pnl || 0), 0);
  const used = openCost + Math.max(0, -realised);
  if (used + cost > o.bankroll + 1e-9) return `bankroll limit: $${used.toFixed(2)} in use or lost of $${o.bankroll}`;
  return null;
}

async function buyingPower(creds) {
  const r = await signed(creds, 'GET', '/v1/account/balances');
  const usd = (r.balances || []).find((b) => !b.currency || b.currency === 'USD');
  const bp = num(usd?.buyingPower);
  if (!Number.isFinite(bp)) throw new Error('could not read buying power');
  return bp;
}

async function placeOrder(creds, m, sideName, limitPrice, shares) {
  const yesPrice = sideName === 'long' ? limitPrice : 1 - limitPrice; // the API always takes the YES-side price
  const tick = Number(m.orderPriceMinTickSize) || 0.01;
  const body = {
    marketSlug: m.slug, type: 'ORDER_TYPE_LIMIT', tif: 'TIME_IN_FORCE_IMMEDIATE_OR_CANCEL',
    price: { value: (Math.round(yesPrice / tick) * tick).toFixed(4), currency: 'USD' }, quantity: shares,
    intent: sideName === 'long' ? 'ORDER_INTENT_BUY_LONG' : 'ORDER_INTENT_BUY_SHORT',
    manualOrderIndicator: 'MANUAL_ORDER_INDICATOR_AUTOMATIC', synchronousExecution: true, maxBlockTime: '10',
  };
  const r = await signed(creds, 'POST', '/v1/orders', body);
  const last = (r.executions || []).map((e) => e.order).filter(Boolean).pop() || {};
  let avg = num(last.avgPx);
  if (avg != null && sideName === 'short' && avg < 0.5) avg = 1 - avg; // reported on the YES side
  return { id: r.id || last.id || '', state: last.state || 'unknown', filled: Number(last.cumQuantity || 0), avg,
    fee: num(last.commissionNotionalTotalCollected) };
}

// ---------- scan ----------
export async function scan(o, now = Date.now(), log = console.log, creds = null) {
  const rows = readLedger(o, LEDGER); const held = new Set(rows.map((r) => r.slug));
  const markets = await upcoming(now, o); const entries = []; const skipped = [];
  for (const m of markets) {
    if (held.has(m.slug)) continue;
    let book;
    try { book = (await gateway(`/v1/markets/${encodeURIComponent(m.slug)}/book`)).marketData || {}; } catch (e) { skipped.push(`${m.slug}: ${e.message}`); continue; }
    const b = sideBooks(book);
    const pick = ['long', 'short'].find((s) => b[s].ask != null && b[s].ask >= o.minPrice && b[s].ask < o.maxPrice);
    if (!pick) { skipped.push(`${m.slug}: no side priced ${o.minPrice}-${o.maxPrice}`); continue; }
    if (b.spread == null || b.spread > o.maxSpread + 1e-9) { skipped.push(`${m.slug}: spread ${b.spread?.toFixed(3)} > ${o.maxSpread}`); continue; }
    const s = b[pick]; const limit = Math.min(s.ask + 0.01, o.maxPrice - 0.001);
    const stake = o.live ? o.maxTrade : o.stake;
    const fill = simulateBuy(s.asks, stake, limit);
    if (!fill) { skipped.push(`${m.slug}: under $${stake} within 1c of the ask`); continue; }
    const team = (m.marketSides || []).find((x) => x.long === (pick === 'long'));
    const coef = Number(m.feeCoefficient ?? DEFAULT_FEE);
    const row = {
      entered_at: new Date(now).toISOString(), mode: 'paper', slug: m.slug, question: m.question, side: pick,
      team: team?.team?.name || team?.description || pick, game_start: new Date(Date.parse(m.gameStartTime)).toISOString(),
      minutes_to_start: Math.round((Date.parse(m.gameStartTime) - now) / 60000), best_bid: s.bid?.toFixed(3), best_ask: s.ask.toFixed(3),
      spread: b.spread.toFixed(3), shares: fill.shares, avg_price: fill.avgPrice.toFixed(4), cost: fill.cost.toFixed(2),
      fee: usFee(fill.shares, fill.avgPrice, coef).toFixed(2), order_id: '', order_state: '', status: 'open', settled_at: '', payout: '', pnl: '',
    };
    if (o.live && !o.dry) {
      const step = Number(m.minimumTradeQty) || 1;
      const shares = Math.floor(o.maxTrade / limit / step) * step;
      const cost = shares * limit;
      const block = shares <= 0 ? 'max trade too small for one contract' : riskCheck([...rows, ...entries], o, cost, now);
      if (block) { skipped.push(`${m.slug}: LIVE blocked: ${block}`); continue; }
      let bp;
      try { bp = await buyingPower(creds); } catch (e) { skipped.push(`${m.slug}: LIVE blocked: balance check failed (${e.message})`); continue; }
      if (bp < cost) { skipped.push(`${m.slug}: LIVE blocked: buying power $${bp.toFixed(2)} < $${cost.toFixed(2)}`); continue; }
      let r;
      try { r = await placeOrder(creds, m, pick, limit, Number(shares.toFixed(4))); } catch (e) { skipped.push(`${m.slug}: LIVE order failed: ${e.message}`); continue; }
      Object.assign(row, { mode: 'live', order_id: r.id, order_state: r.state, shares: r.filled });
      if (!(r.filled > 0)) { Object.assign(row, { status: 'unfilled', cost: '0.00', fee: '0.00', avg_price: '', pnl: '0' }); }
      else {
        const avg = r.avg ?? limit;
        Object.assign(row, { avg_price: avg.toFixed(4), cost: (r.filled * avg).toFixed(2),
          fee: (r.fee ?? usFee(r.filled, avg, coef)).toFixed(2) });
      }
    }
    entries.push(row);
    log(`${row.mode === 'live' ? 'LIVE BUY ' : 'PAPER BUY'}  ${row.team} @ ${row.avg_price || '-'}  ${row.shares} sh  $${row.cost}  fee $${row.fee}`
      + `  ${m.question}  (starts in ${row.minutes_to_start} min)${row.order_state ? `  [${row.order_state}]` : ''}`);
  }
  if (entries.length && !o.dry) writeLedger(o, [...rows, ...entries], LEDGER, COLUMNS);
  log(`scan: ${markets.length} US moneyline games start in ${o.windowMin}-${o.windowMax} min; ${entries.length} buy(s)`
    + `${o.dry ? ' (dry run, not recorded)' : ''}; ${skipped.length} skipped`);
  for (const s of skipped) log(`  skip ${s}`);
  return { markets: markets.length, entries, skipped };
}

// ---------- settle / report ----------
export async function settle(o, now = Date.now(), log = console.log) {
  const rows = readLedger(o, LEDGER); let n = 0;
  for (const r of rows) {
    if (r.status !== 'open') continue;
    let m;
    try { m = ((await gateway(`/v1/markets?slug=${encodeURIComponent(r.slug)}`)).markets || [])[0]; } catch (e) { log(`  ${r.slug}: ${e.message}`); continue; }
    if (!m || m.status !== 'MARKET_STATUS_RESOLVED') continue;
    const mine = (m.marketSides || []).find((x) => x.long === (r.side === 'long'));
    const p = num(mine?.price);
    if (p == null || (p > 0.01 && p < 0.99)) continue;
    const payout = p >= 0.99 ? Number(r.shares) : 0;
    Object.assign(r, { status: payout > 0 ? 'won' : 'lost', settled_at: new Date(now).toISOString(), payout: payout.toFixed(2),
      pnl: (payout - Number(r.cost) - Number(r.fee)).toFixed(2) });
    n++; log(`SETTLED ${r.mode.toUpperCase()} ${r.status.toUpperCase()}  ${r.team}  pnl $${r.pnl}  ${r.question}`);
  }
  if (n) writeLedger(o, rows, LEDGER, COLUMNS);
  log(`settle: ${n} settled, ${rows.filter((r) => r.status === 'open').length} still open`);
  return n;
}

export function report(o, log = console.log) {
  const rows = readLedger(o, LEDGER); const out = {};
  for (const mode of ['paper', 'live']) {
    const all = rows.filter((r) => r.mode === mode); const done = all.filter((r) => r.status === 'won' || r.status === 'lost');
    if (!all.length) continue;
    const pnl = done.reduce((s, r) => s + Number(r.pnl), 0); const wins = done.filter((r) => r.status === 'won').length;
    const open = all.filter((r) => r.status === 'open');
    out[mode] = { settled: done.length, wins, pnl, open: open.length, openCost: open.reduce((s, r) => s + Number(r.cost), 0) };
    log(`${mode.toUpperCase()}${mode === 'paper' ? ' (not revenue)' : ' (real money)'}: ${done.length} settled, won ${wins}, `
      + `P&L $${pnl.toFixed(2)}; ${open.length} open ($${out[mode].openCost.toFixed(2)} at stake)`);
  }
  if (!rows.length) log('report: no positions yet.');
  return out;
}

// ---------- CLI ----------
export function parseArgs(argv) {
  const o = { ...DEFAULTS }; const cmd = argv[0] && !argv[0].startsWith('--') ? argv[0] : 'report';
  const nums = { '--stake': 'stake', '--min-price': 'minPrice', '--max-price': 'maxPrice', '--max-spread': 'maxSpread', '--window-min': 'windowMin',
    '--window-max': 'windowMax', '--every': 'every', '--max-trade': 'maxTrade', '--daily-loss': 'dailyLoss', '--bankroll': 'bankroll' };
  for (let i = 0; i < argv.length; i++) {
    if (nums[argv[i]]) o[nums[argv[i]]] = Number(argv[++i]);
    else if (argv[i] === '--data') o.data = path.resolve(argv[++i]);
    else if (argv[i] === '--dry') o.dry = true;
    else if (argv[i] === '--live') o.live = true;
  }
  if (o.live) {
    for (const k of ['maxTrade', 'dailyLoss', 'bankroll']) if (!(o[k] > 0)) throw new Error('--live needs --max-trade, --daily-loss and --bankroll (all > 0)');
    if (o.maxTrade > o.bankroll) throw new Error('--max-trade cannot exceed --bankroll');
  }
  return { cmd, o };
}

async function main() {
  const { cmd, o } = parseArgs(process.argv.slice(2));
  let creds = null;
  if (o.live) {
    creds = loadCredentials(o.credentials);
    if (!creds) throw new Error(`live mode needs your API key file at ${o.credentials} (see README)`);
    console.log(`PaperBot US ${cmd}  LIVE: real money. Max $${o.maxTrade}/trade, stop after -$${o.dailyLoss}/day, $${o.bankroll} bankroll. `
      + `Halt: touch ${path.join(o.data, 'STOP')}`);
  } else console.log(`PaperBot US ${cmd}  (paper only: no orders)`);
  const tick = async () => { await settle(o); await scan(o, Date.now(), console.log, creds); report(o); };
  if (cmd === 'scan') await scan(o, Date.now(), console.log, creds);
  else if (cmd === 'settle') await settle(o);
  else if (cmd === 'report') report(o);
  else if (cmd === 'run') {
    for (;;) {
      console.log(`\n--- ${new Date().toLocaleString()}`);
      try { await tick(); } catch (e) { console.log(`error: ${e.message} (will retry)`); }
      await new Promise((r) => setTimeout(r, o.every * 60000));
    }
  } else { console.log('commands: scan | settle | report | run'); process.exitCode = 1; }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((e) => { console.log(`error: ${e.message}`); process.exitCode = 1; });
}
