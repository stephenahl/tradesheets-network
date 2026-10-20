# Why Etsy shows 1 of 5 listings active, and why views are near zero (Researcher, 2026-10-20)

Board task: "find why Etsy shows 1 of 5 listings active / near-zero views; evidence only". Tuesday run, current-business mode. Scouting stays on Thursday.

## Bottom line
- **Listing count: not resolved from the cloud, and the "1 active" reading itself is unverified.** No Etsy email says any listing was deactivated, removed, put under review or that the shop is paused (Gmail, all Etsy mail since 10-13, checked). On 10-15 Shop Manager showed 6 active (5 + the duplicate Cleaning, which we deactivated), so the 4 later listings were active then. The "1 active listing" figure comes only from the Analyst's automated read of the public shop page; this run's fetch of that page was not permitted (same "permission not answered" the Analyst hit on 10-16 and 10-18), so I could not confirm it. Confidence that the 4 listings are actually inactive: **low (about 30%)**. The decisive check is 2 minutes in Shop Manager on the Mac (below).
- **Near-zero views: expected for a 6-day-old shop with no paid or external traffic yet. Low confidence that anything is broken.** Week ending Oct 16: 1 shop visit, 0 from Etsy Ads, 0 from Offsite Ads (Etsy weekly email). But the shop was only declared "officially open for business" by Etsy on **2026-10-15 20:17 UTC**, the Pinterest ad campaign only went live **10-18**, and the 16 organic pins started **10-19**. So the traffic test has had about 2 days, not a week. Judge views after Nov 3 (end of the pin schedule) with a Stats export, not now.

## Evidence
| Signal | Source | What it says |
|---|---|---|
| 5 + 1 duplicate active on 10-15 | LOG.md 2026-10-15 (operator, Shop Manager) | "Etsy now shows 6 active listings"; duplicate 4596142179 deactivated, leaving 5 |
| Shop opened | Etsy email "TradeSheetsShop, you're officially open for business!" 2026-10-15 20:17 UTC | Shop live from 10-15; no mention of review or limits |
| Traffic | Etsy email "This week in your shop", week ending Oct 16 | 1 visit; 0 Etsy Ads; 0 Offsite Ads |
| No enforcement | Gmail search of all Etsy mail since 10-13 (16 threads) | Only promos, onboarding, Plus, setup fee, identity verified (10-14). No deactivation, removal, policy, review or pause notice |
| Public page "1 active" | Analyst runs 10-17, 10-19, 10-20 | Automated read; Etsy pages are JS-heavy and block bots, so a partial page is possible. This run's fetch was not permitted |
| Google index | Web search "TradeSheetsShop etsy" | Shop and listings not in Google results yet (normal at 6 days) |
| Indexing time | listifyai.net 8-check guide | New or heavily edited listings need crawling and re-scoring; Etsy publishes no timeframe; "a day or two"; repeated edits can restart it. Next checks: listing status in Shop Manager, the Search Visibility page, shipping/region, missing attributes |
| Known hidden-listing causes | valueaddedresource.net (Feb 2024) | Listings flagged by Etsy's review sweeps stay "active" but are hidden from search; reviews usually <24h, auto-visible after 48h. Shop page still showed them. So a review hold would not explain a shop page showing 1 of 5 for 5 days |

## Likely explanations, ranked
1. **The automated read is wrong** (partial or bot-blocked page, or the tool summarised only the first card). Fits: no Etsy notices, and Shop Manager showed them active on 10-15. ~45%.
2. **The 4 listings really are inactive or in draft** (e.g. a step on 10-15 such as the duplicate deactivation, or a renewal/credit setting, caught more than one listing). Would need fixing fast: every day they're down, the Pinterest pins that point at them send clicks to a dead page. ~30%.
3. **Etsy limit on a new shop's listings** (a quiet review hold). No email and no public evidence that Etsy does this for shop pages; ~15%.
4. Other (vacation mode, sections, region). ~10%.

## What Stephen (or the operator on the Mac) should do: 2 minutes, $0
1. Shop Manager > Listings, filter **Active**: count them. If fewer than 5, filter **Inactive** and **Draft**, and reactivate Lawn Care 4595734716, Pressure Washing 4595743330, Auto Detailing 4595855724, Window Cleaning 4595835191 (free while unexpired; ask Stephen).
2. Shop Manager > **Search visibility** page (if shown): note any flags.
3. Signed out (private window), open etsy.com/shop/TradeSheetsShop and one listing, e.g. etsy.com/listing/4595734716. If it says "Sorry, this item is unavailable", it is not active.
4. Shop Manager > Stats, last 7 days: views per listing and traffic sources (Pinterest?). Export the CSV into businesses/etsy-digital/data/ so the Analyst can track views.

## Side finding: spend not in METRICS
- Etsy charged a **$29 one-time shop set-up fee** on 2026-10-14 (email "Payment confirmation for your $29 one-time shop set-up fee"), inside the budget window that starts 10-14. METRICS shows $0 of $50 spent.
- **Etsy Plus** was started and cancelled on 2026-10-14; the cancel email says it runs until **Nov 14**, so the first month was probably billed (Etsy Plus is a monthly plan; amount not in the emails I saw, so unconfirmed). The "free listing credits" used for listings likely came from Plus.
- Recommendation: Analyst logs $29 (confirmed) and checks the Etsy bill (Shop Manager > Finances > Monthly statements) for the Plus charge. If both count, about $39 of the $50 may already be used, which changes what the network can try next.

## Recommendation
Do the 2-minute Shop Manager check before any more listings or pins go out: if 4 of 5 listings are down, the whole traffic test since 10-15 is invalid for those trades. Do not change titles, tags or prices yet: there is no view data to justify it (the 1 visit is not a signal). Re-judge views after Nov 3 with a Stats CSV.
Confidence: medium on "views are too early to judge"; low on the cause of the "1 active" reading, which only Shop Manager can settle.

## Sources
- Etsy emails in the shop inbox (Gmail): "officially open for business" 2026-10-15; "This week in your shop" week ending 2026-10-16; "$29 one-time shop set-up fee" 2026-10-14; "You have canceled Etsy Plus... will end on November 14, 2026" 2026-10-14; "Your identity has been verified" 2026-10-14
- [Etsy Listing Not Showing in Search? 8 Checks in Order (2026), listifyai.net](https://www.listifyai.net/blog/etsy-listing-not-showing-in-search)
- [Etsy routine-sweep glitch and listing review holds, Value Added Resource](https://www.valueaddedresource.net/etsy-routine-sweep-tech-glitch-visibility/)
- Etsy Community threads with the same symptom (bodies need a login, so causes not readable): [new listings not showing in shop but showing as active](https://community.etsy.com/t5/Technical-Issues/new-listings-not-showing-in-shop-but-showing-as-active-listings/td-p/145428515), [Active listings not shown in my shop](https://community.etsy.com/t5/Technical-Issues/Active-listings-not-shown-in-my-shop/m-p/143318893/highlight/true)
- LOG.md 2026-10-15 (Shop Manager showed 6 active), METRICS.md
- Etsy pages opened this run: 0 (1 attempt, not permitted)
