# QA: Airbnb Host Business Manager

## 2026-10-21: PASSED (re-test of the #REF! fix)
Tested by the QA agent on the files at commit 94b37e9 (xlsx, guide and Start Here changed; images unchanged since 5c72bab). LibreOffice (UNO calculateAll), buyer steps done in LibreOffice. TODAY = 2026-10-21.
- Fresh: 21,489 formulas, 0 errors.
- Defect 1 fixed: deleting the EXAMPLE rows (Properties 5, Bookings 5-6, Expenses 5-6) gives 0 errors (was 15 #REF!); clearing their contents also 0. Blank workbook: Dashboard shows "-", by-property rows, Settings L5 picker and Pricing B5 blank, no junk.
- New buyer test, run both ways (rows deleted / contents cleared), identical results, 0 errors:
  - Properties: Maple Studio ($100/$140, clean $60, cleaner $40, 2 incl, $15 extra), Ridge House ($200/$260, $120, $80, 4 incl, $25).
  - Bookings: Thu-Sun Maple Airbnb 3 guests: $100+2x$140=$380 + $45 extra + $60 = $485, 3% $14.55, payout $470.45, net $430.45. Ridge 7 nights Vrbo, -$50: $1,520-10%=$1,368+$120-$50=$1,438, 8% $115.04, payout $1,322.96, net $1,242.96. Maple direct Nov 29-Dec 2, unpaid: $360, $10.80, $349.20, net $309.20. Ridge Booking.com 6 guests, actual payout $500: $400+$100+$120=$620, fee $120, net $420. Cancelled Maple stay excluded everywhere.
  - Dashboard 2026: payout $2,642.61, profit $2,297.61, unpaid $349.20, tax set-aside $574.40, 15 nights / 730 = 2%, ADR $2,448/15 = $163. Nov 14 nights / 60 = 23%, ADR $168, RevPAR $39, payout $2,526.21, cleaning $226.67, expenses $105, profit $2,194.54; Dec 1 night, $116.40 / $13.33 / $103 (cross-month stay split 2/1). By property: Maple 6 nights $819.65 payout, $664.65 profit; Ridge 9, $1,822.96, $1,662.96; shared -$30; sum = year profit.
  - Monthly Summary (Ridge House): Nov 9 nights, 30%, ADR $196, rent $1,768, 2 stays, avg 4.5, cleaning fees $240, platform fees $235.04.
  - Turnovers: Nov 8 Maple -> next check-in Nov 29 (cancelled Nov 20 skipped), gap 21; Nov 16 Ridge SAME-DAY, next guests 6. Properties status Vacant, next check-in Nov 5 / Nov 9.
  - Pricing (Ridge, Fri Dec 11, 7 nights, 7 guests, Booking.com): 2 weekend + 5 weekday, $1,520-$152+$120+$525 = $2,013, fee $301.95, payout $1,711.05, net $1,631.05, $233.01/night. Break-even ((2400+6.587x80)/0.85-6.587x120)/19.76 = $134.26; target-profit rate $193.80.
- Guide (1 page) and Start Here C27 now say clear the contents; followed exactly, works.
- Images unchanged and previously checked; 7_included re-checked, claims true.
- Non-blocking notes: (a) LISTING.md 'How it works' step 3 still says 'delete the example rows' (works now, but differs from the guide); low-priority Builder task added. (b) If a buyer deletes Properties rows, the fixed ranges shrink (A5:A23) while the whole-column INDEX still reads row 24, so a 20th property would show on the Dashboard but not price its bookings; only matters for 20 listings after deleting rows, which the guide says not to do. (c) Google Sheets still not tested (no access); worth one open before publish.

## 2026-10-21: Builder fix for defect 1 (re-test needed)
- Dashboard A27:A46 and Settings L5:L24 now use `=IF(INDEX(Properties!$A:$A,n)="","",INDEX(Properties!$A:$A,n))` (whole-column INDEX, so deleting rows can't break it); Pricing Calculator B5 default is the same for row 5.
- Guide step 3 and Start Here C27 now say clear the contents (select, press Delete), don't delete the rows. Guide still 1 page.
- Cell diff vs 5c72bab: 42 cells (20 Dashboard, 20 Settings, Pricing B5, Start Here text). Images unchanged (byte-identical except image 6, which only differs by TODAY status, so the QA-checked image 6 is kept).
- LibreOffice (UNO) re-test, both ways: deleting the EXAMPLE rows 0 errors (old file: 15), clearing contents 0 errors; then 2 properties + 2 bookings: 0 errors both ways, Dashboard rows show Pine Loft $464.10 / Beach House $1,827.40 profit, picker and Pricing B5 show Pine Loft. Hand math: $420+$80+$30=$530, 3% fee $15.90, net $464.10; 7 nights $1,850-10%=$1,665+$150+$280=$2,095, 8% $167.60, net $1,827.40; Pricing 3 nights 5 guests $590, fee $17.70.

## 2026-10-20: FAILED (1 major defect)
Tested by the QA agent on the files at commit 5c72bab. xlsx loaded fresh with openpyxl and recalculated in LibreOffice (UNO calculateAll); buyer steps done through LibreOffice so row deletion behaves as it would for a buyer. TODAY = 2026-10-20.

### Defect (send back to Builder)
1. **Major: following the guide's step 3 ("Delete the rows marked EXAMPLE in Properties, Bookings and Expenses") leaves permanent #REF! errors.** Several cells point straight at `Properties!A5`, so deleting that row breaks them:
   - Dashboard A27 `=IF(Properties!A5="","",Properties!A5)` → #REF!, so the whole first BY PROPERTY row (A27:L27) and Shared costs H47/I47 show #REF!.
   - Settings L5 (property picker) → #REF!, which puts "#REF!" into the Monthly Summary property dropdown.
   - Pricing Calculator B5 `=Properties!A5` → #REF! until the buyer picks a property.
   - Fresh file deleted this way: 15 errors. After I then entered my own 2 properties, 5 bookings and 3 expenses: still 14 errors (Dashboard row 27, H47/I47, Settings L5). It never recovers, and the Dashboard is the first thing a buyer looks at.
   - Side effect: row deletion also shrinks every range (Properties A5:A23 = 19 listings, not 20; Bookings 5:1002).
   - Start Here C27 says the same ("Delete them when you start").
   - Fix: make these cells survive row deletion, e.g. `=IF(INDEX(Properties!$A$5:$A$24,n)="","",INDEX(Properties!$A$5:$A$24,n))` for Dashboard A27:A46 and Settings L5:L24, and Pricing B5 `=INDEX(Properties!$A$5:$A$24,1)` (or a plain text default). Also say "clear the contents of" in the guide and Start Here, as a second line of defence. Then re-check the cleared workbook with rows deleted *and* with contents cleared.

### What passed
- Fresh recalculation: 21,489 formulas, 0 errors. MINIFS is written as `_xlfn.MINIFS` (correct for Excel); no other post-2010 functions.
- Clearing the EXAMPLE contents (instead of deleting rows): 0 errors, all-zero dashboard, no junk.
- Buyer test, my own data (contents cleared): Pine Loft ($120/$150, clean $80, cleaner $50, 2 incl, $10 extra, listed 2026-09-15) and Beach House ($250/$300, $150, $100, 6 incl, $20). 5 bookings: Fri-Mon Airbnb 3 guests; 7-night Vrbo 8 guests crossing Oct/Nov; 1-night direct, -$20, unpaid, same-day turnover; Airbnb with actual payout $300; a cancelled Booking.com stay. 3 expenses (one shared). Every number matched my hand math:
  - Bookings: $420 rent + $80 + $30 extra = $530, fee $15.90, payout $514.10, net $464.10; 7 nights 1,850 − 10% = $1,665 + $150 + $280 = $2,095, fee $167.60, payout $1,927.40; $180 / $5.40 / $174.60; actual payout $300 → fee $50; cancelled excluded.
  - Dashboard 2026: payout $2,916.10, profit $2,346.10, occupancy 13/473 = 2.75% (Pine Loft available from Sep 15 = 108 nights), ADR $190.38, unpaid $174.60, tax set-aside $586.53. Oct: 10 nights / 62 = 16.1%, ADR $176.14, payout $2,090.07, cleaning $207.14, expenses $120, profit $1,762.93 (7-night stay split 4/7). Nov: 3 nights / 60 = 5%, profit $583.17. By property: Pine $748.70, Beach $1,627.40, shared −$30.
  - Monthly Summary: Oct stays 4, avg 3.25, cleaning fees $325.71, platform fees $167.07; Pine Loft only: Oct 6 nights, 19.4%, ADR $135.
  - Turnovers: Oct 26 Pine SAME-DAY (next guest 2), Oct 27, Nov 4 (cancelled stay correctly not shown as next check-in). Properties: both Vacant, next check-in Oct 23 / Oct 28, upcoming 2 / 1.
  - Pricing Calculator (Beach House, Fri Dec 4, 7 nights, 7 guests, direct): 2 weekend + 5 weekday, 1,850 − 185 + 150 + 140 = $1,955, fee $58.65, net $1,796.35, $256.62/night. Break-even $109.58, target-profit rate $161.75.
  - Double booking flags both rows; check-out before check-in shows "Check dates" and is excluded. Supplies: 10 on hand vs reorder at 12 → Reorder, qty 14, $7.70.
- Dropdowns: property, channel, status, paid, cleaner, clean done, expense property/category/payment, supplies property, pricing property/channel, Monthly Summary property all present and point at the right lists.
- Listing: title 137 chars, 13 tags all ≤20, AI disclosure present, not-affiliated line present. Every feature claim is true of the file.
- Images (all 7 looked at): no typos; numbers match demo.py's workbook recalculated by me (payout $112,618.54, profit $36,374.89, occupancy 50.3%, ADR $183.35, unpaid $2,153.40, per-property rows); spot-checked booking rows (e.g. Thu-Sat $585, 3% = $20.40) and the supplies reorder total $31.45.
- Guide (1 page): every step works except step 3 (defect 1).
- Not tested: Google Sheets (no Google account access in the QA run). Every function used (MINIFS, SUMPRODUCT, COUNTIFS, SUMIFS, WEEKDAY, TEXT, TODAY) exists in Google Sheets, but a person should open it there once before publishing.
