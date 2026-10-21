#!/usr/bin/env node
// PaperBot: our own Polymarket paper trader. Strategy H2 (see ../HYPOTHESIS.md): buy deep sports
// favourites shortly before the game starts and hold to settlement.
//
// Safe by construction:
//   - PAPER ONLY. There is no order code, no wallet and no private key anywhere in this file.
//   - Read-only: the only network call is an HTTP GET to Polymarket's two public data hosts (allowlist below).
//   - Zero dependencies: plain Node 18+, nothing to npm install.
//
//   node polymarket/paperbot/paperbot.mjs scan      # look for entries now, record paper buys
//   node polymarket/paperbot/paperbot.mjs settle    # score finished games
//   node polymarket/paperbot/paperbot.mjs report    # results so far
//   node polymarket/paperbot/paperbot.mjs run       # scan + settle every 5 minutes until Ctrl+C
//   options: --stake 10  --min-price 0.90  --max-price 0.99  --max-spread 0.015
//            --window-min 15  --window-max 60  --every 5  --data <dir>  --dry (scan without recording)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const GAMMA = 'https://gamma-api.polymarket.com';
const CLOB = 'https://clob.polymarket.com';
const ALLOWED_HOSTS = new Set(['gamma-api.polymarket.com', 'clob.polymarket.com']);
const DEFAULT_FEE_RATE = 0.05; // Polymarket sports taker rate (docs.polymarket.com/trading/fees), used if a market has no feeSchedule
const EXCLUDE = ['-spread-', '-over-', '-under-', '-total-', '-handicap-', '-pt5'];

export const DEFAULTS = {
  stake: 10, minPrice: 0.90, maxPrice: 0.99, maxSpread: 0.015,
  windowMin: 15, windowMax: 60, every: 5, data: path.join(HERE, 'data'), dry: false,
};

const COLUMNS = ['entered_at', 'market_id', 'slug', 'question', 'outcome', 'token_id', 'game_start',
  'minutes_to_start', 'best_bid', 'best_ask', 'spread', 'shares', 'avg_price', 'cost', 'fee', 'fee_rate',
  'status', 'settled_at', 'payout', 'pnl'];

// ---------- network (GET only, two hosts only) ----------
export async function getJson(url) {
  const u = new URL(url);
  if (u.protocol !== 'https:' || !ALLOWED_HOSTS.has(u.hostname)) throw new Error(`blocked host: ${u.hostname}`);
  const res = await fetch(u, { method: 'GET', headers: { accept: 'application/json' }, signal: AbortSignal.timeout(20000) });
  if (!res.ok) throw new Error(`${u.hostname} ${u.pathname} -> HTTP ${res.status}`);
  return res.json();
}

// ---------- helpers ----------
const parseList = (v) => { if (Array.isArray(v)) return v; try { return JSON.parse(v ?? '[]'); } catch { return []; } };

// Gamma writes game times like "2026-10-20 19:00:00+00".
export function parseGameStart(s) {
  if (!s) return null;
  let t = String(s).trim().replace(' ', 'T');
  if (/[+-]\d\d$/.test(t)) t += ':00';
  const ms = Date.parse(t);
  return Number.isFinite(ms) ? ms : null;
}

export const feeFor = (shares, price, rate) => Math.round(shares * rate * price * (1 - price) * 1e5) / 1e5;

// Fill `stake` dollars against the asks, cheapest first, never paying above maxPrice.
export function simulateBuy(asks, stake, maxPrice) {
  const levels = asks.map((a) => ({ price: Number(a.price), size: Number(a.size) }))
    .filter((a) => a.price > 0 && a.size > 0 && a.price <= maxPrice).sort((a, b) => a.price - b.price);
  let left = stake; let shares = 0; let cost = 0;
  for (const l of levels) {
    if (left <= 1e-9) break;
    const take = Math.min(l.size, left / l.price);
    shares += take; cost += take * l.price; left -= take * l.price;
  }
  if (left > 0.01) return null; // book too thin for the stake
  return { shares: Math.round(shares * 1e4) / 1e4, cost: Math.round(cost * 1e4) / 1e4, avgPrice: cost / shares };
}

export function topOfBook(book) {
  const bids = (book.bids || []).map((b) => Number(b.price)).filter((p) => p > 0);
  const asks = (book.asks || []).map((a) => Number(a.price)).filter((p) => p > 0);
  return { bid: bids.length ? Math.max(...bids) : null, ask: asks.length ? Math.min(...asks) : null };
}

// ---------- ledger (CSV, append-only apart from settling open rows) ----------
const ledgerPath = (o, file = 'ledger.csv') => path.join(o.data, file);
const csvCell = (v) => { const s = v == null ? '' : String(v); return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };

function parseCsvLine(line) {
  const out = []; let cur = ''; let q = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (q) { if (c === '"' && line[i + 1] === '"') { cur += '"'; i++; } else if (c === '"') q = false; else cur += c; }
    else if (c === '"') q = true; else if (c === ',') { out.push(cur); cur = ''; } else cur += c;
  }
  out.push(cur); return out;
}

