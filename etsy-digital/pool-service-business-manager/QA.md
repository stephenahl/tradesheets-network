# QA: Pool Service Business Manager

## 2026-10-23: PASSED
Tested by the QA agent at commit a5438da. Fresh xlsx loaded with openpyxl and recalculated in LibreOffice (UNO calculateAll); buyer steps done in LibreOffice (EXAMPLE rows deleted as rows, as the guide says). The repo xlsx is identical (0 cell diffs) to a fresh run of its build.py.
- Fresh file: 7,642 formulas, 0 errors. Demo invoice J-0003: INV-0003, Oct 13 → due Oct 27, DUE, Lakeview HOA, $95 + $35 = $130. Invoice client name (A12) is bold again.
- Cleared workbook (Clients 2, Jobs 3, Expenses 2 EXAMPLE rows deleted): 0 errors, blank invoice, all-zero dashboard, no junk. Jobs client dropdown still points at Clients.
- Buyer test, 4 clients (phone-only weekly, twice-a-week HOA, one-time opening, monthly with no visits), 5 visits (one $120 override + $15 add-on, two unpaid, one Sep, one Dec 2025), 3 expenses (one 2025). All match hand math:
  - Visits: 65+12=77 (labor 0.75×$22=16.50, 5 mi×$0.70=3.50, chem 6, profit 51.00); 110 (27.50, 5.60, 18 → 58.90); 120+15=135 (22, 5.60, 20 → 87.40); opening 275+35=310 (66, 8.40, 40 → 195.60); Dec 2025 65 (→ 45.50).
  - Clients: Rivera 2 visits $142, next Oct 27 Scheduled; HOA 2/$245, last Oct 23 + 3 = Oct 26 Due soon; Kim 1/$310, —; Okafor New.
  - Dashboard 2026: Sep 310 / 114.40 / 48 / profit 147.60; Oct 322 / 124.70 / 80 / 117.30, unpaid $245; year revenue $632, profit $264.90, tax set-aside $66. 2025: Dec 65 / 19.50 / 30 → $15.50.
  - Invoices: J-0001 phone-only client prints blank address/email (no "0"), falls back to client service "Full Service Visit", PAID, due Nov 3; J-0003 $135 DUE; J-0004 "Pool Opening" $310; unknown J-0099 blank.
- Quote calculator: default 40 + 0 + 10 + 5 + 12 = 67, −5% weekly → $64, 0.8 h, labor $17.60, profit $46.40, $80/h (= image 3). Mine: Green-to-Clean, 32,000 gal, pool + spa, debris 3, one-time, shock + phosphate: 395+10+15+20+42 = $482, 4.95 h, labor $108.90, profit $373.10, $97.37/h. Small pool (10,000 gal) gets no size charge; twice a week −10%: $36.
- Dropdowns: client, service, tech, paid, payment method, expense category, frequency, quote service/frequency/add-ons all point at the right Settings lists. Conditional formatting for Overdue/Due soon present; dashboard chart present.
- Listing: title 139 chars, 13 tags (max 19 chars, no duplicates), AI disclosure present. Services, add-ons, quote factors, frequencies, gate-code notes column, expense categories and 8 tabs all match the file. No leftover wording from other trades.
- Images (all 7 looked at): dashboard months sum to $24,666 revenue / 240 jobs, profit and tax ($15,352 × 25% = $3,838) check out; jobs image matches clients image (last visits) and invoice image (J-0239 Sunset Apartments $110, due Nov 4). No typos.
- Quick-start guide (1 page) followed step by step: works as written (delete EXAMPLE rows → 0 errors).

### Notes (not blocking)
- LibreOffice only: with the Invoice Job ID cell empty, Service date shows "Dec 30, 1899" (MATCH on a blank matches the blank Job ID cells). Same formula in all trades; Excel and Google Sheets should show blank via #N/A. Optional fix: wrap E7 in IF($B$4="","",...).
- Listing says every formula was "tested" for Excel and Google Sheets; QA (and Builder) tested in LibreOffice only. Same wording on the live listings.
- Guide still says "Message us on Etsy" (Gumroad buyers too).
