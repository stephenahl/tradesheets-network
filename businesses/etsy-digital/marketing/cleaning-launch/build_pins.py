"""Builds 5 Pinterest pins (1000x1500) for the Cleaning Business Manager.
Crops come from the real listing screenshots in etsy-digital/cleaning-business-manager/images/.
Run: python3 build_pins.py  (needs Pillow + Playwright with Chromium)"""
import base64, io, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parents[3] / "etsy-digital" / "cleaning-business-manager" / "images"
OUT = HERE / "pins"; OUT.mkdir(exist_ok=True)

def crop(img, *boxes, stack=False):
    """Crop bands (x0,y0,x1,y1) and join them side by side (or stacked if stack=True)."""
    im = Image.open(SRC / img).convert("RGB")
    parts = [im.crop(b) for b in boxes]
    if stack:
        w = max(p.width for p in parts); h = sum(p.height for p in parts) + 20 * (len(parts) - 1)
    else:
        w = sum(p.width for p in parts); h = max(p.height for p in parts)
    canvas = Image.new("RGB", (w, h), "white"); x = y = 0
    for p in parts:
        canvas.paste(p, (x, y))
        if stack: y += p.height + 20
        else: x += p.width
    buf = io.BytesIO(); canvas.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

PINS = [
    dict(slug="1_one-spreadsheet", kicker="For house cleaners & maid services",
         head="Run your cleaning business from one spreadsheet",
         sub="Quotes, clients, jobs, invoices and profit. No app, no subscription.",
         shot=crop("2_dashboard.png", (90, 470, 990, 586), (90, 610, 1066, 655), (90, 870, 1066, 1215), stack=True)),
    dict(slug="2_how-much-to-charge", kicker="Cleaning business pricing",
         head="How much should you charge for a house clean?",
         sub="Enter size, rooms, add-ons and frequency. See price, hours and profit before you say yes.",
         shot=crop("3_quote.png", (1020, 645, 1770, 1218))),
    dict(slug="3_recurring-clients", kicker="Client tracker",
         head="Never miss a recurring clean",
         sub="Next due dates fill in. Due-soon and overdue clients highlight themselves.",
         shot=crop("4_clients.png", (90, 721, 357, 1153), (1351, 721, 1910, 1153))),
    dict(slug="4_profit-per-job", kicker="Know your numbers",
         head="See the real profit on every cleaning job",
         sub="Labor, supplies and mileage subtracted automatically. Unpaid jobs turn red.",
         shot=crop("5_jobs.png", (438, 657, 727, 1218), (1003, 657, 1331, 1218), (1598, 657, 1910, 1218))),
    dict(slug="5_invoices", kicker="Invoice template",
         head="Cleaning invoices that fill themselves in",
         sub="Type a Job ID. Print or save as PDF. Plus a tax set-aside on the dashboard.",
         shot=crop("6_invoice.png", (500, 570, 1500, 1170))),
]

CSS = """
*{margin:0;box-sizing:border-box}
body{width:1000px;height:1500px;font-family:Inter,sans-serif;color:#1f3a3d;
 background:linear-gradient(160deg,#e6f0ef 0%,#f3f2ec 100%);display:flex;flex-direction:column;
 padding:80px 60px 0 60px;overflow:hidden}
.kicker{font-size:30px;font-weight:600;color:#2e6e72;text-transform:uppercase;letter-spacing:2px}
h1{font-size:82px;line-height:1.05;font-weight:800;letter-spacing:-1.5px;margin-top:22px}
.sub{font-size:34px;line-height:1.3;color:#3d5a5c;margin-top:26px}
.shot{margin-top:40px;flex:1;display:flex;align-items:center;justify-content:center}
.card{background:#fff;border-radius:22px;box-shadow:0 20px 50px rgba(30,60,60,.18);padding:22px;max-width:880px}
.card img{display:block;width:836px;max-height:680px;object-fit:contain}
.foot{height:170px;margin:0 -60px;background:#2e6e72;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 60px}
.foot b{font-size:38px;font-weight:800}.foot span{font-size:27px;white-space:nowrap;opacity:.9;text-align:right;line-height:1.35}
"""

def html(p):
    return f"""<html><head><style>{CSS}</style></head><body>
<div class=kicker>{p['kicker']}</div><h1>{p['head']}</h1><div class=sub>{p['sub']}</div>
<div class=shot><div class=card><img src="{p['shot']}"></div></div>
<div class=foot><b>Cleaning Business<br>Manager</b><span>Google Sheets &amp; Excel<br>Instant download</span></div>
</body></html>"""

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 1500})
    for p in PINS:
        pg.set_content(html(p)); pg.wait_for_timeout(200)
        pg.screenshot(path=str(OUT / f"{p['slug']}.png")); print("wrote", p["slug"])
    b.close()