export function readLedger(o, file) {
  const f = ledgerPath(o, file);
  if (!fs.existsSync(f)) return [];
  const [head, ...lines] = fs.readFileSync(f, 'utf8').split('\n').filter(Boolean);
  const cols = parseCsvLine(head);
  return lines.map((l) => Object.fromEntries(parseCsvLine(l).map((v, i) => [cols[i], v])));
}

export function writeLedger(o, rows, file, columns = COLUMNS) {
  fs.mkdirSync(o.data, { recursive: true });
  const body = [columns.join(','), ...rows.map((r) => columns.map((c) => csvCell(r[c])).join(','))].join('\n') + '\n';
  const tmp = ledgerPath(o, file) + '.tmp'; fs.writeFileSync(tmp, body); fs.renameSync(tmp, ledgerPath(o, file));
}

// ---------- scan ----------
async function upcomingMoneylines(now, o) {
  const min = new Date(now - 6 * 3600e3).toISOString(); const max = new Date(now + 2 * 86400e3).toISOString();
  const out = [];
  for (let offset = 0; offset < 5000; offset += 500) {
    const page = await getJson(`${GAMMA}/markets?active=true&closed=false&sports_market_types=moneyline`
      + `&end_date_min=${min}&end_date_max=${max}&limit=500&offset=${offset}`);
    out.push(...page);
    if (page.length < 500) break;
  }
  return out.filter((m) => {
    const start = parseGameStart(m.gameStartTime);
    if (start == null) return false;
    const mins = (start - now) / 60000;
    // some listings carry a stale game time (slug says August, start time says today): skip those
    const slugDate = String(m.slug || '').match(/\d{4}-\d\d-\d\d/)?.[0];
    if (slugDate && Math.abs(Date.parse(slugDate) - start) > 1.5 * 86400e3) return false;
    return mins >= o.windowMin && mins <= o.windowMax && m.enableOrderBook !== false && m.acceptingOrders !== false
      && !EXCLUDE.some((x) => String(m.slug || '').includes(x));
  });
}

export async function scan(o, now = Date.now(), log = console.log) {
  const ledger = readLedger(o);
  const held = new Set(ledger.map((r) => r.market_id));
  const markets = await upcomingMoneylines(now, o);
  const entries = []; const skipped = [];
  for (const m of markets) {
    if (held.has(String(m.id))) continue;
    const outcomes = parseList(m.outcomes); const tokens = parseList(m.clobTokenIds); const prices = parseList(m.outcomePrices).map(Number);
    // the favourite by the displayed price; the order book decides whether it is tradeable
    const fav = prices.indexOf(Math.max(...prices));
    if (fav < 0 || !tokens[fav]) continue;
    if (prices[fav] < o.minPrice - 0.02) continue; // nowhere near the band: skip the book request
    let book;
    try { book = await getJson(`${CLOB}/book?token_id=${tokens[fav]}`); } catch (e) { skipped.push(`${m.slug}: book error ${e.message}`); continue; }
    const { bid, ask } = topOfBook(book);
    const why = ask == null ? 'no asks' : bid == null ? 'no bids'
      : ask < o.minPrice || ask >= o.maxPrice ? `ask ${ask} outside ${o.minPrice}-${o.maxPrice}`
      : ask - bid > o.maxSpread + 1e-9 ? `spread ${(ask - bid).toFixed(3)} > ${o.maxSpread}` : null;
    if (why) { skipped.push(`${m.slug}: ${why}`); continue; }
    const fill = simulateBuy(book.asks, o.stake, Math.min(ask + 0.01, o.maxPrice - 1e-9));
    if (!fill) { skipped.push(`${m.slug}: under $${o.stake} within 1c of the ask`); continue; }
    const rate = Number(m.feeSchedule?.rate ?? DEFAULT_FEE_RATE);
    const fee = feeFor(fill.shares, fill.avgPrice, m.feesEnabled === false ? 0 : rate);
    const row = {
      entered_at: new Date(now).toISOString(), market_id: String(m.id), slug: m.slug, question: m.question,
      outcome: outcomes[fav], token_id: tokens[fav], game_start: new Date(parseGameStart(m.gameStartTime)).toISOString(),
      minutes_to_start: Math.round((parseGameStart(m.gameStartTime) - now) / 60000), best_bid: bid, best_ask: ask,
      spread: (ask - bid).toFixed(3), shares: fill.shares, avg_price: fill.avgPrice.toFixed(4), cost: fill.cost.toFixed(4),
      fee: fee.toFixed(5), fee_rate: m.feesEnabled === false ? 0 : rate, status: 'open', settled_at: '', payout: '', pnl: '',
    };
    entries.push(row);
    log(`PAPER BUY  ${row.outcome} @ ${row.avg_price}  $${row.cost}  fee $${row.fee}  ${m.question}  (starts in ${row.minutes_to_start} min)`);
  }
  if (entries.length && !o.dry) writeLedger(o, [...ledger, ...entries]);
  log(`scan: ${markets.length} moneyline games start in ${o.windowMin}-${o.windowMax} min; ${entries.length} paper buy(s)`
    + `${o.dry ? ' (dry run, not recorded)' : ''}; ${skipped.length} skipped`);
  for (const s of skipped) log(`  skip ${s}`);
  return { markets: markets.length, entries, skipped };
}

