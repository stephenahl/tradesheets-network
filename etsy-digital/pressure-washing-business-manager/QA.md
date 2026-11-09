# QA: Pressure Washing Business Manager

## 2026-11-06: new listing photos (quote-calculator hero + rising demo dashboard) PASSED
Tested at 6778b0f. Scope: the 7 images and LISTING.md photo order; the xlsx and guide are not part of this change.
- xlsx and guide untouched: last changed in 41730d4 (QA-passed 11-02). Engine build.py output = shipped xlsx (0 cell diffs). Shipped xlsx recalculated fresh: 7,642 formulas, 0 errors.
- Reproduced the images myself from the engine: build.py -> demo.py (ramp seed 34, 33 jobs) -> LibreOffice recalc (7,642 formulas, 0 errors) -> shots.py -> render.js. All 7 PNGs are pixel-identical to the committed ones, so every number in them comes from the recalculated workbook.
- Dashboard (image 2), recomputed from the raw job inputs (client price + add-ons; hours x $25 + supplies + miles x $0.70) and expenses, not from the formulas: Jun $860/$219, Jul $1,760/$782, Aug $1,975/$972, Sep $3,015/$1,705, Oct $3,340/$1,913 (revenue/profit); total $10,950, job costs $3,501, expenses $1,858, 33 jobs, profit $5,591, margin 51%, unpaid $1,145 (= J-0031 $495 + J-0032 $175 + J-0033 $475), tax set-aside $1,398 (25%). All match. 0 job-row mismatches. Revenue now rises every month.
- Hero (image 1) and image 3 quote: 325 + 75 + 60 (1 surface) + 60 (2,600 sq ft = 3 x 250 over 2,000 x $20) + 50 (window rinse) = 570, -5% annual = 541.50 -> $542; hours 3 + 0.75 + 0.75 + 0.75 + 0.5 = 5.75; labor $143.75; profit $398.25; $94.26/h. The shipped file's Quote Calculator shows exactly these defaults, so a buyer opening it sees the hero's $542.
- Looked at all 7 images: no typos; tab names in the window chrome match the file's 8 sheets; clients/jobs/invoice cross-check (Lakeview HOA 2 visits $915 = $420 + $495; Kim invoice $175 = J-0032; due Nov 7 = Oct 24 + 14 days). Hero readable at a 340 px thumbnail.
- Hero claims: "Pricing Calculator + Business Spreadsheet", Quote Calculator inputs and outputs are true of the file. "Instant Download" true (digital download).
- make_trade.py with the new demo.py/shots.py: all 7 other trades convert with leftovers [] (engine change doesn't break them).

### Notes (not blocking)
- "Excel & Google Sheets" badge: same claim as the live title, description and image 7, but QA has still never tested the file in Google Sheets (no access). Worth one manual check by Stephen.
- Quote shows subtotal $570, discount -$28.50, quote $542.00 (file rounds to whole dollars, unlabeled). A careful buyer may see $541.50. Pre-existing; a "(rounded)" label or ROUND to cents would remove the question.
- Photo order puts the Quote Calculator (image 3) 5th, so the buyer sees the same quote twice. Fine, but the slot could go to something new later.
- Demo oddity: Kim Residence "Roof Soft Wash" at $175 while Settings base is $450 (image 5 and the image 6 invoice). Per-client prices are allowed; pre-existing random demo data.
- Engine: demo.py's ramp loop keeps the last seed (499) silently if no seed gives a rising series; for later trades, check the printed "ramp seed" line.
- Client statuses (Overdue/Scheduled) use TODAY() at render time; re-rendering on another day can change image 4.

## 2026-11-02: bold client name re-check PASSED
Tested by the QA agent at commit 41730d4 (Builder: bold client name on Invoice A12). xlsx loaded fresh with openpyxl, recalculated in LibreOffice.
- Independent cell-by-cell diff vs the previous shipped file (41730d4~1), covering values/formulas, number formats, fonts, fills, borders, alignment, validations, conditional formats, merges and column widths: the only difference is Invoice A12 font bold False -> True. 7,642 formulas. Committed xlsx values/formulas = a fresh run of this folder's build.py.
- 0 errors fresh. Buyer test (EXAMPLE rows cleared; 3 clients incl. a phone-only client with no email/address and one with no service; 3 jobs incl. a $80 override and 2 unpaid; 2 expenses Oct/Nov): 0 errors; job prices, labor, mileage, profit, next-due/status, dashboard 2026 (revenue $195, unpaid $125, tax $0 on a loss) match hand math; invoice J-0002 shows "Ray Ortiz" bold, blank address/email, $80 total, DUE. Invoice rendered to PDF and looked at (Lawn Care, Pet Sitting): client name bold.
- Non-blocking, pre-existing (not caused by this change): the Invoice sheet has no fit-to-page setting (fitToPage off, columns A-E about 6.85 in vs 7.0 in printable at 0.75 in margins). Printed or exported to PDF from LibreOffice, the Amount column and dates spill onto a second page and "INVOICE" is cut off. Excel probably fits by a hair; untested. Fix: Invoice page setup fitToWidth=1 (fitToPage on) in _engine/build.py and each trade's build.py.
- Verdict: ready for the optional re-upload.

## 2026-10-19: invoice fix PASSED (spot-check of the rebuilt xlsx for the live re-upload)
Tested by the QA agent at commit a373056 (Builder's invoice fix). Fresh xlsx loaded with openpyxl and recalculated in LibreOffice (UNO calculateAll); buyer steps done in LibreOffice (EXAMPLE rows deleted as rows).
- Cell-by-cell diff against the previous shipped file: only Invoice A12, A13, A14, A17 changed; 7,642 formulas; nothing else (values, validations) differs.
- Fresh file: 0 errors; demo invoice J-0003 unchanged (INV-0003 $300 + $40 = $340).
- Cleared workbook (all EXAMPLE rows deleted): 0 errors, invoice fully blank.
- Buyer test, 4 clients + 5 jobs of my own: phone-only client (no email/address), client with no service, client with address but no email, a full client, and a job for a name not in Clients. Invoices: blank address/email now print blank (old file printed "0" and "0", reproduced); no service on job or client prints "Pressure washing service" (old file printed "0"); job service, client service, override $100 + $15 add-on = $115, paid/due status, INV numbers all right. Unknown Job ID and blank Job ID: blank invoice. 0 errors after entry.
- Non-blocking regression: the client name on the invoice (A12) is no longer bold. In _engine/build.py and each trade build.py the `iv["A12"].font=font(bold=True)` statement ended up inside the new line's trailing # comment. Listing image 6 shows it bold. Cosmetic only; fix on the next rebuild.
- Pre-existing, not blocking: with the Job ID cell empty, the Add-on amount shows "-" (zero) on an otherwise blank invoice.
- Dependent numbers checked by hand: labor at $25/h = $175 total, job costs $190 (189.90), Oct 2026 revenue $263, profit $73, unpaid $205, tax set-aside $18 (25%); Monthly client next due Nov 11 (Scheduled); lifetime revenue per client includes add-ons. All match. Verdict: rebuilt xlsx is good to re-upload to the live Etsy and Gumroad listings.

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

## 2026-11-09: Invoice print fit (6cba74e): PASSED
- Own cell-by-cell diff vs the previous shipped xlsx (values, formulas, number formats, fonts, fills, borders, alignment, validations, CF, merges, widths, page setup on every sheet; zip members): only Invoice page setup changed (fitToPage on, fitToWidth 1, fitToHeight 0, portrait; print area A1:E25 unchanged). Same in all 10 trades.
- Fresh LibreOffice recalc: 0 errors in all 10 (7,642 formulas; Snow 7,643).
- LibreOffice PDF export: invoice now 1 page in all 10 (workbook 108 -> 107 pages); looked at all 10 rendered: INVOICE title, dates, Amount column and TOTAL whole. Demo totals hand-checked (e.g. Auto $180+$45=$225, Pet $28+$8=$36, Snow due Nov 20+14=Dec 4).
- Buyer test (Lawn Care, Snow Removal): deleted EXAMPLE rows, added 2 clients incl. a 50-char LLC name, long suite address and long email, 2 jobs (one $25.50 add-on unpaid, one $75 override paid). 0 errors; invoice J-0001 = $145 + $25.50 = $170.50, due Nov 3+14 = Nov 17, DUE; still prints on 1 page with the long text whole.
- Not tested: Excel/Google Sheets print preview (no access); fitToPage is the standard Excel setting.
