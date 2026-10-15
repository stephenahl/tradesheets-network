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
