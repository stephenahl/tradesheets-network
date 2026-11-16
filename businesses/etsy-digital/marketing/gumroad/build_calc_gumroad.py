"""Gumroad cover (1280x720) and thumbnail (1000x1000) for the Pricing Calculator pilot (Builder 2026-11-16).
Same style as build_gumroad.py covers. GUMROAD.md for each is written alongside. Run: python3 build_calc_gumroad.py"""
import pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
ITEMS = [("pressure-washing-pricing-calculator", "Pressure Washing Pricing Calculator", "1F5E8C", "E5EEF6"),
         ("house-cleaning-pricing-calculator", "House Cleaning Pricing Calculator", "2F6F73", "E6F1F1")]
def html(name, acc, light, w, h, size):
    return f"""<html><head><meta charset="utf-8"><style>body{{margin:0;width:{w}px;height:{h}px;font-family:Inter,Arial,sans-serif;background:linear-gradient(135deg,#{light},#F8F5EE);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
h1{{font-size:{size}px;line-height:1.08;color:#{acc};margin:0 60px 18px;font-weight:800}} .s{{font-size:{size*0.36:.0f}px;color:#15324a;font-weight:700;margin-bottom:26px}}
.p{{background:#{acc};color:#fff;font-size:{size*0.3:.0f}px;font-weight:700;padding:14px 32px;border-radius:40px}}</style></head>
<body><h1>{name}</h1><div class="s">Price every job in 60 seconds · Printable estimate · Quote log</div><div class="p">Google Sheets &amp; Excel · Instant download</div></body></html>"""
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for slug, name, acc, light in ITEMS:
        d = HERE / slug; d.mkdir(exist_ok=True)
        for fn, w, h, size in (("gumroad-cover-1280x720.png", 1280, 720, 76), ("gumroad-thumb-1000.png", 1000, 1000, 84)):
            p = b.new_page(viewport={"width": w, "height": h}); p.set_content(html(name, acc, light, w, h, size)); p.screenshot(path=str(d / fn)); p.close()
    b.close()
print("ok")
