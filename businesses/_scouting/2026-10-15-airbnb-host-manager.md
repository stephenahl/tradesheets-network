# Scouting brief: Airbnb / short-term rental Host Business Manager (spreadsheet)
Researcher, 2026-10-15 (Thursday scouting). Web search first; 5 Etsy pages read, one at a time.

## Part 1: quick pass on the 8 seeded ideas (VENTURES.md rubric, each 1-5)
| Idea | Proof | Margin | AI does it | Reuse | Fast test | Total | Call |
|---|---|---|---|---|---|---|---|
| Spreadsheet templates, non-trade niches (Airbnb host first) | 5 | 5 | 5 | 4 | 5 | **24** | Full brief below. Launch candidate |
| Niche "start a ___ business" guide kits (bundle with templates) | 2 | 5 | 5 | 5 | 5 | 22 | Real but unproven: Gumroad/Payhip sellers exist with no visible counts ([Gumroad](https://isaiahashley.gumroad.com/l/SdcRk), [Payhip](https://payhip.com/b/Ru3zM)). Better as an add-on to TradeSheets than a new venture |
| Excel/Sheets dashboard templates (Gumroad, Creative Market) | 3 | 5 | 5 | 4 | 4 | 21 | Many sellers ([1](https://exceldashboards.gumroad.com/l/dynamic-dashboard), [2](https://masu84.gumroad.com/l/kpidashboard)); generic, crowded, no counts seen. Creative Market needs a new account |
| Canva social-post packs for trades | 2 | 5 | 3 | 4 | 4 | 18 | Sellers exist ([cleaning](https://remotesharks.gumroad.com/l/cleaning-social-media-templates), [handyman](https://remotesharks.gumroad.com/l/handyman-social-media-templates), [TemplateMonster](https://www.templatemonster.com/social-media/cleaning-service-instagram-post-templates-564873.html)); no sales counts. Needs Canva in the browser |
| Amazon KDP logbooks for trades | 3 | 2 | 4 | 3 | 4 | 16 | Saturated low-content niche ([kdpbuilder](https://kdpbuilder.com/niches/logbooks)); ~$2-3 royalty; KDP account + tax interview for Stephen |
| Web quote-calculator subscription | 2 | 5 | 4 | 3 | 2 | 16 | Competes with Jobber-type SaaS; needs hosting, billing, support. Not a one-week test |
| Local lead-gen sites (rank and rent) | 3 | 5 | 3 | 2 | 1 | 14 | Months of SEO, domains cost money, renting needs sales calls by Stephen. Effectively auto-kill (ongoing owner time) |
| Fiverr custom spreadsheet service | 4 | 4 | 3 | 3 | 3 | 17 | **Auto-kill**: buyers message and revise; needs Stephen's ongoing time. Fiverr gigs exist ([example](https://de.fiverr.com/kwlbrdr/create-an-airbnb-and-vrbo-host-operations-kit-spreadsheet)) |

## Part 2: full brief on the top idea
**Product:** "Airbnb Host Business Manager" — Excel + Google Sheets, built on the existing make_trade.py / build.py engine. Sold in TradeSheetsShop (Etsy) and on Gumroad at $14.99, like the trades.

### Demand signals (real)
- Etsy search "airbnb spreadsheet template google sheets": **5,000+ results**; the first visible listings show review counts of **12.6k, 456, 384, 277, 53, 29** (the count shown on search cards; may be shop-level). [Etsy search](https://www.etsy.com/market/airbnb_spreadsheet_template_google_sheets)
- Adjacent landlord niche: Landlord Rental Property Spreadsheet, $5.25, 26 item reviews, shop **7.1k sales**. [Etsy 1294366220](https://www.etsy.com/listing/1294366220/landlord-rental-property-spreadsheet)
- Rental Bookkeeping Spreadsheet, $9.59 (sale from $12.79), 11 item reviews (4.4), shop **2.2k sales**, Star Seller. [Etsy 1298969279](https://www.etsy.com/listing/1298969279)
- Market size: 5.5M+ Airbnb hosts and 9.5M+ active listings worldwide; ~2.25M US listings. [DemandSage](https://demandsage.com/airbnb-statistics)
- Many independent copies on Gumroad and template sites ([dreamsdigitale](https://dreamsdigitale.gumroad.com/l/AirbnbDashboard), [mostlyhostly](https://mostlyhostly.gumroad.com/l/performance-dashboard), [MonsterOne](https://monsterone.com/google-sheets/ultimate-tool-for-host-airbnb-income-amp-expense-tracker-template-for-google-sheets-and-excel-o548306/)): people keep making these because they sell.

### Competition and prices
- Crowded. Prices run **$3.53-$22.96**, most on deep "sale" (e.g. $25.88 → $6.47). Top seller ($32.80 list, 12.6k reviews) shows buyers pay $20+ for a strong one.
- Feature set of typical listings: income/expense register, monthly P&L, annual summary, multi-property, charts, bank reconciliation ([Etsy 1318177230](https://www.etsy.com/listing/1318177230), $16.50, 0 reviews: new listings start at zero).
- Gap we can fill: most are bookkeeping-only. Our engine already does jobs, scheduling, invoices and a dashboard. Host version: booking log (nights × rate + cleaning fee − platform fee = payout), occupancy %, ADR, RevPAR per property, turnover/cleaning schedule, supplies restock, expenses with tax-style categories (labeled "not tax advice"), 1-sheet dashboard.

### What buyers complain about
- Visible reviews on the 3 listings read were positive ("Very easy to use, well set up", "works great easy to use"); one buyer bought the wrong item. No complaint data found; low-confidence on pain points. Guesty's host guide stresses simple categories and tax-time totals ([Guesty](https://www.guesty.com/blog/airbnb-expenses-sheet/)).

### Risks
- Saturated search: a new listing with 0 reviews may get few views (same open question as the trades, which have 0 sales so far).
- Off-brand for "TradeSheets"; fine in the same shop for a test, a separate shop only if it sells.
- Tax categories must be labeled as organisation aids, not tax advice (auto-kill rule on financial advice).

### Recommendation
**Score 24/25 → launch candidate for Monday's pick.** Confidence: **medium** (buyers clearly pay in this niche; whether a new listing gets seen is unproven). Smallest test: 1 Etsy listing (free credit, 12 left) + 1 Gumroad product, $0 spend, built in one Builder run with make_trade.py. "Working" in 30 days = 3+ sales or 300+ views. Stephen's time: ~2 minutes to click Publish.

### New ideas found while scouting
1. **Airbnb turnover cleaner variant** of the Cleaning Business Manager (cleaners who serve STR hosts: per-turnover pricing, linen counts, host invoices). Reuses a built product; near-zero cost.
2. **Landlord / long-term rental manager** (rent roll, late fees, maintenance log): shops at 2.2k-7.1k sales show demand. Second product if the host manager gets views.
3. **Airbnb welcome book / house manual** templates: very large Etsy niche ([Etsy search](https://www.etsy.com/market/airbnb_welcome_book)), but usually Canva; could be done as an editable Google Doc/PDF. Needs a check on Canva-free versions.
