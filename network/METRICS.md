# Metrics

Etsy shop: TradeSheetsShop (https://www.etsy.com/shop/TradeSheetsShop). Brand: TradeSheets Co.

Budget: $50, from 2026-10-14 to 2026-11-13. Spent so far: $29.00 (58%): Etsy one-time shop set-up fee $29, paid 2026-10-14 (Etsy payment confirmation email). Etsy Plus (started and cancelled 2026-10-14, runs to Nov 14) may have billed a first month; no charge amount in Gmail, needs the Etsy monthly statement (Shop Manager > Finances), so not counted yet.
Upgrade trigger (Stephen, 2026-10-15): move to the $200/month Claude plan once total real revenue reaches $20. The Analyst flags it the day revenue crosses $20.
Ad spend (Stephen approved, outside the $50 for week 1): Pinterest campaign "TradeSheets week 1" (ID 626760069079), $3/day, Oct 15 to Oct 22 (ends Oct 23 00:00 UTC), max ~$24. Etsy Ads $3/day for a week once Etsy unlocks them (~Oct 29).
Pinterest campaign actuals (Ads Manager, 2026-10-20, Oct 13-20 UTC): $13.94 spent, 3,526 impressions, 28 pin clicks, CPC $0.50. Best: pricing pins (Pressure Washing 3.7% CTR, Car Detailing 6 clicks at $0.38). Etsy stats (Oct 14-20): 38 visits (27 from Pinterest), 42 listing views, 0 favorites, 0 orders. All 5 Etsy listings active in Shop Manager (the public-page '1 active' reading was wrong).
Live 2026-10-20: 6 Etsy listings (Pet Sitting 4599722321 added) and 7 Gumroad products (6 singles + 6-trade $39 bundle). All carry the invoice-fixed xlsx.
Standing cost outside the $50 (existed before the budget): DigitalOcean droplet for the Polymarket paper bot, $6/month (Stephen, 2026-10-15). Review it if H1 fails.

| Week of | Live listings | Views | Orders | Revenue | Etsy fees | Net | Spend | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-10-12 | 5 Etsy + 6 Gumroad | 1 Etsy shop visit (wk ending Oct 16, Etsy email) | 0 | $0 | $0 | $0 | $0 | 5 live on Etsy as of 2026-10-15: Cleaning 4595582995, Lawn Care 4595734716, Pressure Washing 4595743330, Auto Detailing 4595855724, Window Cleaning 4595835191 (duplicate Cleaning 4596142179 deactivated). Gumroad: 6 live as of 2026-10-16: Cleaning, Lawn Care, Pressure Washing, Auto Detailing, Window Cleaning ($14.99 each) and the $39 5-trade bundle. Listing 1 live 2026-10-14. Checked 2026-10-14 6:50pm: Etsy shop page 1 active listing, 0 sales, 0 reviews; Gumroad public page shows no sales data; no orders logged |
| 2026-10-19 | 1 Etsy (public page, 5 recorded) + 6 Gumroad | no data yet | 0 | $0 | $0 | $0 | $0 of $50 (Pinterest ad spend not visible to Analyst) | Checked 2026-10-19 6:50pm: Etsy public page 1 active listing (Cleaning), 0 sales, 0 reviews; Gumroad public page shows no products or sales data; orders.md 0 orders; Gmail last 2 days no sale/order/review emails. Pinterest email 2026-10-18 says the first campaign is now live (it may have been in review Oct 15-18). Checked 2026-10-20 6:50pm: unchanged (Etsy 1 active listing, 0 sales, 0 reviews; Gumroad page no product data; orders.md 0; Gmail last 2 days no sale/order/review emails, Etsy 'Start the week' email has no stats). Checked 2026-10-22 6:50pm: orders.md 0 orders; Gmail (last 3 days) no sale, order or review emails; Etsy 'weekly listing performance' email (10-21): most viewed listing Auto Detailing, 14 views in the last 7 days, 0 orders. Etsy and Gumroad public pages could not be fetched this run (permission not granted). Spend now $29 of $50 (Etsy set-up fee logged). Checked 2026-10-23 6:50pm: orders.md 0 orders; Gmail (last 2 days) no sale, order or review emails (6 Etsy promos/notices only); Etsy and Gumroad public pages not fetched (permission not granted); Pinterest week-1 campaign ended Oct 23 00:00 UTC, final spend not yet visible to Analyst |

Rule: Etsy keeps about 12.5% plus $0.45 per sale on a $14.99 item (6.5% transaction fee, 3% + $0.25 payment processing, $0.20 listing renewal).

## Data sources (Analyst)
- Orders: `businesses/etsy-digital/data/orders.md`, logged by Support from order emails. Not created yet (no orders).
- Etsy: one read-only look per run at the public shop page (active listings, sales count, reviews). Views are only in Etsy Stats, so Stephen can drop a Stats CSV export in `businesses/etsy-digital/data/` when he wants view numbers tracked.
- Gumroad: the public storefront shows no sales counts; sales arrive as Gumroad emails, which Support logs into orders.md.

Last updated: 2026-10-23 6:50pm (Analyst). No new data: orders.md 0 orders; Gmail (last 2 days) only Etsy promos/notices. Revenue $0 (all time, all channels). Spend $29 of $50 (58%; Etsy Plus charge still unconfirmed). Pinterest week-1 campaign ended Oct 23 00:00 UTC; final actual not visible (last known $13.94 on 10-20). Public shop pages not fetched this run.
