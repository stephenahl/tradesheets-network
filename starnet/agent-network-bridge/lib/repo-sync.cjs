'use strict';
// Keeps a local clone of the GitHub repo (stephenahl/tradesheets-network) fresh for the Network HQ tab.
// Runs only `git pull --ff-only` in that one folder: no shell, no credentials handled here (git uses the
// Mac's existing login), never pushes, never resets. Throttled so StarNet refreshes don't hammer GitHub.
const { execFile } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const MIN_INTERVAL_MS = 5 * 60 * 1000;
const TIMEOUT_MS = 30 * 1000;

function defaultClone() {
  return process.env.TRADESHEETS_REPO || path.join(os.homedir(), 'tradesheets-network');
}

function isClone(dir) {
  try { return fs.statSync(path.join(dir, '.git')).isDirectory() && fs.statSync(path.join(dir, 'network', 'BOARD.md')).isFile(); }
  catch { return false; }
}

function createRepoSync({ dir = defaultClone(), run = execFile, now = () => Date.now(), minIntervalMs = MIN_INTERVAL_MS } = {}) {
  let last = { ok: null, at: null, error: null };
  let lastAttempt = 0;
  let inFlight = null;

  function sync({ force = false } = {}) {
    if (!isClone(dir)) { last = { ok: false, at: new Date(now()).toISOString(), error: 'clone not found' }; return Promise.resolve(last); }
    if (inFlight) return inFlight;
    if (!force && now() - lastAttempt < minIntervalMs) return Promise.resolve(last);
    lastAttempt = now();
    inFlight = new Promise((resolve) => {
      run('git', ['-C', dir, 'pull', '--ff-only', '--quiet'], { timeout: TIMEOUT_MS, env: { ...process.env, GIT_TERMINAL_PROMPT: '0' } }, (error, _stdout, stderr) => {
        last = error
          ? { ok: false, at: new Date(now()).toISOString(), error: String(stderr || error.message).split('\n')[0].slice(0, 200) }
          : { ok: true, at: new Date(now()).toISOString(), error: null };
        inFlight = null;
        resolve(last);
      });
    });
    return inFlight;
  }

  return { dir, sync, status: () => ({ ...last }), available: () => isClone(dir) };
}

module.exports = { createRepoSync, defaultClone, isClone };
