"""Pricing Calculator pilot pin kit: 5 organic Pinterest pins (1000x1500) each for the Pressure Washing and
House Cleaning Pricing Calculators, pricing pin first. Crops come from the real listing images in
etsy-digital/<slug>-pricing-calculator/images/ (2000x1600, same layout for both trades).
Reuses the page template from ../organic-pins/build_pins.py.
Run: python3 build_pins.py  (Pillow + Playwright with Chromium)"""
import os, pathlib, sys
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent / "organic-pins"))
import build_pins as base  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = HERE / "pins"; OUT.mkdir(exist_ok=True)

def im(slug, name):
    return Image.open(ROOT / "etsy-digital" / f"{slug}-pricing-calculator" / "images" / name).convert("RGB")

def crop(slug, name, *boxes, stack=True, gap=20):
    src = im(slug, name); parts = [src.crop(b) for b in boxes]
    if stack: w = max(p.width for p in parts); h = sum(p.height for p in parts) + gap * (len(parts) - 1)
    else: w = sum(p.width for p in parts) + gap * (len(parts) - 1); h = max(p.height for p in parts)
    c = Image.new("RGB", (w, h), "white"); x = y = 0
    for p in parts:
        c.paste(p, (x, y))
        if stack: y += p.height + gap
        else: x += p.width + gap
    return base.uri(c)

# Crop boxes in listing-image pixels (2000x1600).
QUOTE = ("1_hero.png", (1020, 536, 1912, 1268))                       # "Your quote" panel: adjustments -> price, hours, profit, $/hr
PROFIT = ("3_profit.png", (380, 580, 1620, 1300))                      # Result table: labor, profit, margin, target check, yearly value
ESTIMATE = ("2_estimate.png", (430, 480, 1570, 1300))                  # printable estimate
LOG = ("4_log.png", (90, 640, 1000, 752), (1006, 640, 1910, 752))      # KPI cards, split into 2 rows
# service price list + your rates (House Cleaning has 5 services vs 6, so its boxes sit higher)
SHEET = {"pressure-washing": ("5_settings.png", (90, 640, 985, 950), (90, 970, 985, 1240)),
         "house-cleaning": ("5_settings.png", (90, 639, 985, 908), (90, 926, 985, 1196))}

def log_rows(slug):
    """Quote Log: KPI cards (2 rows) above the Customer column and the Quoted price..Next step columns."""
    kpi = [im(slug, "4_log.png").crop(b) for b in LOG[1:]]
    src = im(slug, "4_log.png")
    tbl = [src.crop((270, 770, 520, 1240)), src.crop((1000, 770, 1910, 1240))]
    tw = sum(p.width for p in tbl); w = max(tw, kpi[0].width)
    c = Image.new("RGB", (w, kpi[0].height * 2 + 20 + 30 + tbl[0].height), "white"); y = 0
    for p in kpi: c.paste(p, (0, y)); y += p.height + 10
    y += 30; x = 0
    for p in tbl: c.paste(p, (x, y)); x += p.width
    return base.uri(c)

TRADES = {
 "pressure-washing": dict(name="Pressure Washing", acc="#1F5E8C", bg1="#e5eef6",
     kick="For pressure washing businesses",
     q="How much should you charge to soft wash a house?",
     qs="Size, stories, surfaces and add-ons in. Price, hours and profit out.",
     sheet="Pressure washing price sheet you set once"),
 "house-cleaning": dict(name="House Cleaning", acc="#2F6F73", bg1="#e4f0f0",
     kick="For house cleaning businesses",
     q="How much should you charge to clean a house?",
     qs="Square feet, rooms and add-ons in. Price, hours and profit out.",
     sheet="House cleaning price list you set once"),
}

def pins(slug, t):
    return [
     ("1_pricing", t["kick"], t["q"], t["qs"], crop(slug, *QUOTE)),
     ("2_profit", "Never underprice a job", "Know your profit before you say yes",
      "Set the hourly rate you want. Low quotes get flagged, with the price that hits your target.", crop(slug, *PROFIT)),
     ("3_estimate", "Printable estimate", "Send a professional estimate in minutes",
      "Every line fills in from your quote. Print it or save it as a PDF.", crop(slug, *ESTIMATE)),
     ("4_quote-log", "Quote tracker", "Track every quote and win more jobs",
      "Won, lost or pending, your win rate, and which quotes to follow up on today.", log_rows(slug)),
     ("5_price-sheet", "Your prices, your rates", t["sheet"],
      "Services, add-ons, labor cost, target rate and minimum charge. Every quote uses them.", crop(slug, *SHEET[slug])),
    ]

if __name__ == "__main__":
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("PW_CHROMIUM") or None)
        pg = b.new_page(viewport={"width": 1000, "height": 1500})
        for slug, t in TRADES.items():
            for n, k, h, s, shot in pins(slug, t):
                html = base.page(t, k, h, s, shot, brand=f"{t['name']}<br>Pricing Calculator")
                pg.set_content(html.replace("max-height:640px", "max-height:820px"))  # these crops are taller; fill the pin
                pg.wait_for_timeout(200); pg.screenshot(path=str(OUT / f"{slug}-calc_{n}.png")); print("wrote", slug, n)
        b.close()
