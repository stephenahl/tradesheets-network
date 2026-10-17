# Metrics

Etsy shop: TradeSheetsShop (https://www.etsy.com/shop/TradeSheetsShop). Brand: TradeSheets Co.

Budget: $50, from 2026-10-14 to 2026-11-13. Spent so far: $0.00.
Upgrade trigger (Stephen, 2026-10-15): move to the $200/month Claude plan once total real revenue reaches $20. The Analyst flags it the day revenue crosses $20.
Ad spend (Stephen approved, outside the $50 for week 1): Pinterest campaign "TradeSheets week 1" (ID 626760069079), $3/day, Oct 15 to Oct 22 (ends Oct 23 00:00 UTC), max ~$24. Etsy Ads $3/day for a week once Etsy unlocks them (~Oct 29).
Standing cost outside the $50 (existed before the budget): DigitalOcean droplet for the Polymarket paper bot, $6/month (Stephen, 2026-10-15). Review it if H1 fails.

| Week of | Live listings | Views | Orders | Revenue | Etsy fees | Net | Spend | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-10-12 | 5 Etsy + 6 Gumroad | 1 Etsy shop visit (wk ending Oct 16, Etsy email) | 0 | $0 | $0 | $0 | $0 | 5 live on Etsy as of 2026-10-15: Cleaning 4595582995, Lawn Care 4595734716, Pressure Washing 4595743330, Auto Detailing 4595855724, Window Cleaning 4595835191 (duplicate Cleaning 4596142179 deactivated). Gumroad: 6 live as of 2026-10-16: Cleaning, Lawn Care, Pressure Washing, Auto Detailing, Window Cleaning ($14.99 each) and the $39 5-trade bundle. Listing 1 live 2026-10-14. Checked 2026-10-14 6:50pm: Etsy shop page 1 active listing, 0 sales, 0 reviews; Gumroad public page shows no sales data; no orders logged |

Rule: Etsy keeps about 12.5% plus $0.45 per sale on a $14.99 item (6.5% transaction fee, 3% + $0.25 payment processing, $0.20 listing renewal).

## Data sources (Analyst)
- Orders: `businesses/etsy-digital/data/orders.md`, logged by Support from order emails. Not created yet (no orders).
- Etsy: one read-only look per run at the public shop page (active listings, sales count, reviews). Views are only in Etsy Stats, so Stephen can drop a Stats CSV export in `businesses/etsy-digital/data/` when he wants view numbers tracked.
- Gumroad: the public storefront shows no sales counts; sales arrive as Gumroad emails, which Support logs into orders.md.

Last updated: 2026-10-17 6:50pm (Analyst). No sales: orders.md has 0 orders; Gmail (Etsy/Gumroad, last 2 days) has no real sale, order or review emails (only Stephen's $0 Gumroad delivery test, not revenue). Revenue $0 (all time, all channels), spend $0 of $50. Etsy weekly email (week ending Oct 16): 1 shop visit, 0 from Etsy Ads, 0 from Offsite Ads. Etsy public shop page (read 2026-10-17): 1 active listing shown, 0 sales, 0 reviews; that conflicts with the 5 live listings recorded above (flagged to operator on BOARD; may be a page-render limit). Gumroad public page: brand shows "Stephen Ahl", no products or sales in page text. Pinterest campaign actual spend still not available to the Analyst.
