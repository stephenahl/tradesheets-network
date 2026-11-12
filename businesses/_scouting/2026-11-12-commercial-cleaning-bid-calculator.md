# Scouting: Commercial / janitorial cleaning bid calculator (2026-11-12, Researcher)

**Idea:** an Excel + Google Sheets bid calculator for office/janitorial contracts: sq ft, production rate (sq ft/hr by facility type), visits per week, wage + burden, supplies, overhead, margin → hours per visit, monthly contract price, break-even and an "am I underpricing?" check. Cut from the Cleaning Business Manager's quote engine. Third SKU for the standalone Pricing Calculator pilot (brief 2026-11-10).

**Score: 22 / 25** (Proof 2, Margin 5, AI 5, Reuse 5, Fast/cheap 5). Clears 18, but proof is the weak factor: paid products exist, sales counts were not visible. **Confidence: low.**

## Demand signals
- Market: Census Nonemployer Statistics via startbusinessbystate: 1,173,265 no-employee businesses in NAICS 56172 (janitorial, includes house cleaning/maid) in 2024, up 19% from 985,676 in 2019; average sales ~$21,483. Commercial-only share not given. [source](https://startbusinessbystate.com/solo-cleaning-businesses/)
- Etsy demand pages exist for "janitorial bid template", "commercial cleaning bid sheet", "cleaning bid template", "commercial cleaning service bid template" (Etsy generates market pages for searched phrases). Counts not read. [1](https://www.etsy.com/market/janitorial_bid_template) [2](https://www.etsy.com/market/commercial_cleaning_bid_sheet) [3](https://www.etsy.com/market/commercial_cleaning_service_bid_template)
- 2026-11-10 brief: Etsy 'cleaning pricing calculator' page 1 had a janitorial bid tool at $17.00, priced above residential calculators ($7.99-$19.95). Review count not read.
- Etsy pages could not be opened this run: the one Etsy fetch was refused (permission prompt unanswered in a scheduled run). 0 Etsy pages read.

## Competition and prices
| Product | Where | Price | Format | Proof |
|---|---|---|---|---|
| Cleaning Contract Pricing Calculator (ProSheet Studio): break-even per visit/month, contract price, underpricing check, ISSA 612 production rates, 6 facility types, 6 tabs | [Payhip](https://payhip.com/b/O5aoY) | $39 ("On Sale") | XLSX, Excel + Sheets | no sales/reviews shown |
| Commercial Cleaning Bidding Tool (CleanBidsPro) | [Gumroad](https://cleanbidspro.gumroad.com/l/tkosu) | $99 | not shown | no ratings shown |
| Commercial cleaning pricing system | [Stan Store](https://stan.store/Cassmiller/p/commercial-cleaning-pricing-system?lang=en) | not read | n/a | creator-course style |
| Janitorial bid tool | Etsy (11-10 brief) | $17.00 | spreadsheet | not read |
| Free web calculators: cleaning-calcs (sq ft, days/wk, service level, restrooms, margin; no wage/production-rate inputs), Connecteam, Janitorial Manager, ContractorPlus, feesum, sweepops | [cleaning-calcs](https://cleaning-calcs.pages.dev/office-cleaning-bid/), [Connecteam](https://connecteam.com/free-tools/janitorial-bidding-calculator/), [Janitorial Manager](https://www.janitorialmanager.com/work-management-system/commercial-cleaning-calculator/) | free | web | many AI/SEO sites in 2026 |
| Bidding software (Janitorial Manager, CleanGuru-type) | [CMM list](https://cmmonline.com/articles/janitorial-bidding-estimating-software) | subscription | SaaS | established |

Read: commercial bids are priced higher ($17-$99) than residential calculators because a contract is worth thousands a year. Free web calculators are shallow (no wage, burden or production-rate inputs), which leaves room for a spreadsheet that shows the math and saves bids.

## What buyers complain about
No reviews could be read this run (Etsy blocked; Payhip/Gumroad show none). From the guides: new cleaners underprice by skipping labor burden, supplies and travel, and by guessing production rates ([Swept](https://learn.sweptworks.com/how-to-quote-a-commercial-cleaning-job)). The $39 Payhip product leads with exactly that "Am I underpricing?" pitch.

## Recommendation
Build it **only as the third SKU of the Pricing Calculator pilot**, after PW + Cleaning are live and getting views; not a separate venture. Price $9.99-$12.99 on Etsy (above residential, under the $17 rival), $19 on Gumroad. Pair with a Word/Google Docs commercial cleaning bid proposal (new idea below), since the Etsy demand pages are mostly "bid template / bid sheet" phrases. Traffic is still the bottleneck (top listing 1 view/week), so this does not beat fixing exposure. Confidence low until one Etsy page shows review counts for the $17 tool and the bid-template leaders.

**Next check (Tuesday, if Etsy fetch is allowed):** open etsy.com/market/janitorial_bid_template and the $17 janitorial tool; record review counts.

**Not revenue:** all numbers here are competitor prices and public statistics.
