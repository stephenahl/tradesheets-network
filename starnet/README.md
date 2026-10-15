# StarNet: the network's visual HQ

StarNet (pixel-art station on Stephen's Mac) and NEXUS stay, per Stephen 2026-10-14. Their job changes: they are the **window** onto the network, not its engine. The engine is the 7 scheduled Claude agents working through this repo. Only the operator changes anything here; scheduled agents leave `starnet/` alone.

## How data reaches StarNet
```
scheduled agents ──push──▶ GitHub (stephenahl/tradesheets-network)
                                   │  git pull --ff-only, at most every 5 min, when the HQ tab refreshes
                                   ▼
          Mac clone ~/tradesheets-network ──read-only──▶ agent-network-bridge ──▶ StarNet "Network HQ" tab
```
- v1 (installed 2026-10-14) read the Mac's old copy of `network/`, which went stale once the agents moved to GitHub.
- v2 (this folder) reads a GitHub clone instead and shows per-agent stations. If the clone is missing, it falls back to the old copy and says "local copy" in the badge.
- No secrets in the plugin. Git uses the Mac's existing GitHub login. The plugin only pulls: no push, no reset, no writes to agent files.

## Stations: where each agent sits, and the 14 NEXUS roles folded in
Paper merge only. NEXUS stays execution-disabled and its $15 OpenAI allowance ($14.87 left) is untouched.

| Agent | Room | Original NEXUS roles absorbed |
|---|---|---|
| Operator (Claude, this chat) | HOME | NEXUS CONTROL |
| Strategist | Central HQ | ATLAS (priorities, synthesis) |
| Researcher | Opportunity Research | NOVA (demand evidence) |
| Builder | Product Studio | FORGE (engineering), MERCHANT (listing prep), PIXEL (visuals), SCRIBE (copy) |
| QA | Review & Operations | SENTINEL (independent review) |
| Marketer | Content & Digital | ORBIT (acquisition), PULSE (publishing schedule) |
| Analyst | Shared Knowledge Hub | LEDGER (margins, costs), ARCHIVE (evidence, memory) |
| Support | Customer & Business Ops (future area) | ECHO (message triage), HARBOR (routine ops) |
| — | Polymarket Lab | QUANT: frozen with the paper bot |

All 14 are covered exactly once (a test checks this). The native StarNet workers from the ChatGPT pilot (ATLAS/FORGE/SENTINEL LOCAL) keep their desks and stay idle. The map and desk bindings are unchanged.

Each station card shows: room, working / queued / blocked counts from BOARD.md, absorbed NEXUS roles, and the agent's latest LOG.md line. The header badge shows tasks waiting on Stephen and when the last GitHub sync happened.

## Brain (2026-10-15)
StarNet's 4 agents now run on Claude through Claude Code, signed in with Stephen's Claude Pro plan (no API key, $0 per turn): NEXUS CONTROL on Opus 5.5; ATLAS, FORGE and SENTINEL on Sonnet 5.5. They share the Pro usage limit with the scheduled agents, so use them lightly. The old ChatGPT/OpenAI sign-in is left in place and unused ($14.87 of the $15 pilot allowance untouched). Use only one StarNet tab at a time: two windows cause save conflicts.

## Install (operator, when the Mac is linked)
1. One-time: `git clone https://github.com/stephenahl/tradesheets-network ~/tradesheets-network` (uses Stephen's GitHub login on the Mac; ask first if git prompts for credentials).
2. `starnet/agent-network-bridge/install.sh <path to installed agent-network-bridge>`: backs up the plugin, copies `lib/repo-sync.cjs` and `lib/network-files.cjs` plus tests, patches `index.js` and `ui/app.js` (idempotent), runs the tests.
3. Stephen re-approves the changed plugin in StarNet.

## Next (after v2 is live)
- Show the stations on the pixel map itself (desk status lights driven by the same data), reusing ChatGPT's continuous-local-001 progress view if it fits.
- Optional: a tap-to-approve button that writes APPROVED into APPROVALS.md, but only with Stephen's sign-off, since it would make the plugin write to the repo.
