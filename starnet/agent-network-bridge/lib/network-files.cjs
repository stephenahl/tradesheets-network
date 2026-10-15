'use strict';
// Read-only view of the Claude agent network's shared files (network/*.md, LOG.md).
// Fixed filenames only, size-capped, never writes. Used by the StarNet panel's "Network HQ" tab.
const fs = require('node:fs');
const path = require('node:path');

const { defaultClone, isClone } = require('./repo-sync.cjs');

// Prefer the GitHub clone (the live source of truth); fall back to the old Mac copy beside the plugin.
const LOCAL_ROOT = path.resolve(__dirname, '..', '..');
function resolveRoot() { const clone = defaultClone(); return isClone(clone) ? { root: clone, source: 'github' } : { root: LOCAL_ROOT, source: 'local' }; }

// Where each agent sits in the StarNet station, and which original NEXUS roles it absorbed (paper merge only;
// NEXUS stays execution-disabled). See starnet/README.md.
const ROOMS = {
  operator: { room: 'HOME', nexus: ['NEXUS CONTROL'] },
  strategist: { room: 'Central HQ', nexus: ['ATLAS'] },
  researcher: { room: 'Opportunity Research', nexus: ['NOVA'] },
  builder: { room: 'Product Studio', nexus: ['FORGE', 'MERCHANT', 'PIXEL', 'SCRIBE'] },
  qa: { room: 'Review & Operations', nexus: ['SENTINEL'] },
  marketer: { room: 'Content & Digital', nexus: ['ORBIT', 'PULSE'] },
  analyst: { room: 'Shared Knowledge Hub', nexus: ['LEDGER', 'ARCHIVE'] },
  support: { room: 'Customer & Business Operations', nexus: ['ECHO', 'HARBOR'] },
};
const FROZEN = [{ room: 'Polymarket Lab', nexus: ['QUANT'], note: 'BTC bot frozen (no edge). Sports scanner: research boards + picks panel (paper trial C1)' }];

// Latest LOG.md line written by each agent ("- 2026-10-15: QA: tested ...").
function lastActivity(logText) {
  const out = {};
  for (const line of logText.split('\n')) {
    const m = line.match(/^\s*-\s*(\d{4}-\d{2}-\d{2}):\s*([A-Za-z]+):\s*(.*)$/);
    if (m) out[m[2].toLowerCase()] = { date: m[1], text: m[3].trim() };
  }
  return out;
}
const MAX_BYTES = 200000;

function readCapped(file) {
  try {
    const stat = fs.statSync(file);
    if (!stat.isFile()) return null;
    const fd = fs.openSync(file, 'r');
    try { const buf = Buffer.alloc(Math.min(stat.size, MAX_BYTES)); fs.readSync(fd, buf, 0, buf.length, 0); return { text: buf.toString('utf8'), mtime: stat.mtime.toISOString() }; }
    finally { fs.closeSync(fd); }
  } catch { return null; }
}

function sections(markdown) {
  const out = {}; let current = null;
  for (const line of markdown.split('\n')) {
    const h = line.match(/^##\s+(.+?)\s*$/);
    if (h) { current = h[1].trim().toLowerCase(); out[current] = []; continue; }
    if (current && /^\s*(?:[-*]|\d+\.)\s+/.test(line)) out[current].push(line.replace(/^\s*(?:[-*]|\d+\.)\s+/, '').trim());
  }
  return out;
}

function parseTask(item) {
  const m = item.match(/^\[([^\]]+)\]\s*(.*)$/);
  return m ? { agent: m[1].trim(), text: m[2].trim() } : { agent: '', text: item };
}

function tableRows(markdown) {
  const rows = markdown.split('\n').filter((l) => /^\|.*\|\s*$/.test(l) && !/^\|\s*-/.test(l)).map((l) => l.trim().slice(1, -1).split('|').map((c) => c.trim()));
  return rows.length ? { header: rows[0], rows: rows.slice(1) } : { header: [], rows: [] };
}

function readNetwork(rootArg, sync = null) {
  const resolved = rootArg ? { root: rootArg, source: 'given' } : resolveRoot();
  const root = resolved.root;
  const net = path.join(root, 'network');
  const board = readCapped(path.join(net, 'BOARD.md'));
  const approvals = readCapped(path.join(net, 'APPROVALS.md'));
  const metrics = readCapped(path.join(net, 'METRICS.md'));
  const readme = readCapped(path.join(net, 'README.md'));
  const log = readCapped(path.join(root, 'LOG.md'));
  const b = board ? sections(board.text) : {};
  const a = approvals ? sections(approvals.text) : {};
  const agentTable = readme ? tableRows(readme.text.split('## Shared files')[0]) : { rows: [] };
  const activity = log ? lastActivity(log.text) : {};
  const ready = (b.ready || []).map(parseTask); const doing = (b.doing || []).map(parseTask); const blocked = (b.blocked || []).map(parseTask);
  const openApprovals = (a.open || []);
  return {
    schema_version: 1,
    source: resolved.source,
    sync: sync || null,
    stations: Object.entries(ROOMS).map(([key, r]) => {
      const mine = (t) => t.agent.toLowerCase() === key;
      return { agent: key, room: r.room, nexus_roles: r.nexus, last: activity[key] || null,
        doing: doing.filter(mine).length, ready: ready.filter(mine).length, blocked: blocked.filter(mine).length };
    }),
    frozen: FROZEN,
    waiting_on_stephen: openApprovals.filter((x) => !/APPROVED/.test(x)).length,
    observed_at_utc: new Date().toISOString(),
    available: !!board,
    agents: agentTable.rows.filter((r) => r.length >= 3).map((r) => ({ name: r[0], schedule: r[1], job: r[2] })),
    board: {
      ready: (b.ready || []).map(parseTask), doing: (b.doing || []).map(parseTask),
      blocked: (b.blocked || []).map(parseTask), done: (b.done || []).map(parseTask).slice(0, 15),
      updated_at: board?.mtime || null,
    },
    approvals: { open: (a.open || []).slice(0, 30), closed: (a.closed || []).slice(0, 15), updated_at: approvals?.mtime || null },
    metrics: { ...(metrics ? tableRows(metrics.text) : { header: [], rows: [] }), notes: metrics ? metrics.text.split('\n').filter((l) => l && !l.startsWith('|') && !l.startsWith('#')).slice(0, 6) : [] },
    log: log ? log.text.split('\n').filter((l) => /^\s*-\s/.test(l)).slice(-15).reverse().map((l) => l.replace(/^\s*-\s*/, '')) : [],
  };
}

module.exports = { readNetwork, ROOMS, _internals: { sections, parseTask, tableRows, lastActivity } };
