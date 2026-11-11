# Gumroad storefront fix: tradesheetsshop.gumroad.com

Marketer, 2026-11-11. Draft only; applying it needs Stephen's Gumroad login (APPROVALS item).

## What the public page shows today (checked 2026-11-11)
- Profile page https://tradesheetsshop.gumroad.com/ : HTTP 200, title and og:title "Subscribe to Stephen Ahl", meta description "Get the latest products and updates from Stephen Ahl on Gumroad." No bio. Static HTML has no product list (the page is JS-rendered; a headless browser could not reach gumroad.com from the cloud, so whether products show on the profile is still unconfirmed).
- Bundle https://tradesheetsshop.gumroad.com/l/service-business-manager-bundle : live, $39, "Service Business Manager Bundle: 6 Spreadsheets for Cleaning, Lawn Care, Pressure Washing, Auto Detailing, Window Cleaning & Pet Sitting".
- Pet Sitting https://tradesheetsshop.gumroad.com/l/pet-sitting-dog-walking-business-manager : live, $14.99.
- Pool Service https://tradesheetsshop.gumroad.com/l/pool-service-business-manager : fetch failed (client error, no page). Consistent with Pool not being on Gumroad yet (open Gumroad approval item).
- Problem: every buyer who clicks the seller link or the profile sees a personal name, not the brand, and the brand (TradeSheets Co., used on Etsy and Pinterest) never appears. The 2026-10-14 setup kit asked for name "TradeSheets Co."; it was not applied.

## Settings → Profile (about 3 minutes)
- **Name:** `TradeSheets Co.`
- **Profile picture / logo:** `avatar-500.png` (this folder; same icon as the Etsy shop and Pinterest)
- **Bio:**
  > Spreadsheet templates that run a service business: pricing calculator, quotes, clients, jobs, invoices and profit in one file. Built for cleaners, lawn care, pressure washing, detailing, window cleaning and pet sitters. Instant download, Excel (also opens in Google Sheets).
- Social link: Pinterest https://www.pinterest.com/tradesheetsshop/ (and the Etsy shop link if the field allows a website).
- Username stays `tradesheetsshop` (changing it would break every live link).

## Public profile → Edit profile (about 5 minutes)
Add sections in this order (Gumroad's profile editor; names may differ slightly):
1. **Featured product:** Service Business Manager Bundle ($39). It is the best value and the one product every trade page already points to.
2. **Products** section titled `Pick your trade`, in this order: Cleaning, Lawn Care, Pressure Washing, Auto Detailing, Window Cleaning, Pet Sitting & Dog Walking. Check that all 6 singles + bundle (7 live products) appear and none are hidden/unlisted.
3. Optional **text** section:
   > One spreadsheet per trade. Type in a job and it prices the quote, tracks the client, fills the invoice and updates your monthly profit. $14.99 each, or all 6 for $39.

When Pool, Snow, Handyman and Carpet go live on Gumroad, add them to `Pick your trade` and update the bundle count in the bio/text.

## Check after saving
Open the profile logged out (private window): title should read TradeSheets Co., the bundle shows first, 7 products listed, avatar shows. Note it in LOG.md.
