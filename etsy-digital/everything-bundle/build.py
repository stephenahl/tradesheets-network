"""Everything Bundle (2 tiers) packager. Packages EXISTING QA-passed files only; builds no new workbook.

Tier 1 "Everything Bundle" ($49): 10 trade Business Managers + 2 Pricing Calculators + START HERE.pdf
Tier 2 "Everything Bundle Pro" ($79): Tier 1 + Airbnb Host Business Manager + Client Setup License (PDF)
Run: python3 build.py            -> writes the 2 zips, 2 START HERE PDFs (+ PNG previews), MANIFEST.md
     python3 build.py --verify   -> also unzips both, recalculates every xlsx in LibreOffice, counts formulas/errors
"""
import hashlib, html, pathlib, shutil, subprocess, sys, tempfile, zipfile
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
P = HERE.parent  # etsy-digital/
DATE = (2026, 11, 23, 0, 0, 0)

# (folder slug, display name, file stem, one-line "what it prices")
MANAGERS = [
    ("cleaning", "Cleaning", "Cleaning", "bedrooms, bathrooms and square feet; weekly to one-time clients"),
    ("lawn-care", "Lawn Care", "Lawn-Care", "lawn size, beds, trees and obstacles; weekly mowing routes"),
    ("pressure-washing", "Pressure Washing", "Pressure-Washing", "house size, stories and extra surfaces; seasonal clients"),
    ("auto-detailing", "Auto Detailing", "Auto-Detailing", "vehicle size, pet hair and travel; maintenance clients"),
    ("window-cleaning", "Window Cleaning", "Window-Cleaning", "panes, stories and French windows; storefront routes"),
    ("pet-sitting-dog-walking", "Pet Sitting & Dog Walking", "Pet-Sitting-Dog-Walking", "service, number of pets, medications and travel"),
    ("pool-service", "Pool Service", "Pool-Service", "gallons, spa and debris level; weekly to monthly routes"),
    ("snow-removal", "Snow Removal", "Snow-Removal", "per-push and season contract by area, depth and obstacles"),
    ("handyman", "Handyman", "Handyman", "flat-rate job menu, materials markup and minimum charge"),
    ("carpet-cleaning", "Carpet Cleaning", "Carpet-Cleaning", "rooms, staircases, soil level and upholstery add-ons"),
]
CALCS = [
    ("pressure-washing", "Pressure Washing", "Pressure-Washing"),
    ("house-cleaning", "House Cleaning", "House-Cleaning"),
]
AIRBNB = ("airbnb-host", "Airbnb Host", "Airbnb-Host")

TIERS = {
    "everything": dict(title="Everything Bundle", zipname="TradeSheets-Everything-Bundle.zip", pro=False),
    "pro": dict(title="Everything Bundle Pro", zipname="TradeSheets-Everything-Bundle-Pro.zip", pro=True),
}


def entries(pro):
    """(archive path, source path) for every file in a tier."""
    root = "TradeSheets Everything Bundle Pro/" if pro else "TradeSheets Everything Bundle/"
    out = [(root + "00 START HERE.pdf", HERE / ("START-HERE-Pro.pdf" if pro else "START-HERE.pdf"))]
    for i, (slug, name, stem, _) in enumerate(MANAGERS, 1):
        src = P / f"{slug}-business-manager"
        f = f"{root}1 Business Managers/{i:02d} {name} Business Manager/"
        out += [(f + f"{stem}-Business-Manager.xlsx", src / f"{stem}-Business-Manager.xlsx"),
                (f + f"{stem}-Quick-Start-Guide.pdf", src / "Quick-Start-Guide.pdf")]
    for slug, name, stem in CALCS:
        src = P / f"{slug}-pricing-calculator"
        f = f"{root}2 Pricing Calculators/{name} Pricing Calculator/"
        out += [(f + f"{stem}-Pricing-Calculator.xlsx", src / f"{stem}-Pricing-Calculator.xlsx"),
                (f + f"{stem}-Pricing-Calculator-Guide.pdf", src / "Quick-Start-Guide.pdf")]
    if pro:
        slug, name, stem = AIRBNB
        src = P / f"{slug}-business-manager"
        f = f"{root}3 Short-Term Rental/{name} Business Manager/"
        out += [(f + f"{stem}-Business-Manager.xlsx", src / f"{stem}-Business-Manager.xlsx"),
                (f + f"{stem}-Quick-Start-Guide.pdf", src / "Quick-Start-Guide.pdf"),
                (root + "Client Setup License.pdf", HERE / "Client-Setup-License.pdf")]
    return out


