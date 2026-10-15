# QA: Pressure Washing Business Manager

## 2026-10-15 re-test: PASSED
Re-tested by the QA agent on the files at commit 7aa6d9d (xlsx opened fresh in LibreOffice, recalculated; buyer steps done in LibreOffice so row deletion behaves as it would for a buyer).

### The 3 earlier defects: all fixed
1. Clients "Lifetime revenue" now sums Jobs Total charged (incl. add-ons). Fresh file: client lifetime totals add up to the Jobs total charged. My test: Garcia Home $140 + ($140 + $30 add-on) = $310, correct.
2. Both Expenses example rows are marked EXAMPLE in Description. Following the guide (delete the EXAMPLE rows in Clients, Jobs, Expenses) leaves no example data: dashboard all zeros, no junk.
3. Ghost invoice gone: after setup the invoice is fully blank (no INV number, status, description or total).

### Buyer test
- Fresh: 7,642 formulas, 0 errors. After deleting the example rows: 7,614 formulas, 0 errors, blank invoice, all-zero dashboard.
- Entered 4 clients (weekly, a second recurring frequency, one-time, one with no jobs), 5 jobs (one $200 price override, two add-ons, two unpaid, one in Sep, one in Dec 2025) and 3 expenses (one in 2025). Every number matched my independent calculation: price, total, labor, mileage and profit per job; visits, lifetime revenue, last/next due and status per client (Overdue / Scheduled / — for one-time / New); all 12 dashboard months, totals (revenue $795, unpaid $455, tax set-aside 25% of profit), 2025 correctly excluded; switching the year to 2025 shows only the 2025 job and expense with tax set-aside $0 on a loss; invoice J-0002 (client, address, email, service, $140 + $30 = $170, due +14 days, DUE). 0 errors after entry.
- Quote calculator, my own inputs: Roof Soft Wash, 3,100 sq ft, 3 stories, 2 surfaces, gutter brightening + sealing, every 6 months: subtotal $1,045, quote $941, 11.0 h, labor $275, profit $666, $85.55/h. Matches hand math.
- Dropdowns (client, service, staff, paid, payment method, category, frequency, quote add-ons) point at the right lists. Conditional formatting (overdue, due soon, unpaid, negative profit) and dashboard chart present.
- Listing: title 138 chars, 13 tags all <=20 chars, AI disclosure present; every claim checked against the file.
- Images: Image 4 lifetime revenue now includes add-ons (Bright Dental 2 visits = $760). Dashboard totals, quote ($542), invoice (INV-0035, $280, PAID) images recompute correctly. No typos.
- Quick-Start guide followed step by step; works as written.

### Notes (not blocking)
- Last visit uses MAXIFS, which needs Excel 2019/365 (or Google Sheets). Excel 2016 would show #NAME? in that column. Consider saying "Excel 2019 or later" in GOOD TO KNOW.
- The guide PDF doesn't repeat the Start Here tip to clear (not delete) job rows after setup; worth adding on the next rebuild.

## 2026-10-15: FAILED
Tested by the QA agent on the files in this folder (xlsx loaded fresh with openpyxl, recalculated in LibreOffice).

### What passed
- Fresh recalculation: 7,642 formulas, 0 errors. Blank workbook (all example rows cleared): 0 errors, dashboard all zeros.
- Buyer test: cleared the example rows, entered 5 clients (annual, every 6 months, one-time, quarterly, monthly with no jobs), 5 jobs (one price override, one $40 add-on, two unpaid, two in September) and 3 expenses (one dated 2025). Every number matched my hand calculation at the $25/hr labor default: e.g. J-0002 350 + 40 = 390, labor 37.50, mileage 7, profit 343.50; dashboard Sep 500 / 69.75 / 120 / 310.25, Oct 680 / 236.20 / 50 / 393.80, total profit 704.05, unpaid 540, tax set-aside 176.01; 2025 expense excluded; next due dates correct (annual +365, 6 months +182, quarterly +91; e.g. 2026-09-10 → 2026-12-10); invoice J-0002 correct.
- Quote calculator default: 325 + 75 + 60 + 60 + 50 = 570, −5% = 541.50 → $542; 5.75 h; labor $143.75; matches image 3.
- Dropdowns all point at the right lists. Dashboard chart present.
- Listing: title 138 chars, 13 tags all ≤20 chars, AI disclosure present; feature claims (frequencies, add-ons, expense categories, 8 tabs) are true of the file. Image numbers are internally consistent (e.g. Oct revenue $750 = J-0035 $280 + J-0036 $470); no typos found.

### Defects (send back to Builder)
1. **Blocking: Clients "Lifetime revenue" leaves out add-on charges.** Column K sums Jobs!H (base price) instead of Jobs!J (Total charged). My test: Miller had $350 and $350 + $40 add-on; Lifetime revenue shows $700, should be $740. Image 4 shows the same error: Lakeview HOA 4 visits = $1,680 (4 × $420) while image 5 shows its jobs at $495 and $470. Fix: SUMIFS on Jobs!$J, and re-render image 4.
2. **Blocking: the guide's setup step leaves fake data in.** Quick-Start step 3 and Start Here say "delete the rows marked EXAMPLE in Clients, Jobs and Expenses", but the 2 Expenses example rows ($64.20 chemicals, $48.00 insurance, Oct 2026) are not marked EXAMPLE, so $112.20 of fake October expenses stays in the dashboard. Fix: mark them EXAMPLE.
3. **Minor: ghost invoice after setup.** Invoice B4 defaults to J-0003, an example job. Once examples are deleted the invoice shows "INV-0003", "DUE", "Pressure washing service" and a $0 total. Fix: blank Invoice #, Status and Description when the Job ID isn't found.

### Notes (not blocking)
- Image 6 shows "PAID" in red; in the file the status is plain black text. Cosmetic.
- Job IDs are ROW()-based, so deleting a job row later renumbers the jobs below it and changes past invoice numbers.
- The APPROVALS item says this product's Gumroad copy is in `marketing/lawn-care-gumroad/`; that folder is the Lawn Care draft (looks like a copy-paste slip).
