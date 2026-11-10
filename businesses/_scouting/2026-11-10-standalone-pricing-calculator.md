# Scouting: low-price standalone Pricing / Quote Calculator per trade (Researcher, 2026-11-10)

Mode: Tuesday, but no [researcher] task in Ready, so scouting per VENTURES.md. Picked the IDEAS.md row "Low-price standalone Pricing/Quote Calculator per trade" because it is built from files we already have and bears on the 11-13 kill-rule decision.

## Bottom line
- **Score 24/25 (launch threshold 18).** Buyers on Etsy visibly pay for single-job pricing calculators, and we can cut one from the existing Quote Calculator tab in each trade manager in one Builder run.
- **It does not fix the traffic problem by itself.** Each new listing is one more search surface (~$0.20 listing fee, inside budget), but views across the shop are near zero. Treat it as a cheap, reversible test, not a rescue.
- Recommendation: pilot **2 calculators** (Pressure Washing, Cleaning) at **$6.99**, each telling buyers the full manager exists (Etsy "more from this shop" and a note in the file). Judge after 30 live days. Confidence: **medium** that buyers want the format, **low** that our 0-review listings get seen without the pending retitles and pins.

## Demand evidence
| Signal | What it shows | Source |
|---|---|---|
| "Pressure Washing Pricing Calculator - Quote, Cost & Profit Spreadsheet", $9.98, **604 reviews**, top of page 1 | One standalone calculator outsells every full business spreadsheet in that niche (next best 19 reviews) | Etsy market page read 2026-11-03 (brief 2026-11-03) |
| Etsy "cleaning pricing calculator": **5,000+ results**, all 8 readable page-1 cards are pricing/quote calculators, 7 of 8 standalone, priced **$7.99-$19.95** (median ~$12; one at $9.99 sale from $19.99) | Sellers crowd this exact format; 3 of the 8 are ads, so sellers pay to show it (a sign it sells). Review counts were not in the page text | https://www.etsy.com/market/cleaning_pricing_calculator (read 2026-11-10) |
| Etsy has indexed market pages for many single-job phrases: cleaning price/estimate calculator, residential cleaning calculator, house cleaning quote sheet, lawn care estimate calculator, lawn care quote template, pressure washing quote, power wash estimate sheet | Etsy only builds market pages for phrases people search | web search 2026-11-10 (links below) |
| RankHero "cleaning estimate": **170 Etsy searches/mo** (82% US), peaks 260 in Mar/Sep, ~489 competing listings, keyword difficulty 32/100 | Small but steady demand on just one phrasing; the others were not readable | https://www.rankhero.com/keywords/cleaning-estimate |
| Pinterest week 1: pricing pins had the best CTR (Pressure Washing 3.7%, Car Detailing 6 clicks at $0.38) | Our own audience clicks the pricing job first | METRICS.md, 2026-10-20 |

## Competition and risks
- **Crowded and cheap.** Page 1 is $4.99-$19.99; the leader is $9.98. A $6.99 entry price undercuts most of it while keeping ~85% after fees (Etsy keeps ~$0.90 on $6.99).
- **Free tools exist.** ResponsiBid, Jobber, FieldCamp and ContractorPlus give away web pricing calculators for home-service pros (lead magnets for their software). Etsy buyers still pay for a spreadsheet they own, as the 604 reviews show, but this caps the price.
- **Cannibalization.** Some buyers who would pay $14.99 for the full manager may stop at $6.99. With 0 sales so far, this is a lower risk than having no entry product.
- **Strategist rule (11-02): no new products until live listings get traffic.** This idea is small enough to sit inside that rule only if the Strategist agrees; flagged for the 11-13 review.
- Buyer complaints could not be read this run (review text not reachable). The 11-03 brief found buyers reward pricing-first titles and cheap, discounted products.

## Score (VENTURES.md rubric)
| Factor | Score | Why |
|---|---|---|
| Proof of paying buyers | 4 | 604-review leader; ads on page 1; review counts for cleaning not visible |
| Margin | 5 | ~87% digital |
| AI can do the work | 5 | Builder cuts the Quote Calculator tab via build.py/_engine |
| Reuses what we have | 5 | Same engine, Etsy shop, Gumroad, pins, upsell to existing managers |
| Fast, cheap test | 5 | One Builder run; $0.20 Etsy listing fee each; live in a day after approval |
| **Total** | **24/25** | Launch candidate (as a product-line test inside TradeSheets, not a separate venture slot) |

Auto-kill check: no ongoing Stephen time, no inventory, no regulatory risk, paying buyers visible. Passes.

## Suggested MVP (for Strategist)
- 2 files: "Pressure Washing Pricing Calculator" and "House Cleaning Pricing Calculator", Excel + Google Sheets, one tab plus a short How-to, built from the existing Quote Calculator logic (house size, surfaces, add-ons, frequency, est. hours, profit).
- Title leads with the job: `<Trade> Pricing Calculator, Quote & Estimate Spreadsheet, Excel Google Sheets, ...`.
- $6.99; hero image reuses the new "Price Every Job in 60 Seconds" design QA passed on 11-06.
- 30-day target: 3 sales across the 2, or any upsell to a full manager. Under that, kill.
- Stephen's step: approve 2 new listings (~$0.40 in fees).

## New idea found
- **Commercial / janitorial cleaning bid calculator** (office sq ft, frequency, labor rate, supplies, bid price). A "Commercial Cleaning Pricing Calculator (janitorial bid tool, Google Sheets)" sits on page 1 at $17.00, higher than residential ones; commercial cleaners bid by the job and the engine's quote logic carries over. Added to IDEAS.md as `idea`.

## What's not known
- Review counts and buyer complaints for the cleaning calculators (not in the page text).
- Search volume for "pricing calculator" phrasings per trade: RankHero and a second Etsy page (lawn_care_pricing_calculator) were blocked by an unanswered fetch permission in this unattended run.

## Sources
- https://www.etsy.com/market/cleaning_pricing_calculator (read 2026-11-10)
- https://www.etsy.com/market/pressure_washing_profit (read 2026-11-03; see businesses/etsy-digital/research/2026-11-03-views-no-orders-pressure-washing.md)
- https://www.rankhero.com/keywords/cleaning-estimate (read 2026-11-10)
- Etsy market pages found by search (not opened): https://www.etsy.com/market/cleaning_price_calculator, https://www.etsy.com/market/cleaning_estimate_calculator, https://www.etsy.com/market/residential_cleaning_calculator, https://www.etsy.com/market/house_cleaning_quote_sheet, https://www.etsy.com/market/lawn_care_estimate_calculator, https://www.etsy.com/market/lawn_care_quote_template, https://www.etsy.com/market/pressure_washing_quote, https://www.etsy.com/market/power_wash_estimate_sheet
- Free rivals: https://responsibid.com/m-free-price-calculator/, https://getjobber.com/free-tools/lawn-care-cost-calculator/, https://fieldcamp.ai/cleaning-business-software/free-tools/house-cleaning-cost-calculator/, https://contractorplus.app/resources/cost-calculator/house-cleaning-cost-calculator
- Etsy pages opened this run: 1 read, 1 blocked (permission unanswered). RankHero: 1 read, 1 blocked. $0 spent.
