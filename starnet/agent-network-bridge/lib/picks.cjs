'use strict';
// Polymarket picks: reads Claude's newest research board from the repo clone and (on request) live prices from
// Polymarket's PUBLIC market-data API, then ranks legs and combos. Read-only: no keys, no orders, no writes.
// Shared by StarNet's Polymarket tab and polymarket/scanner/combo.mjs, so both always agree.
const fs = require('node:fs');
const path = require('node:path');

const RULES = { minEdge: 0.03, maxSpread: 0.05, minLiquidity: 500, comboHaircut: 0.02, maxLegs: 3, keepEdge: 0.05 };
const GAMMA = 'https://gamma-api.polymarket.com/markets?slug=';
const MAX_BOARD_BYTES = 500000;
const round = (x) => Math.round(x * 1000) / 1000;

function boardsDir(root) { return path.join(root, 'polymarket', 'scanner', 'boards'); }

function newestBoardPath(root) {
  try {
    const files = fs.readdirSync(boardsDir(root)).filter((f) => /^\d{4}-\d{2}-\d{2}.*\.json$/.test(f)).sort();
    return files.length ? path.join(boardsDir(root), files[files.length - 1]) : null;
  } catch { return null; }
}

function loadBoard(file) {
  const stat = fs.statSync(file);
  if (stat.size > MAX_BOARD_BYTES) throw new Error('board too large');
  const board = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!Array.isArray(board.legs)) throw new Error('board has no legs');
  return board;
}

// Price for one outcome. Gamma quotes bestBid/bestAsk for outcome index 0; index 1 is the mirror.
function priceFromMarket(m, outcome) {
  if (!m || m.closed) return null;
  let outcomes; try { outcomes = JSON.parse(m.outcomes || '[]'); } catch { return null; }
  const idx = outcomes.indexOf(outcome);
  const bid0 = Number(m.bestBid), ask0 = Number(m.bestAsk);
  if (idx < 0 || !(ask0 > 0)) return null;
  const [bid, ask] = idx === 0 ? [bid0 || 0, ask0] : [1 - ask0, 1 - (bid0 || 0)];
  return { ask: round(ask), bid: round(bid), liquidity: Number(m.liquidityNum ?? m.liquidity ?? 0), live: !!m.live, score: m.score || null };
}

async function livePrice(leg, fetchImpl) {
  const res = await fetchImpl(GAMMA + encodeURIComponent(leg.market_slug), { headers: { accept: 'application/json' }, signal: AbortSignal.timeout(10000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const [m] = await res.json();
  return priceFromMarket(m, leg.outcome);
}

function combos(legs, k) {
  const out = [];
  const rec = (start, acc) => {
    if (acc.length === k) { out.push(acc.slice()); return; }
    for (let i = start; i < legs.length; i++) {
      if (acc.some((a) => a.market_slug === legs[i].market_slug)) continue;   // never two outcomes of one market
      acc.push(legs[i]); rec(i + 1, acc); acc.pop();
    }
  };
  rec(0, []);
  return out;
}

// P(all legs hit): product of Claude's probabilities x researched lift for same-game pairs, capped at the weakest leg.
function jointProb(set, lifts) {
  let p = set.reduce((acc, l) => acc * l.prob, 1);
  for (let i = 0; i < set.length; i++) for (let j = i + 1; j < set.length; j++) {
    const lift = lifts[[set[i].id, set[j].id].sort().join('|')];
    if (lift) p *= lift;
  }
  return Math.min(p, ...set.map((l) => l.prob));
}

// Market makers price the correlation too, so the combo's estimated cost carries the same lift: the edge has to
// come from the legs themselves.
function rankCombos(good, lifts, rules = RULES) {
  const ranked = [];
  for (let k = 2; k <= rules.maxLegs; k++) for (const set of combos(good, k)) {
    const p = jointProb(set, lifts);
    const indep = set.reduce((a, l) => a * l.prob, 1);
    const price = Math.min(1, set.reduce((a, l) => a * l.ask, 1) * (p / indep) * (1 + rules.comboHaircut * set.length));
    ranked.push({ legs: set.map((l) => l.id), labels: set.map((l) => l.label), p: round(p), price: round(price),
      payout: round(1 / price), ev: round(p / price - 1), min_payout: round((1 + rules.keepEdge) / p) });
  }
  return ranked.sort((a, b) => b.ev - a.ev);
}

// Main entry. options: { root, live, fetchImpl, now, board (object, for tests) }
async function readPicks({ root, live = false, fetchImpl = globalThis.fetch, now = Date.now(), board: given = null, rules = RULES } = {}) {
  const file = given ? null : newestBoardPath(root);
  if (!given && !file) return { schema_version: 1, available: false, reason: 'No research board yet. The research agent writes one Thu/Sat/Sun mornings.' };
  let board;
  try { board = given || loadBoard(file); } catch (e) { return { schema_version: 1, available: false, reason: `Board unreadable: ${String(e.message).slice(0, 120)}` }; }
  const lifts = board.lifts || {};
  const legs = []; const errors = [];
  for (const leg of board.legs) {
    if (typeof leg.prob !== 'number' || !leg.market_slug || !leg.outcome) continue;
    const started = leg.starts_utc ? Date.parse(leg.starts_utc) <= now : false;
    let px = null; let priceSource = 'research';
    if (live) {
      try { px = await livePrice(leg, fetchImpl); priceSource = 'live'; } catch (e) { errors.push(`${leg.id}: ${String(e.message).slice(0, 60)}`); }
    }
    if (!px) px = { ask: leg.ask_at_research, bid: leg.bid_at_research ?? (leg.ask_at_research - 0.01), liquidity: leg.liquidity_at_research ?? 0, live: false, score: null };
    if (!(px.ask > 0 && px.ask < 1)) continue;
    const spreadOk = px.ask - px.bid <= rules.maxSpread + 1e-9; const liqOk = px.liquidity >= rules.minLiquidity;
    const edge = round(leg.prob - px.ask);
    legs.push({ id: leg.id, label: leg.label, market_slug: leg.market_slug, outcome: leg.outcome, starts_utc: leg.starts_utc || null,
      prob: leg.prob, ask: px.ask, bid: px.bid, liquidity: px.liquidity, edge, price_source: priceSource,
      started, in_play: !!px.live, score: px.score,
      tradeable: spreadOk && liqOk && !started, value: spreadOk && liqOk && !started && edge >= rules.minEdge,
      flag: started ? 'started' : !liqOk ? 'thin book' : !spreadOk ? 'wide spread' : '',
      why: String(leg.why || '').slice(0, 600), sources: Array.isArray(leg.sources) ? leg.sources.slice(0, 6) : [] });
  }
  legs.sort((a, b) => b.edge - a.edge);
  const good = legs.filter((l) => l.value);
  return {
    schema_version: 1, available: true,
    board: file ? path.basename(file) : 'given', researched_at: board.researched_at || null, method: board.method || null, notes: board.notes || null,
    prices: live ? (errors.length === legs.length && legs.length ? 'research (live fetch failed)' : 'live') : 'research',
    errors: errors.slice(0, 10), rules, legs, combos: rankCombos(good, lifts, rules).filter((c) => c.payout >= (rules.minPayout || 0)).slice(0, 10),
    observed_at_utc: new Date(now).toISOString(),
  };
}

module.exports = { readPicks, RULES, _internals: { priceFromMarket, jointProb, rankCombos, combos, newestBoardPath } };