CSS = """@page{size:Letter;margin:0}body{font-family:Inter,Arial,sans-serif;margin:0;color:#15324a;font-size:12.5px;line-height:1.45}
.pg{padding:44px 54px;page-break-after:always}.pg:last-child{page-break-after:auto}
h1{color:#1F5E8C;margin:0;font-size:30px}h2{color:#1F5E8C;font-size:16px;margin:20px 0 6px}.s{color:#57606a;margin-top:3px}
table{border-collapse:collapse;width:100%;margin-top:4px}td,th{border-bottom:1px solid #dfe5ea;padding:5px 6px;text-align:left;vertical-align:top}
th{background:#1F5E8C;color:#fff;font-weight:600}td.n{color:#57606a;width:22px}.box{background:#E7EFF7;border-radius:10px;padding:10px 16px;margin-top:12px}
li{margin:3px 0}code{background:#f1f3f5;padding:0 4px;border-radius:3px}"""


def start_here(pro):
    t = TIERS["pro" if pro else "everything"]
    rows = "".join(f"<tr><td class=n>{i:02d}</td><td><b>{html.escape(n)}</b></td><td>{html.escape(w)}</td></tr>"
                   for i, (_, n, _, w) in enumerate(MANAGERS, 1))
    n_files = 12 + (1 if pro else 0)
    use = ("Use them in your own business and, under the Client Setup License, for up to 10 client businesses. "
           "Don't resell or share the files publicly." if pro else
           "For use in your own business. Please don't resell or share the files.")
    pro_sec = ""
    if pro:
        pro_sec = """<h2>3 Short-Term Rental</h2><p><b>Airbnb Host Business Manager:</b> properties, bookings, turnovers, cleaning and supplies,
expenses, a nightly-rate Pricing Calculator (break-even and profit-target rates) and a dashboard with occupancy and payout by month.</p>
<h2>Client Setup License</h2><p>This Pro edition lets you set up these workbooks for <b>up to 10 client businesses</b> (for example as a
virtual assistant, bookkeeper or business coach). Read <i>Client Setup License.pdf</i> for exactly what is and isn't allowed.</p>"""
    return f"""<html><head><style>{CSS}</style></head><body>
<div class=pg><h1>{t['title']}</h1><div class=s>TradeSheets Co. · {n_files} spreadsheets · Google Sheets &amp; Excel · start here</div>
<h2>What's in the folder</h2>
<p><b>1 Business Managers</b>: one complete spreadsheet per trade. Each has a Quote Calculator, Client Tracker, Jobs Log,
Invoice Generator, Expense Tracker and Profit Dashboard, with its own quick start guide.</p>
<table><tr><th></th><th>Business Manager</th><th>Quotes are priced by</th></tr>{rows}</table>
<h2>2 Pricing Calculators</h2><p><b>Pressure Washing</b> and <b>House Cleaning</b> Pricing Calculators: a lighter file just for quoting.
Price a job, check profit and your hourly rate against a target, apply a minimum charge, print a customer estimate and keep a
Quote Log with your win rate and follow-ups.</p>
{pro_sec}
<div class=box><b>Pick your files.</b> Open only the trades you run; you don't need the rest. Running two services (say lawn care
and snow removal)? Keep one file per service so each has its own prices and quote factors.</div>
</div>
<div class=pg><h1 style="font-size:24px">Get started in 10 minutes</h1>
<h2>1. Open a file</h2><p><b>Excel:</b> double-click the .xlsx file.<br><b>Google Sheets:</b> drive.google.com → New → File upload →
choose the file → open it → <b>File › Save as Google Sheets</b>. Work in the Google Sheets copy.</p>
<h2>2. Set it up</h2><ol><li>Go to <b>Settings</b>: your business name and contact, hourly labor cost, mileage rate and your own prices.
The prices in the files are examples.</li><li>Add your clients, then delete or clear the rows marked <b>EXAMPLE</b>
(each file's quick start guide says which).</li><li>Yellow cells with blue text are yours to type in. White cells calculate, so don't type over them.</li></ol>
<h2>3. Calculator and manager work together</h2><p>Each Pricing Calculator uses the same Settings cells as its full Business Manager
(services D5:F12, quote factors E15:E20, add-ons D24:F29, frequency D33:F37). Set your prices once, then copy those ranges and
paste them into the other file. Use the calculator on the road for quick quotes, and the manager to run the jobs. Its last tab
describes the full manager, which you already have in folder 1.</p>
<h2>Good to know</h2><ul><li>Digital download; nothing is shipped. You need Excel or a free Google account.</li>
<li>The tax set-aside is a planning estimate, not tax advice.</li>
<li>{use}</li>
<li>Designed by TradeSheets Co. with the help of AI tools. Every workbook uses only functions that Excel and Google Sheets both
support, and every formula was checked before release.</li></ul>
<div class=box>Questions or need a tweak? Message us on Etsy (TradeSheetsShop) or reply to your Gumroad receipt and we'll help.</div>
</div></body></html>"""


