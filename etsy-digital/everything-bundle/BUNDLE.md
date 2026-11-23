# Everything Bundle (2 tiers): build record, 2026-11-23

BUILD ONLY. Not published. Packages existing QA-passed files only (no new workbook). Listing copy, cover and thumbnail are the Marketer's task (BOARD, Sat 11-28); this folder is what they and QA work from.

## Tiers
| | Everything Bundle | Everything Bundle Pro |
|---|---|---|
| Price (Strategist 11-23) | $49 | $79 |
| Zip | `TradeSheets-Everything-Bundle.zip` (1,229 KB, 25 files) | `TradeSheets-Everything-Bundle-Pro.zip` (1,514 KB, 28 files) |
| 10 trade Business Managers + guides | yes | yes |
| Pressure Washing + House Cleaning Pricing Calculators + guides | yes | yes |
| Airbnb Host Business Manager + guide | no | yes |
| Client Setup License (up to 10 client businesses, for VAs, bookkeepers, coaches) | no | yes |
| START HERE PDF (contents, setup, calculator-to-manager tip) | 2 pages | 2 pages |
| Value at single prices | $163.88 (10 × $14.99 + 2 × $6.99): saves $114.88, 70% | $178.87 (+ Airbnb $14.99): saves $99.87, 56%, plus the license |

Why the Pro tier is shaped this way: with existing files only, the one extra file is Airbnb, which alone doesn't justify +$30. The license is the real Pro feature, aimed at the "coaches, bookkeepers and VAs" buyer the bundle copy already names (TradeTemplatesCo benchmark: 16-pack $99). **The license terms are a business decision for Stephen** (see APPROVALS). If he says no to the license, ship Pro as "+ Airbnb" at a lower price, or ship only the $49 tier.

## Overlap to decide with the publish
- The live Gumroad bundle is 6 trades at $39; the 10-trade $39 update (`businesses/etsy-digital/marketing/gumroad/bundle-10/`) is still unapproved. The $49 tier is that 10-trade bundle plus the 2 calculators. Selling both at $39 and $49 would undercut this one; simplest is to make the $49 Everything Bundle the bundle, and point the old URL's buyers to it.

## Delivery notes
- Etsy digital listing: up to 5 files, 20 MB each. One zip per tier fits (1.2 / 1.5 MB). Gumroad: upload the zip as the content.
- Zip layout: `00 START HERE.pdf`, `1 Business Managers/01 Cleaning ... 10 Carpet Cleaning/`, `2 Pricing Calculators/`, Pro adds `3 Short-Term Rental/` and `Client Setup License.pdf`.
- The calculators' last tab ("Full Business Manager") links to the Etsy/Gumroad manager; START HERE tells bundle buyers they already have it in folder 1. Files left unchanged because they are QA-passed.

## Checks (Builder, 2026-11-23)
- Every file in both zips is byte-identical to its source in `etsy-digital/<product>/` (sha256 in MANIFEST.md); zip integrity test passed.
- Unzipped and recalculated in LibreOffice: Everything 12 workbooks, 79,569 formulas, 0 errors; Pro 13 workbooks, 101,058 formulas, 0 errors (managers 7,642 each, Snow 7,643, calculators 1,574, Airbnb 21,489: same counts QA passed).
- Hand-checked in the bundled files after recalculation: PW calculator and PW manager default quote 325+75+60+60+50 = 570, -5% = 541.50 -> $542; House Cleaning calculator 120+20+15+56+65 = 276, -10% = 248.40 -> $248.
- START HERE (both tiers) and Client Setup License rendered to PNG (`previews/`) and looked at.

Rebuild: `python3 build.py --verify` (needs Playwright Chromium, LibreOffice, pdftoppm).
