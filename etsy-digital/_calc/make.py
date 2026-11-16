"""Build a Pricing Calculator product end to end (Builder 2026-11-16).
python3 make.py <key> <workdir>  ->  workdir/<key>/: product xlsx (recalculated), demo.xlsx, img_*.png, Quick-Start-Guide.pdf
Needs LibreOffice (recalc.py from the xlsx skill) and Playwright/Chromium."""
import os, shutil, subprocess, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from calc import TRADES, build
key, work = sys.argv[1], sys.argv[2]
T = TRADES[key]; d = os.path.join(work, key); os.makedirs(d, exist_ok=True)
RECALC = "/mnt/skills/public/xlsx/scripts/recalc.py"
prod = os.path.join(d, T["file"]); demo = os.path.join(d, "demo.xlsx")
build(key, prod); build(key, demo, demo=True)
for f in (prod, demo):
    r = json.loads(subprocess.run(["python3", RECALC, f, "120"], capture_output=True, text=True).stdout)
    print(os.path.basename(f), r["total_formulas"], "formulas,", r["total_errors"], "errors"); assert r["total_errors"] == 0
subprocess.run(["python3", os.path.join(HERE, "shots.py"), key, demo, d], check=True)
ACC = "#" + T["accent"]; LIGHT = "#" + T["light"]
guide = f"""<html><head><meta charset="utf-8"><style>body{{font-family:Inter,Arial;margin:34px 54px;color:#15324a;font-size:14px;line-height:1.45}}h1{{color:{ACC};margin-bottom:0}}h2{{color:{ACC};font-size:17px;margin:18px 0 6px}}.s{{color:#57606a;margin-top:4px}}li{{margin:5px 0}}.box{{background:{LIGHT};border-radius:10px;padding:12px 18px}}</style></head><body>
<h1>{T["name"]}</h1><div class="s">Quick start guide · Google Sheets &amp; Excel</div>
<h2>Open it</h2>
<p><b>Excel:</b> double-click <i>{T["file"]}</i>.<br>
<b>Google Sheets:</b> go to drive.google.com → New → File upload → choose the file → open it → <b>File › Save as Google Sheets</b>. Work in the Google Sheets copy.</p>
<h2>Set up (5 minutes)</h2><ol>
<li><b>Settings:</b> your business name and contact, what one labor hour costs you, the hourly rate you want to earn (your <i>target rate</i>), your minimum job charge and how many days an estimate stays valid.</li>
<li>Still in <b>Settings:</b> your services with base prices and hours, the quote factors, add-ons and frequency discounts. The defaults are examples; replace them with your own prices.</li>
<li><b>Quote Log:</b> delete the rows marked <b>EXAMPLE</b>.</li></ol>
<h2>Every quote</h2><ol>
<li><b>Quote Calculator:</b> type the job details ({T["inputs_words"]}) and set each add-on to Yes or No. The price, estimated hours, labor cost, profit, margin and hourly rate fill in.</li>
<li>Check the <b>Target check</b> line. If it says <i>Below target</i>, the job pays less per hour than you want; <i>Price that hits your target rate</i> shows what to charge instead.</li>
<li>Type the customer's name and address, then open <b>Estimate</b>. Give it a number, then print it or use File › Download as PDF and send it.</li>
<li>Add a row to the <b>Quote Log</b>: date, customer, service, frequency, price and hours. Set <i>Status</i> to Pending with a follow-up date, then Won or Lost when you hear back. <i>Next step</i> turns red on the day to follow up.</li></ol>
<div class="box"><b>Color key:</b> yellow cells with blue text are yours to type in. White cells calculate automatically, so don't type over them.<br>
<b>How the price works:</b> base price + size and room/surface adjustments + add-ons, minus the frequency discount, rounded to the nearest $1. If that is below your minimum job charge, the minimum is used and the Estimate shows the adjustment.</div>
<h2>Want the whole business in one file?</h2>
<p>The <b>{T["manager"]}</b> uses the same pricing factors and Settings cells for services, add-ons and discounts, and adds clients with repeat-visit reminders, a jobs log with profit per job, invoices, expenses and a monthly profit dashboard. See the <i>Full Business Manager</i> tab for links.</p>
<p class="s">Questions? Message us on Etsy and we'll help.</p>
</body></html>"""
open(os.path.join(d, "guide.html"), "w").write(guide)
js = """const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
(async()=>{const b=await chromium.launch(); const dir=process.argv[2];
const p=await b.newPage({viewport:{width:2000,height:1600}});
for(const f of fs.readdirSync(dir).filter(f=>f.startsWith('img_')&&f.endsWith('.html'))){await p.goto('file://'+path.join(dir,f));await p.screenshot({path:path.join(dir,f.replace('img_','').replace('.html','.png'))});}
const g=await b.newPage(); await g.goto('file://'+path.join(dir,'guide.html')); await g.pdf({path:path.join(dir,'Quick-Start-Guide.pdf'),format:'Letter'});
await b.close();})();"""
open(os.path.join(work, "render.js"), "w").write(js)
subprocess.run(["node", os.path.join(work, "render.js"), d], check=True)
print("done", d)
