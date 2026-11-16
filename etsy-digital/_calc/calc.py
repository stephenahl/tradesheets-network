"""Standalone Pricing Calculator generator (pilot, Builder 2026-11-16).
Cut from the Business Manager engine (etsy-digital/_engine/build.py): same Settings layout
(services D5:F12, quote factors E15:E20, add-ons D24:F29, frequency D33:F37) so a buyer who upgrades
can copy their prices straight across.

Tabs: Start Here, Quote Calculator, Estimate (printable, customer-facing), Quote Log, Settings,
Full Business Manager (upsell).

Usage: python3 calc.py <key> <out.xlsx> [demo]
  key  = pw | cleaning   (see TRADES)
  demo = fills the Quote Log with sample rows for the listing images
"""
import sys
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.comments import Comment
from openpyxl.worksheet.properties import PageSetupProperties

TRADES = {
 "pw": dict(
  name="Pressure Washing Pricing Calculator", manager="Pressure Washing Business Manager",
  file="Pressure-Washing-Pricing-Calculator.xlsx", accent="1F5E8C", light="E5EEF6",
  biz="Blue Wave Pressure Washing", labor_label="Hourly labor cost (what you pay per crew-hour)", labor=25,
  target=75, minimum=150,
  svcs=[("House Soft Wash",325,3),("Driveway & Walkways",150,1.5),("Deck / Patio Clean",225,2.5),("Roof Soft Wash",450,4),("Fence Cleaning",200,2.5),("Commercial Flatwork",300,3)],
  qf=[("Per extra story (over 1)",75,"$"),("Per extra surface (patio, walkway, steps)",60,"$"),("Per 250 sq ft over 2,000",20,"$"),("Extra hours per extra story",0.75,"0.00"),("Extra hours per extra surface",0.75,"0.00"),("Extra hours per 250 sq ft over 2,000",0.25,"0.00")],
  adds=[("Gutter brightening",75,0.75),("Window rinse",50,0.5),("Rust / stain removal",85,1),("Concrete sealing",150,2),("Trash can cleaning",15,0.25),("Oil stain treatment",40,0.5)],
  fq=[("Annual",365,0.05),("Every 6 months",182,0.10),("Quarterly",91,0.10),("Monthly",30,0.15),("One-time",None,0)],
  qi=[("Service","House Soft Wash"),("House size (sq ft)",2600),("Stories",2),("Extra surfaces",1),("Frequency","Annual")],
  addon_yes=(1,),
  adj=[("Story adjustment","MAX(0,B6-1)","$E$15","$E$18"),("Extra surface adjustment","MAX(0,B7)","$E$16","$E$19"),("Size adjustment","MAX(0,ROUNDUP((B5-2000)/250,0))","$E$17","$E$20")],
  detail='TEXT(\'Quote Calculator\'!B5,"#,##0")&" sq ft, "&\'Quote Calculator\'!B6&IF(\'Quote Calculator\'!B6=1," story, "," stories, ")&\'Quote Calculator\'!B7&IF(\'Quote Calculator\'!B7=1," extra surface"," extra surfaces")',
  generic="Pressure washing service", inputs_words="house size, stories, extra surfaces, add-ons and frequency",
  cust=("EXAMPLE – Johnson Family","12 Oak St, Springfield"),
  log=[(date(2026,10,20),"Lakeview HOA","(555) 410-2200","Commercial Flatwork","Quarterly",420,4.5,"Won",None,"Pool deck + entry walks"),
       (date(2026,10,22),"Patel Residence","(555) 320-1188","House Soft Wash","Annual",542,5.75,"Won",None,"2-story, rinse windows"),
       (date(2026,10,24),"Greene Residence","greene@example.com","Deck / Patio Clean","One-time",265,3.25,"Lost",None,"Went with cheaper bid"),
       (date(2026,10,27),"Ortiz Residence","(555) 870-4410","Driveway & Walkways","Every 6 months",185,2.25,"Won",None,"Oil stain on drive"),
       (date(2026,10,29),"Maple Dental","office@example.com","Commercial Flatwork","Monthly",300,3,"Won",None,"Sundays only"),
       (date(2026,11,2),"Kim Residence","(555) 640-0091","Roof Soft Wash","One-time",510,4.75,"Lost",None,"Wants spring"),
       (date(2026,11,5),"Brooks Residence","(555) 230-7720","House Soft Wash","Annual",470,4.5,"Pending",date(2026,11,12),"Call after 5pm"),
       (date(2026,11,9),"Hill Residence","hill@example.com","Fence Cleaning","One-time",240,3,"Pending",date(2026,11,16),"Cedar fence"),
       (date(2026,11,11),"Rivera Residence","(555) 902-3344","House Soft Wash","Every 6 months",515,5.25,"Pending",date(2026,11,20),"Sent estimate by text"),
       (date(2026,11,13),"Shah Residence","(555) 777-1203","Driveway & Walkways","Annual",205,2.5,"Pending",date(2026,11,23),"")],
  example_log=[(date(2026,10,22),"EXAMPLE – Patel Residence","(555) 320-1188","House Soft Wash","Annual",542,5.75,"Won",None,"2-story, rinse windows"),
               (date(2026,10,24),"EXAMPLE – Greene Residence","greene@example.com","Deck / Patio Clean","One-time",265,3.25,"Lost",None,"Went with cheaper bid"),
               (date(2026,11,9),"EXAMPLE – Hill Residence","hill@example.com","Fence Cleaning","One-time",240,3,"Pending",date(2026,11,16),"Cedar fence")],
 ),
 "cleaning": dict(
  name="House Cleaning Pricing Calculator", manager="Cleaning Business Manager",
  file="House-Cleaning-Pricing-Calculator.xlsx", accent="2F6F73", light="E6F1F1",
  biz="Sparkle & Shine Cleaning", labor_label="Hourly labor cost (what you pay per cleaner-hour)", labor=20,
  target=40, minimum=100,
  svcs=[("Standard Clean",120,2.5),("Deep Clean",220,4.5),("Move-In / Move-Out",280,5.5),("Office Clean",150,3),("Airbnb Turnover",95,2)],
  qf=[("Per extra bedroom (over 2)",20,"$"),("Per extra bathroom (over 1)",15,"$"),("Per 100 sq ft over 1,500",8,"$"),("Extra hours per bedroom",0.4,"0.0"),("Extra hours per bathroom",0.4,"0.0"),("Extra hours per 100 sq ft over 1,500",0.15,"0.00")],
  adds=[("Inside oven",35,0.5),("Inside fridge",30,0.5),("Interior windows",40,1),("Baseboards",30,0.75),("Inside cabinets",45,1),("Laundry",20,0.5)],
  fq=[("Weekly",7,0.15),("Every 2 weeks",14,0.10),("Every 4 weeks",28,0.05),("Monthly",30,0.05),("One-time",None,0)],
  qi=[("Service","Standard Clean"),("Square feet",2200),("Bedrooms",3),("Bathrooms",2),("Frequency","Every 2 weeks")],
  addon_yes=(0,3),
  adj=[("Bedroom adjustment","MAX(0,B6-2)","$E$15","$E$18"),("Bathroom adjustment","MAX(0,B7-1)","$E$16","$E$19"),("Size adjustment","MAX(0,ROUNDUP((B5-1500)/100,0))","$E$17","$E$20")],
  detail='TEXT(\'Quote Calculator\'!B5,"#,##0")&" sq ft, "&\'Quote Calculator\'!B6&" bed / "&\'Quote Calculator\'!B7&" bath"',
  generic="House cleaning service", inputs_words="square feet, bedrooms, bathrooms, add-ons and frequency",
  cust=("EXAMPLE – Johnson Family","12 Oak St, Springfield"),
  log=[(date(2026,10,19),"Patel Home","(555) 320-1188","Standard Clean","Every 2 weeks",248,5.6,"Won",None,"2 dogs, key under mat"),
       (date(2026,10,21),"Nguyen Home","nguyen@example.com","Deep Clean","One-time",310,6.5,"Won",None,"Before holiday guests"),
       (date(2026,10,23),"Greene Home","(555) 610-4422","Standard Clean","Weekly",145,3.4,"Lost",None,"Price too high"),
       (date(2026,10,26),"Oak St Apartments","leasing@example.com","Move-In / Move-Out","One-time",295,5.75,"Won",None,"Unit 4B"),
       (date(2026,10,28),"Bright Dental","office@example.com","Office Clean","Weekly",140,3,"Won",None,"After 6pm"),
       (date(2026,11,2),"Lake House Rental","host@example.com","Airbnb Turnover","Every 2 weeks",105,2.5,"Lost",None,"Hired in-house"),
       (date(2026,11,4),"Brooks Home","(555) 230-7720","Standard Clean","Every 4 weeks",195,4.4,"Pending",date(2026,11,11),"Wants Fridays"),
       (date(2026,11,9),"Hill Home","hill@example.com","Deep Clean","One-time",265,5.3,"Pending",date(2026,11,16),"Oven + fridge"),
       (date(2026,11,11),"Rivera Home","(555) 902-3344","Standard Clean","Every 2 weeks",215,4.6,"Pending",date(2026,11,20),"Sent estimate by text"),
       (date(2026,11,13),"Shah Home","(555) 777-1203","Standard Clean","Weekly",160,3.6,"Pending",date(2026,11,23),"")],
  example_log=[(date(2026,10,19),"EXAMPLE – Patel Home","(555) 320-1188","Standard Clean","Every 2 weeks",248,5.6,"Won",None,"2 dogs, key under mat"),
               (date(2026,10,23),"EXAMPLE – Greene Home","(555) 610-4422","Standard Clean","Weekly",145,3.4,"Lost",None,"Price too high"),
               (date(2026,11,9),"EXAMPLE – Hill Home","hill@example.com","Deep Clean","One-time",265,5.3,"Pending",date(2026,11,16),"Oven + fridge")],
 ),
}
# where the full manager is sold (live listings recorded in the repo)
LINKS = {"pw": ("https://www.etsy.com/listing/4595743330", "https://tradesheetsshop.gumroad.com/l/pressure-washing-business-manager"),
         "cleaning": ("https://www.etsy.com/listing/4595582995", "https://tradesheetsshop.gumroad.com/l/cleaning-business-manager")}

