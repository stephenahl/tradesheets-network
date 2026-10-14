# Agent Network: how it works

Six agents run as Claude scheduled tasks. Each run starts fresh, so **these files are the network's memory.** Every agent reads this README, its own role file, `BOARD.md` and `APPROVALS.md` before doing anything.

Project root: the GitHub repo `stephenahl/tradesheets-network` (the source of truth since 2026-10-14). Every path below is relative to it. Stephen's Mac folder is no longer needed for agent runs.

## Working with the repo (every agent, every run)
1. Work in your clone of the repo and `git pull --rebase` before reading anything.
2. Make your changes, then commit with a message starting with your agent name (e.g. `Builder: lawn care v1`).
3. Before pushing, `git pull --rebase` again. If a rebase conflict hits BOARD.md, APPROVALS.md or LOG.md, keep both sides' lines; never drop another agent's lines. Then `git push`. Retry once if the push is rejected.
4. Big binary outputs (xlsx, pdf, png) go in the product folder; keep each under 10 MB.

## Agents
| Agent | When (Boise time) | Job |
|---|---|---|
| Strategist | Mon 7:50am | Reviews results, sets the week's priorities on the board, brainstorms and vets new businesses |
| Researcher | Tue & Thu 8:50am | Researches the markets, niches and competitors on the board and writes evidence-backed briefs |
| Builder | Mon, Wed & Fri 10:50am | Builds products (templates, guides, listing images, copy), tests them and packages them ready to list |
| Marketer | Wed & Sat 1:50pm | SEO for titles and tags, Pinterest pins, social and blog drafts, launch plans. Drafts only |
| QA | Mon, Wed & Fri 3:50pm | Independently tests every finished product as a buyer would; passes it or sends it back |
| Analyst | Daily 6:50pm | Logs sales, views and spend from the data available, updates METRICS.md, flags problems |
| Support | Daily 9:50am | Drafts replies to buyer messages and reviews; logs orders |

## Shared files
- `network/BOARD.md`: the task queue. Columns: Ready → Doing → Done, plus Blocked. One line per task: `- [agent] task, ref, date`.
- `network/APPROVALS.md`: anything Stephen must decide. Agents add items; Stephen answers inline with `APPROVED`, `NO`, or a note.
- `network/METRICS.md`: the scoreboard (revenue, net after fees, spend, listings, sales, views).
- `network/IDEAS.md`: the business idea pipeline: idea → researched → proposed → approved/rejected.
- `businesses/<name>/`: everything for one business. The Etsy shop is `businesses/etsy-digital/` (currently also `etsy-digital/`).
- `LOG.md`: one dated line per meaningful action, prefixed with the agent's name.

## Product flow
Builder finishes a product → adds `Publish <product>, QA: pending` to APPROVALS.md → QA tests it and marks `QA: passed` or `QA: failed` (sending it back to the Builder) → Stephen approves only items that passed QA.

## Hard rules (every agent)
1. **Stephen approves:** spending any money, publishing or posting anything public (listings, pins, posts, emails, messages to real people), creating accounts, entering credentials, live trading, deleting files, and any VPS change. Prepare everything up to that point, then add it to `APPROVALS.md`. Never act on an item until Stephen has marked it APPROVED there or said so in chat.
2. **Budget:** $50 total for the first 30 days (from 2026-10-14). Track every dollar in METRICS.md. Nothing is spent without approval.
3. **Real evidence only.** Cite sources. Simulated, estimated or forecast numbers are labeled as such and never counted as revenue.
4. **Don't scrape Etsy in bulk.** It got Stephen's network blocked. Read at most a few Etsy pages per run, one at a time. Prefer web search.
5. **Do real work.** Finish one thing fully rather than starting five. No status essays, no new frameworks, no new agents.
6. **Leave the old system alone:** `nexus-runtime/`, `starnet*/`, `agent-network-bridge/`, `dashboard-preview/`, `server-review/`.
7. **Finish every run** by updating BOARD, LOG and (if relevant) APPROVALS, then send Stephen a message of 5 lines or fewer: what you did, what needs him, what's next.
