"""Snow Removal pin kit: 5 organic Pinterest pins (1000x1500), pricing pin first.
Reuses the crop helpers and page template from ../organic-pins/build_pins.py (same listing-image layout).
Run: python3 build_pins.py  (Pillow + Playwright with Chromium)"""
import os, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "organic-pins"))
import build_pins as base  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = HERE / "pins"; OUT.mkdir(exist_ok=True)
S = "snow-removal"
T = dict(name="Snow Removal", acc="#2B5C8A", bg1="#e6eef6")
K = "For snow plowing businesses"
QUOTE_NOTE = "Snow quote layout has one more row (season contract price), so its crop box differs from base.QUOTE"

PINS = [
 ("1_pricing", K, "How much should you charge per push?",
  "Pick the service, depth, obstacles and add-ons. Get a per-push and a season contract price.", base.crop(S, "3_quote.png", (1020, 630, 1770, 1246))),
 ("2_dashboard", K, "Run your snow removal business from one spreadsheet",
  "Quotes, clients, every push, invoices and season profit. No app, no subscription.", base.crop(S, *base.DASH, stack=True)),
 ("3_who-owes-you", "Client tracker", "Know who still owes you after every storm",
  "Pushes and unpaid balances fill in. Clients who owe you turn red.", base.clients(S)),
 ("4_profit-per-push", "Know your numbers", "See the real profit on every push",
  "Crew labor, salt and mileage subtracted automatically. Unpaid pushes turn red.", base.jobs(S)),
 ("5_invoices", "Invoice template", "Snow plow invoices that fill themselves in",
  "Type a Job ID. Print or save as PDF. Plus a tax set-aside on the dashboard.", base.crop(S, *base.INVOICE)),
]

if __name__ == "__main__":
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("PW_CHROMIUM") or None)
        pg = b.new_page(viewport={"width": 1000, "height": 1500})
        for n, k, h, s, shot in PINS:
            pg.set_content(base.page(T, k, h, s, shot))
            pg.wait_for_timeout(200); pg.screenshot(path=str(OUT / f"snow-removal_{n}.png")); print("wrote", n)
        b.close()
