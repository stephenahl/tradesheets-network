# Paper trial C1: Polymarket sports combos (started 2026-10-15)

Stephen asked for a trial run. This is a **paper** trial: real picks against real prices, logged before kickoff, no money. Claude never places trades. Any real-money step is Stephen's decision, placed by Stephen, after he confirms Polymarket US is allowed for Idaho residents.

## Method (fixed before the first pick)
- **Edge source: price comparison, not game predictions.** For each candidate leg (NFL/college/NBA moneyline or spread), compute the sharp fair probability from a sharp sportsbook consensus line with the vig removed. A leg qualifies only if the Polymarket ask is at least **3 cents below** that fair probability.
- **Combos:** 2-leg only (more legs compound the market maker's margin). Paper combo price = product of the two Polymarket leg asks, then **2% worse** to approximate the RFQ quote. Stake: $1 paper per combo.
- **Singles:** every qualifying leg is also logged as a $1 paper single at its Polymarket ask. This shows whether any profit comes from real value or from parlay variance.
- **Logged before the event starts** in `combos/picks.csv`: date, event, leg, Polymarket ask, sharp fair probability, edge, combo id. Results added after settlement. No edits to past rows.

## Scoring and stop rules
- Report paper P&L and ROI for singles and combos separately, plus win counts and the average edge at entry.
- Review after 4 weeks or 40 combos, whichever comes first.
- **Pass:** singles ROI > 0 AND combos ROI > 0 AND average closing price moved toward our side (we beat the closing line). Then Stephen decides about a small real-money test.
- **Fail:** singles ROI <= 0 or we don't beat the closing line. Stop; no real money.
- Paper results are never revenue.

## Log notes
- 2026-10-15 (12:50 Boise): first slate (Stephen asked for practice). Fair probabilities: TNF from consensus SEA -160/DEN +135, SEA -3 (+100)/DEN +3 (-120), total 40.5 (-110/-110) via thespread.com; tennis from matchstat best odds (bet365, not a sharp book: weaker comparison). Only Keegan Smith qualified (+8.4c). Both combos are PRACTICE rows, not counted in the trial score.
- 2026-10-15 (12:55 Boise): player props for SEA at DEN checked (Stephen asked). Polymarket's props event has almost no liquidity: most props quote 1c bid / 95-99c ask with $1-$30 of liquidity; no anytime-TD market for JSN, Walker or Sutton; Darnold O/U 1.5 pass TD shows ask 0.44-0.45 with an empty bid side. A paper fill at those prices would be fiction, so no prop bet or combo was logged. Rule added: a leg is only eligible if bid-ask spread <= 5c and the book has at least $500 liquidity.
- 2026-10-16: slate 1 scored. Broncos 17-14 Seahawks (OT; 31 points, Under 40.5 won); Landaluce d. Smith 3-6 6-2 6-3 (Smith won set 1); Jodar d. Ruud 4-6 6-4 6-3; JSN 12-134-0; Nix 27 attempts. Trial C1 counted bets: 1 single (Smith) lost, -$1.00 paper. Practice combos: 0 of 5 won, -$5.00 paper (not counted). Closing line: Smith ~0.255 vs 0.26 entry (no closing-line gain). Polymarket's API still showed pre-game prices when scored, so closing prices are approximate. Paper only, not revenue.
