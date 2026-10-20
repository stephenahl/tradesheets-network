# Board

## Ready
- [builder] AFTER Stephen APPROVES the Airbnb venture (see APPROVALS): add key `airbnb` to make_trade.py, build the Airbnb Host Business Manager, guide, 7 images, LISTING.md; apply the invoice blank-field fix first. Plan: businesses/_proposals/airbnb-host-business-manager.md, 2026-10-19
- [qa] AFTER the Airbnb build: full buyer test, 2026-10-19
- [marketer] After the invoice-fix QA pass: rebuild the 6-trade bundle zip from the fixed xlsx (build_gumroad.py), 2026-10-19
- [marketer] AFTER the Airbnb QA pass: Gumroad copy/cover/thumb, SEO title + 13 tags, 5 pins, 2026-10-19
- [researcher] Thu: scout next venture (guide kits 22, dashboards 21); evidence only, 2026-10-19
- [analyst] Log the $29 Etsy shop set-up fee (paid 2026-10-14, Etsy email) in METRICS spend, and check the Etsy monthly statement for an Etsy Plus charge (started and cancelled 10-14, runs to Nov 14). See businesses/etsy-digital/research/2026-10-20-etsy-visibility-and-views.md, 2026-10-20
- [strategist] Next Mon: if no Airbnb sales/views signal, judge the 30-day kill rule for TradeSheets (due ~2026-11-13: <3 sales across listings = pivot), 2026-10-19
- [marketer] After Nov 3: re-pin the top 3 organic pins by outbound clicks to a second board (needs Pinterest analytics via Chrome on the Mac), 2026-10-16
- [builder] Low priority, next rebuild: restore bold client name on Invoice A12 (the `iv["A12"].font=font(bold=True)` statement is inside the trailing # comment in _engine/build.py and all 6 trade build.py; image 6 shows it bold). Not blocking; QA re-checks only that cell, 2026-10-19
- [builder] Next trade per research brief: Pool Service (Snow Removal if time before Nov); Pet Sitting done 10-16, businesses/etsy-digital/research/2026-10-15-next-10-trades.md, 2026-10-15
- [strategist] First weekly plan, and seed IDEAS.md with 5 non-Etsy business ideas that fit an AI operator with a $50 budget, 2026-10-14
- [marketer] For each new product: Gumroad copy, cover and thumbnail (done through Pet Sitting; add the trade to TRADES/NEW in businesses/etsy-digital/marketing/gumroad/build_gumroad.py, which also rebuilds the bundle-<n>/ draft), 2026-10-14
- [marketer] Gumroad storefront (tradesheetsshop.gumroad.com) shows seller name "Stephen Ahl" and no products in the public page text; check the profile name/brand (TradeSheets Co.) and that the product is visible on the profile, 2026-10-14

- [marketer] Traffic is near zero: Etsy weekly email shows 1 shop visit for week ending Oct 16, 0 from ads, despite the Pinterest campaign since Oct 15 (pins may link to Gumroad/still in review). Check where ad and organic pins send clicks (Marketer 10-17: repo pin kits link every trade pin to its Etsy listing and only the 2 bundle pins to Gumroad; next step needs Pinterest Analytics/Ads Manager on the Mac: outbound clicks per pin, and confirm the live pin links match), 2026-10-17

## Doing

## Blocked

## Done
- [operator] Verified 5 of 5 Etsy listings active in Shop Manager; logged Pinterest actuals ($13.94, 3,526 impr, 28 clicks); uploaded the QA-passed invoice-fix xlsx to all 5 Etsy listings and all 5 Gumroad single products (bundle zip still needs the Marketer rebuild), 2026-10-20
- [stephen] Etsy suggests clearer titles for 4 listings (Shop Manager > Etsy search visibility > Update titles); Claude's attempt to publish them was blocked, so Stephen reviews and clicks Publish, 2026-10-20
- [researcher] Etsy 1-of-5 / near-zero views: no deactivation, review or pause email from Etsy; '1 active' is an unverified automated read (Shop Manager showed 6 active on 10-15); views too early to judge (shop open 10-15, ads live 10-18, pins from 10-19). Found $29 set-up fee not in METRICS. Brief: businesses/etsy-digital/research/2026-10-20-etsy-visibility-and-views.md, 2026-10-20
- [qa] Re-tested the invoice fix: Pet Sitting PASSED (ready to publish) and all 5 live-trade xlsx PASSED (ready to re-upload). 0 errors fresh/cleared/buyer test; blank address, email and service print blank; dashboards match hand math. 1 cosmetic note (client name not bold), 2026-10-19
- [builder] Invoice blank-field fix in _engine/build.py and all 6 trades (A13/A14 address/email, plus A12 client and the A17 description fallback that also showed 0); all 6 xlsx rebuilt: 7,642 formulas, 0 errors each; old file reproduces the defect, new one shows blanks; demo invoices and images unchanged. Pet Sitting back to QA; live re-uploads in APPROVALS, 2026-10-19
- [marketer] Pet Sitting & Dog Walking Gumroad draft (GUMROAD.md, cover, thumbnail) and 6-trade bundle update draft ($39 kept, BUNDLE.md, cover, thumbnail, 693 KB zip) in businesses/etsy-digital/marketing/gumroad/; both wait on QA pass + Stephen, 2026-10-17
- [qa] Tested Pet Sitting & Dog Walking (FAILED: 1 minor defect, invoice shows 0 for a blank client address/email) and re-tested Auto Detailing and Window Cleaning (all checks passed except the same shared invoice defect). 0 errors, buyer tests and quotes match hand math, images match, 2026-10-16
- [builder] Pet Sitting & Dog Walking Business Manager built via make_trade.py ('pet'): 7,642 formulas, 0 errors (demo and cleared-workbook too); quote hand-checked ($48); 7 images and guide reviewed; LISTING.md; awaiting QA, 2026-10-16
- [operator] Organic pin kit: 16 pins (Lawn Care x5, Pressure Washing/Auto Detailing/Window Cleaning pins 3-5, 2 bundle pins) with copy and a 1-a-day schedule in businesses/etsy-digital/marketing/organic-pins/; every trade now has 5 pins. Scheduled on Pinterest (Oct 19 to Nov 3), 2026-10-16
- [stephen] Gumroad tax info and payout bank set, 2026-10-15
- [operator] Published Pressure Washing, Auto Detailing, Window Cleaning and the $39 bundle on Gumroad (all APPROVED); bundle line added to all 5 single descriptions; 6 live products, 2026-10-16
- [operator] Gumroad drafts for Pressure Washing, Auto Detailing, Window Cleaning and the 5-trade $39 bundle (copy, covers, thumbnails, bundle zip) in businesses/etsy-digital/marketing/gumroad/, 2026-10-15
- [researcher] Scouting: scored 8 seeded ideas (killed Fiverr service and lead-gen sites); top is Airbnb Host Business Manager spreadsheet, 24/25, launch candidate for Strategist's Monday pick. Brief: businesses/_scouting/2026-10-15-airbnb-host-manager.md, 2026-10-15
- [support] Created businesses/etsy-digital/data/orders.md (empty; 0 orders so far), 2026-10-15
- [researcher] Ranked next 10 trades: 1 pet sitting/dog walking, 2 pool service, 3 handyman, 4 carpet cleaning, 5 painting, 6 snow removal (timely), 7 pest control, 8 electrician, 9 plumbing/HVAC, 10 junk removal. Brief: businesses/etsy-digital/research/2026-10-15-next-10-trades.md, 2026-10-15
- [operator] Cleaning pins: 1 and 2 live; 3/4/5 scheduled in Pinterest (Oct 16-18, noon), no Mac needed. Tip for Marketer: use Pinterest's 'Publish at a later date' to schedule future pins in one session, 2026-10-15
- [operator] Built Auto Detailing and Window Cleaning Business Managers via etsy-digital/make_trade.py (adapter over the pressure-washing generator): 7,642 formulas, 0 errors each; quotes hand-checked ($329 detailing, $452 windows); cleared-workbook test passed; 7 images each reviewed, 2026-10-15
- [operator] StarNet Network HQ v2 live: installed into StarNet's plugin folder (backup starnet-local/backups/installed-agent-network-20261015-040248), approved on Stephen's instruction, reading the GitHub clone (synced 10:04pm), 2026-10-14
- [qa] Re-tested Cleaning, Lawn Care and Pressure Washing: all PASSED (3 defects fixed; 0 errors; buyer test and quotes match hand math). Lawn Care and Pressure Washing can publish; Cleaning needs the fixed file re-uploaded, 2026-10-15
- [operator] Fixed QA's 3 defects in build.py for Cleaning, Lawn Care and Pressure Washing (lifetime revenue sums Jobs!J; Expenses examples marked EXAMPLE; invoice blank when Job ID not found; Start Here tip to clear, not delete, job rows). Rebuilt: 7,642 formulas, 0 errors each; images re-rendered; pins unchanged (pin 3 crop excludes revenue), 2026-10-14
- [qa] Tested Lawn Care, Cleaning and Pressure Washing Business Managers: all FAILED (same 3 defects from the shared build.py, sent to Builder), 2026-10-15
- [marketer] Lawn Care Gumroad draft: name, description, cover 1280x720, square thumbnail in businesses/etsy-digital/marketing/lawn-care-gumroad/; publishes under the existing Lawn Care approval after QA, 2026-10-15
- [operator] Pressure Washing Business Manager built: 0 formula errors, quote math hand-checked ($542 test quote), 7 images, guide, listing, 2026-10-14
- [marketer] Cleaning Business Manager launch kit: 5 pins (1000x1500) + titles, descriptions, alt text, boards, schedule and launch checklist in businesses/etsy-digital/marketing/cleaning-launch/; posting awaits approval, 2026-10-15
- [analyst] METRICS.md tracking set up; data sources defined in METRICS.md, 2026-10-14
- [operator] Lawn Care Business Manager built: 7,642 formulas, 0 errors, quote math hand-checked, 7 images, guide, listing, 2026-10-14
- [operator] Etsy shop TradeSheetsShop opened; listing 1 published, 2026-10-14
- [operator] Cleaning Business Manager v1 built and tested, 2026-10-14
