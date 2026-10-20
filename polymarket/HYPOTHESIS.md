# H1 (frozen 2026-10-15, before any data after 2026-10-12 was seen)

**Rule:** at 180 seconds before a BTC 15-minute market resolves, if either side's mid price is >= 0.90, buy that favorite side at its best ask. Hold to settlement. One position per market.

**Evaluation data:** only markets that resolve after this commit. Target at least 200 qualifying trades (about 4-5 days of markets; ~45% of markets qualify).

**Metrics, decided now:**
- Net P&L per contract = settlement (0/1) - ask - actual Polymarket US fee per contract (look up the official fee schedule at evaluation time; do not assume).
- Report mean, 95% confidence interval (bootstrap by market), win rate, worst daily loss, Up-side vs Down-side split.

**Decision:**
- Lower 95% bound > 0 after fees AND both sides non-negative -> worth a further pre-registered test. Still no live trading without Stephen's explicit, written approval of capital, market and bounds.
- Otherwise -> H1 is dead. Shut down the BTC research or move to a different market type.

**Known limit:** with ~200 trades the standard error per contract is about 1.2c, so an edge smaller than about 2.5c cannot be confirmed. A null result is the most likely outcome; that is an acceptable answer.

# H2 (frozen 2026-10-20, before any PaperBot data was collected)

**Source:** KryPolybot's research note (2026-07-25, Polymarket sports 2024-04 to 2026-07, 35,784 settled markets). It found favourites priced 90-99c at T-60 won 95.3% (n=768), worth +1.28c per contract after a 0.5c half-spread and fees, with the edge gone once the spread passed 1.5c. We have not verified that claim; H2 tests it forward.

**Rule (paperbot/paperbot.mjs):** for a Polymarket sports moneyline market starting in 15-60 minutes, if the favourite's best ask is >= 0.90 and < 0.99 and the spread is <= 1.5c, paper-buy $10 by walking the ask side (max 1c above the best ask). Fee = shares x feeSchedule.rate x p x (1-p). Hold to settlement. One position per market.

**Metric:** net P&L per share after fees: mean and 95% interval.

**Decision:**
- After 500 settled trades, if the mean is <= 0, stop H2.
- After 1,000 settled trades, if the lower 95% bound is > 0, H2 is worth a small real-money test. That test needs Stephen's written approval of capital and bounds, and Stephen places the orders himself.
- Anything else after 1,000 trades: H2 is dead.

**Known limit:** at a ~95% win rate one trade's result has a standard deviation of about 22c, so even 1,000 trades leave about ±1.4c of noise. A +1.3c edge may never become provable. That's an acceptable answer.
