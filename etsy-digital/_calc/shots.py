"""Listing images for a Pricing Calculator (Builder 2026-11-16). Same look as _engine/shots.py.
Usage: python3 shots.py <key> <demo-recalculated.xlsx> <outdir>   -> writes img_*.html into outdir (render with render.js)."""
import datetime, html, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calc import TRADES
from openpyxl import load_workbook
key, src, outdir = sys.argv[1:4]
T = TRADES[key]; ACC = "#" + T["accent"]; LIGHT = "#" + T["light"]; NAME = T["name"]; TRADE = NAME.replace(" Pricing Calculator", "")
wb = load_workbook(src, data_only=True)
def fmt(v, kind=None):
    if v is None or v == "": return ""
    if isinstance(v, (datetime.datetime, datetime.date)): return v.strftime("%b %-d, %Y")
    if kind == "$": return "-" if v == 0 else ("−$" if v < 0 else "$") + f"{abs(v):,.2f}"
    if kind == "$0": return "-" if v == 0 else ("−$" if v < 0 else "$") + f"{abs(v):,.0f}"
    if kind == "%": return f"{v*100:.0f}%"
    if kind == "h": return f"{v:g}"
    if isinstance(v, float): return f"{v:,.2f}".rstrip("0").rstrip(".")
    if isinstance(v, int): return f"{v:,}"
    return html.escape(str(v))
TABS = ["Start Here", "Quote Calculator", "Estimate", "Quote Log", "Settings", "Full Business Manager"]
def win(tab, body, w=1700):
    t = "".join(f'<span class="tab {"on" if x == tab else ""}">{x}</span>' for x in TABS)
    return f'<div class="win" style="width:{w}px"><div class="bar"><i></i><i></i><i></i><span>{NAME}</span></div><div class="sheet">{body}</div><div class="tabs">{t}</div></div>'
CSS = f"""*{{box-sizing:border-box}}body{{margin:0;width:2000px;height:1600px;font-family:Inter,Arial,sans-serif;background:linear-gradient(135deg,{LIGHT},#F8F5EE);display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden}}
h1{{font-size:78px;margin:0 0 10px;color:#15324a;letter-spacing:-1px;text-align:center}} h2{{font-size:38px;margin:0 0 40px;color:{ACC};font-weight:600;text-align:center}}
.win{{background:#fff;border-radius:18px;box-shadow:0 30px 80px rgba(20,50,50,.25);overflow:hidden}}
.bar{{background:#f1f3f4;height:48px;display:flex;align-items:center;padding:0 18px;gap:9px;font-size:20px;color:#555}}.bar i{{width:14px;height:14px;border-radius:50%;background:#e0e0e0;display:inline-block}}.bar span{{margin-left:16px}}
.sheet{{padding:26px 30px}} .tabs{{background:#f1f3f4;padding:10px 20px;display:flex;gap:6px}}.tab{{font-size:17px;padding:7px 14px;border-radius:6px;color:#555}}.tab.on{{background:#fff;color:{ACC};font-weight:700;box-shadow:0 1px 3px rgba(0,0,0,.15)}}
table{{border-collapse:collapse;width:100%;font-size:21px}}th{{background:{ACC};color:#fff;padding:11px 10px;font-weight:600;text-align:left}}td{{padding:9px 10px;border-bottom:1px solid #e3e8ea;white-space:nowrap}}td.in{{background:#FFF7D6;color:#1F4EB4}}
td.r{{text-align:right}} .ok{{background:#DFF0D8!important;color:#2E6B2E!important;font-weight:700}} .bad{{background:#F8D7DA!important;color:#9C1C28!important;font-weight:700}} .lost{{color:#8A8F98}}
.kpis{{display:flex;gap:18px;margin-bottom:24px}}.kpi{{flex:1;background:{LIGHT};border-radius:14px;padding:16px 20px}}.kpi b{{display:block;font-size:40px;color:{ACC}}}.kpi span{{font-size:19px;color:#57606a}}
.ttl{{font-size:34px;font-weight:800;color:{ACC};margin-bottom:6px}}.sub{{font-size:20px;color:#57606a;margin-bottom:20px;font-style:italic}}
"""
def page(name, inner, head=None, sub=None, extra=""):
    hh = (f"<h1>{head}</h1>" if head else "") + (f"<h2>{sub}</h2>" if sub else "")
    open(os.path.join(outdir, f"img_{name}.html"), "w").write(f"<html><head><meta charset='utf-8'><style>{CSS}{extra}</style></head><body>{hh}{inner}</body></html>")