// ---------- settle ----------
export async function settle(o, now = Date.now(), log = console.log) {
  const ledger = readLedger(o); let n = 0;
  for (const r of ledger) {
    if (r.status !== 'open') continue;
    let m;
    try { m = await getJson(`${GAMMA}/markets/${encodeURIComponent(r.market_id)}`); } catch (e) { log(`  ${r.slug}: ${e.message}`); continue; }
    if (!m.closed) continue;
    const prices = parseList(m.outcomePrices).map(Number); const outcomes = parseList(m.outcomes);
    if (!(Math.max(...prices) >= 0.99 && Math.min(...prices) <= 0.01)) continue; // closed but not resolved yet
    const won = prices[outcomes.indexOf(r.outcome)] >= 0.99;
    const payout = won ? Number(r.shares) : 0;
    r.status = won ? 'won' : 'lost'; r.settled_at = new Date(now).toISOString();
    r.payout = payout.toFixed(4); r.pnl = (payout - Number(r.cost) - Number(r.fee)).toFixed(4);
    n++; log(`SETTLED ${r.status.toUpperCase()}  ${r.outcome}  pnl $${r.pnl}  ${r.question}`);
  }
  if (n) writeLedger(o, ledger);
  log(`settle: ${n} settled, ${ledger.filter((r) => r.status === 'open').length} still open`);
  return n;
}

// ---------- report ----------
export function report(o, log = console.log) {
  const rows = readLedger(o); const done = rows.filter((r) => r.status === 'won' || r.status === 'lost');
  const open = rows.length - done.length;
  if (!done.length) { log(`report: ${rows.length} paper position(s), none settled yet. Paper only, not revenue.`); return null; }
  const pnl = done.reduce((s, r) => s + Number(r.pnl), 0); const cost = done.reduce((s, r) => s + Number(r.cost), 0);
  const perShare = done.map((r) => Number(r.pnl) / Number(r.shares));
  const mean = perShare.reduce((a, b) => a + b, 0) / perShare.length;
  const sd = Math.sqrt(perShare.reduce((s, x) => s + (x - mean) ** 2, 0) / Math.max(1, perShare.length - 1));
  const se = sd / Math.sqrt(perShare.length); const wins = done.filter((r) => r.status === 'won').length;
  const out = { settled: done.length, open, wins, pnl, roi: pnl / cost, centsPerShare: mean * 100, ci95: [(mean - 1.96 * se) * 100, (mean + 1.96 * se) * 100] };
  log(`report (PAPER ONLY, not revenue): ${done.length} settled, ${open} open`);
  log(`  won ${wins}/${done.length} (${(wins / done.length * 100).toFixed(1)}%)   P&L $${pnl.toFixed(2)} on $${cost.toFixed(2)} staked (ROI ${(out.roi * 100).toFixed(2)}%)`);
  log(`  per share after fees: ${out.centsPerShare.toFixed(2)}c  (95% range ${out.ci95[0].toFixed(2)}c to ${out.ci95[1].toFixed(2)}c)`);
  log(done.length < 1000 ? `  ${done.length} of ~1,000 settled trades needed before the result means anything (see HYPOTHESIS.md H2).`
    : '  Sample is large enough to judge H2 against its decision rule.');
  return out;
}

// ---------- CLI ----------
export function parseArgs(argv) {
  const o = { ...DEFAULTS }; const cmd = argv[0] && !argv[0].startsWith('--') ? argv[0] : 'report';
  const num = { '--stake': 'stake', '--min-price': 'minPrice', '--max-price': 'maxPrice', '--max-spread': 'maxSpread',
    '--window-min': 'windowMin', '--window-max': 'windowMax', '--every': 'every' };
  for (let i = 0; i < argv.length; i++) {
    if (num[argv[i]]) o[num[argv[i]]] = Number(argv[++i]);
    else if (argv[i] === '--data') o.data = path.resolve(argv[++i]);
    else if (argv[i] === '--dry') o.dry = true;
  }
  return { cmd, o };
}

async function main() {
  const { cmd, o } = parseArgs(process.argv.slice(2));
  console.log(`PaperBot ${cmd}  (paper only: no wallet, no orders)  ledger: ${ledgerPath(o)}`);
  if (cmd === 'scan') await scan(o);
  else if (cmd === 'settle') await settle(o);
  else if (cmd === 'report') report(o);
  else if (cmd === 'run') {
    for (;;) {
      console.log(`\n--- ${new Date().toLocaleString()}`);
      try { await settle(o); await scan(o); report(o); } catch (e) { console.log(`error: ${e.message} (will retry)`); }
      await new Promise((r) => setTimeout(r, o.every * 60000));
    }
  } else { console.log('commands: scan | settle | report | run'); process.exitCode = 1; }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((e) => { console.log(`error: ${e.message}`); process.exitCode = 1; });
}
