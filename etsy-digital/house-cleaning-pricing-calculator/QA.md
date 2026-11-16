# QA: House Cleaning Pricing Calculator

## 2026-11-16: PASSED
Tested by the QA agent at commit 3afa4d3. Fresh xlsx recalculated in LibreOffice (UNO calculateAll); buyer steps done in LibreOffice (EXAMPLE rows deleted as whole rows). The repo xlsx is identical (0 cell diffs) to a fresh run of its build.py.
- Fresh file: 1,574 formulas, 0 errors. Default quote: 120 + 20 (3rd bedroom) + 15 (2nd bath) + 56 (2,200 sq ft = 7 × 100 over 1,500 × $8) + 35 oven + 30 baseboards = 276, −10% = 248.40 → $248; 5.6 h (2.5 + .4 + .4 + 1.05 + .5 + .75), labor $112, profit $136, 55%, $44.29/h, meets $40 target, 26 visits (365/14), $6,448/yr. Estimate: 211 + 35 + 30 − 28 = $248. Matches LISTING.md example.
- 5 buyer scenarios vs my own model (all checks passed): Deep Clean one-time $244; Office 3,100 sq ft 4 bed/3 bath + oven/windows/cabinets monthly $445 (12 visits); Airbnb Turnover with minimum raised to $300: $95 + $205 top-up; Move-out with target raised to $120: flagged Below target; Standard all 6 add-ons weekly $370 (52 visits). Estimate lines always add up to the total.
- Quote Log: EXAMPLE rows deleted → stats 0, 0 errors; my 5 rows give correct rate/hour, yearly value, Next step, win rate and follow-up count.
- Blank calculator: 0 errors, price $0.
- Settings services, factors, add-ons and frequency cells are identical to the Cleaning Business Manager's ("copy straight across" is true).
- Estimate exports as 1 page in LibreOffice (looked at).
- Listing: title 133 chars, 13 tags (max 19, no duplicates), AI disclosure present; claims match the file. Upsell links are the known Cleaning listing 4595582995 and Gumroad page.
- Images (7) and Gumroad cover/thumbnail looked at: hero/estimate = $248 defaults; Quote Log image hand-checked (won per visit 248+310+295+140 = $993; yearly 6,448+310+295+7,280 = $14,333; 67%); no typos.
- Quick-start guide followed: works as written.

### Notes (not blocking)
- Google Sheets untested (no access); standard functions only.
- Settings labels "Extra hours per bedroom / per bathroom" don't say "(over 2)" / "(over 1)" though the formula applies that (the price labels do say it).
- Blank calculator: Estimate line 1 reads "House cleaning service — 0 sq ft,  bed /  bath". Guide "File › Download as PDF" and "Message us on Etsy" wording as in the PW file.