q = wb["Quote Calculator"]
def qrows(rows, big=False):
    h = ""
    for r in rows:
        lab = q.cell(r, 1).value; v = q.cell(r, 2).value
        if not lab: continue
        if r == 24: h += f'<tr class="qp"><td>Quote price</td><td class="r">{fmt(v, "$0")}</td></tr>'; continue
        kind = {26: "h", 29: "%", 35: None}.get(r, "$")
        cls = "r"
        if r == 32: cls += " ok" if str(v).startswith("✔") else " bad"; kind = None
        if r in (23,) and not v: continue
        h += f'<tr><td>{lab}</td><td class="{cls}">{fmt(v, kind) if kind else html.escape(str(v))}</td></tr>'
    return h
qi = "".join(f'<tr><td>{q.cell(r,1).value}</td><td class="in">{fmt(q.cell(r,2).value)}</td></tr>' for r in range(4, 9))
qa = "".join(f'<tr><td>{q.cell(r,4).value}</td><td class="in">{q.cell(r,5).value}</td></tr>' for r in range(4, 10))
HCSS = f"""body{{justify-content:flex-start;padding-top:52px}} .hero table{{font-size:28px}} .hero td{{padding:12px 14px}} .hero th{{font-size:28px;padding:13px}}
tr.qp td{{background:{ACC};color:#fff;font-size:42px;font-weight:800;padding:14px 12px;border:0}}
.hl{{font-size:112px;font-weight:800;color:#15324a;letter-spacing:-2px;margin:0;line-height:1.05;text-align:center}}
.hs{{font-size:46px;font-weight:700;color:{ACC};margin:14px 0 22px;text-align:center}}
.pill{{display:inline-flex;align-items:center;gap:14px;background:#15324a;color:#fff;font-size:34px;font-weight:700;padding:14px 34px;border-radius:50px;margin-bottom:30px}}"""
hb = (f'<div class="ttl" style="font-size:40px">Quote Calculator</div><div class="sub" style="font-size:23px">Type the job details. Price, hours and profit fill in instantly.</div>'
      f'<div style="display:flex;gap:44px"><div style="flex:1"><table><tr><th colspan=2>Job details</th></tr>{qi}</table><table style="margin-top:20px"><tr><th colspan=2>Add-ons</th></tr>{qa}</table></div>'
      f'<div style="flex:1"><table><tr><th colspan=2>Your quote</th></tr>{qrows([16,17,18,19,20,22,23,24,26,28,30,32])}</table></div></div>')
open(os.path.join(outdir, "img_1_hero.html"), "w").write(f'<html><head><meta charset="utf-8"><style>{CSS}{HCSS}</style></head><body><div class="hl">Price Every Job in 60 Seconds</div><div class="hs">{TRADE} Pricing Calculator + Printable Estimate</div><div class="pill">&#x2B07; Instant Download &nbsp;·&nbsp; Excel &amp; Google Sheets</div><div class="hero">{win("Quote Calculator", hb, 1880)}</div></body></html>')

