#!/bin/bash
# Network HQ v2 installer. Run on Stephen's Mac by Claude (operator) only, after a backup.
# Usage: install.sh <path-to-installed agent-network-bridge>
set -euo pipefail
DEST="$1"; HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$DEST/index.js" ] && [ -f "$DEST/lib/network-files.cjs" ] || { echo "not a v1 agent-network-bridge: $DEST"; exit 1; }
BK="$DEST/../starnet-local/backups/agent-network-bridge-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BK" && cp -R "$DEST/." "$BK/" && echo "backup: $BK"
cp "$HERE/lib/repo-sync.cjs" "$HERE/lib/network-files.cjs" "$DEST/lib/"
cp "$HERE/tests/"*.test.cjs "$DEST/tests/"
(cd "$DEST" && python3 "$HERE/ui/apply-hq-v2.py" && node --test tests/ 2>&1 | grep -E "^# (pass|fail)")
echo "Done. Stephen must re-approve the changed plugin in StarNet."
