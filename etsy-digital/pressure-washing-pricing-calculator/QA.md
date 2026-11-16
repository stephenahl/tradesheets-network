# QA: Pressure Washing Pricing Calculator

## 2026-11-16: PASSED
Tested by the QA agent at commit 3afa4d3. Fresh xlsx recalculated in LibreOffice (UNO calculateAll); buyer steps done in LibreOffice (EXAMPLE rows deleted as whole rows, as the guide says). The repo xlsx is identical (0 cell diffs) to a fresh run of its build.py.
- Fresh file: 1,574 formulas, 0 errors. Default quote: 325 + 75 (2nd story) + 60 (1 surface) + 60 (2,600 sq ft = 3 × 250 over 2,000 × $20) + 50 (window rinse) = 570, −5% annual = 541.50 → $542; 5.75 h (3 + .75 + .75 + .75 + .5), labor $143.75, profit $398.25, 73%, $94.26/h, meets $75 target, target price $431, 1 visit/yr. Estimate: 520 + 50 − 28 = $542, valid Nov 16 → Dec 16. Matches LISTING.md example.
- 5 buyer scenarios vs my own Python model of the pricing rules (all 196 checks across both trades passed): Driveway 1,800 sq ft one-time $150; Roof 3,100 sq ft, 4 stories, 3 surfaces, 3 add-ons, monthly: 1,130 − 169.50 → $961, 10.25 h, 12 visits, $11,532/yr; Fence quarterly with minimum raised to $300: 180 + $120 top-up = $300 and Estimate shows a "Minimum job charge" line; Deck with target raised to $120: flagged "Below target", target price matches hours × 120; House 2,450 sq ft all 6 add-ons annual: $998. In every case the Estimate lines add up to the total and the quote date / valid-until follow my date.
- Quote Log: EXAMPLE rows deleted → all stats 0, 0 errors. My 5 rows (Won annual, Lost one-time, Pending with past follow-up, Pending with future follow-up and 0 hours, Pending with no follow-up): rate/hour, yearly value (365/days rounded), Next step (Won ✔ / Lost / Follow up now / Waiting / Set follow-up), quotes 5, win rate 50%, won per visit and yearly value, follow-ups 1 all correct. Red "Follow up now" formatting present.
- Blank calculator (all inputs cleared): 0 errors, price $0, no target message.
- Dropdowns: service and frequency point at Settings, add-ons Yes/No, status Pending/Won/Lost.
- Settings services D5:F12, factors D14:E20, add-ons D23:F29, frequency D32:F37 are identical to the Pressure Washing Business Manager's, so the "copy straight across" claim is true.
- Estimate prints/exports as 1 page in LibreOffice (looked at).
- Listing: title 133 chars, 13 tags (max 19, no duplicates), AI disclosure present; services, add-ons, 6 tabs, example numbers and rounding note all true of the file. Upsell links are the known PW listing 4595743330 and Gumroad page.
- Images (7) and Gumroad cover/thumbnail looked at: hero and estimate = $542 file defaults; Quote Log image totals hand-checked (won per visit 420+542+185+300 = $1,447; yearly 1,680+542+370+3,600 = $6,192; 4/6 = 67%); no typos.
- Quick-start guide (1 page) followed: works as written.

### Notes (not blocking)
- "Works in Google Sheets" is untested (no access), same as the other products. Formulas use standard functions only (SUMIFS, INDEX/MATCH, ROUNDUP, TEXT, COUNTIFS), so risk is low.
- With every calculator input cleared, Estimate line 1 reads "Pressure washing service — 0 sq ft,  stories,  extra surfaces" and "One-time service." Only seen in a fully blank quote.
- Guide says "File › Download as PDF" (Google Sheets wording); Excel users use File › Save As / Export. Guide says "Message us on Etsy" (Gumroad buyers too).
