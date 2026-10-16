"""Organic Pinterest pins (1000x1500) that finish the 5-pin kits: Lawn Care x5 (it had none), Pressure Washing,
Auto Detailing and Window Cleaning x3 each (their pricing + dashboard pins are in ads-week1/), and 2 bundle pins.
Crops come from the real listing images. Run: python3 build_pins.py  (Pillow + Playwright with Chromium)"""
import base64, io, os, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[3]
OUT = HERE / "pins"; OUT.mkdir(exist_ok=True)

def img(slug, name):
    return Image.open(ROOT / "etsy-digital" / f"{slug}-business-manager" / "images" / name).convert("RGB")

def uri(c):
    buf = io.BytesIO(); c.save(buf, "PNG"); return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def crop(slug, name, *boxes, stack=False):
    im = img(slug, name); parts = [im.crop(b) for b in boxes]
    if stack: w = max(p.width for p in parts); h = sum(p.height for p in parts) + 20 * (len(parts) - 1)
    else: w = sum(p.width for p in parts); h = max(p.height for p in parts)
    c = Image.new("RGB", (w, h), "white"); x = y = 0
    for p in parts:
        c.paste(p, (x, y))
        if stack: y += p.height + 20
        else: x += p.width
    return uri(c)

def cols(slug, name, y0, y1):
    """Left edges of each table column, found from the white header text (column widths differ per trade)."""
    a = img(slug, name).crop((90, y0, 1910, y1)).convert("L").point(lambda v: 255 if v > 200 else 0)
    xs = [x for x in range(a.width) if any(a.getpixel((x, y)) for y in range(a.height))]
    starts = [xs[0]] + [q for p, q in zip(xs, xs[1:]) if q - p > 28]
    return [90 + x - 11 for x in starts] + [1910]

def clients(slug):  # client name | last visit, next due, status
    c = cols(slug, "4_clients.png", 721, 766)
    return crop(slug, "4_clients.png", (c[0], 721, c[1], 1153), (c[6], 721, 1910, 1153))

def jobs(slug):  # client | total charged, paid? | labor cost, profit
    c = cols(slug, "5_jobs.png", 657, 702)
    return crop(slug, "5_jobs.png", (c[2], 657, c[3], 1218), (c[5], 657, c[7], 1218), (c[8], 657, 1910, 1218))

# Same crop boxes as cleaning-launch/build_pins.py (quote, dashboard and invoice share one layout across trades).
QUOTE = ("3_quote.png", (1020, 645, 1770, 1218))
DASH = ("2_dashboard.png", (90, 470, 990, 586), (90, 610, 1066, 655), (90, 870, 1066, 1215))
INVOICE = ("6_invoice.png", (500, 570, 1500, 1170))

TRADES = {
 "lawn-care": dict(name="Lawn Care", acc="#3E6E2F", bg1="#e9f0e4", job="mowing", visit="recurring mow"),
 "pressure-washing": dict(name="Pressure Washing", acc="#1F5E8C", bg1="#e5eef6", job="pressure washing", visit="repeat wash"),
 "auto-detailing": dict(name="Auto Detailing", acc="#8A2C2C", bg1="#f6e9e9", job="detailing", visit="recurring detail"),
 "window-cleaning": dict(name="Window Cleaning", acc="#5B4A8B", bg1="#eeeaf6", job="window cleaning", visit="recurring window clean"),
}

def trade_pins(slug, t):
    pins = []
    if slug == "lawn-care":
        pins += [("1_pricing", "For lawn care & mowing businesses", "How much should you charge to mow a lawn?",
                  "Enter lawn size, extras, add-ons and frequency. See price, hours and profit before you say yes.", crop(slug, *QUOTE)),
                 ("2_dashboard", "For lawn care & mowing businesses", "Run your lawn care business from one spreadsheet",
                  "Quotes, clients, jobs, invoices and profit. No app, no monthly subscription.", crop(slug, *DASH, stack=True))]
    pins += [("3_recurring-clients", "Client tracker", f"Never miss a {t['visit']}",
              "Next due dates fill in. Due-soon and overdue clients highlight themselves.", clients(slug)),
             ("4_profit-per-job", "Know your numbers", f"See the real profit on every {t['job']} job",
              "Labor, supplies and mileage subtracted automatically. Unpaid jobs turn red.", jobs(slug)),
             ("5_invoices", "Invoice template", f"{t['name']} invoices that fill themselves in",
              "Type a Job ID. Print or save as PDF. Plus a tax set-aside on the dashboard.", crop(slug, *INVOICE))]
    return [(f"{slug}_{n}", t, k, h, s, shot) for n, k, h, s, shot in pins]

