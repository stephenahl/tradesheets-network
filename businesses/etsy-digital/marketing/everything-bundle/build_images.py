"""Everything Bundle marketing images (Marketer, 2026-11-25). Drafts only.
Per tier (everything/, pro/): gumroad-cover-1280x720.png, gumroad-thumb-1000.png, etsy-1-hero.png (2000x1600), etsy-2-inside.png (2000x1600).
Screens are crops of the QA-passed listing images in etsy-digital/<product>/images/ (no new numbers).
Run: python3 build_images.py
"""
import base64, html, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
P = HERE.parents[2].parent / "etsy-digital"
TRADES = [  # name, accent (same as gumroad/build_gumroad.py), what the quote is priced by (START HERE text)
    ("Cleaning", "2F6F73", "bedrooms, bathrooms, sq ft"),
    ("Lawn Care", "3E6B2F", "lawn size, beds, trees"),
    ("Pressure Washing", "1F5E8C", "house size, stories, surfaces"),
    ("Auto Detailing", "8A2C2C", "vehicle size, pet hair, travel"),
    ("Window Cleaning", "5B4A8B", "panes, stories, French windows"),
    ("Pet Sitting & Dog Walking", "A0522D", "service, pets, medications"),
    ("Pool Service", "0E7C86", "gallons, spa, debris level"),
    ("Snow Removal", "37474F", "per push or season contract"),
    ("Handyman", "8C5A16", "flat-rate jobs, materials markup"),
    ("Carpet Cleaning", "9C2A5B", "rooms, stairs, soil level"),
]
TIERS = {
    "everything": dict(name="Everything Bundle", n=12, price=49, value=163.88, ink="1d2428", bg="eef0f2", gold=None,
                       line="10 Business Managers + 2 Pricing Calculators"),
    "pro": dict(name="Everything Bundle Pro", n=13, price=79, value=178.87, ink="1F3A5F", bg="e9eef5", gold="B8860B",
                line="10 Business Managers + 2 Pricing Calculators + Airbnb Host Manager"),
}
BOX = {  # browser-window box inside each 2000x1600 listing image (measured)
    "pressure-washing-business-manager/images/3_quote.png": (200, 481, 1800, 1310),
    "lawn-care-business-manager/images/2_dashboard.png": (60, 307, 1940, 1294),
    "handyman-business-manager/images/6_invoice.png": (350, 445, 1650, 1261),
}


def img(rel):
    return "data:image/png;base64," + base64.b64encode((P / rel).read_bytes()).decode()


def shot(rel, w, extra=""):
    """A div showing only the window part of a listing image, scaled to width w."""
    x0, y0, x1, y1 = BOX[rel]
    s = w / (x1 - x0)
    return (f'<div class=shot style="width:{w}px;height:{(y1 - y0) * s:.0f}px;background:url({img(rel)}) '
            f'-{x0 * s:.0f}px -{y0 * s:.0f}px / {2000 * s:.0f}px auto no-repeat;{extra}"></div>')


BASE = """*{margin:0;box-sizing:border-box}body{font-family:Inter,Helvetica,Arial,sans-serif;color:#%(ink)s;
background:linear-gradient(140deg,#%(bg)s,#f8f7f3);overflow:hidden;position:relative}
.chip{color:#fff;font-weight:700;border-radius:12px;white-space:nowrap}
.shot{border-radius:14px;box-shadow:0 18px 50px rgba(20,30,40,.25);position:absolute;border:1px solid rgba(0,0,0,.08)}
.pill{background:#%(ink)s;color:#fff;font-weight:700;border-radius:999px;display:inline-block}
.pro{background:#%(gold)s;color:#fff;font-weight:800;border-radius:10px;letter-spacing:2px;display:inline-block}
.sub{font-weight:600;opacity:.85}"""


def chips(size, pad):
    return "".join(f'<div class=chip style="background:#{a};font-size:{size}px;padding:{pad}">{html.escape(n)}</div>'
                   for n, a, _ in TRADES)


