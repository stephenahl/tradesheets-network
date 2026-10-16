# QA: window-cleaning business manager

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
