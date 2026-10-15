#!/usr/bin/env python3
"""Apply Network HQ v2 to an installed agent-network-bridge (run from the plugin folder).
Idempotent. Copies nothing itself; install.sh copies lib/ files first. Fails loudly if anchors moved."""
import sys
def patch(path, pairs):
    s = open(path).read(); orig = s
    for old, new, marker in pairs:
        if marker in s: continue
        if old not in s: sys.exit(f"anchor not found in {path}: {old[:70]!r}")
        s = s.replace(old, new, 1)
    if s != orig: open(path, "w").write(s); print("patched", path)
    else: print("already applied", path)

patch("index.js", [(
    "const { readNetwork } = require('./lib/network-files.cjs');",
    "const { readNetwork } = require('./lib/network-files.cjs');\nconst { createRepoSync } = require('./lib/repo-sync.cjs');\nconst repoSync = createRepoSync();",
    "createRepoSync()"),
  ("    api.handle('network', () => readNetwork());",
   "    // Pulls the GitHub clone at most every 5 min (ff-only), then reads it. Still read-only toward the agents.\n    api.handle('network', async () => readNetwork(undefined, await repoSync.sync()));",
   "repoSync.sync()")])

STATIONS = r"""
    const stations = list(data.stations);
    if (stations.length) {
      $('hq-agents').replaceChildren(...stations.map((s) => {
        const node = text('article', undefined, 'panel');
        const busy = s.doing ? 'working' : s.ready ? `${s.ready} queued` : 'idle';
        node.append(text('h4', `${safeText(s.agent).replace(/^./, (c) => c.toUpperCase())} · ${safeText(s.room)}`),
          text('p', `${busy}${s.blocked ? ` · ${s.blocked} blocked` : ''} · NEXUS: ${list(s.nexus_roles).join(', ')}`, 'record-meta'),
          text('p', s.last ? `${safeText(s.last.date)}: ${safeText(s.last.text).slice(0, 220)}` : 'No logged runs yet', 'record-description'));
        return node; }));
    }
    const sy = data.sync; const src = data.source === 'github' ? 'GitHub' : 'local copy';
    $('network-badge').textContent += ` · ${src}${sy && sy.at ? (sy.ok ? ` synced ${new Date(sy.at).toLocaleTimeString()}` : ` sync failed: ${safeText(sy.error).slice(0, 60)}`) : ''}`;
"""
patch("ui/app.js", [(
    "    const column = (title, items) =>",
    STATIONS + "    const column = (title, items) =>",
    "const stations = list(data.stations)")])
