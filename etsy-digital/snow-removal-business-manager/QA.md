# QA: Snow Removal Business Manager

## 2026-10-26: PASSED
Tested by the QA agent at commit a6c0ad3. Fresh xlsx loaded with openpyxl and recalculated in LibreOffice (UNO calculateAll); buyer steps done in LibreOffice (EXAMPLE rows deleted as whole rows, as the guide says). The repo xlsx is identical (0 cell diffs) to a fresh run of its build.py.
- Fresh file: 7,643 formulas, 0 errors. Demo checks: J-0001 45+25=70, costs 6+10+3.50 → profit 50.50; J-0002 160+40=200 → 137.70; J-0003 → 131.45; Nov 2026 revenue 470, job costs 150.35, Oct expenses 112.20, season profit 207.45, tax 51.86; invoice J-0003 INV-0003, Nov 20 → due Dec 4, DUE, Bright Dental $200. Invoice client name (A12) bold.
- EXAMPLE rows deleted (Clients 2, Jobs 3, Expenses 2): 0 errors, blank invoice, all-zero dashboard (Jul 2026 to Jun 2027), no junk; Jobs client dropdown still points at Clients.
- Buyer test, 4 clients (phone-only per-push, seasonal HOA with override, one-time bakery with address only, per-push church with no pushes), 5 pushes (one previous season, one service override, two unpaid, blank add-ons/materials), 3 expenses (one previous season). All match hand math:
  - Pushes: 50+25=75 (labor 0.5×$25=12.50, 6 mi×$0.70=4.20, salt 5 → 53.30); override 200 (50, 5.60, 30 → 114.40); 35+10=45 (18.75, 2.10 → 24.15); 50 (10, 4.20 → 35.80); Mar 2026 180 (37.50, 5.60, 20 → 116.90).
  - Clients: Garcia 2 pushes/$125, last Jan 15 2027, Paid up; HOA 2/$380, unpaid $200, Unpaid; Lee 1/$45, unpaid $45; Church 0, New.
  - Season 2026: Nov 75/21.70/300/1/−246.70; Dec 245/106.45/0/2/138.55 (57%), unpaid 245; Jan 50/14.20/35.80; Feb expense 150.50; totals revenue $370, profit −$222.85, 4 pushes, unpaid $245, tax set-aside $0. Season 2025: Mar 180/63.10, Jun expense 100 → profit $16.90, tax $4.23.
  - Invoices: J-0001 phone-only client prints blank address/email, falls back to client service "Driveway Plow", PAID, due Dec 2; J-0002 "Salting / De-icing" $200 DUE due Dec 16; J-0003 $45; unknown J-0099 blank.
- Quote calculator: default 45+0+10+15+20=90, −10% seasonal → $81, 0.8 h, labor $20, profit $61, $101.25/h, season $972 (= image 3). Mine: Commercial Lot Plow 12,000 sq ft, depth 3, 2 obstacles, per push, salt + haul-away: 150+40+20+165+110 = $485, 4.25 h, labor $106.25, profit $378.75, $114.12/h, season $5,820. Small (900 sq ft) snow blowing, seasonal: $36, season $432 (no negative area charge).
- Dropdowns: client, service, crew, paid, payment method, expense category/paid with/receipt, quote service/contract/add-ons all point at the right lists. Conditional formatting: Unpaid status and Paid? = No highlighted; chart present.
- Listing: title 134 chars, 13 tags (max 19 chars, no duplicates), AI disclosure present. Services, add-ons, quote factors, contract types, season dashboard, expense categories and 8 tabs all match the file. No leftover wording from other trades in the xlsx.
- Images (all 7 looked at): dashboard months sum to $14,165 revenue / 136 pushes / $6,930 profit, tax $1,732 (25%); jobs image matches the clients image unpaid balances (Bright Dental $180, Garcia, Patel, Oak Street, Rivera) and the invoice image (INV-0135 Patel $40, Mar 16 → Mar 30). Clients image shows the first 9 of the demo clients, so its totals are below the dashboard's (expected). No typos.
- Quick-start guide (1 page) followed step by step: works as written (delete EXAMPLE rows → 0 errors).

### Notes (not blocking)
- Dashboard's top "Unpaid" tile is all-time unpaid, while the table's Unpaid total is for the chosen season; they differ when viewing a past season (my test: tile $245, 2025 table $0).
- Seasonal-contract clients are logged per push at their per-push price; the guide doesn't say how to record a flat season fee (e.g. one row with a Price override). A one-line tip would help buyers who bill by the season.
- Tag "lawn care business" is a stretch for a snow product (many plow operators are lawn companies, so it's defensible); Marketer may swap it.
- Same as other trades: LibreOffice-only "Dec 30, 1899" service date when the Invoice Job ID is empty; MAXIFS needs Excel 2019/365 or Google Sheets; listing says formulas were checked for Google Sheets but QA tested in LibreOffice only; guide says "Message us on Etsy" (Gumroad buyers too).
