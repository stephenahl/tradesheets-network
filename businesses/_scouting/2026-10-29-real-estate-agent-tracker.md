# Scouting: Real Estate Agent Business Manager (commission/GCI tracker + pipeline) — 2026-10-29

Researcher, Thursday scouting run. Idea from IDEAS.md (found 2026-10-27). Web search first; 5 Etsy pages opened one at a time (2 returned "unavailable"). $0 spent.

## The idea
A spreadsheet for solo real estate agents: transactions/pipeline, commission calculator (splits, caps, referral fees), GCI goal plan, lead sources, expenses, mileage, tax set-aside dashboard. Excel + Google Sheets. Same engine and tab pattern as the trade managers (clients/jobs → transactions, expenses, mileage, tax).

## Demand signals (real)
- Market size: NAR has 1,438,569 members; median agent did 9 transaction sides in 2025, median gross income $59,200, median business expenses $9,530 (vehicle the largest, $1,580). 15% have 2 years or less experience (the likely template buyers). Sources: [NAR release 2026-06-25](https://www.nar.realtor/newsroom/experienced-realtors-anchor-the-industry-as-housing-affordability-remains-top-hurdle-new-nar-report), [HousingWire](https://www.housingwire.com/articles/nar-2026-member-profile-experience/).
- Realtor-template shops sell on Etsy: RealEstateDesignCo, 18.3k sales, 1.3k shop reviews 4.9, Star Seller. Its Google Sheets **Transaction Coordinator client dashboard** is $12 with 12 reviews 4.9, 176 favorites (Sheets only, no Excel). [listing 1701929614](https://www.etsy.com/listing/1701929614)
- TrackerPro (generic tracker shop, 19.9k sales, 1.5k reviews 4.7) sells a Realtor Transaction Checklist / TC tracker at $3.59 (sale from $7.32); listing review count not shown, 22 favorites. [listing 1503119514](https://www.etsy.com/listing/1503119514)
- Direct commission/GCI tracker competitor: HonestMarginCo, "Real Estate Agent Commission Tracker, GCI & Business Plan (Excel, Google Sheets)", 10 tabs (Dashboard, Transactions, Commission Calculator, Goals, Lead Sources, Expenses, Mileage...), $1.89 sale from $3.77, **0 reviews, shop has 1 sale, new on Etsy.** Nearly the exact product we would build, apparently also AI-built, priced near zero. [listing 4591322540](https://www.etsy.com/listing/4591322540)
- Off-Etsy: CitrusTemplates on Payhip, team/brokerage sales tracker, Google Sheets, $29.50, no sales count shown ([payhip](https://payhip.com/b/Sd2Vu)); a free Notion commission tracker on Gumroad ([gumroad](https://notionforagents.gumroad.com/l/commission-tracker)).
- Two older bundle listings from search results (1060179724 "Real Estate Google Sheets Essentials", 4547739918) are now unavailable: could not read their counts.

**What's missing:** no listing-level review count above 12 for a realtor *spreadsheet*. The big realtor shops' sales are mostly Canva marketing (flyers, social posts, open-house signs), not trackers. Demand for the tracker itself is shown but thin.

## Competition and price
- $1.89-$12 on Etsy, $29.50 on Payhip. Most realtor trackers are Google Sheets only (the TC dashboard says it does not transfer to Excel); Excel + Sheets is a small edge, but HonestMarginCo already offers both.
- Free CRMs and brokerage-provided tools (kvCORE, Follow Up Boss through brokerages) compete for the pipeline part; the commission/expense/tax side is less covered.

## Buyer complaints
None visible (the listings read show only positive reviews, and few of them). No complaint data to design against: low confidence on what to improve.

## Score (VENTURES.md rubric)
| Factor | Score | Why |
|---|---|---|
| Proof of paying buyers | 3 | Realtor shops at 18-20k sales, but the closest tracker listing has 12 reviews; direct GCI tracker has 0 |
| Margin | 5 | Digital, ~87% |
| AI can do the work | 5 | make_trade.py pattern plus a commission-split calculator |
| Reuses what we have | 4 | Engine, Etsy, Gumroad, mileage/expense/tax tabs; new audience (not trades) |
| Fast, cheap test | 5 | One Builder run, $0.20 listing fee |
| **Total** | **22** | Passes 18, below Etsy Seller (24) and Landlord (24) |

No auto-kill rule hit (it tracks the agent's own numbers; no financial advice).

## Recommendation (confidence: medium-low)
Keep as a queued candidate at 22, behind Etsy Seller and Landlord. Do not build it next. Reasons: thinner listing-level proof than those two, and an identical AI-built competitor already sells at $1.89, which signals a race to the bottom.

Better variant found: a **Transaction Coordinator (TC) tracker** (per-deal checklist from listing to close, deadlines, client status view). It is the one realtor spreadsheet with real reviews (12 at $12, Sheets only) and TCs are paid per file, so they buy tools. Added to IDEAS.md as an idea to check next.

Network note (not a score input): TradeSheets has $0 revenue after 2 weeks with 8+ listings and views (61 shop visits week ending Oct 23). The pipeline already holds two 24-point spreadsheet ideas waiting on approval. More spreadsheet ideas are not the bottleneck; conversion and traffic on the live shop are. A Tuesday task on why listings with views get 0 orders (price, thumbnails, Sheets-vs-Excel, reviews) may be worth more than the next scouted idea.
