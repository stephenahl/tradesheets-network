# QA: auto-detailing business manager

## 2026-10-19: invoice fix PASSED (spot-check of the rebuilt xlsx for the live re-upload)
Tested by the QA agent at commit a373056 (Builder's invoice fix). Fresh xlsx loaded with openpyxl and recalculated in LibreOffice (UNO calculateAll); buyer steps done in LibreOffice (EXAMPLE rows deleted as rows).
- Cell-by-cell diff against the previous shipped file: only Invoice A12, A13, A14, A17 changed; 7,642 formulas; nothing else (values, validations) differs.
- Fresh file: 0 errors; demo invoice J-0003 unchanged (INV-0003 $180 + $45 = $225).
- Cleared workbook (all EXAMPLE rows deleted): 0 errors, invoice fully blank.
- Buyer test, 4 clients + 5 jobs of my own: phone-only client (no email/address), client with no service, client with address but no email, a full client, and a job for a name not in Clients. Invoices: blank address/email now print blank (old file printed "0" and "0", reproduced); no service on job or client prints "Detailing service" (old file printed "0"); job service, client service, override $100 + $15 add-on = $115, paid/due status, INV numbers all right. Unknown Job ID and blank Job ID: blank invoice. 0 errors after entry.
- Non-blocking regression: the client name on the invoice (A12) is no longer bold. In _engine/build.py and each trade build.py the `iv["A12"].font=font(bold=True)` statement ended up inside the new line's trailing # comment. Listing image 6 shows it bold. Cosmetic only; fix on the next rebuild.
- Pre-existing, not blocking: with the Job ID cell empty, the Add-on amount shows "-" (zero) on an otherwise blank invoice.
- Dependent numbers checked by hand: labor at $22/h = $154 total, job costs $169 (168.90), Oct 2026 revenue $263, profit $94, unpaid $205, tax set-aside $24 (25%); Monthly client next due Nov 11 (Scheduled); lifetime revenue per client includes add-ons. All match. Verdict: rebuilt xlsx is good to re-upload to the live Etsy and Gumroad listings.

## 2026-10-16 re-test (QA agent): all checks passed except 1 minor shared defect
Independent re-test on the repo files (commit eaf2e21; identical to a fresh make_trade.py build).
- **Defect (minor, all 6 trades): the invoice prints "0" for a blank client address or email** (Invoice A13/A14, Excel/LibreOffice). Not a defect in this product alone; fix in etsy-digital/_engine/build.py, rebuild, re-upload the xlsx to the live Etsy and Gumroad listings. Details in ../pet-sitting-dog-walking-business-manager/QA.md.
- Fresh: 7,642 formulas, 0 errors. Examples cleared: 0 errors, blank invoice, all-zero dashboard.
- Buyer test (4 clients: Monthly, Every 2 weeks, One-time, Weekly with no jobs; 4 jobs incl. a $700 override + $60 add-on, two unpaid, one in Nov 2025; 3 expenses incl. one 2025): every job, client and dashboard number matched hand math (Sep 940 / 400.20 / 120 / 419.80, Oct 290 / 110 / 60 / 120, profit $539.80, unpaid $940, tax set-aside $134.95; Metro Realty every-2-weeks from Sep 30 → Overdue). Invoice J-0003: INV-0003, Ceramic Coating, $700 + $60 = $760, DUE, due +14 days.
- Quote: default $329 (5.95 h, $130.90 labor) matches image; my inputs (Paint Correction, 27 mi, truck, soil 2, Weekly, engine bay + clay bar): 450 + 50 + 40 + 20 + 120 = 680, −15% → $578, 9.9 h, labor $217.80, profit $360.20. Matches.
- Listing: title 133 chars, 13 tags ≤20 chars, AI disclosure present, claims true of the file. All 7 images looked at: dashboard arithmetic, jobs (Oct 7 jobs = $2,150, unpaid $840), clients' due dates and invoice J-0052 ($500 DUE) are consistent; no typos. Guide followed; works.

## 2026-10-15: PASSED (operator self-test, same checks as the QA agent's last run)
- Fresh recalculation: 7,642 formulas, 0 errors (product and demo workbook).
- Quote calculator hand-checked (see LOG.md for the exact figures).
- Cleared-workbook test: example rows deleted -> 0 errors, blank invoice, all-zero dashboard.
- Expenses example rows are marked EXAMPLE; demo client lifetime revenue equals Jobs total charged.
- All 7 listing images looked at; trade wording checked (no pressure-washing leftovers).
- Listing: title <=140 chars, 13 tags all <=20 chars, AI disclosure present.
The scheduled QA agent should still re-test on its next run.
