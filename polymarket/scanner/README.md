# Scanner + combo builder

Two parts. Neither one places orders: Stephen reviews the tickets and places what he likes himself.

1. **Research (Claude, scheduled).** Every leg goes through the sport's checklist in `RESEARCH.md` (player and team stats, injuries, form, matchups, rest, weather). Before a slate, Claude researches the games and writes a board to `boards/YYYY-MM-DD.json`. For each candidate leg it records its own probability and the reasoning and sources behind it. It starts from the sharpest sportsbook price with the vig removed and moves off that only for evidence the market may have missed. Then it commits the board to GitHub.
2. **Combo builder (`combo.mjs`, run on Stephen's Mac).** Reads the newest board, pulls live Polymarket prices from the public API (no keys), recomputes each leg's edge and ranks 2- and 3-leg combos built only from legs with real edge.

## Run it (Mac Terminal)
```
cd ~/tradesheets-network && git pull && node polymarket/scanner/combo.mjs
```
Options: `--min-edge 0.03` (default 3c), `--max-legs 3`, `--min-payout 10` (only combos paying at least 10x), `--top 10`, `--stake 2`, `--board <file>`, `--offline` (use the board's saved prices).
The cloud workspace can't reach Polymarket from a shell; the Mac can.

## Reading the output
- **LEGS:** Claude's probability vs the live ask. `VALUE` = edge at least 3c, spread at most 5c, liquidity at least $500. `thin` = the book is too thin to trust the price.
- **COMBOS:** only VALUE legs are combined. Same-game pairs use the board's `lifts` (how often the two hit together). Market makers price that correlation too, so it is never counted as edge.
- **Ticket:** request the combo in the app and take it only if the quoted payout is at least the number shown (that keeps a 5% edge). Otherwise skip it.
- "None today" is a normal answer. Most nights the market is right.

## Board format
```json
{"researched_at": "...", "legs": [{"id", "label", "market_slug", "outcome", "prob", "starts_utc",
  "ask_at_research", "bid_at_research", "liquidity_at_research", "why", "sources"}],
 "lifts": {"idA|idB": 1.0}}
```
`lifts` keys are the two leg ids sorted alphabetically. 1.0 = independent, above 1 = they tend to hit together.

## Rules
- Paper trial C1 is still running (`../COMBOS_TRIAL.md`). Anything ordered with real money is Stephen's call. Log it in `../combos/picks.csv` so the trial can score it.
- No API keys in this folder, ever. The `polymarket-us` SDK keys stay in Stephen's own environment.