# 2 estimate
e = wb["Estimate"]
lines = "".join(f'<tr><td>{fmt(e.cell(r,1).value)}</td><td class="r">{fmt(e.cell(r,5).value,"$")}</td></tr>' for r in range(12, 21) if e.cell(r, 1).value not in (None, ""))
est = (f'<div style="width:1150px;padding:24px 34px;font-size:23px;line-height:1.45"><div style="display:flex;justify-content:space-between"><div><b style="font-size:32px;color:{ACC}">{fmt(e["A1"].value)}</b><br>{fmt(e["A2"].value)}<br>{fmt(e["A3"].value)}<br>{fmt(e["A4"].value)}</div>'
       f'<div style="text-align:right"><b style="font-size:48px;color:{ACC}">ESTIMATE</b><br>Estimate # {e["E3"].value}<br>Date {fmt(e["E4"].value)}<br>Valid until {fmt(e["E5"].value)}</div></div><br>'
       f'<b style="color:{ACC}">PREPARED FOR</b><br><b>{fmt(e["A8"].value)}</b><br>{fmt(e["A9"].value)}<br><br>'
       f'<table><tr><th>Description</th><th style="text-align:right">Amount</th></tr>{lines}<tr><td class="r"><b>TOTAL</b></td><td class="r"><b style="font-size:30px;color:{ACC}">{fmt(e["E22"].value,"$")}</b></td></tr></table>'
       f'<div style="color:#57606a;font-style:italic;margin-top:10px">{fmt(e["A23"].value)}</div><div style="margin-top:14px;font-size:20px">{fmt(e["A25"].value)}</div><div style="margin-top:22px;font-size:20px">{fmt(e["A27"].value)}</div></div>')
page("2_estimate", win("Estimate", f'<div style="display:flex;justify-content:center">{est}</div>', 1300), "Send a professional estimate", "Every line fills in from your quote. Print or save as PDF.")

# 3 profit check
pb = (f'<div class="ttl">Know your profit before you say yes</div><div class="sub">Labor cost, profit, margin and your real hourly rate — checked against the rate you want to earn</div>'
      f'<table style="font-size:28px"><tr><th colspan=2>Result</th></tr>{qrows([24,26,27,28,29,30,31,32,33,35,36])}</table>')
page("3_profit", win("Quote Calculator", pb, 1300), "Never underprice a job again", "Set a target hourly rate and a minimum charge. The calculator flags low quotes.", extra=f"tr.qp td{{background:{ACC};color:#fff;font-size:38px;font-weight:800;border:0}} td{{padding:12px 14px}}")

# 4 quote log
l = wb["Quote Log"]
K = [(1, None), (2, None), (3, None), (4, None), (5, "%"), (6, "$0"), (7, "$0"), (8, None)]
kp = "".join(f'<div class="kpi"><span>{l.cell(4,c).value}</span><b>{fmt(l.cell(5,c).value,k)}</b></div>' for c, k in K)
rows = [r for r in range(8, 30) if l.cell(r, 2).value]
cols = [1, 2, 4, 5, 6, 8, 9, 12, 13]; kinds = [None, None, None, None, "$0", None, None, "$0", None]
th = "".join(f"<th>{l.cell(7,c).value}</th>" for c in cols)
tb = ""
for r in rows:
    tb += "<tr>"
    for c, k in zip(cols, kinds):
        v = l.cell(r, c).value; cls = "in" if c <= 10 else ""
        if c == 13: cls = {"Follow up now": "bad", "Won ✔": "ok", "Lost": "lost"}.get(v, "")
        tb += f'<td class="{cls}">{fmt(v, k)}</td>'
    tb += "</tr>"
lb = f'<div class="ttl">Quote Log</div><div class="sub">Won, lost or pending — plus the follow-ups to make today</div><div class="kpis">{kp}</div><table style="font-size:19px"><tr>{th}</tr>{tb}</table>'
page("4_log", win("Quote Log", lb, 1880), "Track every quote. Win more jobs.", "Win rate, yearly value and follow-up reminders")

# 5 settings
s = wb["Settings"]
def tbl(rng, cols, kinds, head):
    h = "<table><tr>" + "".join(f"<th>{x}</th>" for x in head) + "</tr>"
    for r in rng:
        if s.cell(r, cols[0]).value in (None, ""): continue
        h += "<tr>" + "".join(f'<td class="in">{fmt(s.cell(r,c).value,k)}</td>' if c != 4 or head[0] != "Quote factor" else f'<td>{fmt(s.cell(r,c).value)}</td>' for c, k in zip(cols, kinds)) + "</tr>"
    return h + "</table>"