CSS = """*{margin:0;box-sizing:border-box}body{width:1000px;height:1500px;font-family:Inter,sans-serif;color:#15324a;
background:linear-gradient(160deg,BG1 0%,#f6f3ec 100%);display:flex;flex-direction:column;padding:80px 60px 0;overflow:hidden}
.k{font-size:30px;font-weight:600;color:ACC;text-transform:uppercase;letter-spacing:2px}
h1{font-size:80px;line-height:1.05;font-weight:800;letter-spacing:-1.5px;margin-top:22px}
.s{font-size:34px;line-height:1.3;color:#3d5060;margin-top:26px}.shot{margin-top:40px;flex:1;display:flex;align-items:center;justify-content:center}
.card{background:#fff;border-radius:22px;box-shadow:0 20px 50px rgba(20,40,60,.18);padding:22px}.card img{display:block;width:836px;max-height:640px;object-fit:contain}
.f{height:170px;margin:0 -60px;background:ACC;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 60px}
.f b{font-size:38px;font-weight:800}.f span{font-size:27px;text-align:right;line-height:1.35;opacity:.92}"""

def page(t, kicker, head, sub, shot, brand=None, right="Google Sheets &amp; Excel<br>Instant download"):
    css = CSS.replace("ACC", t["acc"]).replace("BG1", t["bg1"])
    brand = brand or f"{t['name']} Business<br>Manager"
    return f"""<html><head><style>{css}</style></head><body><div class=k>{kicker}</div><h1>{head}</h1><div class=s>{sub}</div>
<div class=shot><div class=card><img src="{shot}"></div></div><div class=f><b>{brand}</b><span>{right}</span></div></body></html>"""

def bundle_grid():
    """The 5 real dashboards' KPI bands, stacked with a trade label above each."""
    from PIL import ImageDraw, ImageFont
    rows = ["cleaning", "lawn-care", "pressure-washing", "auto-detailing", "window-cleaning"]
    bands = [img(s, "2_dashboard.png").crop((90, 470, 1910, 586)) for s in rows]
    try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    except OSError: font = ImageFont.load_default()
    lab = 50; c = Image.new("RGB", (1820, len(bands) * (116 + lab + 24)), "white"); d = ImageDraw.Draw(c); y = 0
    for s, b in zip(rows, bands):
        d.text((4, y + 6), s.replace("-", " ").title(), fill="#1f2a30", font=font); c.paste(b, (0, y + lab)); y += 116 + lab + 24
    return uri(c)

BUNDLE = dict(name="Bundle", acc="#1f2a30", bg1="#eceff1")
cover = Image.open(HERE.parent / "gumroad" / "bundle" / "gumroad-cover-1280x720.png").convert("RGB").crop((40, 130, 1240, 600))
BUNDLE_PINS = [
 ("bundle_1_all-five", BUNDLE, "5 service business spreadsheets", "All 5 business managers for $39",
  "Cleaning, lawn care, pressure washing, auto detailing and window cleaning. Save $35.95 vs buying separately.", uri(cover)),
 ("bundle_2_which-trade", BUNDLE, "Pick your trade", "One spreadsheet to run your service business",
  "Each one has its own quote calculator, client tracker, jobs log, invoices and profit dashboard.", bundle_grid()),
]

if __name__ == "__main__":
    pins = [p for s, t in TRADES.items() for p in trade_pins(s, t)]
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("PW_CHROMIUM") or None); pg = b.new_page(viewport={"width": 1000, "height": 1500})
        for name, t, k, h, s, shot in pins:
            pg.set_content(page(t, k, h, s, shot)); pg.wait_for_timeout(200); pg.screenshot(path=str(OUT / f"{name}.png")); print("wrote", name)
        for name, t, k, h, s, shot in BUNDLE_PINS:
            pg.set_content(page(t, k, h, s, shot, brand="Service Business<br>Manager Bundle", right="Gumroad · $39<br>Instant download"))
            pg.wait_for_timeout(200); pg.screenshot(path=str(OUT / f"{name}.png")); print("wrote", name)
        b.close()
