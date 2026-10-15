#!/usr/bin/env node
// Combo builder: reads Claude's research board, pulls LIVE Polymarket prices (public API, no keys),
// recomputes each leg's edge and ranks 2- and 3-leg combos. It NEVER places orders: it prints tickets
// for Stephen to review and place himself. The math lives in starnet/agent-network-bridge/lib/picks.cjs,
// shared with StarNet's Polymarket tab so both always show the same numbers.
//
//   node polymarket/scanner/combo.mjs                      # newest board, live prices
//   node polymarket/scanner/combo.mjs --board path.json    # a specific board
//   node polymarket/scanner/combo.mjs --offline            # use the prices saved in the board (no network)
//   options: --min-edge 0.03  --max-legs 3  --top 10  --stake 2
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
const { readPicks, RULES } = createRequire(import.meta.url)(path.join(ROOT, 'starnet/agent-network-bridge/lib/picks.cjs'));

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
const OFFLINE = args.includes('--offline');
const TOP = Number(opt('--top', 10)); const STAKE = Number(opt('--stake', 2));
const rules = { ...RULES, minEdge: Number(opt('--min-edge', RULES.minEdge)), maxLegs: Number(opt('--max-legs', RULES.maxLegs)) };
const boardArg = opt('--board', null);

const r = await readPicks({ root: ROOT, live: !OFFLINE, rules, board: boardArg ? JSON.parse(fs.readFileSync(boardArg, 'utf8')) : null,
  now: OFFLINE ? 0 : Date.now() });
if (!r.available) { console.log(r.reason); process.exit(0); }

console.log(`\nBoard: ${boardArg ? path.basename(boardArg) : r.board} (researched ${r.researched_at})   prices: ${r.prices}`);
if (r.errors.length) console.log(`  (live price errors: ${r.errors.join('; ')})`);
console.log('\nLEGS (sorted by edge)                                       Claude  Ask    Edge   OK?');
for (const l of r.legs) {
  console.log(`  ${l.label.padEnd(58).slice(0, 58)} ${(l.prob * 100).toFixed(0).padStart(3)}%  ${l.ask.toFixed(3)} ${(l.edge >= 0 ? '+' : '') + l.edge.toFixed(3)}  ${l.value ? 'VALUE' : l.flag}`);
}
console.log(`\nCOMBOS (legs with edge >= ${(rules.minEdge * 100).toFixed(0)}c and tradeable; ${r.combos.length} found). Order nothing you don't understand.`);
if (!r.combos.length) console.log('  None today. Singles marked VALUE above are the only plays; no play is also a fine answer.');
for (const [i, c] of r.combos.slice(0, TOP).entries()) {
  console.log(`\n#${i + 1}  EV ${(c.ev * 100).toFixed(0)}%   hits ${(c.p * 100).toFixed(1)}% of the time   est. price ${(c.price * 100).toFixed(1)}c -> pays ${c.payout.toFixed(2)}x`);
  for (const label of c.labels) console.log(`     - ${label}`);
  console.log(`     Ticket: request this combo in the app; take it only if the payout is >= ${c.min_payout.toFixed(2)}x (keeps 5% edge). Suggested stake $${STAKE}.`);
}
console.log('\nPaper-trial reminder: log what you actually order in polymarket/combos/picks.csv (or tell Claude).\n');