def pages(t):
    T = TIERS[t]
    css = BASE % dict(ink=T["ink"], bg=T["bg"], gold=T["gold"] or T["ink"])
    pro = t == "pro"
    save = T["value"] - T["price"]
    # Gumroad cover 1280x720
    cover = f"""<style>{css}body{{width:1280px;height:720px;padding:56px 64px}}
h1{{font-size:{58 if pro else 68}px;font-weight:800;letter-spacing:-1.5px;line-height:1}}.row{{display:flex;flex-wrap:wrap;gap:10px;width:640px;margin:26px 0}}</style>
{'<div class=pro style="font-size:22px;padding:6px 14px;margin-bottom:14px">PRO · CLIENT SETUP LICENSE</div>' if pro else ''}
<h1>{T['name'].replace(' Pro', '')}{' <span style="color:#' + T['gold'] + '">Pro</span>' if pro else ''}</h1>
<div class=sub style="font-size:28px;margin-top:14px;width:640px">{T['n']} service business spreadsheets<br>Google Sheets &amp; Excel · Instant download</div>
<div class=row>{chips(20, '9px 14px')}<div class=chip style="background:#{T['ink']};font-size:20px;padding:9px 14px">+ 2 Pricing Calculators</div>
{'<div class=chip style="background:#D35400;font-size:20px;padding:9px 14px">+ Airbnb Host</div>' if pro else ''}</div>
<div class=pill style="font-size:26px;padding:14px 28px">All {T['n']} for ${T['price']} · ${T['value']:.2f} separately</div>
{shot('pressure-washing-business-manager/images/3_quote.png', 440, 'right:30px;top:70px;transform:rotate(3deg)')}
{shot('lawn-care-business-manager/images/2_dashboard.png', 470, 'right:40px;top:380px;transform:rotate(-2deg)')}"""
    # Gumroad thumbnail 1000x1000
    thumb = f"""<style>{css}body{{width:1000px;height:1000px;padding:70px 60px;text-align:center}}
h1{{font-size:{104 if not pro else 96}px;font-weight:800;letter-spacing:-3px;line-height:.98}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:30px 0 28px}}</style>
{'<div class=pro style="font-size:30px;padding:8px 20px;margin-bottom:18px">PRO</div>' if pro else ''}
<h1>{T['n']} Business<br>Spreadsheets</h1>
<div class=sub style="font-size:34px;margin-top:16px">{'+ Client Setup License' if pro else '10 trades + 2 Pricing Calculators'}</div>
<div class=grid>{chips(25, '11px')}</div>
<div class=pill style="font-size:32px;padding:16px 36px">${T['price']} · save ${int(save)}</div>"""
    # Etsy photo 1 (no price on Etsy images: Etsy shows the price, and sales change it)
    hero = f"""<style>{css}body{{width:2000px;height:1600px;padding:110px 120px}}
h1{{font-size:150px;font-weight:800;letter-spacing:-4px;line-height:.95}}
.row{{display:flex;flex-wrap:wrap;gap:16px;width:1000px;margin:44px 0 48px}}
ul{{list-style:none;font-size:40px;line-height:1.55;font-weight:600}}li:before{{content:"✓  ";color:#{T['gold'] or '2F8F4E'};font-weight:800}}</style>
{'<div class=pro style="font-size:40px;padding:12px 26px;margin-bottom:30px">PRO EDITION</div>' if pro else ''}
<h1>{T['n']} Service<br>Business<br>Spreadsheets</h1>
<div class=sub style="font-size:48px;margin-top:34px;width:1000px">{T['line'] if not pro else '10 trades + 2 Pricing Calculators + Airbnb'}</div>
<div class=row>{chips(34, '14px 22px')}</div>
<ul><li>Quotes, clients, jobs, invoices, profit</li><li>{'License to set up 10 client businesses' if pro else 'Pricing Calculators with profit check'}</li><li>Google Sheets &amp; Excel · Instant download</li></ul>
{shot('pressure-washing-business-manager/images/3_quote.png', 760, 'right:70px;top:110px;transform:rotate(3deg)')}
{shot('lawn-care-business-manager/images/2_dashboard.png', 800, 'right:80px;top:560px;transform:rotate(-2deg)')}
{shot('handyman-business-manager/images/6_invoice.png', 620, 'right:110px;top:1000px;transform:rotate(2deg)')}"""
    # Etsy photo 2: what's inside
    rows = "".join(f'<tr><td><span class=dot style="background:#{a}"></span>{html.escape(n)}</td><td>{html.escape(b)}</td></tr>'
                   for n, a, b in TRADES)
    extra = ("<tr class=sec><td>Pricing Calculators (2)</td><td>Pressure Washing · House Cleaning: price, profit, estimate, quote log</td></tr>")
    if pro:
        extra += ("<tr class=sec><td>Airbnb Host Manager</td><td>bookings, turnovers, nightly-rate calculator, occupancy</td></tr>"
                  f"<tr class=sec><td style='color:#{T['gold']}'>Client Setup License</td><td>set up the files for up to 10 client businesses</td></tr>")
    inside = f"""<style>{css}body{{width:2000px;height:1600px;padding:{90 if pro else 110}px 130px}}
h1{{font-size:96px;font-weight:800;letter-spacing:-2px}}table{{width:100%;border-collapse:collapse;margin-top:{30 if pro else 44}px;font-size:{36 if pro else 39}px}}
td{{padding:{14 if pro else 17}px 10px;border-bottom:2px solid rgba(0,0,0,.08)}}td:first-child{{font-weight:700;width:44%}}
.dot{{display:inline-block;width:26px;height:26px;border-radius:7px;margin-right:22px;vertical-align:-3px}}
.sec td{{background:rgba(255,255,255,.6)}}.foot{{font-size:34px;margin-top:{26 if pro else 36}px;opacity:.85}}</style>
<h1>What's inside: {T['n']} spreadsheets</h1>
<div class=sub style="font-size:42px;margin-top:10px">10 Business Managers, each with Quote Calculator, Client Tracker, Jobs, Invoice, Expenses, Profit Dashboard</div>
<table><tr><td style="opacity:.6;font-size:30px">BUSINESS MANAGER</td><td style="opacity:.6;font-size:30px">QUOTES PRICED BY</td></tr>{rows}{extra}</table>
<div class=foot>One zip · {T['n']} .xlsx + a PDF guide for each + START HERE · Google Sheets &amp; Excel</div>"""
    return {"gumroad-cover-1280x720.png": (cover, 1280, 720), "gumroad-thumb-1000.png": (thumb, 1000, 1000),
            "etsy-1-hero.png": (hero, 2000, 1600), "etsy-2-inside.png": (inside, 2000, 1600)}


if __name__ == "__main__":
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for t in TIERS:
            out = HERE / t
            out.mkdir(exist_ok=True)
            for fn, (doc, w, h) in pages(t).items():
                pg = b.new_page(viewport={"width": w, "height": h})
                pg.set_content(doc)
                pg.wait_for_timeout(150)
                pg.screenshot(path=str(out / fn))
                pg.close()
                print(t, fn)
        b.close()
