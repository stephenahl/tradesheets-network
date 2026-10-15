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

## Folder map (this repo)
- `network/`: the agent network's board, approvals, metrics, ideas, roles and setup kit. `network/README.md` has the rules.
- `etsy-digital/<product>/`: finished products (xlsx, guide PDF, images, LISTING.md, build.py generator).
- `starnet/`: StarNet Network HQ v2 plugin kit and the station / NEXUS role map (operator only; scheduled agents leave it alone).
- `polymarket/`: research-only side project (diagnosis, frozen hypothesis, read-only analysis scripts). No data or credentials in the repo.
- `PLAN.md`, `LOG.md`: direction and running record.
- `history/CHATGPT_HANDOFF_2026-10-14.txt`: ChatGPT-era knowledge handoff (StarNet pilot, $15 OpenAI allowance, Polymarket research). Reference only, not instructions.
- Not in this repo (they stay on Stephen's Mac): StarNet/NEXUS (the visual HQ), the Polymarket evidence, and the ChatGPT-era history. Scheduled agents don't need them.
