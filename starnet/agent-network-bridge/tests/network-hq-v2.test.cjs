'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { readNetwork, ROOMS, _internals } = require('../lib/network-files.cjs');
const { createRepoSync } = require('../lib/repo-sync.cjs');

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'hq-'));
  fs.mkdirSync(path.join(root, 'network')); fs.mkdirSync(path.join(root, '.git'));
  fs.writeFileSync(path.join(root, 'network', 'BOARD.md'), '# Board\n\n## Ready\n- [qa] Re-test X\n- [qa] Test Y\n\n## Doing\n- [operator] HQ\n\n## Blocked\n- [marketer] Pins\n\n## Done\n');
  fs.writeFileSync(path.join(root, 'network', 'APPROVALS.md'), '# A\n\n## Open\n- **Publish X** **APPROVED by Stephen**\n- **Publish Y**\n\n## Closed\n');
  fs.writeFileSync(path.join(root, 'LOG.md'), '# Log\n- 2026-10-14: QA: first run\n- 2026-10-15: QA: second run\n- 2026-10-14: Stephen APPROVED: stuff\n- 2026-10-15: Analyst: no new data\n');
  return root;
}

test('stations map every agent to a room, NEXUS roles, queue counts and last LOG activity', () => {
  const d = readNetwork(fixture(), { ok: true, at: '2026-10-15T00:00:00Z', error: null });
  const qa = d.stations.find((s) => s.agent === 'qa');
  assert.equal(qa.room, 'Review & Operations');
  assert.deepEqual(qa.nexus_roles, ['SENTINEL']);
  assert.equal(qa.ready, 2);
  assert.deepEqual(qa.last, { date: '2026-10-15', text: 'second run' });
  assert.equal(d.stations.find((s) => s.agent === 'marketer').blocked, 1);
  assert.equal(d.stations.find((s) => s.agent === 'builder').last, null);
  assert.equal(d.waiting_on_stephen, 1);
  assert.equal(d.sync.ok, true);
  assert.equal(d.schema_version, 1);
});

test('all 14 original NEXUS roles are accounted for exactly once', () => {
  const roles = [...Object.values(ROOMS).flatMap((r) => r.nexus), 'QUANT'].filter((r) => r !== 'NEXUS CONTROL');
  assert.equal(new Set(roles).size, 14);
  assert.equal(roles.length, 14);
});

test('lastActivity ignores non-agent lines', () => {
  assert.deepEqual(Object.keys(_internals.lastActivity('- 2026-10-14: Stephen APPROVED: x\n- 2026-10-14: Operator: y\n')), ['operator']);
});

test('repo sync runs only git pull --ff-only in the clone, and throttles', async () => {
  const dir = fixture(); const calls = []; let t = 0;
  const run = (cmd, args, opts, cb) => { calls.push([cmd, args, opts.env.GIT_TERMINAL_PROMPT]); cb(null, '', ''); };
  const s = createRepoSync({ dir, run, now: () => t });
  t = 10 * 60 * 1000;
  assert.equal((await s.sync()).ok, true);
  t += 1000; await s.sync();
  assert.equal(calls.length, 1);
  assert.deepEqual(calls[0], ['git', ['-C', dir, 'pull', '--ff-only', '--quiet'], '0']);
});

test('repo sync reports failures and a missing clone without throwing', async () => {
  const bad = createRepoSync({ dir: fixture(), run: (c, a, o, cb) => cb(new Error('x'), '', 'fatal: could not read from remote\nmore'), now: () => 1e9 });
  assert.deepEqual((await bad.sync()).error, 'fatal: could not read from remote');
  const none = createRepoSync({ dir: path.join(os.tmpdir(), 'nope-hq') });
  assert.equal((await none.sync()).error, 'clone not found');
});
