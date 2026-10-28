"""Gumroad drafts for each trade and the all-trades bundle.
Per trade in NEW: GUMROAD.md (description adapted from the Etsy LISTING.md), cover 1280x720, thumbnail 1000x1000.
Bundle (folder BUNDLE_DIR): cover, thumbnail and TradeSheets-<n>-Trade-Bundle.zip (n workbooks + n guides).
History: 2026-10-15 PW/AD/WC + 5-trade bundle (live, assets in bundle/); 2026-10-17 Pet Sitting + 6-trade bundle (bundle-6/, live 10-20);
2026-10-28 Pool Service, Snow Removal, Handyman + 9-trade bundle draft (bundle-9/).
Same cover style as lawn-care-gumroad/build_gumroad.py. Run: python3 build_gumroad.py"""
import base64, os, pathlib, re, zipfile
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PRODUCTS = HERE.parents[3] / "etsy-digital"
# slug, name, accent, light (accent/light from each product's build.py / make_trade.py)
TRADES = [
    ("cleaning", "Cleaning", "2F6F73", "E6F1F1"),
    ("lawn-care", "Lawn Care", "3E6B2F", "EAF2E4"),
    ("pressure-washing", "Pressure Washing", "1F5E8C", "E5EEF6"),
    ("auto-detailing", "Auto Detailing", "8A2C2C", "F6E9E9"),
    ("window-cleaning", "Window Cleaning", "5B4A8B", "EEEAF6"),
    ("pet-sitting-dog-walking", "Pet Sitting & Dog Walking", "A0522D", "FBEDE3"),
    ("pool-service", "Pool Service", "0E7C86", "E0F2F3"),
    ("snow-removal", "Snow Removal", "37474F", "ECEFF1"),
    ("handyman", "Handyman", "8C5A16", "F7EFE1"),
]
NEW = ["pool-service", "snow-removal", "handyman"]
DATE = "2026-10-28"
N = len(TRADES)
BUNDLE_DIR = f"bundle-{N}"
SINGLES = round(N * 14.99, 2)
FILE = lambda name: name.replace(" & ", "-").replace(" ", "-") + "-Business-Manager.xlsx"


def gumroad_md(slug, name):
    listing = (PRODUCTS / f"{slug}-business-manager" / "LISTING.md").read_text()
    desc = listing.split("## Description\n", 1)[1].strip()
    out = []
    for line in desc.splitlines():
        if line.isupper() and line.strip():
            line = f"**{line.capitalize()}**"
        elif line.startswith("• "):
            m = re.match(r"• ([^:]{2,30}): (.*)", line)
            line = f"- **{m[1]}:** {m[2]}" if m else "- " + line[2:]
        out.append(line)
    desc = "\n".join(out).replace("Send me a message and I'm happy to help.", "Reply to your receipt email and I'll help.")
    desc = desc.replace("This template was designed by me", "Designed by TradeSheets Co.")
    desc = desc.replace("Every formula was built for both Excel and Google Sheets and tested before release.",
                        "It uses only functions that Excel and Google Sheets both support, and every formula was checked before release.")
    return f"""# Gumroad product draft: {name} Business Manager ({DATE})

DRAFT. Not published. Going live on Gumroad needs Stephen's APPROVED (see network/APPROVALS.md).

Set up like the live Cleaning and Lawn Care products (https://tradesheetsshop.gumroad.com/l/lawn-care-business-manager).

- **Name:** {name} Business Manager: Google Sheets & Excel Template
- **URL slug:** `{slug}-business-manager`
- **Price:** $14.99 (same as Etsy; Gumroad keeps about 10% + card processing, so about $12.75 per sale)
- **Cover:** `{slug}/gumroad-cover-1280x720.png`, then the 7 images from `etsy-digital/{slug}-business-manager/images/` in listing order (1_hero, 3_quote, 4_clients, 5_jobs, 2_dashboard, 6_invoice, 7_included)
- **Thumbnail:** `{slug}/gumroad-thumb-1000.png` (square)
- **Content:** upload `etsy-digital/{slug}-business-manager/{FILE(name)}` and `Quick-Start-Guide.pdf`
- **Summary (the "You'll get" line):** One spreadsheet for quotes, recurring clients, jobs, invoices, expenses and profit. Google Sheets & Excel.
- **Additional details:** Format: .xlsx + PDF guide · Tabs: 8 · Works in: Google Sheets, Excel
- **Cross-sell:** end the description with the same linked bundle line the other singles use, updated to the bundle's trade count (bundle: https://tradesheetsshop.gumroad.com/l/service-business-manager-bundle).

## Description
{desc}
"""


BASE = ("*{{margin:0;box-sizing:border-box}}body{{font-family:Inter,Helvetica,Arial,sans-serif;"
        "background:linear-gradient(135deg,#{light},#f7f6f2);color:#1d2428;display:flex;flex-direction:column;"
        "align-items:center;justify-content:center;text-align:center;overflow:hidden}}"
        ".pill{{background:#{acc};color:#fff;font-weight:700;border-radius:999px}}.sub{{color:#{acc};font-weight:600}}")


