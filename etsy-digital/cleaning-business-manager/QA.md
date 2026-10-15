# QA: Cleaning Business Manager v1 (live listing 4595582995)

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
