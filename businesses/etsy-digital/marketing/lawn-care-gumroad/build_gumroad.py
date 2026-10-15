"""Gumroad cover (1280x720) and thumbnail (1000x1000) for the Lawn Care Business Manager.
Matches the setup-kit Cleaning cover style, in the lawn product's green palette. Run: python3 build_gumroad.py"""
import base64, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
SHOT = HERE.parents[3] / "etsy-digital" / "lawn-care-business-manager" / "images" / "1_hero.png"
img = "data:image/png;base64," + base64.b64encode(SHOT.read_bytes()).decode()
BASE = "*{margin:0;box-sizing:border-box}body{font-family:Inter,sans-serif;background:linear-gradient(135deg,#eaf1e6,#f5f3ec);color:#23391f;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;overflow:hidden}.pill{background:#3d6b30;color:#fff;font-weight:700;border-radius:999px}"
COVER = f"""<style>{BASE}body{{width:1280px;height:720px}}h1{{font-size:76px;font-weight:800;letter-spacing:-1.5px}}
.sub{{font-size:32px;font-weight:600;color:#3d6b30;margin:18px 0 32px}}.pill{{font-size:27px;padding:16px 32px}}</style>
<h1>Lawn Care Business Manager</h1><div class=sub>Quotes · Clients · Jobs · Invoices · Profit dashboard</div>
<div class=pill>Google Sheets &amp; Excel · Instant download</div>"""
THUMB = f"""<style>{BASE}body{{width:1000px;height:1000px;justify-content:flex-start;padding-top:90px}}h1{{font-size:96px;line-height:1.02;font-weight:800;letter-spacing:-2px}}
.sub{{font-size:34px;font-weight:600;color:#3d6b30;margin:22px 0 34px}}.pill{{font-size:28px;padding:14px 30px}}
.shot{{margin-top:50px;width:808px;height:520px;border-radius:20px;background:url({img}) -95px -515px / 1900px auto no-repeat;box-shadow:0 20px 50px rgba(30,60,30,.2)}}</style>
<h1>Lawn Care<br>Business Manager</h1><div class=sub>Quotes · Clients · Invoices · Profit</div>
<div class=pill>Google Sheets &amp; Excel</div><div class=shot></div>"""
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page()
    for name, html, w, h in [("gumroad-cover-1280x720.png", COVER, 1280, 720), ("gumroad-thumb-1000.png", THUMB, 1000, 1000)]:
        pg.set_viewport_size({"width": w, "height": h}); pg.set_content(html); pg.wait_for_timeout(200)
        pg.screenshot(path=str(HERE / name)); print("wrote", name)
    b.close()
