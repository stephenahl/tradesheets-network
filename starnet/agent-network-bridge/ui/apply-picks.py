#!/usr/bin/env python3
"""Add the Polymarket picks panel to an installed agent-network-bridge (run from the plugin folder).
Idempotent; fails loudly if anchors moved. install.sh copies lib/picks.cjs first."""
import sys
def patch(path, pairs):
    s = open(path).read(); orig = s
    for old, new, marker in pairs:
        if marker in s: continue
        if old not in s: sys.exit(f"anchor not found in {path}: {old[:70]!r}")
        s = s.replace(old, new, 1)
    if s != orig: open(path, "w").write(s); print("patched", path)
    else: print("already applied", path)

HANDLER = """
    // Polymarket picks: newest research board from the GitHub clone, optionally with live public prices.
    // Read-only: no keys, no orders. Live fetches are cached for 60 s so repeated clicks don't hammer the API.
    api.handle('picks', async (args) => {
      const live = !!(args && args.live);
      if (live && picksCache && Date.now() - picksCache.at < 60000) return picksCache.data;
      await repoSync.sync();
      const data = await readPicks({ root: repoSync.dir, live });
      if (live) picksCache = { at: Date.now(), data };
      return data;
    });
"""
patch("index.js", [
  ("const repoSync = createRepoSync();",
   "const repoSync = createRepoSync();\nconst { readPicks } = require('./lib/picks.cjs');\nlet picksCache = null;",
   "require('./lib/picks.cjs')"),
  ("    api.handle('network', async () => readNetwork(undefined, await repoSync.sync()));",
   "    api.handle('network', async () => readNetwork(undefined, await repoSync.sync()));" + HANDLER,
   "api.handle('picks'"),
])

PANEL = """<div id="picks-panel" class="panel"><div class="panel-heading"><div><h3>Today's picks</h3><p class="subtext">Claude's research board vs Polymarket prices. You place orders yourself in the Polymarket app; this panel never trades.</p></div><div class="header-actions"><span id="picks-badge" class="badge neutral">Loading</span><button id="picks-live" class="button subtle" type="button">Get live prices</button></div></div><div id="picks-legs" class="record-list"></div><div class="panel-heading spaced"><h3>Best combos</h3></div><div id="picks-combos" class="record-list"></div></div>
        <div id="evidence-content"></div>"""
patch("ui/index.html", [(
  '<div id="evidence-content"></div>', PANEL, 'id="picks-panel"')])

RENDER = r"""
  const pct = (x) => `${Math.round(Number(x) * 100)}%`;
  const cents = (x) => `${Math.round(Number(x) * 100)}¢`;
  function renderPicks(data) {
    if (!data || data.schema_version !== 1) return;
    if (!data.available) { $('picks-badge').textContent = 'No board'; $('picks-legs').replaceChildren(empty('No research board yet', safeText(data.reason, ''))); $('picks-combos').replaceChildren(); return; }
    const legs = list(data.legs); const value = legs.filter((l) => l.value);
    $('picks-badge').textContent = `${value.length} value · ${safeText(data.board)} · ${data.prices === 'live' ? `live ${new Date(data.observed_at_utc).toLocaleTimeString()}` : safeText(data.prices)}`;
    $('picks-badge').className = `badge ${value.length ? 'good' : 'neutral'}`;
    $('picks-legs').replaceChildren(...(legs.length ? legs.map((l) => {
      const node = text('article', undefined, 'record'); const top = text('div', undefined, 'record-top');
      top.append(text('h3', safeText(l.label), 'record-title'), badge(l.value ? 'VALUE' : l.flag || (l.edge > 0 ? 'small edge' : 'no edge'), l.value ? 'good' : 'neutral'));
      const when = l.starts_utc ? new Date(l.starts_utc).toLocaleString([], { weekday: 'short', hour: 'numeric', minute: '2-digit' }) : '';
      node.append(top, text('p', `Claude ${pct(l.prob)} · price ${cents(l.ask)} · edge ${l.edge >= 0 ? '+' : ''}${Math.round(l.edge * 100)}¢ · book $${Math.round(l.liquidity).toLocaleString()}${when ? ` · ${when}` : ''}${l.in_play ? ` · LIVE ${safeText(l.score, '')}` : ''}`, 'record-meta'));
      if (l.why) node.append(text('p', safeText(l.why).slice(0, 600), 'record-description'));
      return node; }) : [empty('No legs on this board', '')]));
    const combos = list(data.combos);
    $('picks-combos').replaceChildren(...(combos.length ? combos.slice(0, 5).map((c, i) => {
      const node = text('article', undefined, 'record');
      node.append(text('h3', `#${i + 1} · EV ${Math.round(c.ev * 100)}% · hits ${pct(c.p)} · pays ~${Number(c.payout).toFixed(2)}x`, 'record-title'),
        text('p', list(c.labels).join('  +  '), 'record-description'),
        text('p', `Request it in the app; take it only if the payout is at least ${Number(c.min_payout).toFixed(2)}x.`, 'control-note'));
      return node; }) : [empty('No combo today', 'Combos are built only from VALUE legs. No play is a fine answer.')]));
  }
  async function refreshPicks(live = false) {
    if (!state.ready) return;
    try { if (live) { $('picks-live').disabled = true; $('picks-badge').textContent = 'Fetching live prices…'; } renderPicks(await state.bridge.backend.call('picks', live ? { live: true } : {})); }
    catch (error) { $('picks-badge').textContent = 'Unavailable'; }
    finally { $('picks-live').disabled = false; }
  }
"""
patch("ui/app.js", [
  ("  async function refreshNetwork() {", RENDER + "  async function refreshNetwork() {", "function renderPicks("),
  ("      renderNetwork(data);", "      renderNetwork(data);\n      if (state.tab === 'polymarket' && !state.picksLoaded) { state.picksLoaded = true; refreshPicks(false); }", "state.picksLoaded"),
  ("  $('refresh').addEventListener('click', refresh);",
   "  $('picks-live').addEventListener('click', () => refreshPicks(true));\n  document.querySelectorAll('[data-tab=\"polymarket\"]').forEach((b) => b.addEventListener('click', () => refreshPicks(false)));\n  $('refresh').addEventListener('click', refresh);",
   "$('picks-live').addEventListener"),
])