biz = "<table><tr><th colspan=2>Your rates</th></tr>" + "".join(f'<tr><td>{s.cell(r,1).value.split(" (")[0]}</td><td class="in">{fmt(s.cell(r,2).value,"$" if r in (8,9,10) else None)}</td></tr>' for r in (4, 8, 9, 10, 11)) + "</table>"
sb = (f'<div class="ttl">Settings</div><div class="sub">Every price, factor and discount is yours to change</div><div style="display:flex;gap:30px"><div style="flex:1">'
      f'{tbl(range(5,13),[4,5,6],[None,"$","h"],["Service","Base price","Est. hours"])}<div style="height:20px"></div>{biz}</div><div style="flex:1">'
      f'{tbl(range(24,30),[4,5,6],[None,"$","h"],["Add-on","Price","Hours"])}<div style="height:20px"></div>{tbl(range(33,38),[4,5,6],[None,"h","%"],["Frequency","Days between","Discount"])}</div></div>')
page("5_settings", win("Settings", sb, 1880), "Your prices. Your rates.", "Services, add-ons, discounts, labor cost and minimum charge")

# 6 upgrade
calc_f = ["Quote Calculator with profit and hourly rate", "Target-rate check and minimum charge", "Printable customer estimate", "Quote Log with win rate and follow-ups", "Editable prices, add-ons and discounts"]
mgr_f = ["The same pricing factors and Settings cells", "Client tracker with repeat-visit reminders", "Jobs log with profit on every job", "Invoice generator (print or PDF)", "Expense tracker and monthly profit dashboard"]
li = lambda xs: "".join(f'<div style="font-size:28px;margin:14px 0">✔ {x}</div>' for x in xs)
card = lambda t, p, xs, hl: f'<div style="flex:1;background:#fff;border-radius:22px;padding:40px 44px;box-shadow:0 20px 50px rgba(20,50,50,.15);{"border:5px solid "+ACC if hl else ""}"><div style="font-size:24px;font-weight:700;color:#57606a">{p}</div><div style="font-size:46px;font-weight:800;color:{ACC};margin:6px 0 18px">{t}</div>{li(xs)}</div>'
ub = f'<div style="display:flex;gap:40px;width:1800px">{card(NAME, "THIS FILE", calc_f, True)}{card(T["manager"], "WHEN YOU GROW", mgr_f, False)}</div><div style="font-size:30px;color:#15324a;margin-top:40px">Your services, add-ons and discounts copy straight across: same Settings cells in both files.</div>'
page("6_upgrade", ub, "Start with pricing. Grow into the full system.", None, extra="h1{margin-bottom:50px}")

# 7 included
feat = [("🧮", "Quote calculator", T["inputs_words"].capitalize()), ("💰", "Profit per job", "Labor cost, profit, margin and hourly rate"), ("🎯", "Target rate check", "Flags quotes below the rate you want"),
        ("🧾", "Printable estimate", "Customer-ready, print or save as PDF"), ("📋", "Quote log", "Won / lost / pending and win rate"), ("🔔", "Follow-up reminders", "See which quotes to chase today"),
        ("⚙️", "Fully editable", "Your services, prices, add-ons and discounts"), ("✅", "Google Sheets + Excel", "Instant download — no app, no subscription")]
fb = "".join(f'<div style="background:#fff;border-radius:16px;padding:28px;box-shadow:0 10px 30px rgba(20,50,50,.12)"><div style="font-size:46px">{a}</div><div style="font-size:30px;font-weight:800;color:#15324a;margin:8px 0">{b}</div><div style="font-size:22px;color:#57606a">{c}</div></div>' for a, b, c in feat)
page("7_included", f'<div style="display:grid;grid-template-columns:repeat(4,400px);gap:26px">{fb}</div>', "What's included", "6 tabs + quick start guide · instant digital download")
print("ok", key)
