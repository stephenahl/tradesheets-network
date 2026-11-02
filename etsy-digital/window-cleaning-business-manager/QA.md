# QA: window-cleaning business manager

## 2026-11-02: bold client name re-check PASSED
Tested by the QA agent at commit 41730d4 (Builder: bold client name on Invoice A12). xlsx loaded fresh with openpyxl, recalculated in LibreOffice.
- Independent cell-by-cell diff vs the previous shipped file (41730d4~1), covering values/formulas, number formats, fonts, fills, borders, alignment, validations, conditional formats, merges and column widths: the only difference is Invoice A12 font bold False -> True. 7,642 formulas. Committed xlsx values/formulas = a fresh run of this folder's build.py.
- 0 errors fresh. Buyer test (EXAMPLE rows cleared; 3 clients incl. a phone-only client with no email/address and one with no service; 3 jobs incl. a $80 override and 2 unpaid; 2 expenses Oct/Nov): 0 errors; job prices, labor, mileage, profit, next-due/status, dashboard 2026 (revenue $195, unpaid $125, tax $0 on a loss) match hand math; invoice J-0002 shows "Ray Ortiz" bold, blank address/email, $80 total, DUE. Invoice rendered to PDF and looked at (Lawn Care, Pet Sitting): client name bold.
- Non-blocking, pre-existing (not caused by this change): the Invoice sheet has no fit-to-page setting (fitToPage off, columns A-E about 6.85 in vs 7.0 in printable at 0.75 in margins). Printed or exported to PDF from LibreOffice, the Amount column and dates spill onto a second page and "INVOICE" is cut off. Excel probably fits by a hair; untested. Fix: Invoice page setup fitToWidth=1 (fitToPage on) in _engine/build.py and each trade's build.py.
- Verdict: ready for the optional re-upload.

## 2026-10-19: invoice fix PASSED (spot-check of the rebuilt xlsx for the live re-upload)
Tested by the QA agent at commit a373056 (Builder's invoice fix). Fresh xlsx loaded with openpyxl and recalculated in LibreOffice (UNO calculateAll); buyer steps done in LibreOffice (EXAMPLE rows deleted as rows).
- Cell-by-cell diff against the previous shipped file: only Invoice A12, A13, A14, A17 changed; 7,642 formulas; nothing else (values, validations) differs.
- Fresh file: 0 errors; demo invoice J-0003 unchanged (INV-0003 $45 + $25 = $70).
- Cleared workbook (all EXAMPLE rows deleted): 0 errors, invoice fully blank.
- Buyer test, 4 clients + 5 jobs of my own: phone-only client (no email/address), client with no service, client with address but no email, a full client, and a job for a name not in Clients. Invoices: blank address/email now print blank (old file printed "0" and "0", reproduced); no service on job or client prints "Window cleaning service" (old file printed "0"); job service, client service, override $100 + $15 add-on = $115, paid/due status, INV numbers all right. Unknown Job ID and blank Job ID: blank invoice. 0 errors after entry.
- Non-blocking regression: the client name on the invoice (A12) is no longer bold. In _engine/build.py and each trade build.py the `iv["A12"].font=font(bold=True)` statement ended up inside the new line's trailing # comment. Listing image 6 shows it bold. Cosmetic only; fix on the next rebuild.
- Pre-existing, not blocking: with the Job ID cell empty, the Add-on amount shows "-" (zero) on an otherwise blank invoice.
- Dependent numbers checked by hand: labor at $22/h = $154 total, job costs $169 (168.90), Oct 2026 revenue $263, profit $94, unpaid $205, tax set-aside $24 (25%); Monthly client next due Nov 11 (Scheduled); lifetime revenue per client includes add-ons. All match. Verdict: rebuilt xlsx is good to re-upload to the live Etsy and Gumroad listings.

## 2026-10-16 re-test (QA agent): all checks passed except 1 minor shared defect
Independent re-test on the repo files (commit eaf2e21; identical to a fresh make_trade.py build).
- **Defect (minor, all 6 trades): the invoice prints "0" for a blank client address or email** (Invoice A13/A14, Excel/LibreOffice). Reproduced here: client "Hill Bakery" with no address/email, invoice J-0001 → BILL TO shows 0 and 0. Fix in etsy-digital/_engine/build.py, rebuild, re-upload the xlsx to the live Etsy and Gumroad listings.
- Fresh: 7,642 formulas, 0 errors. Examples cleared: 0 errors, blank invoice, all-zero dashboard.
- Buyer test (4 clients: Every 2 weeks, Every 6 months, One-time, Quarterly with no jobs; 5 jobs incl. a $250 override, add-ons, two unpaid, one Oct 2025; 3 expenses incl. one 2025): every number matched hand math (Apr 360 / 91.40 / 50 / 218.60, Sep 65 / 15.10 / 0 / 49.90, Oct 290 / 99.60 / 210 / −19.60; revenue $715, profit $248.90, unpaid $315, tax $62.23; Dana Cole every 6 months from Apr 10 → due Oct 9 → Overdue). Invoice J-0001 falls back to the client's service (Storefront Route), $40, PAID.
- Quote: default $452 (6.55 h) matches image; my inputs (Exterior Windows, 45 panes, 3 stories, 0 French, Monthly, screens + solar): 180 + 100 + 0 + 120 + 120 = 520, −10% → $468, 6.3 h, labor $138.60, profit $329.40. Matches.
- Listing: title 132 chars, 13 tags ≤20 chars, AI disclosure present, claims true of the file. All 7 images looked at: dashboard arithmetic (Jun–Oct sum to $9,100; tax $1,234), jobs (Oct 7 jobs = $1,205, unpaid $425), client due dates and invoice J-0051 ($210 PAID) are consistent; no typos. Guide followed; works.

## 2026-10-15: PASSED (operator self-test, same checks as the QA agent's last run)
- Fresh recalculation: 7,642 formulas, 0 errors (product and demo workbook).
- Quote calculator hand-checked (see LOG.md for the exact figures).
- Cleared-workbook test: example rows deleted -> 0 errors, blank invoice, all-zero dashboard.
- Expenses example rows are marked EXAMPLE; demo client lifetime revenue equals Jobs total charged.
- All 7 listing images looked at; trade wording checked (no pressure-washing leftovers).
- Listing: title <=140 chars, 13 tags all <=20 chars, AI disclosure present.
The scheduled QA agent should still re-test on its next run.
