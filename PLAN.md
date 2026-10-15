# Agent Network: reset plan

Owner: Stephen · Operator: Claude · Written 2026-10-14

This replaces the ChatGPT-era roadmap. The older documents (`CURRENT_SYSTEM_STATUS.md`, `DECISION_LOG.md`, `DEVELOPMENT_ROADMAP.md`, `AGENT_NETWORK_MASTER.md`) are now history. I haven't deleted them, and nothing in them is a standing instruction.

## Where things actually stand (from the files, as of Oct 13)

| Piece | Reality |
|---|---|
| Revenue | **$0.** No product listed, no live trade. |
| Polymarket paper bot (VPS) | Running, but entries are disabled. On 123 validation markets the fitted model scored worse than the market's own prices (Brier 0.1337 vs 0.1325). A realistic fee/depth/latency replay lost 5.18%. There are now 493 settled markets. **No edge has been shown.** |
| NEXUS (custom 14-role Python orchestrator) | Has **never run a single live task.** Execution is off, there's no key, the budget is $0, and the attempts ledger is empty. |
| StarNet (open-source pixel-art agent harness, v0.13.2, locally modified) | 4 local agents. The real output so far is 7 short runs that built one offline demo HTML board with fake data. The last coordination attempt failed on provider overload. |
| Bridge plugin | Links StarNet to NEXUS. It only displays NEXUS's roles and saves inert drafts. |
| Etsy print-on-demand | One AI T-shirt graphic and a listing draft. There's no supplier, no real cost quote, no shop, and no listing. |
| Documentation | Status reports, decision logs and test counts outweigh the product work. |

## Diagnosis

1. **Three agent frameworks and zero business outcomes.** Most of four days went into building orchestration, then safety rails around the orchestration, then reports about the rails.
2. **Fourteen personas aren't fourteen capabilities.** ATLAS, LEDGER and ORBIT are all prompts on the same model. One capable agent with real tools does that work without losing information at every handoff.
3. **The approval gates were in the wrong places.** Every local edit needed sign-off, yet nothing ever reached the gates that matter: spending money, publishing, or trading.
4. **Polymarket's data says to stop tuning.** The market already prices what the model sees.

## New operating model

- **One operator.** Claude does the work: research, writing and design in the Claude app, and code in Claude Code inside this folder. Scheduled tasks replace "24/7 agents" for anything recurring. There's no persona roster and no orchestration layer until a real job needs one.
- **Stephen approves only these:** spending money; publishing anything public (listings, posts, emails to real people); live trading; giving access to accounts or credentials; deleting things; any change on the VPS. Everything else I just do and record in `LOG.md`.
- **The scoreboard is money:** revenue, contribution margin, and cash spent, reviewed weekly. Test counts aren't progress.

## Decisions 2026-10-14 (Stephen)
- Budget cap: **$50** for the first 30 days.
- Stephen will open the Etsy shop.
- StarNet can be shut down; it was only meant to organize agents, and it isn't needed.
- Goal: highest profit margin, done as efficiently as possible. **So digital downloads come first** (no supplier, no samples, no shipping). After Etsy fees, about 80–85% of the price is kept, versus about 20–30% on a POD shirt. T-shirt POD is parked.

## Decision 2026-10-15 (Stephen): many businesses
Goal: start as many businesses as possible and make as much money as possible. The network now runs a venture pipeline (`network/VENTURES.md`): Researcher scouts weekly, Strategist proposes the best idea weekly, Stephen approves, Builder and Marketer launch an MVP in about a week, and the Analyst kills losers at 30 days. At most 2 ventures in build at once, under $50 per test, at most 30 minutes of Stephen's time each.

## Workstreams

### A0. Etsy digital downloads (active, primary)
Functional spreadsheet templates (Google Sheets and Excel) for one specific type of small business. Formula-driven tools are where AI has a real quality edge over the mass of AI image printables, and they sell for $10–25 instead of $3–5. The niche is chosen from live Etsy data (see LOG.md).

- **Product 1 (built):** Cleaning Business Manager, in `etsy-digital/cleaning-business-manager/`. The workbook, guide, 7 listing images and listing copy are ready. Price $14.99, which keeps about $13.12 per sale (87%) after Etsy fees.
- **Next:** reuse the same engine for other trades. Each one is a cheap new listing that targets its own searches: lawn care, pressure washing, handyman, dog grooming, window cleaning, pool service, then a bundle. `build.py` is the generator.
- **Kill rule:** if 30 days after the first listings go live there are fewer than 3 sales across all of them, change the niche or the format.

### A. Etsy print-on-demand (parked)
POD on Etsy is crowded and margins are thin. The draft's own math shows about $3–9 per shirt at $27.99, and that turns negative with Offsite Ads. It's still the cheapest way to make real money from where we are, so it gets 30 days and a clear kill rule.

1. Get real landed costs from Printify and Printful for one or two standard blanks, and pick a provider.
2. Choose a niche using actual Etsy search and competition signals. The single moonlit-camp design wasn't validated.
3. Make **10–15 designs**, not one. On Etsy, volume and search coverage matter more than perfecting a single design.
4. Prepare mockups, listings with AI disclosure, and pricing set so contribution is ≥ $6 without ads.
5. **Gate:** Stephen opens or connects the shop and approves listing fees (about $0.20 each) and one sample order.
6. **After 30 days:** keep it if there are sales and views are trending up. If there are no sales, kill or pivot the niche once.

### B. Polymarket: side project (Stephen 2026-10-15: fix it, after Etsy and StarNet)
See polymarket/README.md and polymarket/HYPOTHESIS.md (H1 frozen 2026-10-15). Operator only; agents don't touch it.

#### Original note
- Leave the paper bot and learning/memory timers exactly as they are. They're cheap and they're collecting data.
- Write down one rule now (a frozen hypothesis) and evaluate it only on the **next 200** settled markets, after fees and latency.
- If it isn't clearly positive, shut the research down. Until then, no engineering time goes into it.

### C. StarNet and NEXUS: kept (Stephen, 2026-10-14), redesigned by Claude
Stephen wants StarNet and NEXUS kept running. New role: they are the network's visual HQ and control room, not its engine. The scheduled agents stay the engine. Plan: StarNet shows the 7 agents, the board, approvals and metrics, read live from the `network/` files. NEXUS's 14 roles are retired or merged into the 7 real agents. Changes are made on copies first, with the old state backed up.

#### Old note (superseded)
- NEXUS, the bridge, and the StarNet modifications stay on disk untouched. Stop the local preview processes whenever convenient.
- Revisit this only if a workstream produces a repeatable job that a scheduled task can't handle.

## Next 7 days
1. Supplier cost comparison and blank choice (Claude).
2. Niche research shortlist with evidence (Claude), then Stephen picks one.
3. First 10 designs, mockups and listing drafts (Claude).
4. Frozen Polymarket hypothesis written into `LOG.md` (Claude).
5. Shop opened and spend approved, up to the cap Stephen sets (Stephen).
