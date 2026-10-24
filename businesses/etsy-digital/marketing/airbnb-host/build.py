"""Airbnb Host Business Manager marketing kit (2026-10-24): Gumroad draft (GUMROAD.md, cover 1280x720, thumbnail 1000)
and 5 organic Pinterest pins (1000x1500), all cropped from the real listing images (example data).
Not part of the trade bundle (different buyer). Pin template and crop helper reused from ../organic-pins/build_pins.py.
Run: PW_CHROMIUM=/opt/pw-browsers/chromium python3 build.py"""
import base64, os, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "organic-pins"))
import build_pins as base  # noqa: E402
from playwright.sync_api import sync_playwright

S = "airbnb-host"  # -> etsy-digital/airbnb-host-business-manager/
PROD = HERE.parents[3] / "etsy-digital" / f"{S}-business-manager"
ACC, LIGHT = "1E6B64", "E3F1EF"  # from the product's build.py
T = dict(name="Airbnb Host", acc="#" + ACC, bg1="#" + LIGHT)
K = "For Airbnb &amp; Vrbo hosts"
PINS = [
 ("1_pricing", K, "How much should you charge per night?",
  "Enter your monthly costs and occupancy. Get your break-even rate and the rate for your profit goal.",
  base.crop(S, "5_pricing.png", (1020, 340, 1820, 925), (180, 1270, 980, 1365), stack=True)),
 ("2_dashboard", K, "Run your short-term rental from one spreadsheet",
  "Nights, occupancy, ADR and profit for every month, every property. No app, no monthly subscription.",
  base.crop(S, "2_dashboard.png", (180, 592, 770, 1198), (770, 592, 885, 1198), (1640, 592, 1820, 1198))),
 ("3_turnovers", "Cleaning schedule", "Never miss a turnover again",
  "Every check-out with the next check-in, guest count and cleaner. Same-day turnovers turn red.",
  base.crop(S, "4_turnovers.png", (90, 657, 565, 1218), (757, 657, 955, 1218), (1235, 657, 1520, 1218))),
 ("4_bookings", "Know your numbers", "See what you really keep from every booking",
  "Platform fee and cleaning subtracted on each stay. Unpaid direct bookings turn red.",
  base.crop(S, "3_bookings.png", (90, 678, 480, 1197), (1420, 678, 1910, 1197))),
 ("5_supplies", "Supplies tracker", "Never run out of toilet paper mid-stay",
  "Set par levels. Low items turn red with the quantity and cost to reorder.",
  base.crop(S, "6_supplies.png", (90, 657, 1003, 1218))),
]


def gumroad_md():
    desc = (PROD / "LISTING.md").read_text().split("## Description\n", 1)[1].strip()
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
    return f"""# Gumroad product draft: Airbnb Host Business Manager (2026-10-24)

DRAFT. Not published. Going live on Gumroad is part of the open "Publish Airbnb Host Business Manager" item in network/APPROVALS.md (Etsy + Gumroad).

Set up like the live singles (e.g. https://tradesheetsshop.gumroad.com/l/pet-sitting-dog-walking-business-manager).

- **Name:** Airbnb Host Business Manager: Short-Term Rental Spreadsheet for Google Sheets & Excel
- **URL slug:** `airbnb-host-business-manager`
- **Price:** $14.99 (same as Etsy; Gumroad keeps about 10% + card processing, so about $12.75 per sale)
- **Cover:** `airbnb-host/gumroad-cover-1280x720.png`, then the 7 images from `etsy-digital/airbnb-host-business-manager/images/` in listing order (1_hero, 3_bookings, 4_turnovers, 2_dashboard, 5_pricing, 6_supplies, 7_included)
- **Thumbnail:** `airbnb-host/gumroad-thumb-1000.png` (square)
- **Content:** upload `etsy-digital/airbnb-host-business-manager/Airbnb-Host-Business-Manager.xlsx` and `Quick-Start-Guide.pdf`
- **Summary (the "You'll get" line):** One spreadsheet for bookings, payouts, turnovers, expenses, supplies and profit for every property. Google Sheets & Excel.
- **Additional details:** Format: .xlsx + PDF guide · Tabs: 10 · Works in: Google Sheets, Excel · Properties: up to 20
- **Cross-sell:** none. Do NOT add the trade-bundle line (the bundle is for cleaning/lawn/etc. businesses, a different buyer) and don't add Airbnb to the bundle.
- **Tags (Gumroad discover):** airbnb, short term rental, vacation rental, vrbo, spreadsheet

## Description
{desc}
"""


def pages():
    hero = "data:image/png;base64," + base64.b64encode((PROD / "images" / "1_hero.png").read_bytes()).decode()
    css = (f"*{{margin:0;box-sizing:border-box}}body{{font-family:Inter,Helvetica,Arial,sans-serif;background:linear-gradient(135deg,#{LIGHT},#f7f6f2);"
           f"color:#1d2428;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;overflow:hidden}}"
           f".pill{{background:#{ACC};color:#fff;font-weight:700;border-radius:999px}}.sub{{color:#{ACC};font-weight:600}}h1{{font-weight:800;color:#{ACC}}}")
    cover = f"""<style>{css}body{{width:1280px;height:720px}}h1{{font-size:76px;letter-spacing:-1.5px}}
.sub{{font-size:32px;margin:18px 0 32px}}.pill{{font-size:27px;padding:16px 32px}}</style>
<h1>Airbnb Host Business Manager</h1><div class=sub>Bookings · Turnovers · Occupancy · Expenses · Profit</div>
<div class=pill>Google Sheets &amp; Excel · Instant download</div>"""
    thumb = f"""<style>{css}body{{width:1000px;height:1000px;justify-content:flex-start;padding-top:90px}}h1{{font-size:96px;line-height:1.02;letter-spacing:-2px}}
.sub{{font-size:34px;margin:22px 0 34px}}.pill{{font-size:28px;padding:14px 30px}}
.shot{{margin-top:80px;width:712px;height:250px;border-radius:20px;background:#fff url({hero}) -76px -540px / 1500px auto no-repeat;box-shadow:0 20px 50px rgba(20,30,40,.2)}}</style>
<h1>Airbnb Host<br>Business Manager</h1><div class=sub>Bookings · Turnovers · Profit</div>
<div class=pill>Google Sheets &amp; Excel</div><div class=shot></div>"""
    return cover, thumb


if __name__ == "__main__":
    (HERE / "GUMROAD.md").write_text(gumroad_md())
    (HERE / "pins").mkdir(exist_ok=True)
    cover, thumb = pages()
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("PW_CHROMIUM") or None); pg = b.new_page()
        for fname, html, w, h in [("gumroad-cover-1280x720.png", cover, 1280, 720), ("gumroad-thumb-1000.png", thumb, 1000, 1000)]:
            pg.set_viewport_size({"width": w, "height": h}); pg.set_content(html); pg.wait_for_timeout(200)
            pg.screenshot(path=str(HERE / fname)); print("wrote", fname)
        pg.set_viewport_size({"width": 1000, "height": 1500})
        for n, k, h, s, shot in PINS:
            pg.set_content(base.page(T, k, h, s, shot, brand="Airbnb Host<br>Business Manager"))
            pg.wait_for_timeout(200); pg.screenshot(path=str(HERE / "pins" / f"airbnb_{n}.png")); print("wrote", n)
        b.close()