def trade_pages(slug, name, acc, light):
    hero = PRODUCTS / f"{slug}-business-manager" / "images" / "1_hero.png"
    img = "data:image/png;base64," + base64.b64encode(hero.read_bytes()).decode()
    base = BASE.format(acc=acc, light=light)
    cover = f"""<style>{base}body{{width:1280px;height:720px}}h1{{font-size:{76 if len(name) <= 20 else 64}px;font-weight:800;letter-spacing:-1.5px;color:#{acc}}}
.sub{{font-size:32px;margin:18px 0 32px}}.pill{{font-size:27px;padding:16px 32px}}</style>
<h1>{name.replace('&', '&amp;')}{' ' if len(name) <= 20 else '<br>'}Business Manager</h1><div class=sub>Quotes · Clients · Jobs · Invoices · Profit dashboard</div>
<div class=pill>Google Sheets &amp; Excel · Instant download</div>"""
    thumb = f"""<style>{base}body{{width:1000px;height:1000px;justify-content:flex-start;padding-top:90px}}h1{{font-size:{96 if len(name) <= 20 else 74}px;line-height:1.02;font-weight:800;letter-spacing:-2px;color:#{acc}}}
.sub{{font-size:34px;margin:22px 0 34px}}.pill{{font-size:28px;padding:14px 30px}}
.shot{{margin-top:50px;width:808px;height:520px;border-radius:20px;background:url({img}) -95px -515px / 1900px auto no-repeat;box-shadow:0 20px 50px rgba(20,30,40,.2)}}</style>
<h1>{name.replace('&', '&amp;')}<br>Business Manager</h1><div class=sub>Quotes · Clients · Invoices · Profit</div>
<div class=pill>Google Sheets &amp; Excel</div><div class=shot></div>"""
    return cover, thumb


def bundle_pages():
    base = BASE.format(acc="1d2428", light="eef0f2")
    chips = "".join(f'<div class=chip style="background:#{a}">{n.replace("&", "&amp;")}</div>' for _, n, a, _ in TRADES)
    chip = ".chip{{color:#fff;font-weight:700;border-radius:14px}}"
    cover = f"""<style>{base}{chip.format()}body{{width:1280px;height:720px}}h1{{font-size:70px;font-weight:800;letter-spacing:-1.5px}}
.sub{{font-size:30px;margin:14px 0 34px}}.row{{display:flex;flex-wrap:wrap;justify-content:center;gap:16px;width:1120px;margin-bottom:36px}}
.chip{{font-size:28px;padding:16px 26px}}.pill{{font-size:26px;padding:15px 30px}}</style>
<h1>Service Business Manager Bundle</h1><div class=sub>{N} trade-specific spreadsheets · Google Sheets &amp; Excel</div>
<div class=row>{chips}</div><div class=pill>All {N} for $39 · save ${SINGLES - 39:.2f}</div>"""
    thumb = f"""<style>{base}{chip.format()}body{{width:1000px;height:1000px}}h1{{font-size:88px;line-height:1.02;font-weight:800;letter-spacing:-2px}}
.sub{{font-size:34px;margin:16px 0 30px}}.col{{display:flex;flex-direction:column;gap:12px;width:640px;margin-bottom:30px}}
.chip{{font-size:{28 if N <= 6 else 24}px;padding:11px}}.pill{{font-size:30px;padding:16px 34px}}
{".col{display:grid;grid-template-columns:1fr 1fr;width:860px}.chip:last-child:nth-child(odd){grid-column:span 2}" if N > 6 else ""}</style>
<h1>{N} Business<br>Managers</h1><div class=sub>Google Sheets &amp; Excel</div>
<div class=col>{chips}</div><div class=pill>Bundle · $39</div>"""
    return cover, thumb


def build_zip():
    path = HERE / BUNDLE_DIR / f"TradeSheets-{N}-Trade-Bundle.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for slug, name, _, _ in TRADES:
            src = PRODUCTS / f"{slug}-business-manager"
            folder = f"{name} Business Manager/"
            for arc, f in [(FILE(name), src / FILE(name)),
                           (FILE(name).replace("-Business-Manager.xlsx", "-Quick-Start-Guide.pdf"), src / "Quick-Start-Guide.pdf")]:
                info = zipfile.ZipInfo(folder + arc, date_time=tuple(map(int, DATE.split("-"))) + (0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, f.read_bytes())
    print("wrote", path.relative_to(HERE), f"{path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    pages = []
    for slug, name, acc, light in TRADES:
        if slug in NEW:
            (HERE / slug).mkdir(exist_ok=True)
            (HERE / slug / "GUMROAD.md").write_text(gumroad_md(slug, name))
            pages.append((slug, *trade_pages(slug, name, acc, light)))
    (HERE / BUNDLE_DIR).mkdir(exist_ok=True)
    pages.append((BUNDLE_DIR, *bundle_pages()))
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("PW_CHROMIUM")); pg = b.new_page()
        for folder, cover, thumb in pages:
            for fname, html, w, h in [("gumroad-cover-1280x720.png", cover, 1280, 720), ("gumroad-thumb-1000.png", thumb, 1000, 1000)]:
                pg.set_viewport_size({"width": w, "height": h}); pg.set_content(html); pg.wait_for_timeout(200)
                pg.screenshot(path=str(HERE / folder / fname)); print("wrote", f"{folder}/{fname}")
        b.close()
    build_zip()
