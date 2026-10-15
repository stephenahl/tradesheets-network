# QA: Cleaning Business Manager v1 (live listing 4595582995)

## 2026-10-15 re-test: PASSED
Re-tested by the QA agent on the files at commit 7aa6d9d (xlsx opened fresh in LibreOffice, recalculated; buyer steps done in LibreOffice so row deletion behaves as it would for a buyer).

### The 3 earlier defects: all fixed
1. Clients "Lifetime revenue" now sums Jobs Total charged (incl. add-ons). Fresh file: client lifetime totals add up to the Jobs total charged. My test: Garcia Home $140 + ($140 + $30 add-on) = $310, correct.
2. Both Expenses example rows are marked EXAMPLE in Description. Following the guide (delete the EXAMPLE rows in Clients, Jobs, Expenses) leaves no example data: dashboard all zeros, no junk.
3. Ghost invoice gone: after setup the invoice is fully blank (no INV number, status, description or total).

### Buyer test
- Fresh: 7,642 formulas, 0 errors. After deleting the example rows: 7,614 formulas, 0 errors, blank invoice, all-zero dashboard.
- Entered 4 clients (weekly, a second recurring frequency, one-time, one with no jobs), 5 jobs (one $200 price override, two add-ons, two unpaid, one in Sep, one in Dec 2025) and 3 expenses (one in 2025). Every number matched my independent calculation: price, total, labor, mileage and profit per job; visits, lifetime revenue, last/next due and status per client (Overdue / Scheduled / — for one-time / New); all 12 dashboard months, totals (revenue $795, unpaid $455, tax set-aside 25% of profit), 2025 correctly excluded; switching the year to 2025 shows only the 2025 job and expense with tax set-aside $0 on a loss; invoice J-0002 (client, address, email, service, $140 + $30 = $170, due +14 days, DUE). 0 errors after entry.
- Quote calculator, my own inputs: Deep Clean, 2,050 sq ft, 4 bed, 3 bath, fridge + laundry, weekly: subtotal $388, quote $330, 8.0 h, labor $160, profit $170, $41.25/h. Matches hand math.
- Dropdowns (client, service, staff, paid, payment method, category, frequency, quote add-ons) point at the right lists. Conditional formatting (overdue, due soon, unpaid, negative profit) and dashboard chart present.
- Listing: title 139 chars, 13 tags all <=20 chars, AI disclosure present; every claim checked against the file.
- Images: Image 4 lifetime revenue now includes add-ons (Bright Dental $3,180); the 9 clients sum to $14,000 = dashboard revenue. Dashboard, quote ($248), invoice (INV-0094, $150, DUE) images recompute correctly. No typos.
- Quick-Start guide followed step by step; works as written.

### Notes (not blocking)
- Last visit uses MAXIFS, which needs Excel 2019/365 (or Google Sheets). Excel 2016 would show #NAME? in that column. Consider saying "Excel 2019 or later" in GOOD TO KNOW.
- The guide PDF doesn't repeat the Start Here tip to clear (not delete) job rows after setup; worth adding on the next rebuild.

## 2026-10-15: FAILED
Tested by the QA agent on the files in this folder (xlsx loaded fresh with openpyxl, recalculated in LibreOffice).

### What passed
- Fresh recalculation: 7,642 formulas, 0 errors. Blank workbook (all example rows cleared): 0 errors, dashboard all zeros.
- Buyer test: cleared the example rows, entered 5 clients (weekly, every 2 weeks, one-time, monthly, one with no jobs), 5 jobs (one price override, one $40 add-on, two unpaid, one in September) and 3 expenses (one dated 2025). Every number matched my hand calculation: job price, total, labor (hours × $20), mileage (miles × $0.70), job profit (e.g. 95 − 2 − 30 − 7 = 56); dashboard Sep 100 / 58.50 / 120 / −78.50, Oct 385 / 198.70 / 50 / 136.30, total profit 57.80, unpaid 140, tax set-aside 14.45; the 2025 expense correctly excluded; next due dates and Overdue / Due soon / New / — statuses correct for today (2026-10-15); invoice J-0002 correct (service from client, $55 + $40 add-on = $95, due +14 days, DUE).
- Quote calculator: default and my own inputs both match a hand calculation.
- Dropdowns: client, service, crew/cleaner, paid, payment method, expense category, frequency and quote Yes/No all point at the right lists.
- Listing: title 131/139 chars (≤140), 13 tags all ≤20 chars, AI disclosure present; every feature claim exists in the file (8 tabs, chart on Dashboard, highlights, invoice). Image numbers are internally consistent; no typos found.

### Defects (send back to Builder)
1. **Blocking: Clients "Lifetime revenue" leaves out add-on charges.** Column K sums Jobs!H (base price) instead of Jobs!J (Total charged). My test: Miller had jobs of $55 and $55 + $40 add-on; Lifetime revenue shows $110, should be $150. Clients total $445 vs Dashboard revenue $485. The listing images show the same error: image 4 shows Bright Dental 19 visits = $2,850 (19 × $150) while image 5 shows its jobs at $185. Fix: SUMIFS on Jobs!$J, and re-render image 4.
2. **Blocking: the guide's setup step leaves fake data in.** Quick-Start step 3 and Start Here say "delete the rows marked EXAMPLE in Clients, Jobs and Expenses", but the 2 Expenses example rows ($64.20 and $48.00, Oct 2026) are not marked EXAMPLE. A buyer following the guide keeps $112.20 of fake October expenses in the dashboard. Fix: mark them EXAMPLE (e.g. in Description or Vendor).
3. **Minor: ghost invoice after setup.** Invoice B4 defaults to J-0003, an example job. Once examples are deleted the invoice shows "INV-0003", "DUE", "Cleaning service" and a $0 total. Fix: blank Invoice #, Status and Description when the Job ID isn't found (or leave B4 empty).

### Note (not blocking)
- Job IDs are ROW()-based, so deleting a job row later renumbers every job below it and changes past invoice numbers. Consider telling buyers to clear rather than delete job rows after setup.
