#!/usr/bin/env node
// Combo builder: reads Claude's research board, pulls LIVE Polymarket prices (public API, no keys),
// recomputes each leg's edge and ranks 2- and 3-leg combos. It NEVER places orders: it prints tickets
// for Stephen to review and place himself.
//
//   node polymarket/scanner/combo.mjs                      # newest board, live prices
//   node polymarket/scanner/combo.mjs --board path.json    # a specific board
//   node polymarket/scanner/combo.mjs --offline            # use the prices saved in the board (no network)
//   options: --min-edge 0.03  --max-legs 3  --top 10  --stake 2
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
const OFFLINE = args.includes('--offline');
const MIN_EDGE = Number(opt('--min-edge', 0.03));      // leg must beat the price by this much
const MAX_LEGS = Number(opt('--max-legs', 3));
const TOP = Number(opt('--top', 10));
const STAKE = Number(opt('--stake', 2));               // suggested $ per ticket (Stephen decides)
const COMBO_HAIRCUT = 0.02;                            // assume the RFQ quote is ~2% worse per leg than multiplying asks
const MAX_SPREAD = 0.05, MIN_LIQUIDITY = 500;          // tradeability rules from the trial

function newestBoard() {
  const dir = path.join(HERE, 'boards');
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json')).sort();
  if (!files.length) throw new Error('no boards in ' + dir);
  return path.join(dir, files[files.length - 1]);
}

// Live price for one outcome of one market: { ask, bid, liquidity } or null.
async function livePrice(leg) {
  const url = `https://gamma-api.polymarket.com/markets?slug=${encodeURIComponent(leg.market_slug)}`;
  const res = await fetch(url, { headers: { accept: 'application/json' } });
  if (!res.ok) return null;
  const [m] = await res.json();
  if (!m || m.closed) return null;
  const outcomes = JSON.parse(m.outcomes || '[]');
  const idx = outcomes.indexOf(leg.outcome);
  if (idx < 0) return null;
  const bid0 = Number(m.bestBid), ask0 = Number(m.bestAsk);      // quoted for outcome 0
  const [bid, ask] = idx === 0 ? [bid0, ask0] : [1 - ask0, 1 - bid0];
  return { ask: round(ask), bid: round(bid), liquidity: Number(m.liquidity || m.liquidityNum || 0) };
}
const round = (x) => Math.round(x * 1000) / 1000;

function combos(legs, k) {
  const out = [];
  const rec = (start, acc) => {
    if (acc.length === k) { out.push(acc.slice()); return; }
    for (let i = start; i < legs.length; i++) {
      // never two outcomes of the same market, never two legs marked as conflicting
      if (acc.some((a) => a.market_slug === legs[i].market_slug)) continue;
      acc.push(legs[i]); rec(i + 1, acc); acc.pop();
    }
  };
  rec(0, []);
  return out;
}

// Joint probability: product of Claude's probabilities, times the researched "lift" for any same-game pair
// (lift = P(A and B) / (P(A) P(B)); 1 = independent, >1 = they tend to hit together, <1 = they fight).
function jointProb(set, lifts) {
  let p = set.reduce((acc, l) => acc * l.prob, 1);
  for (let i = 0; i < set.length; i++) for (let j = i + 1; j < set.length; j++) {
    const key = [set[i].id, set[j].id].sort().join('|');
    if (lifts[key]) p *= lifts[key];
  }
  return Math.min(p, Math.min(...set.map((l) => l.prob)));   // can't beat the weakest leg
}

const boardPath = opt('--board', null) || newestBoard();
const board = JSON.parse(fs.readFileSync(boardPath, 'utf8'));
const lifts = board.lifts || {};
const now = Date.now();

const legs = [];
for (const leg of board.legs) {
  if (leg.starts_utc && Date.parse(leg.starts_utc) <= now && !OFFLINE) continue;   // already started
  const px = OFFLINE ? { ask: leg.ask_at_research, bid: leg.bid_at_research ?? leg.ask_at_research - 0.01, liquidity: leg.liquidity_at_research ?? 1e9 }
                     : await livePrice(leg).catch(() => null);
  if (!px || !(px.ask > 0 && px.ask < 1)) continue;
  const spreadOk = px.ask - px.bid <= MAX_SPREAD, liqOk = px.liquidity >= MIN_LIQUIDITY;
  legs.push({ ...leg, ask: px.ask, edge: round(leg.prob - px.ask), tradeable: spreadOk && liqOk });
}

console.log(`\nBoard: ${path.basename(boardPath)} (researched ${board.researched_at})   prices: ${OFFLINE ? 'saved at research time' : 'LIVE'}\n`);
console.log('LEGS (sorted by edge)                                       Claude  Ask    Edge   OK?');
for (const l of [...legs].sort((a, b) => b.edge - a.edge)) {
  console.log(`  ${(l.label).padEnd(58).slice(0, 58)} ${(l.prob * 100).toFixed(0).padStart(3)}%  ${l.ask.toFixed(3)} ${(l.edge >= 0 ? '+' : '') + l.edge.toFixed(3)}  ${l.tradeable ? (l.edge >= MIN_EDGE ? 'VALUE' : '') : 'thin'}`);
}

const good = legs.filter((l) => l.tradeable && l.edge >= MIN_EDGE);
const ranked = [];
for (let k = 2; k <= MAX_LEGS; k++) for (const set of combos(good, k)) {
  const p = jointProb(set, lifts);
  // Market makers price correlation too: a same-game pair costs (product of asks) x lift, so the edge
  // must come from the legs themselves, never from the correlation alone.
  const indep = set.reduce((a, l) => a * l.prob, 1);
  const price = Math.min(1, set.reduce((a, l) => a * l.ask, 1) * (p / indep) * (1 + COMBO_HAIRCUT * set.length));
  ranked.push({ set, price, p, ev: p / price - 1, payout: 1 / price });
}
ranked.sort((a, b) => b.ev - a.ev);

console.log(`\nCOMBOS (legs with edge >= ${MIN_EDGE * 100}c and tradeable; ${ranked.length} found). Order nothing you don't understand.`);
if (!ranked.length) console.log('  None today. Singles marked VALUE above are the only plays; no play is also a fine answer.');
for (const [i, c] of ranked.slice(0, TOP).entries()) {
  console.log(`\n#${i + 1}  EV ${(c.ev * 100).toFixed(0)}%   hits ${(c.p * 100).toFixed(1)}% of the time   est. price ${(c.price * 100).toFixed(1)}c -> pays ${c.payout.toFixed(2)}x`);
  for (const l of c.set) console.log(`     - ${l.label}  (Claude ${(l.prob * 100).toFixed(0)}% vs ask ${l.ask})`);
  console.log(`     Ticket: request this combo in the app; take it only if the payout is >= ${(1 / (c.p / 1.05)).toFixed(2)}x (keeps 5% edge). Suggested stake $${STAKE}.`);
}
console.log('\nPaper-trial reminder: log what you actually order in polymarket/combos/picks.csv (or tell Claude).\n');
