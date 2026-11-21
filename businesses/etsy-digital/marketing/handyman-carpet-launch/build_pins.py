"""Handyman + Carpet Cleaning launch pins: 5 organic Pinterest pins each (1000x1500), pricing pin first.
Reuses the crop helpers and page template from ../organic-pins/build_pins.py (same listing-image layout).
Run: python3 build_pins.py  (Pillow + Playwright with Chromium)"""
import os, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "organic-pins"))
import build_pins as base  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = HERE / "pins"; OUT.mkdir(exist_ok=True)
KITS = {
 "handyman": (dict(name="Handyman", acc="#8C5A17", bg1="#f6eee2"), "For handyman businesses", [
  ("1_pricing", "How much should you charge for handyman jobs?",
   "Pick the job, units, difficulty and materials. See the price, hours and your real hourly rate."),
  ("2_dashboard", "Run your handyman business from one spreadsheet",
   "Flat-rate price list, quotes, clients, jobs, invoices and profit. No app, no subscription."),
  ("3_repeat-clients", "Never miss a maintenance visit",
   "Monthly and quarterly clients show their next due date. Overdue ones highlight themselves."),
  ("4_profit-per-job", "See the real profit on every handyman job",
   "Labor, materials and mileage subtracted automatically. Unpaid jobs turn red."),
  ("5_invoices", "Handyman invoices that fill themselves in",
   "Type a Job ID. Print or save as PDF. Plus a tax set-aside on the dashboard.")]),
 "carpet-cleaning": (dict(name="Carpet Cleaning", acc="#9A2858", bg1="#f7e8ee"), "For carpet cleaning businesses", [
  ("1_pricing", "How much should you charge per room?",
   "Rooms, stairs, soil level and add-ons like pet odor. See price, hours and profit before you say yes."),
  ("2_dashboard", "Run your carpet cleaning business from one spreadsheet",
   "Quotes, clients, jobs, invoices and profit. No app, no monthly subscription."),
  ("3_repeat-clients", "Book every annual and 6-month clean",
   "Next due dates fill in. Due-soon and overdue clients highlight themselves."),
  ("4_profit-per-job", "See the real profit on every carpet job",
   "Labor, supplies and mileage subtracted automatically. Unpaid jobs turn red."),
  ("5_invoices", "Carpet cleaning invoices that fill themselves in",
   "Type a Job ID. Print or save as PDF. Plus a tax set-aside on the dashboard.")]),
}

def shot(slug, n):
    return {"1": lambda: base.crop(slug, *base.QUOTE), "2": lambda: base.crop(slug, *base.DASH, stack=True),
            "3": lambda: base.clients(slug), "4": lambda: base.jobs(slug), "5": lambda: base.crop(slug, *base.INVOICE)}[n[0]]()

if __name__ == "__main__":
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("PW_CHROMIUM") or None)
        pg = b.new_page(viewport={"width": 1000, "height": 1500})
        for slug, (t, kicker, pins) in KITS.items():
            for i, (n, h, s) in enumerate(pins):
                k = kicker if i < 2 else ["", "", "Client tracker", "Know your numbers", "Invoice template"][i]
                pg.set_content(base.page(t, k, h, s, shot(slug, n)))
                pg.wait_for_timeout(200); pg.screenshot(path=str(OUT / f"{slug}_{n}.png")); print("wrote", slug, n)
        b.close()
