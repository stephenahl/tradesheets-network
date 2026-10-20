# PaperBot: our own Polymarket paper trader

Built 2026-10-20 as a safe stand-in for KryPolybot. Stephen asked for the same kind of bot, built on our terms.

**What it does:** it tests strategy H2 from `../HYPOTHESIS.md` on paper. It watches Polymarket sports moneyline markets. When a game starts in 15-60 minutes and one side's best ask is 90-99c with a spread of 1.5c or less, it records a $10 paper buy of that favourite. The fill walks the real order book, and the fee comes from Polymarket's formula (`shares x rate x p x (1-p)`, sports rate 0.05). It holds each position to settlement and scores the result.

**Why it's safe:**
- Paper only. It contains no order code, no wallet and no private key, and it never asks for one.
- Read-only. It only sends GET requests to `gamma-api.polymarket.com` and `clob.polymarket.com`; any other host is refused in code.
- No installs. It's one file of plain Node (`paperbot.mjs`) with zero dependencies, so there's no third-party code to trust.

## Run it (Mac Terminal)
```
cd ~/tradesheets-network && git pull
node polymarket/paperbot/paperbot.mjs run       # leave this window open; it checks every 5 minutes
```
Other commands: `scan` (one look now), `settle` (score finished games), `report` (results so far), `scan --dry` (show what it would buy without recording anything).
Options: `--stake 10`, `--min-price 0.90`, `--max-price 0.99`, `--max-spread 0.015`, `--window-min 15`, `--window-max 60`, `--every 5`.

The paper trades are saved in `polymarket/paperbot/data/ledger.csv` on the Mac, which git ignores. To share results, paste the `report` output into the project, or upload the CSV.
The cloud workspace can't reach Polymarket, so the bot has to run on the Mac.

## Reading the results
- The `report` line "per share after fees" is the number that matters. Above 0 means the favourites paid after costs.
- Expect long runs of small wins (about 95% of trades) broken by an occasional ~$10 loss. A few days of results can't tell an edge from luck. H2 needs about 1,000 settled trades.
- Paper results are never revenue. The prices come from global Polymarket, and Polymarket US (where Stephen trades) can quote differently.

## Tests
`node --test polymarket/paperbot/` runs offline against canned Polymarket replies.
