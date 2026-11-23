# QA: Everything Bundle ($49) + Everything Bundle Pro ($79)

## 2026-11-23: PASSED (files). Listing copy, cover and thumbnail not made yet (Marketer, Sat 11-28): they need their own QA.
Tested at ac3ccb1, from the zips themselves (unzipped fresh, not the Builder's report).

- Zips: `unzip -t` clean on both; 25 / 28 files as stated; no junk (__MACOSX, dotfiles). Layout matches BUNDLE.md.
- Sources: my own sha256 of every extracted file equals its source in `etsy-digital/` (53/53; both START HERE PDFs and the License checked against their own files). Git history (unshallowed): the 10 managers + guides are unchanged since 6cba74e (invoice print fix, QA passed 11-09), Airbnb since 94b37e9 (QA passed 10-21, only LISTING.md/QA.md changed after), calculators since 3afa4d3 (QA passed 11-16). So the earlier buyer tests, blank-workbook and EXAMPLE-delete tests apply to these exact bytes.
- Recalculated all 13 bundled workbooks in LibreOffice: 101,058 formulas, 0 errors (managers 7,642 each, Snow 7,643, calculators 1,574 each, Airbnb 21,489). Every manager has Start Here, Dashboard, Clients, Jobs, Expenses, Quote Calculator, Invoice, Settings, matching the START HERE claim.
- START HERE claim "calculator and manager use the same Settings cells (D5:F12, E15:E20, D24:F29, D33:F37)": true. PW calculator vs PW manager and House Cleaning calculator vs Cleaning manager: 0 differing cells, no formulas in those ranges (safe to paste).
- My buyer test of that workflow: set my own prices in the PW calculator (House Soft Wash $380 / 3.5 h, story $90, surface $50, size step $25, gutter add-on $35), pasted the 4 ranges into the PW manager, quoted 3,000 sq ft, 3 stories, 2 surfaces, gutter + window rinse, annual in both. Hand math: 380+180+100+100+85 = 845, -5% = 802.75 -> $803; hours 3.5+1.5+1.5+1+1.25 = 8.75. Both files: $803 and 8.75 h.
- Per-trade "Quotes are priced by" lines match each Quote Calculator's inputs (all 10 checked).
- Value math: 10 x $14.99 + 2 x $6.99 = $163.88, saves $114.88 (70%) at $49; + $14.99 = $178.87, saves $99.87 (56%) at $79. Correct.
- Looked at START HERE (both, 2 pages each) and Client Setup License (1 page): no typos, nothing cut off, file counts right (12 / 13), AI-tools disclosure present, Etsy shop name TradeSheetsShop matches the repo.

Non-blocking notes
- "Google Sheets & Excel" is still untested in Google Sheets (no access), same as every listing.
- The calculators' last tab points to the single managers' Etsy/Gumroad pages; START HERE tells bundle buyers they already have them. Fine, though those listings should be live before the bundle publishes.
- License wording is a business/legal call for Stephen, not a QA one. It is internally consistent (10 clients, own copy per client, no resale or public sharing).