def build(key, outfile, demo=False):
    T = TRADES[key]; ACC = T["accent"]; LIGHT = T["light"]; F = "Arial"
    def font(**k): k.setdefault("name", F); k.setdefault("size", 10); return Font(**k)
    HDR = PatternFill("solid", fgColor=ACC); IN = PatternFill("solid", fgColor="FFF7D6"); BAND = PatternFill("solid", fgColor=LIGHT)
    thin = Side(style="thin", color="D0D7DE"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
    BLUE = "1F4EB4"; GREY = "57606A"
    MONEY = '$#,##0.00;($#,##0.00);"-"'; DATE = 'mmm d, yyyy'; PCT = '0.0%'
    fmtmap = {"$": MONEY}
    wb = Workbook()
    def sheet(t, first=False):
        ws = wb.active if first else wb.create_sheet(); ws.title = t
        ws.sheet_view.showGridLines = False; ws.sheet_properties.tabColor = ACC; return ws
    def title(ws, text, sub):
        ws["A1"] = text; ws["A1"].font = font(size=18, bold=True, color=ACC)
        ws["A2"] = sub; ws["A2"].font = font(italic=True, color=GREY); ws.row_dimensions[1].height = 30
    def hdr(c):
        c.font = font(bold=True, color="FFFFFF"); c.fill = HDR; c.border = BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    def inp(c, fmt=None):
        c.font = font(color=BLUE); c.fill = IN; c.border = BOX
        if fmt: c.number_format = fmt
    def calc(c, fmt=None, bold=False):
        c.font = font(bold=bold); c.border = BOX
        if fmt: c.number_format = fmt
    def section(ws, ref, text): ws[ref] = text; ws[ref].font = font(bold=True, size=12, color=ACC)
    def wrap(c): c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------------- START HERE
    s = sheet("Start Here", True)
    title(s, T["name"], "Quote Calculator · Printable Estimate · Quote Log — Google Sheets & Excel")
    s.column_dimensions["A"].width = 4; s.column_dimensions["B"].width = 26; s.column_dimensions["C"].width = 80
    section(s, "B4", "HOW TO USE")
    steps = [("1. Settings", "Enter your business name and contact, what one labor hour costs you, the hourly rate you want to earn, your minimum job charge, and your service prices, add-ons and frequency discounts."),
             ("2. Quote Calculator", f"Type the job details ({T['inputs_words']}). Price, hours, labor cost, profit and your hourly rate fill in instantly, with a check against your target rate."),
             ("3. Estimate", "A customer-ready estimate built from the quote: your business details, the customer, each line item and the total. Print it or File > Download as PDF and send it."),
             ("4. Quote Log", "Log each quote you send. Mark it Won, Lost or Pending and set a follow-up date. See your win rate, won value per year and which quotes to chase today.")]
    for i, (a, b) in enumerate(steps):
        r = 5 + i; s.cell(r, 2, a).font = font(bold=True); c = s.cell(r, 3, b); c.font = font(); wrap(c); s.row_dimensions[r].height = 30
    section(s, "B10", "COLOR KEY")
    k = s.cell(11, 2, "Yellow cell, blue text"); inp(k); s.cell(11, 3, "Type here — your inputs").font = font()
    k = s.cell(12, 2, "White cell, black text"); calc(k); s.cell(12, 3, "Calculated automatically — don't type over these").font = font()
    section(s, "B14", "GOOGLE SHEETS")
    c = s.cell(15, 3, "Upload this file to Google Drive, open it, then File > Save as Google Sheets. Everything works in both Excel and Google Sheets."); c.font = font(); wrap(c); s.row_dimensions[15].height = 30
    c = s.cell(16, 3, "The Quote Log rows marked EXAMPLE show the format — delete them when you start. The prices in Settings are examples too: set your own."); c.font = font(italic=True, color=GREY); wrap(c); s.row_dimensions[16].height = 30
    section(s, "B18", "WANT MORE?")
    c = s.cell(19, 3, f"The {T['manager']} adds clients with repeat-visit reminders, a jobs log with profit per job, invoices, expenses and a monthly profit dashboard. See the 'Full Business Manager' tab."); c.font = font(); wrap(c); s.row_dimensions[19].height = 30

    # ---------------- SETTINGS (same D:F layout as the Business Manager)
    st = sheet("Settings")
    title(st, "Settings", "Your business details, prices and rates. Every yellow cell is editable.")
    for col, w in zip("ABCDEFGH", [44, 22, 4, 40, 14, 14, 4, 4]): st.column_dimensions[col].width = w
    rows = [("Business name", T["biz"], None), ("Owner / contact", "Your Name", None), ("Phone", "(555) 555-0123", None), ("Email", "hello@example.com", None),
            (T["labor_label"], T["labor"], MONEY), ("Target rate per hour (what you want each job to earn)", T["target"], MONEY),
            ("Minimum job charge", T["minimum"], MONEY), ("Estimate valid for (days)", 30, "0")]
    for i, (a, b, f) in enumerate(rows):
        r = 4 + i; st.cell(r, 1, a).font = font(); inp(st.cell(r, 2, b), f)
    st["B8"].comment = Comment("Pay rate plus payroll costs per labor hour. Used for labor cost and profit.", "Template")
    st["B9"].comment = Comment("Quote price divided by estimated hours should reach at least this. The Quote Calculator checks it.", "Template")
    st["B10"].comment = Comment("No quote goes below this. The Quote Calculator tops it up and the Estimate shows the adjustment.", "Template")
    section(st, "D3", "SERVICES")
    for j, h in enumerate(["Service", "Base price", "Est. hours"]): hdr(st.cell(4, 4 + j, h))
    svcs = T["svcs"] + [("", None, None)] * (8 - len(T["svcs"]))
    for i, (a, b, cc) in enumerate(svcs):
        r = 5 + i; inp(st.cell(r, 4, a or None)); inp(st.cell(r, 5, b), MONEY); inp(st.cell(r, 6, cc), "0.0")
    section(st, "D14", "QUOTE FACTORS")
    for i, (a, b, f) in enumerate(T["qf"]):
        r = 15 + i; st.cell(r, 4, a).font = font(); inp(st.cell(r, 5, b), fmtmap.get(f, f))
    section(st, "D22", "ADD-ONS")
    for j, h in enumerate(["Add-on", "Price", "Hours"]): hdr(st.cell(23, 4 + j, h))
    for i, (a, b, cc) in enumerate(T["adds"]):
        r = 24 + i; inp(st.cell(r, 4, a)); inp(st.cell(r, 5, b), MONEY); inp(st.cell(r, 6, cc), "0.00")
    section(st, "D31", "FREQUENCY")
    for j, h in enumerate(["Frequency", "Days between", "Discount"]): hdr(st.cell(32, 4 + j, h))
    for i, (a, b, cc) in enumerate(T["fq"]):
        r = 33 + i; inp(st.cell(r, 4, a)); inp(st.cell(r, 5, b), "0"); inp(st.cell(r, 6, cc), PCT)
    st.cell(39, 4, "Leave 'Days between' blank for one-time jobs.").font = font(italic=True, color=GREY)
    SVC = "Settings!$D$5:$D$12"; SVCP = "Settings!$E$5:$E$12"; SVCH = "Settings!$F$5:$F$12"
    FRQ = "Settings!$D$33:$D$37"; FRQD = "Settings!$E$33:$E$37"; FRQP = "Settings!$F$33:$F$37"
    def visits(cell):  # visits per year for a frequency name
        return f'IFERROR(IF(INDEX({FRQD},MATCH({cell},{FRQ},0))="",1,ROUND(365/INDEX({FRQD},MATCH({cell},{FRQ},0)),0)),1)'

    # ---------------- QUOTE CALCULATOR
    q = sheet("Quote Calculator")
    title(q, "Quote Calculator", "Price a job in under a minute. Change the yellow cells; everything else fills in.")
    for col, w in zip("ABCDEFGH", [36, 30, 4, 24, 12, 4, 6, 6]): q.column_dimensions[col].width = w
    section(q, "A3", "JOB DETAILS")
    for i, (a, b) in enumerate(T["qi"]):
        r = 4 + i; q.cell(r, 1, a).font = font(); inp(q.cell(r, 2, b), "#,##0" if isinstance(b, int) else None)
        q.cell(r, 2).alignment = Alignment(horizontal="left")
    for ref, f in (("B4", SVC), ("B8", FRQ)):
        dv = DataValidation(type="list", formula1=f); q.add_data_validation(dv); dv.add(ref)
    section(q, "D3", "ADD-ONS (Yes/No)")
    for i in range(6):
        r = 4 + i
        calc(q.cell(r, 4, f'=IF(Settings!D{24+i}="","",Settings!D{24+i})'))
        inp(q.cell(r, 5, "Yes" if i in T["addon_yes"] else "No"))
        # hidden helpers: G = 1 if this add-on is on, H = running count (lists add-ons on the Estimate without gaps)
        q.cell(r, 7, f'=IF(AND(E{r}="Yes",D{r}<>""),1,0)'); q.cell(r, 8, f'=SUM(G$4:G{r})')
    dv = DataValidation(type="list", formula1='"Yes,No"'); q.add_data_validation(dv); dv.add("E4:E9")
    q.column_dimensions["G"].hidden = True; q.column_dimensions["H"].hidden = True
    section(q, "A10", "CUSTOMER (optional, shows on the Estimate)")
    for i, (a, b) in enumerate([("Customer name", T["cust"][0].replace("EXAMPLE – ", "") if demo else T["cust"][0]), ("Address", T["cust"][1]), ("Quote date (blank = today)", None)]):
        r = 11 + i; q.cell(r, 1, a).font = font(); inp(q.cell(r, 2, b), DATE if i == 2 else None); q.cell(r, 2).alignment = Alignment(horizontal="left")
    section(q, "A15", "RESULT")
    a1, a2, a3 = T["adj"]
    hours = (f'IFERROR(INDEX({SVCH},MATCH(B4,{SVC},0)),0)+{a1[1]}*Settings!{a1[3]}+{a2[1]}*Settings!{a2[3]}+{a3[1]}*Settings!{a3[3]}'
             f'+SUMIFS(Settings!$F$24:$F$29,Settings!$D$24:$D$29,"<>",E4:E9,"Yes")')
    out = [(16, "Base price", f'=IFERROR(INDEX({SVCP},MATCH(B4,{SVC},0)),0)', MONEY),
           (17, a1[0], f'={a1[1]}*Settings!{a1[2]}', MONEY),
           (18, a2[0], f'={a2[1]}*Settings!{a2[2]}', MONEY),
           (19, a3[0], f'={a3[1]}*Settings!{a3[2]}', MONEY),
           (20, "Add-ons", '=SUMIFS(Settings!$E$24:$E$29,Settings!$D$24:$D$29,"<>",E4:E9,"Yes")', MONEY),
           (21, "Subtotal", '=SUM(B16:B20)', MONEY),
           (22, "Frequency discount", f'=-B21*IFERROR(INDEX({FRQP},MATCH(B8,{FRQ},0)),0)', MONEY),
           (23, "Minimum job charge top-up", '=IF(B21=0,0,MAX(0,Settings!$B$10-ROUND(B21+B22,0)))', MONEY),
           (24, "QUOTE PRICE (per visit, rounded to $1)", '=ROUND(B21+B22,0)+B23', MONEY),
           (26, "Estimated hours", "=" + hours, "0.00"),
           (27, "Labor cost", '=B26*Settings!$B$8', MONEY),
           (28, "Profit before supplies & travel", '=B24-B27', MONEY),
           (29, "Profit margin", '=IF(B24=0,0,B28/B24)', '0%'),
           (30, "Effective rate per hour", '=IF(B26=0,0,B24/B26)', MONEY),
           (31, "Your target rate per hour", '=Settings!$B$9', MONEY),
           (32, "Target check", '=IF(B26=0,"",IF(B30>=B31,"✔ Meets your target rate","✖ Below target — raise the price"))', None),
           (33, "Price that hits your target rate", '=ROUND(B26*B31,0)', MONEY),
           (35, "Visits per year", "=" + visits("B8"), "0"),
           (36, "Yearly value of this customer", '=B24*B35', MONEY)]
    for r, a, f, fm in out:
        q.cell(r, 1, a).font = font(bold=(r == 24)); calc(q.cell(r, 2, f), fm, bold=(r == 24))
    q["A24"].font = font(bold=True, size=13, color=ACC); q["B24"].font = font(bold=True, size=13, color=ACC); q["B24"].fill = BAND
    q["B33"].comment = Comment("Estimated hours x your target rate. If the quote is below this, the job earns less per hour than you want.", "Template")
    q.conditional_formatting.add("B32", CellIsRule(operator="equal", formula=['"✖ Below target — raise the price"'], fill=PatternFill("solid", fgColor="F8D7DA"), font=Font(name=F, color="9C1C28", bold=True)))
    q.conditional_formatting.add("B32", CellIsRule(operator="equal", formula=['"✔ Meets your target rate"'], fill=PatternFill("solid", fgColor="DFF0D8"), font=Font(name=F, color="2E6B2E", bold=True)))
    c = q.cell(38, 1, "Prices, quote factors, add-ons and discounts are set in Settings. The defaults are examples — set your own rates. Then log the quote in the Quote Log and send the Estimate."); c.font = font(italic=True, color=GREY)

    # ---------------- ESTIMATE (customer-facing)
    QC = "'Quote Calculator'!"
    e = sheet("Estimate")
    for col, w in zip("ABCDE", [30, 22, 14, 16, 16]): e.column_dimensions[col].width = w
    e["A1"] = "=Settings!B4"; e["A1"].font = font(size=16, bold=True, color=ACC)
    e["A2"] = "=Settings!B5"; e["A3"] = "=Settings!B6"; e["A4"] = "=Settings!B7"
    e["D1"] = "ESTIMATE"; e["D1"].font = font(size=20, bold=True, color=ACC)
    e["D3"] = "Estimate #"; inp(e["E3"]); e["E3"].value = "Q-0001"
    e["E3"].comment = Comment("Type your own estimate number. Everything else on this page fills in from the Quote Calculator.", "Template")
    e["D4"] = "Date"; e["E4"] = f'=IF({QC}B13="",TODAY(),{QC}B13)'; e["E4"].number_format = DATE
    e["D5"] = "Valid until"; e["E5"] = '=E4+Settings!$B$11'; e["E5"].number_format = DATE
    e["A7"] = "PREPARED FOR"; e["A7"].font = font(bold=True, color=ACC)
    e["A8"] = f'={QC}B11&""'; e["A8"].font = font(bold=True); e["A9"] = f'={QC}B12&""'
    for j, h in enumerate(["Description", "", "", "", "Amount"]):
        c = e.cell(11, 1 + j, h or None); c.font = font(bold=True, color="FFFFFF"); c.fill = HDR
    e["A12"] = f'=IF({QC}B4="","{T["generic"]}",{QC}B4)&" — "&{T["detail"]}'
    e["E12"] = f'={QC}B16+{QC}B17+{QC}B18+{QC}B19'
    for k in range(1, 7):
        r = 12 + k; m = f"MATCH({k},{QC}$H$4:$H$9,0)"
        e.cell(r, 1, f'=IFERROR(INDEX({QC}$D$4:$D$9,{m}),"")')
        e.cell(r, 5, f'=IFERROR(INDEX(Settings!$E$24:$E$29,{m}),"")')
    # discount incl. rounding to $1, so the lines add up exactly to the total
    e["A19"] = f'=IF(E19="","",IF({QC}B22<>0,{QC}B8&" discount ("&TEXT(-{QC}B22/{QC}B21,"0%")&IF(ROUND(E19,2)=ROUND({QC}B22,2),")",", rounded to $1)"),"Rounding to $1"))'
    e["E19"] = f'=IF(ROUND({QC}B21+{QC}B22,0)-{QC}B21=0,"",ROUND({QC}B21+{QC}B22,0)-{QC}B21)'
    e["A20"] = f'=IF({QC}B23>0,"Minimum job charge","")'; e["E20"] = f'=IF({QC}B23>0,{QC}B23,"")'
    for r in range(12, 21):
        e.cell(r, 5).number_format = MONEY
        for cc in range(1, 6): e.cell(r, cc).border = Border(bottom=thin)
    e["D22"] = "TOTAL"; e["D22"].font = font(bold=True, size=12)
    e["E22"] = f'={QC}B24'; e["E22"].number_format = MONEY; e["E22"].font = font(bold=True, size=12, color=ACC); e["E22"].fill = BAND
    e["A23"] = f'=IF({QC}B35>1,"Price per visit. "&{QC}B8&" service, about "&{QC}B35&" visits a year.",IF(IFERROR(INDEX({FRQD},MATCH({QC}B8,{FRQ},0))<>"",FALSE),"Price per visit. "&{QC}B8&" service.","One-time service."))'
    e["A23"].font = font(italic=True, color=GREY)
    e["A25"] = '="This estimate is valid until "&TEXT(E5,"mmm d, yyyy")&". The final price may change if the job differs from the details above."'
    e["A27"] = "Accepted by: ______________________________      Date: ______________"
    e["A29"] = "Thank you for the opportunity!"; e["A29"].font = font(italic=True, color=ACC)
    for r in range(1, 30):
        for cc in range(1, 6):
            cell = e.cell(r, cc)
            if cell.font.size == 11: cell.font = font()
    e.print_area = "A1:E30"
    e.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True); e.page_setup.fitToWidth = 1; e.page_setup.fitToHeight = 0; e.page_setup.orientation = "portrait"

    # ---------------- QUOTE LOG
    lg = sheet("Quote Log")
    title(lg, "Quote Log", "Log every quote you send. Mark it Won, Lost or Pending and set a follow-up date.")
    widths = [13, 26, 20, 20, 15, 12, 9, 11, 13, 28, 12, 14, 15]
    for i, w in enumerate(widths): lg.column_dimensions[chr(65 + i)].width = w
    NL = 500; R0 = 8; R1 = R0 + NL - 1
    rng = lambda col: f"${col}${R0}:${col}${R1}"
    kp = [("Quotes", f'=COUNTIFS({rng("B")},"<>")', "0"), ("Won", f'=COUNTIFS({rng("H")},"Won")', "0"), ("Lost", f'=COUNTIFS({rng("H")},"Lost")', "0"),
          ("Pending", f'=COUNTIFS({rng("H")},"Pending")', "0"), ("Win rate", '=IF(B5+C5=0,0,B5/(B5+C5))', "0%"),
          ("Won per visit", f'=SUMIFS({rng("F")},{rng("H")},"Won")', '$#,##0'), ("Won yearly value", f'=SUMIFS({rng("L")},{rng("H")},"Won")', '$#,##0'),
          ("Follow up now", f'=COUNTIFS({rng("M")},"Follow up now")', "0")]
    for i, (a, f, fm) in enumerate(kp):
        c = lg.cell(4, 1 + i, a); c.font = font(bold=True, color=GREY, size=9)
        c = lg.cell(5, 1 + i, f); c.font = font(bold=True, size=15, color=ACC); c.number_format = fm; c.alignment = Alignment(horizontal="left")
    lg.row_dimensions[5].height = 24
    cols = ["Date sent", "Customer", "Phone / email", "Service", "Frequency", "Quoted price", "Est. hours", "Status", "Follow-up date", "Notes", "Rate per hour", "Yearly value", "Next step"]
    for j, h in enumerate(cols): hdr(lg.cell(7, 1 + j, h))
    lg.row_dimensions[7].height = 30
    data = T["log"] if demo else T["example_log"]
    for i in range(NL):
        r = R0 + i; d = data[i] if i < len(data) else [None] * 10
        for j in range(10):
            inp(lg.cell(r, 1 + j, d[j]), DATE if j in (0, 8) else MONEY if j == 5 else "0.00" if j == 6 else None)
        calc(lg.cell(r, 11, f'=IF(OR(F{r}="",N(G{r})=0),"",F{r}/G{r})'), MONEY)
        calc(lg.cell(r, 12, f'=IF(F{r}="","",F{r}*{visits(f"E{r}")})'), MONEY)
        calc(lg.cell(r, 13, f'=IF(B{r}="","",IF(H{r}="Won","Won ✔",IF(H{r}="Lost","Lost",IF(I{r}="","Set follow-up",IF(I{r}<=TODAY(),"Follow up now","Waiting")))))'))
        if i % 2:
            for cc in (11, 12, 13): lg.cell(r, cc).fill = BAND
    for col, f in (("D", SVC), ("E", FRQ), ("H", '"Pending,Won,Lost"')):
        dv = DataValidation(type="list", formula1=f, allow_blank=True); lg.add_data_validation(dv); dv.add(f"{col}{R0}:{col}{R1}")
    red = dict(fill=PatternFill("solid", fgColor="F8D7DA"), font=Font(name=F, color="9C1C28", bold=True))
    lg.conditional_formatting.add(f"M{R0}:M{R1}", CellIsRule(operator="equal", formula=['"Follow up now"'], **red))
    lg.conditional_formatting.add(f"M{R0}:M{R1}", CellIsRule(operator="equal", formula=['"Won ✔"'], fill=PatternFill("solid", fgColor="DFF0D8"), font=Font(name=F, color="2E6B2E", bold=True)))
    lg.conditional_formatting.add(f"M{R0}:M{R1}", CellIsRule(operator="equal", formula=['"Lost"'], font=Font(name=F, color="8A8F98")))
    lg.freeze_panes = "C8"; lg.auto_filter.ref = f"A7:M{R1}"

    # ---------------- UPSELL
    u = sheet("Full Business Manager")
    title(u, f"Ready to run the whole business? Get the {T['manager']}", "Same pricing factors and Settings cells as this file, plus everything below. Google Sheets & Excel.")
    u.column_dimensions["A"].width = 4; u.column_dimensions["B"].width = 30; u.column_dimensions["C"].width = 84
    feats = [("Client tracker", "Every recurring client with their price, next due date and overdue / due-soon alerts, so repeat work comes back on schedule."),
             ("Jobs log", "Pick a client and the price fills in. Labor, supplies and mileage are subtracted to show the profit on every job. Unpaid jobs turn red."),
             ("Invoice generator", "Type a Job ID and a finished invoice fills in. Print or save as PDF."),
             ("Expense tracker", "Supplies, fuel, equipment, insurance and more, with your own categories."),
             ("Profit dashboard", "Revenue, costs, profit, margin and unpaid balance for every month, plus a tax set-aside estimate."),
             ("Your prices carry over", "Its Settings tab uses the same cells (services D5:F12, quote factors E15:E20, add-ons D24:F29, frequency D33:F37). Copy them from this file and paste them in.")]
    section(u, "B4", "WHAT IT ADDS")
    for i, (a, b) in enumerate(feats):
        r = 5 + i; u.cell(r, 2, a).font = font(bold=True); c = u.cell(r, 3, b); c.font = font(); wrap(c); u.row_dimensions[r].height = 30
    section(u, "B12", "WHERE TO GET IT")
    etsy, gum = LINKS[key]
    for r, lab, url in ((13, "On Etsy (TradeSheetsShop)", etsy), (14, "On Gumroad", gum)):
        u.cell(r, 2, lab).font = font(bold=True)
        c = u.cell(r, 3, url); c.hyperlink = url; c.font = font(color="1155CC", underline="single")
    c = u.cell(16, 3, "Or search TradeSheetsShop on Etsy for all our trade templates."); c.font = font(italic=True, color=GREY)

    order = ["Start Here", "Quote Calculator", "Estimate", "Quote Log", "Settings", "Full Business Manager"]
    wb._sheets = [wb[n] for n in order]; wb.active = 0
    wb.save(outfile)

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], len(sys.argv) > 3 and sys.argv[3] == "demo")
