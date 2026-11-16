# Pricing Calculator generator (standalone $6.99 product line, pilot 2026-11-16)

Cut from the Business Manager engine (`../_engine/build.py`). Same Settings cells for services (D5:F12), quote factors (E15:E20), add-ons (D24:F29) and frequency (D33:F37), so buyers can paste their prices into the full manager.

Tabs: Start Here · Quote Calculator (price, hours, labor, profit, margin, $/hour, target-rate check, minimum charge, visits/yr, yearly value) · Estimate (printable, customer-facing, lines add up to the total) · Quote Log (500 rows; win rate, won yearly value, follow-up reminders) · Settings · Full Business Manager (upsell links).

- `calc.py`: TRADES config (`pw`, `cleaning`) + `build(key, out, demo=False)`.
- `shots.py`: 7 listing images (HTML) from a recalculated demo workbook.
- `make.py <key> <workdir>`: builds product + demo, recalculates both in LibreOffice (asserts 0 errors), writes images, guide.html, renders PNGs and Quick-Start-Guide.pdf.
- New trade: add a TRADES entry (copy the trade's services/factors/add-ons/frequency from its Business Manager build.py so the Settings cells match) and a LINKS entry, then run make.py and copy outputs to `etsy-digital/<trade>-pricing-calculator/`.

Hand-checked 2026-11-16: PW default 325+75+60+60+50=570, -5% = 541.50 -> $542, 5.75 h, profit $398.25; Cleaning 120+20+15+56+65=276, -10% = 248.40 -> $248, 5.6 h, 26 visits/yr = $6,448; minimum-charge case $127.50 -> $128 -> topped up to $150.
