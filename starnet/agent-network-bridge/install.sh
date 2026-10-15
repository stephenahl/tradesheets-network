#!/bin/bash
# Network HQ installer (v2 stations + v3 Polymarket picks). Run on Stephen's Mac by Claude (operator) only.
# Usage: install.sh <path-to-installed agent-network-bridge>   (backs up first; idempotent)
set -euo pipefail
DEST="$1"; HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$DEST/index.js" ] && [ -f "$DEST/lib/network-files.cjs" ] || { echo "not an agent-network-bridge: $DEST"; exit 1; }
BK="${BACKUP_DIR:-$HOME/starnet-plugin-backups}/agent-network-bridge-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BK" && cp -R "$DEST/." "$BK/" && echo "backup: $BK"
cp "$HERE/lib/repo-sync.cjs" "$HERE/lib/network-files.cjs" "$HERE/lib/picks.cjs" "$DEST/lib/"
(cd "$DEST" && python3 "$HERE/ui/apply-hq-v2.py" && python3 "$HERE/ui/apply-picks.py" && node --check index.js && node --check ui/app.js)
(cd "$HERE" && node --test tests/*.test.cjs 2>&1 | grep -E "^# (pass|fail)")
echo "Done. Stephen must re-approve the changed plugin in StarNet."
