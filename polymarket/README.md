# Polymarket: side project (Etsy and StarNet come first)

Rules: research only. No live trading, no changes on the VPS, no credentials in this repo, and simulated results are never revenue. Stephen approves anything that touches the server or money.

## Diagnosis (2026-10-15)
Why the ChatGPT-era bot found no edge:
1. **Wrong target.** BTC 15-minute Up/Down contracts are priced from BTC spot, volatility and time left; market makers do that faster from the same public data. The bot's model scored worse than the market's own price (Brier 0.1337 vs 0.1325).
2. **Too slow.** Simulated fills about 15 s late; slow fills are adversely selected. Realistic replay lost 1-5%.
3. **Strategies traded noise** (momentum / mean reversion on contract quotes), never validated.
4. **Tiny, re-used samples:** "champion" picked on 11 validation markets; thresholds tuned and reported on the same 30 settlements; correlated rows counted as independent.
5. **Effort went to infrastructure** (memory vault, AI reviewer, orchestration), not to falsifying the edge question.
6. **$50 scale:** even a real 2% edge on $2 positions is pennies, below hosting cost.

## Study 1: is the market itself mispriced? (snapshot Oct 7-12, 409 settled markets, 113k books)
Script: `calibration.py` (read-only on the Mac's server-review snapshot). Findings:
- The market is well calibrated. Apparent edges in single price buckets flip sign between neighbouring time offsets: noise.
- One consistent pattern: favorites priced >= 90c win slightly more often than priced (favorite-longshot bias). Buying the favorite at the ask: T-300s +1.0c/contract (n=140), T-180s +2.1c (n=191), T-120s -0.1c (n=176), all before fees.
- All of it came from the Down side (Down favorites 100% wins; Up favorites flat or negative), which fits a falling-BTC week rather than a lasting bias.
- One loss costs about 96c, so a few losses erase the edge. Fees of 1-2c likely remove it.

See `HYPOTHESIS.md` for the frozen test.

## PaperBot (2026-10-20)
`paperbot/`: our own read-only Polymarket paper trader for H2 (sports favourites 90-99c). No wallet, no orders, no dependencies. Run it on the Mac; see `paperbot/README.md`.