LICENSE = f"""<html><head><style>{CSS}</style></head><body><div class=pg>
<h1>Client Setup License</h1><div class=s>TradeSheets Everything Bundle Pro · TradeSheets Co.</div>
<p style="margin-top:18px">Thank you for buying the Pro edition. It comes with this license so you can use the spreadsheets for the
businesses you support, not only your own.</p>
<h2>You may</h2><ul>
<li>Use every workbook in this bundle in your own business, with no limit on time.</li>
<li>Set up, customize and fill in the workbooks for <b>up to 10 client businesses</b> (for example as a virtual assistant,
bookkeeper, office manager or business coach).</li>
<li>Give each of those clients their own copy of the workbook you set up for them, for use in their own business.</li>
<li>Change prices, wording, colors and tabs to fit each client.</li></ul>
<h2>You may not</h2><ul>
<li>Resell, give away or share the files, or edited versions of them, as templates or products (on Etsy, Gumroad, your website or anywhere else).</li>
<li>Post the files or download links publicly, or upload them to a shared template library.</li>
<li>Use them for more than 10 client businesses without buying another copy.</li></ul>
<h2>Fine print</h2><ul>
<li>The workbooks are provided as-is. Default prices and rates are examples; you and your clients set your own.</li>
<li>The tax set-aside is a planning estimate, not tax advice.</li>
<li>Need more than 10 clients? Message TradeSheets Co. on Etsy or reply to your Gumroad receipt.</li></ul>
</div></body></html>"""


def render_pdfs():
    jobs = [("START-HERE.pdf", start_here(False)), ("START-HERE-Pro.pdf", start_here(True)),
            ("Client-Setup-License.pdf", LICENSE)]
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        for name, doc in jobs:
            pg.set_content(doc); pg.pdf(path=str(HERE / name), format="Letter", print_background=True)
            print("wrote", name)
        b.close()
    prev = HERE / "previews"; prev.mkdir(exist_ok=True)
    for name, _ in jobs:  # PNG of every page, to look at
        subprocess.run(["pdftoppm", "-r", "70", "-png", str(HERE / name), str(prev / name[:-4])], check=True)


def build_zips():
    man = ["# Everything Bundle: zip manifest", "",
           "Generated by build.py from the QA-passed files in etsy-digital/. sha256 is of the source file (identical bytes in the zip).", ""]
    for key, t in TIERS.items():
        path = HERE / t["zipname"]
        ents = entries(t["pro"])
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for arc, src in ents:
                info = zipfile.ZipInfo(arc, date_time=DATE); info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, src.read_bytes())
        man += [f"## {t['title']}: `{t['zipname']}` ({path.stat().st_size // 1024} KB, {len(ents)} files)", "",
                "| File in zip | Source | KB | sha256 (first 12) |", "|---|---|---|---|"]
        for arc, src in ents:
            man.append(f"| {arc.split('/', 1)[1]} | {src.relative_to(P)} | {src.stat().st_size // 1024} | "
                       f"{hashlib.sha256(src.read_bytes()).hexdigest()[:12]} |")
        man.append("")
        print("wrote", path.name, f"{path.stat().st_size // 1024} KB", len(ents), "files")
    (HERE / "MANIFEST.md").write_text("\n".join(man))


def verify():
    import openpyxl
    errs = ("#REF!", "#VALUE!", "#DIV/0!", "#NAME?", "#N/A", "#NUM!", "#NULL!")
    for t in TIERS.values():
        tmp = pathlib.Path(tempfile.mkdtemp())
        with zipfile.ZipFile(HERE / t["zipname"]) as z:
            assert z.testzip() is None
            z.extractall(tmp)
        xl = sorted(tmp.rglob("*.xlsx"))
        out = tmp / "recalc"; out.mkdir()
        for f in xl:  # LibreOffice recalculates on load and re-saves
            subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(out / f.parent.name), str(f)],
                           check=True, capture_output=True, timeout=180)
        total_f = total_e = 0
        for f in xl:
            nf = sum(1 for ws in openpyxl.load_workbook(f).worksheets for r in ws.iter_rows() for c in r
                     if isinstance(c.value, str) and c.value.startswith("="))
            wb = openpyxl.load_workbook(out / f.parent.name / f.name, data_only=True)
            bad = [(ws.title, c.coordinate, c.value) for ws in wb.worksheets for r in ws.iter_rows() for c in r
                   if isinstance(c.value, str) and c.value.strip() in errs]
            total_f += nf; total_e += len(bad)
            print(f"  {f.name}: {nf} formulas, {len(bad)} errors {bad[:3] if bad else ''}")
        print(f"{t['title']}: {len(xl)} workbooks, {total_f} formulas, {total_e} errors")
        shutil.rmtree(tmp)


if __name__ == "__main__":
    render_pdfs()
    build_zips()
    if "--verify" in sys.argv:
        verify()
