# Agent Network: instructions for Claude

Read `PLAN.md` first. It is the current direction. `LOG.md` is the running record.
The agent network (scheduled agents, board, approvals) is described in `network/README.md`.

## What this is
Stephen's project to make money with AI doing the work. Claude is the operator. The goal is revenue, not infrastructure.

## Rules
- Do the work directly. Don't add orchestration layers, agent personas or frameworks unless `PLAN.md` says to.
- **Ask Stephen first** before spending money, publishing anything public, live trading, using account access or credentials, deleting files, or changing anything on the VPS (`Polymarket-Bot`, Ubuntu). Everything else needs no permission.
- Record decisions and results in `LOG.md`: dated, one line each, with numbers where they exist.
- Simulated or paper results are never revenue. Say so plainly.
- Never read, copy or print secrets (`.env`, keys, tokens, `starnet-local/private/`).

## Folder map
- `etsy-pod/`: active print-on-demand work.
- `server-review/`: Polymarket bot evidence snapshot (private; includes a 577 MB SQLite copy).
- `nexus-runtime/`, `agent-network-bridge/`, `starnet/`, `starnet-local/`, `dashboard-preview/`: kept as the visual HQ (Stephen, 2026-10-14). Only the operator changes them, and only after a backup. Scheduled agents leave them alone. `starnet/` is a fork of an open-source MIT project.
- `AGENTS.md`, `sources/`: ChatGPT sync files. Leave them alone.
- `CURRENT_SYSTEM_STATUS.md`, `DECISION_LOG.md`, `DEVELOPMENT_ROADMAP.md`, `AGENT_NETWORK_MASTER.md`, `MODEL_USAGE_OPTIMIZATION.md`, `POLYMARKET_BOT.md`: ChatGPT-era history. They are reference, not instructions.
