# QA: Pet Sitting & Dog Walking Business Manager

## 2026-10-19: PASSED (invoice blank-field fix re-test)
Tested by the QA agent at commit a373056 (Builder's invoice fix). Fresh xlsx loaded with openpyxl and recalculated in LibreOffice (UNO calculateAll); buyer steps done in LibreOffice (EXAMPLE rows deleted as rows).
- Cell-by-cell diff against the previous shipped file: only Invoice A12, A13, A14, A17 changed; 7,642 formulas; nothing else (values, validations) differs.
- Fresh file: 0 errors; demo invoice J-0003 unchanged (INV-0003 $28 + $8 = $36).
- Cleared workbook (all EXAMPLE rows deleted): 0 errors, invoice fully blank.
- Buyer test, 4 clients + 5 jobs of my own: phone-only client (no email/address), client with no service, client with address but no email, a full client, and a job for a name not in Clients. Invoices: blank address/email now print blank (old file printed "0" and "0", reproduced); no service on job or client prints "Pet care service" (old file printed "0"); job service, client service, override $100 + $15 add-on = $115, paid/due status, INV numbers all right. Unknown Job ID and blank Job ID: blank invoice. 0 errors after entry.
- Non-blocking regression: the client name on the invoice (A12) is no longer bold. In _engine/build.py and each trade build.py the `iv["A12"].font=font(bold=True)` statement ended up inside the new line's trailing # comment. Listing image 6 shows it bold. Cosmetic only; fix on the next rebuild.
- Pre-existing, not blocking: with the Job ID cell empty, the Add-on amount shows "-" (zero) on an otherwise blank invoice.
- Pet full numbers: jobs 25+5=30 (labor 0.5h×$18=9, 3 mi×$0.70=2.10, supplies 1, profit 17.90); 40 (profit 22); 100+15=115 (−2 −72 −7 = 34); 28 (16.20); 50 (32). Dashboard Oct 2026: revenue $263, job costs $141 (140.90), profit $122, unpaid $205, tax set-aside $31 (25%). Next due/status: Weekly Oct 17 Overdue, Monthly Nov 11 Scheduled, One-time —, Daily Oct 16 Overdue. All match hand math.
- Quote calculator, listing, images and guide unchanged since the 2026-10-16 pass (formulas identical; images/LISTING/guide files untouched since v1).
- Verdict: the 2026-10-16 defect is fixed. Ready to publish.

## 2026-10-16: FAILED (1 minor defect)
Tested by the QA agent on the files at commit eaf2e21 (xlsx loaded fresh with openpyxl, recalculated in LibreOffice; buyer steps done through LibreOffice so row deletion behaves as it would for a buyer). The repo xlsx is identical to a fresh `make_trade.py pet` build.

### Defect (send back to Builder)
1. **Minor: the invoice prints "0" for a blank client address or email.** Invoice A13/A14 use `IFERROR(INDEX(Clients!D/C...),"")`; when the client's Address or Email cell is empty, INDEX returns 0, so the BILL TO block shows "0" and "0" (Excel and LibreOffice; Google Sheets shows blank). My test: client "Larsen" with no address/email, invoice J-0005 → A13 = 0, A14 = 0. Pet sitters often keep phone-only clients, so this will print on real invoices. Fix: `=IFERROR(INDEX(...)&"","")` (or an IF on blank) in etsy-digital/_engine/build.py. Same formula in all 6 trades.

### What passed
- Fresh recalculation: 7,642 formulas, 0 errors. After deleting the EXAMPLE rows (Clients 2, Jobs 3, Expenses 2): 0 errors, blank invoice, all-zero dashboard, no junk.
- Example rows: all marked EXAMPLE (clients, jobs via client name, both expenses).
- Buyer test, 5 clients (Daily, Weekly, One-time, Every 2 weeks with no jobs, Monthly), 5 jobs (one $120 price override, add-ons, two unpaid, one Sep, one Dec 2025), 3 expenses (one 2025). Every number matched my hand math: price, total, labor (h × $18), mileage (mi × $0.70), profit (e.g. 135 − 5 − 72 − 7 = 51); visits, lifetime revenue (incl. add-ons), last/next due, status (Daily due today → Due soon, Weekly +1 day → Due soon, Monthly from Dec 2025 → Overdue, One-time → —, no jobs → New). Dashboard 2026: Sep 135 / 84 / 24 / 27, Oct 126 / 54.70 / 45 / 26.30, revenue $261, profit $53.30, unpaid $185, tax set-aside $13.33. Year 2025: Nov expense −30, Dec job 35 − 21.90, profit −16.90, tax set-aside $0.
- Invoice J-0004 (override + add-on): INV-0004, due +14 days, DUE, service "Overnight Stay", $120 + $15 = $135. J-0002 (no service on the job) falls back to the client's service: "Dog Walk (60 min)", $40 + $10 = $50.
- Quote calculator, default inputs: 25 + 8 + 5 + 3 + 10 = 51, −5% weekly → $48, 1.1 h, labor $19.80, profit $28.20 (matches image 3). My inputs (Overnight Stay, 14 mi, 3 pets, 2 meds, Daily, holiday fee + litter box): 90 + 16 + 10 + 6 + 23 = 145, −10% → $131, 4.85 h, labor $87.30, profit $43.70, $27.01/h. Matches.
- Dropdowns: client, service, sitter, paid, payment method, expense category, frequency (incl. Daily), quote add-ons all point at the right Settings lists. Conditional formatting: Overdue/Due soon, unpaid, negative profit. Dashboard chart present.
- Listing: title 136 chars, 13 tags all ≤20 chars, AI disclosure present. Every claim checked against the file (services, add-ons, expense categories, daily/weekly/2-week/monthly/one-time, pets/vet/access notes column, 8 tabs).
- Images (all 7 looked at): numbers match a regenerated, recalculated demo (28 clients sum to $7,509 = dashboard revenue; jobs J-0188..J-0199, invoice J-0198 $30 + $5 = $35 PAID; quote $48). Dashboard arithmetic and margins check out. No typos, no leftover pressure-washing wording.
- Quick-Start guide followed step by step; works as written.

### Notes (not blocking)
- LISTING.md photo order names files `img_1_hero` etc.; the files are `1_hero.png` etc.
- Last visit uses MAXIFS (Excel 2019/365 or Google Sheets); still worth saying "Excel 2019 or later".
- The guide still doesn't repeat the Start Here tip to clear (not delete) job rows after setup, and says "Message us on Etsy" (Gumroad buyers too).
- Dashboard top "Unpaid" card is all-time, while the table's Unpaid column is for the chosen year.
