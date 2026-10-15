# Product engine (the pressure-washing pipeline every trade is cloned from)

All five trade products were made from these files. Scheduled Builders start in a fresh workspace, so the pipeline lives here, not in anyone's scratch folder.

## Make a new trade
1. Add an entry to `TRADES` in `../make_trade.py`: exact-string replacements for build.py, demo.py, shots.py and guide.html. Copy the `detail` or `window` entry as a template. Services, quote factors, add-ons, frequencies, expense categories, example rows, demo clients, captions and colors must all fit the new trade. Every replacement must match, and the script fails on a miss.
2. `python3 etsy-digital/make_trade.py <key>` builds a working folder (e.g. /tmp/trade-<key>) and reports leftover pressure-washing words (must be `[]`).
3. In that folder:
   - `python3 build.py`: the product workbook.
   - `python3 demo.py`: demo.xlsx with realistic sample data.
   - Recalculate both with LibreOffice (`python3 /mnt/skills/public/xlsx/scripts/recalc.py <file>`, or `soffice --headless`) and confirm 0 formula errors.
   - `python3 shots.py`: listing image HTML from the recalculated demo.
   - `node render.js`: images (Playwright, Chromium preinstalled). Look at every PNG.
   - `node pdf.js`: Quick-Start-Guide.pdf.
4. Copy the xlsx, guide PDF, images, build.py and a LISTING.md (title of 140 characters or fewer, 13 tags of 20 characters or fewer, AI disclosure) to `etsy-digital/<slug>/`. Add "Publish <product>, QA: pending" to APPROVALS.md.

Hand-check one quote against the Settings prices before finishing. QA re-tests independently.
