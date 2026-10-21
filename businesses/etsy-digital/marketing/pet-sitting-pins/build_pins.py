"""Pet Sitting & Dog Walking pin kit: 5 organic Pinterest pins (1000x1500), pricing pin first.
Reuses the crop helpers and page template from ../organic-pins/build_pins.py (same listing-image layout).
Run: PW_CHROMIUM=/opt/pw-browsers/chromium python3 build_pins.py  (Pillow + Playwright with Chromium)"""
import os, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "organic-pins"))
import build_pins as base  # noqa: E402  (its __main__ block does not run on import)
from playwright.sync_api import sync_playwright

OUT = HERE / "pins"; OUT.mkdir(exist_ok=True)
S = "pet-sitting-dog-walking"
T = dict(name="Pet Sitting &amp; Dog Walking", acc="#9C4F2C", bg1="#f6eae1")
K = "For pet sitters &amp; dog walkers"

PINS = [
 ("1_pricing", K, "How much should you charge for dog walking?",
  "Pick the walk, add pets, meds, travel and add-ons. See price, hours and profit before you say yes.", base.crop(S, *base.QUOTE)),
 ("2_dashboard", K, "Run your pet sitting business from one spreadsheet",
  "Quotes, regular clients, visits, invoices and profit. No app, no monthly subscription.", base.crop(S, *base.DASH, stack=True)),
 ("3_recurring-clients", "Client tracker", "Never miss a regular walk or drop-in",
  "Next due dates fill in. Due-soon and overdue clients highlight themselves.", base.clients(S)),
 ("4_profit-per-visit", "Know your numbers", "See the real profit on every walk and visit",
  "Sitter pay, supplies and mileage subtracted automatically. Unpaid visits turn red.", base.jobs(S)),
 ("5_invoices", "Invoice template", "Pet sitting invoices that fill themselves in",
  "Type a Job ID. Print or save as PDF. Plus a tax set-aside on the dashboard.", base.crop(S, *base.INVOICE)),
]

if __name__ == "__main__":
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("PW_CHROMIUM") or None)
        pg = b.new_page(viewport={"width": 1000, "height": 1500})
        for n, k, h, s, shot in PINS:
            pg.set_content(base.page(T, k, h, s, shot, brand="Pet Sitting &amp; Dog<br>Walking Manager"))
            pg.wait_for_timeout(200); pg.screenshot(path=str(OUT / f"pet-sitting_{n}.png")); print("wrote", n)
        b.close()
