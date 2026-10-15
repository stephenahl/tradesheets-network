# QA: Pressure Washing Business Manager

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
