"""Week-1 ad pins (1000x1500): a pricing pin and a dashboard pin for Pressure Washing, Auto Detailing and Window
Cleaning. Crops come from the real listing images. Run: python3 build_pins.py"""
import base64, io, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[3]
OUT = HERE / "pins"; OUT.mkdir(exist_ok=True)

def crop(slug, img, *boxes):
    im = Image.open(ROOT / "etsy-digital" / f"{slug}-business-manager" / "images" / img).convert("RGB")
    parts = [im.crop(b) for b in boxes]
    w = max(p.width for p in parts); h = sum(p.height for p in parts) + 20 * (len(parts) - 1)
    c = Image.new("RGB", (w, h), "white"); y = 0
    for p in parts: c.paste(p, (0, y)); y += p.height + 20
    buf = io.BytesIO(); c.save(buf, "PNG"); return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

TRADES = {
 "pressure-washing": dict(name="Pressure Washing", acc="#1F5E8C", bg1="#e5eef6", who="For pressure washing & soft wash pros",
   q="How much should you charge to pressure wash a house?", qs="Enter house size, stories, extra surfaces, add-ons and frequency. See price, hours and profit before you say yes."),
 "auto-detailing": dict(name="Auto Detailing", acc="#8A2C2C", bg1="#f6e9e9", who="For mobile detailers",
   q="How much should you charge for a full detail?", qs="Enter vehicle size, pet hair, travel, add-ons and frequency. See price, hours and profit before you say yes."),
 "window-cleaning": dict(name="Window Cleaning", acc="#5B4A8B", bg1="#eeeaf6", who="For window cleaners",
   q="How much should you charge for window cleaning?", qs="Enter panes, stories, French windows, add-ons and frequency. See price, hours and profit before you say yes."),
}
CSS = """*{margin:0;box-sizing:border-box}body{width:1000px;height:1500px;font-family:Inter,sans-serif;color:#15324a;
background:linear-gradient(160deg,BG1 0%,#f6f3ec 100%);display:flex;flex-direction:column;padding:80px 60px 0;overflow:hidden}
.k{font-size:30px;font-weight:600;color:ACC;text-transform:uppercase;letter-spacing:2px}
h1{font-size:80px;line-height:1.05;font-weight:800;letter-spacing:-1.5px;margin-top:22px}
.s{font-size:34px;line-height:1.3;color:#3d5060;margin-top:26px}.shot{margin-top:40px;flex:1;display:flex;align-items:center;justify-content:center}
.card{background:#fff;border-radius:22px;box-shadow:0 20px 50px rgba(20,40,60,.18);padding:22px}.card img{display:block;width:836px;max-height:640px;object-fit:contain}
.f{height:170px;margin:0 -60px;background:ACC;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 60px}
.f b{font-size:38px;font-weight:800}.f span{font-size:27px;text-align:right;line-height:1.35;opacity:.92}"""
def page(t, kicker, head, sub, shot):
    css = CSS.replace("ACC", t["acc"]).replace("BG1", t["bg1"])
    return f"""<html><head><style>{css}</style></head><body><div class=k>{kicker}</div><h1>{head}</h1><div class=s>{sub}</div>
<div class=shot><div class=card><img src="{shot}"></div></div><div class=f><b>{t['name']} Business<br>Manager</b><span>Google Sheets &amp; Excel<br>Instant download</span></div></body></html>"""

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 1500})
    for slug, t in TRADES.items():
        pins = [(f"{slug}_1_pricing", page(t, t["who"], t["q"], t["qs"], crop(slug, "3_quote.png", (1020, 645, 1770, 1218)))),
                (f"{slug}_2_dashboard", page(t, t["who"], f"Run your {t['name'].lower()} business from one spreadsheet",
                  "Quotes, clients, jobs, invoices and profit. No app, no monthly subscription.",
                  crop(slug, "2_dashboard.png", (90, 470, 989, 586), (1011, 470, 1910, 586), (90, 610, 840, 655), (90, 955, 840, 1215))))]
        for name, h in pins:
            pg.set_content(h); pg.wait_for_timeout(200); pg.screenshot(path=str(OUT / f"{name}.png")); print("wrote", name)
    b.close()
