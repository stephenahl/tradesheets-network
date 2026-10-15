#!/usr/bin/env python3
"""Clone the Pressure Washing pipeline (etsy-digital/_engine) into a new trade folder with exact-string replacements.
Every replacement must match, so a silent miss can't ship a half-converted product."""
import shutil, sys, os, re

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_engine")   # the pressure-washing pipeline, kept in the repo

TRADES = {
"detail": dict(
  dir="/tmp/trade-detail", file="Auto-Detailing-Business-Manager.xlsx", accent="8A2C2C", light="F6E9E9", kpi="#F6E9E9",
  name="Auto Detailing Business Manager",
  build=[
    ('T = dict(name="Pressure Washing Business Manager", trade="pressure washing", accent="1F5E8C", light="E5EEF6")',
     'T = dict(name="Auto Detailing Business Manager", trade="auto detailing", accent="8A2C2C", light="F6E9E9")'),
    ('Price a new property in seconds from house size, stories, extra surfaces, add-ons and frequency.',
     'Price a new job in seconds from vehicle size, pet hair or heavy soil, travel distance, add-ons and frequency.'),
    ('"Blue Wave Pressure Washing"', '"Shine Pro Mobile Detailing"'),
    ('crew-hour)",25,MONEY)', 'detailer-hour)",22,MONEY)'),
    ('per crew-hour. Used', 'per detailer-hour. Used'),
    ('svcs=[("House Soft Wash",325,3),("Driveway & Walkways",150,1.5),("Deck / Patio Clean",225,2.5),("Roof Soft Wash",450,4),("Fence Cleaning",200,2.5),("Commercial Flatwork",300,3),',
     'svcs=[("Express Wash & Wax",75,1.5),("Interior Detail",150,2.5),("Full Detail",250,4),("Paint Correction",450,6),("Ceramic Coating",650,8),("Fleet Wash (per vehicle)",45,0.75),'),
    ('qf=[("Per extra story (over 1)",75,MONEY),("Per extra surface (patio, walkway, steps)",60,MONEY),("Per 250 sq ft over 2,000",20,MONEY),("Extra hours per extra story",0.75,"0.00"),("Extra hours per extra surface",0.75,"0.00"),("Extra hours per 250 sq ft over 2,000",0.25,"0.00")]',
     'qf=[("Per size step over a car (SUV = 2, truck/van = 3)",25,MONEY),("Per pet hair / heavy soil level (0-3)",20,MONEY),("Per 5 miles of travel over 10",5,MONEY),("Extra hours per size step",0.5,"0.00"),("Extra hours per soil level",0.5,"0.00"),("Extra hours per 5 miles over 10",0.1,"0.00")]'),
    ('adds=[("Gutter brightening",75,0.75),("Window rinse",50,0.5),("Rust / stain removal",85,1),("Concrete sealing",150,2),("Trash can cleaning",15,0.25),("Oil stain treatment",40,0.5)]',
     'adds=[("Engine bay",40,0.5),("Headlight restoration",60,0.75),("Odor / ozone treatment",50,0.5),("Clay bar & sealant",80,1),("Leather conditioning",35,0.5),("Water spot removal",45,0.5)]'),
    ('fq=[("Annual",365,0.05),("Every 6 months",182,0.10),("Quarterly",91,0.10),("Monthly",30,0.15),("One-time",None,0)]',
     'fq=[("Weekly",7,0.15),("Every 2 weeks",14,0.10),("Monthly",30,0.10),("Quarterly",91,0.05),("One-time",None,0)]'),
    ('["Chemicals & detergents","Fuel","Equipment & repairs","Water","Insurance","Advertising","Trailer / vehicle","Subcontractors","Other","",""]',
     '["Chemicals & products","Fuel","Equipment & repairs","Water / power","Insurance","Advertising","Vehicle / trailer","Subcontractors","Other","",""]'),
    ('["Me","Crew 2","","","",""]', '["Me","Detailer 2","","","",""]'),
    ('ex=[("EXAMPLE – Johnson Family","(555) 201-3344","jj@example.com","12 Oak St","House Soft Wash","Annual",350,date(2025,10,20),"Spigot on north side"),',
     'ex=[("EXAMPLE – Johnson Family","(555) 201-3344","jj@example.com","12 Oak St","Full Detail","Monthly",260,date(2026,8,20),"Two SUVs, outlet in garage"),'),
    ('("EXAMPLE – Bright Dental","(555) 870-1100","office@example.com","400 Main St","Commercial Flatwork","Quarterly",300,date(2026,4,15),"Sundays only, lot closed")]',
     '("EXAMPLE – Bright Dental","(555) 870-1100","office@example.com","400 Main St","Fleet Wash (per vehicle)","Every 2 weeks",180,date(2026,8,15),"4 vans, after 6pm")]'),
    ('jex=[(date(2026,10,1),"EXAMPLE – Johnson Family",None,3,"Me",None,75,"Yes","Zelle",18,8),',
     'jex=[(date(2026,10,1),"EXAMPLE – Johnson Family",None,4,"Me",None,40,"Yes","Zelle",14,8),'),
    ('(date(2026,7,12),"EXAMPLE – Bright Dental",None,3,"Crew 2",None,0,"Yes","Card",22,4),',
     '(date(2026,9,28),"EXAMPLE – Bright Dental",None,3,"Detailer 2",None,0,"Yes","Card",22,4),'),
    ('(date(2026,10,11),"EXAMPLE – Bright Dental",None,3.5,"Crew 2",None,40,"No",None,22,4)]',
     '(date(2026,10,12),"EXAMPLE – Bright Dental",None,3,"Detailer 2",None,45,"No",None,22,4)]'),
    ('(date(2026,10,3),"Chemicals & detergents","Pool supply store","Sodium hypochlorite, surfactant",64.20,"Card","Yes")',
     '(date(2026,10,3),"Chemicals & products","Detail supply store","Soap, wax, microfiber towels",64.20,"Card","Yes")'),
    ('qi=[("Service","House Soft Wash"),("House size (sq ft)",2600),("Stories",2),("Extra surfaces",1),("Frequency","Annual")]',
     'qi=[("Service","Full Detail"),("Travel miles (one way)",18),("Vehicle size (1 car, 2 SUV, 3 truck/van)",2),("Pet hair / soil level (0-3)",1),("Frequency","Monthly")]'),
    ('("Story adjustment",\'=MAX(0,B6-1)*Settings!$E$15\',MONEY),', '("Vehicle size adjustment",\'=MAX(0,B6-1)*Settings!$E$15\',MONEY),'),
    ('("Extra surface adjustment",\'=MAX(0,B7)*Settings!$E$16\',MONEY),', '("Pet hair / soil adjustment",\'=MAX(0,B7)*Settings!$E$16\',MONEY),'),
    ('("Size adjustment",\'=MAX(0,ROUNDUP((B5-2000)/250,0))*Settings!$E$17\',MONEY),', '("Travel adjustment",\'=MAX(0,ROUNDUP((B5-10)/5,0))*Settings!$E$17\',MONEY),'),
    ('+MAX(0,ROUNDUP((B5-2000)/250,0))*Settings!$E$20', '+MAX(0,ROUNDUP((B5-10)/5,0))*Settings!$E$20'),
    ('"Pressure washing service")))', '"Detailing service")))'),
    ('"Pressure-Washing-Business-Manager.xlsx")', '"Auto-Detailing-Business-Manager.xlsx")'),
  ],
  demo=[
    ("random.seed(7)", "random.seed(11)"),
    ("Pressure-Washing-Business-Manager.xlsx", "Auto-Detailing-Business-Manager.xlsx"),
    ('clients=[("Johnson Family","House Soft Wash","Annual",350),("Bright Dental","Commercial Flatwork","Quarterly",300),("Patel Residence","Driveway & Walkways","Every 6 months",160),',
     'clients=[("Johnson Family","Full Detail","Monthly",260),("Bright Dental","Fleet Wash (per vehicle)","Every 2 weeks",180),("Patel Residence","Express Wash & Wax","Weekly",70),'),
    ('("Lakeview HOA","Commercial Flatwork","Monthly",420),("Garcia Home","House Soft Wash","Annual",325),("Oak Street Cafe","Commercial Flatwork","Monthly",260),',
     '("Lakeview Realty","Fleet Wash (per vehicle)","Monthly",270),("Garcia Family","Interior Detail","Monthly",150),("Oak Street Cafe","Express Wash & Wax","Every 2 weeks",75),'),
    ('("Miller Family","Roof Soft Wash","One-time",475),("Summit Law Office","Commercial Flatwork","Quarterly",280),("Rivera Home","Driveway & Walkways","Every 6 months",150),',
     '("Miller Family","Ceramic Coating","One-time",650),("Summit Law Office","Full Detail","Quarterly",240),("Rivera Family","Express Wash & Wax","Every 2 weeks",75),'),
    ('("Chen Residence","Deck / Patio Clean","Annual",240),("Nguyen Residence","House Soft Wash","One-time",340),("Baker Home","Fence Cleaning","One-time",210)]+[(f"{n} Residence",random.choice(["House Soft Wash","Driveway & Walkways","Deck / Patio Clean","Roof Soft Wash","Fence Cleaning"]),"One-time",random.choice([175,225,295,340,425]))',
     '("Chen Family","Paint Correction","One-time",450),("Nguyen Family","Full Detail","One-time",250),("Baker Family","Interior Detail","One-time",160)]+[(f"{n} Family",random.choice(["Full Detail","Interior Detail","Express Wash & Wax","Paint Correction","Ceramic Coating"]),"One-time",random.choice([150,250,275,450,650]))'),
    ('step={"Annual":365,"Every 6 months":182,"Quarterly":91,"Monthly":30}', 'step={"Weekly":7,"Every 2 weeks":14,"Monthly":30,"Quarterly":91}'),
    ('hrs={"House Soft Wash":3,"Commercial Flatwork":3,"Driveway & Walkways":1.5,"Deck / Patio Clean":2.5,"Roof Soft Wash":4,"Fence Cleaning":2.5}',
     'hrs={"Express Wash & Wax":1.5,"Interior Detail":2.5,"Full Detail":4,"Paint Correction":6,"Ceramic Coating":8,"Fleet Wash (per vehicle)":3}'),
    ('d=date(2026,6,1)+timedelta(days=random.randint(0,40 if f!=\'One-time\' else 130))', 'd=date(2026,8,1)+timedelta(days=random.randint(0,20 if f!=\'One-time\' else 70))'),
    ('random.choice(["Me","Crew 2"])', 'random.choice(["Me","Detailer 2"])'),
    ('9:random.choice([0,0,50,75,85])', '9:random.choice([0,0,0,40,50,60])'),
    ('13:round(random.uniform(12,30),2),14:random.randint(4,20)', '13:round(random.uniform(6,18),2),14:random.randint(3,22)'),
    ('ex+=[(date(2026,m,3),"Chemicals & detergents","Pool supply store",round(random.uniform(90,160),2)),(date(2026,m,5),"Insurance","Next Insurance",65),(date(2026,m,12),"Fuel","Shell",round(random.uniform(80,140),2)),(date(2026,m,22),"Equipment & repairs","Pressure Tek",round(random.uniform(20,120),2))]',
     'ex+=[(date(2026,m,3),"Chemicals & products","Detail supply store",round(random.uniform(70,140),2)),(date(2026,m,5),"Insurance","Next Insurance",65),(date(2026,m,12),"Fuel","Shell",round(random.uniform(90,150),2)),(date(2026,m,22),"Equipment & repairs","Detail King",round(random.uniform(20,90),2))]'),
    ("for m in range(6,11):", "for m in range(8,11):"),
  ],
  shots=[
    ('ACC="#1F5E8C"', 'ACC="#8A2C2C"'),
    ("Pressure Washing Business Manager", "Auto Detailing Business Manager"),
    ("Price any job in under a minute — house size, stories, extra surfaces, add-ons and frequency", "Price any job in under a minute — vehicle size, pet hair, travel, add-ons and frequency"),
    ("Property details", "Job details"),
    ('"Crew labor, chemicals and mileage subtracted automatically"', '"Labor, products and mileage subtracted automatically"'),
    ('"House size, stories, surfaces, add-ons, discounts, hours & profit"', '"Vehicle size, soil level, travel, add-ons, discounts, hours & profit"'),
    ('"Annual, 6-month and quarterly repeat dates with overdue alerts"', '"Weekly, 2-week and monthly maintenance dates with overdue alerts"'),
    ("#E7EFF7", "#F6E9E9"),
  ],
  guide=[
    ("#1F5E8C", "#8A2C2C"),
    ("Pressure Washing Business Manager", "Auto Detailing Business Manager"),
    ("Pressure-Washing-Business-Manager.xlsx", "Auto-Detailing-Business-Manager.xlsx"),
    ("crew names", "detailer names"),
    ("enter house size, stories, extra surfaces, add-ons and frequency", "enter travel miles, vehicle size, pet hair / soil level, add-ons and frequency"),
  ],
),
"window": dict(
  dir="/tmp/trade-window", file="Window-Cleaning-Business-Manager.xlsx", accent="5B4A8B", light="EEEAF6", kpi="#EEEAF6",
  name="Window Cleaning Business Manager",
  build=[
    ('T = dict(name="Pressure Washing Business Manager", trade="pressure washing", accent="1F5E8C", light="E5EEF6")',
     'T = dict(name="Window Cleaning Business Manager", trade="window cleaning", accent="5B4A8B", light="EEEAF6")'),
    ('Price a new property in seconds from house size, stories, extra surfaces, add-ons and frequency.',
     'Price a new home or storefront in seconds from window panes, stories, French windows, add-ons and frequency.'),
    ('"Blue Wave Pressure Washing"', '"Crystal Clear Windows"'),
    ('crew-hour)",25,MONEY)', 'tech-hour)",22,MONEY)'),
    ('per crew-hour. Used', 'per tech-hour. Used'),
    ('svcs=[("House Soft Wash",325,3),("Driveway & Walkways",150,1.5),("Deck / Patio Clean",225,2.5),("Roof Soft Wash",450,4),("Fence Cleaning",200,2.5),("Commercial Flatwork",300,3),',
     'svcs=[("Exterior Windows",180,2),("Inside & Out",300,3.5),("Storefront Route",40,0.5),("Hard Water Removal",220,3),("Gutter Cleaning",150,2),("Post-Construction",400,5),'),
    ('qf=[("Per extra story (over 1)",75,MONEY),("Per extra surface (patio, walkway, steps)",60,MONEY),("Per 250 sq ft over 2,000",20,MONEY),("Extra hours per extra story",0.75,"0.00"),("Extra hours per extra surface",0.75,"0.00"),("Extra hours per 250 sq ft over 2,000",0.25,"0.00")]',
     'qf=[("Per extra story (over 1)",50,MONEY),("Per French / divided-light window",8,MONEY),("Per 10 panes over 20",40,MONEY),("Extra hours per extra story",0.5,"0.00"),("Extra hours per French window",0.15,"0.00"),("Extra hours per 10 panes over 20",0.6,"0.00")]'),
    ('adds=[("Gutter brightening",75,0.75),("Window rinse",50,0.5),("Rust / stain removal",85,1),("Concrete sealing",150,2),("Trash can cleaning",15,0.25),("Oil stain treatment",40,0.5)]',
     'adds=[("Screen cleaning",30,0.5),("Tracks & sills",40,0.75),("Skylights",45,0.5),("Interior mirrors",25,0.25),("Light fixtures",50,0.75),("Solar panel rinse",90,1)]'),
    ('fq=[("Annual",365,0.05),("Every 6 months",182,0.10),("Quarterly",91,0.10),("Monthly",30,0.15),("One-time",None,0)]',
     'fq=[("Every 2 weeks",14,0.15),("Monthly",30,0.10),("Quarterly",91,0.10),("Every 6 months",182,0.05),("One-time",None,0)]'),
    ('["Chemicals & detergents","Fuel","Equipment & repairs","Water","Insurance","Advertising","Trailer / vehicle","Subcontractors","Other","",""]',
     '["Supplies & solution","Fuel","Ladders & equipment","Water-fed pole / RO","Insurance","Advertising","Vehicle","Subcontractors","Other","",""]'),
    ('["Me","Crew 2","","","",""]', '["Me","Tech 2","","","",""]'),
    ('ex=[("EXAMPLE – Johnson Family","(555) 201-3344","jj@example.com","12 Oak St","House Soft Wash","Annual",350,date(2025,10,20),"Spigot on north side"),',
     'ex=[("EXAMPLE – Johnson Family","(555) 201-3344","jj@example.com","12 Oak St","Inside & Out","Every 6 months",320,date(2026,4,20),"Dog in back yard"),'),
    ('("EXAMPLE – Bright Dental","(555) 870-1100","office@example.com","400 Main St","Commercial Flatwork","Quarterly",300,date(2026,4,15),"Sundays only, lot closed")]',
     '("EXAMPLE – Bright Dental","(555) 870-1100","office@example.com","400 Main St","Storefront Route","Every 2 weeks",45,date(2026,8,15),"Before 8am")]'),
    ('jex=[(date(2026,10,1),"EXAMPLE – Johnson Family",None,3,"Me",None,75,"Yes","Zelle",18,8),',
     'jex=[(date(2026,10,1),"EXAMPLE – Johnson Family",None,3.5,"Me",None,30,"Yes","Zelle",6,8),'),
    ('(date(2026,7,12),"EXAMPLE – Bright Dental",None,3,"Crew 2",None,0,"Yes","Card",22,4),',
     '(date(2026,9,29),"EXAMPLE – Bright Dental",None,0.5,"Tech 2",None,0,"Yes","Card",2,4),'),
    ('(date(2026,10,11),"EXAMPLE – Bright Dental",None,3.5,"Crew 2",None,40,"No",None,22,4)]',
     '(date(2026,10,13),"EXAMPLE – Bright Dental",None,0.5,"Tech 2",None,25,"No",None,2,4)]'),
    ('(date(2026,10,3),"Chemicals & detergents","Pool supply store","Sodium hypochlorite, surfactant",64.20,"Card","Yes")',
     '(date(2026,10,3),"Supplies & solution","Window supply store","Squeegee rubbers, scrim, soap",64.20,"Card","Yes")'),
    ('qi=[("Service","House Soft Wash"),("House size (sq ft)",2600),("Stories",2),("Extra surfaces",1),("Frequency","Annual")]',
     'qi=[("Service","Inside & Out"),("Window panes",32),("Stories",2),("French / divided-light windows",4),("Frequency","Quarterly")]'),
    ('("Extra surface adjustment",\'=MAX(0,B7)*Settings!$E$16\',MONEY),', '("French window adjustment",\'=MAX(0,B7)*Settings!$E$16\',MONEY),'),
    ('("Size adjustment",\'=MAX(0,ROUNDUP((B5-2000)/250,0))*Settings!$E$17\',MONEY),', '("Pane count adjustment",\'=MAX(0,ROUNDUP((B5-20)/10,0))*Settings!$E$17\',MONEY),'),
    ('+MAX(0,ROUNDUP((B5-2000)/250,0))*Settings!$E$20', '+MAX(0,ROUNDUP((B5-20)/10,0))*Settings!$E$20'),
    ('"Pressure washing service")))', '"Window cleaning service")))'),
    ('"Pressure-Washing-Business-Manager.xlsx")', '"Window-Cleaning-Business-Manager.xlsx")'),
  ],
  demo=[
    ("random.seed(7)", "random.seed(5)"),
    ("Pressure-Washing-Business-Manager.xlsx", "Window-Cleaning-Business-Manager.xlsx"),
    ('clients=[("Johnson Family","House Soft Wash","Annual",350),("Bright Dental","Commercial Flatwork","Quarterly",300),("Patel Residence","Driveway & Walkways","Every 6 months",160),',
     'clients=[("Johnson Family","Inside & Out","Every 6 months",320),("Bright Dental","Storefront Route","Every 2 weeks",45),("Patel Residence","Exterior Windows","Quarterly",190),'),
    ('("Lakeview HOA","Commercial Flatwork","Monthly",420),("Garcia Home","House Soft Wash","Annual",325),("Oak Street Cafe","Commercial Flatwork","Monthly",260),',
     '("Lakeview Bakery","Storefront Route","Every 2 weeks",40),("Garcia Home","Inside & Out","Quarterly",300),("Oak Street Cafe","Storefront Route","Monthly",55),'),
    ('("Miller Family","Roof Soft Wash","One-time",475),("Summit Law Office","Commercial Flatwork","Quarterly",280),("Rivera Home","Driveway & Walkways","Every 6 months",150),',
     '("Miller Family","Post-Construction","One-time",420),("Summit Law Office","Exterior Windows","Monthly",160),("Rivera Home","Exterior Windows","Every 6 months",180),'),
    ('("Chen Residence","Deck / Patio Clean","Annual",240),("Nguyen Residence","House Soft Wash","One-time",340),("Baker Home","Fence Cleaning","One-time",210)]+[(f"{n} Residence",random.choice(["House Soft Wash","Driveway & Walkways","Deck / Patio Clean","Roof Soft Wash","Fence Cleaning"]),"One-time",random.choice([175,225,295,340,425]))',
     '("Chen Residence","Hard Water Removal","One-time",240),("Nguyen Residence","Inside & Out","One-time",310),("Baker Home","Gutter Cleaning","One-time",160)]+[(f"{n} Residence",random.choice(["Inside & Out","Exterior Windows","Hard Water Removal","Gutter Cleaning","Post-Construction"]),"One-time",random.choice([160,190,240,310,400]))'),
    ('step={"Annual":365,"Every 6 months":182,"Quarterly":91,"Monthly":30}', 'step={"Every 2 weeks":14,"Monthly":30,"Quarterly":91,"Every 6 months":182}'),
    ('hrs={"House Soft Wash":3,"Commercial Flatwork":3,"Driveway & Walkways":1.5,"Deck / Patio Clean":2.5,"Roof Soft Wash":4,"Fence Cleaning":2.5}',
     'hrs={"Exterior Windows":2,"Inside & Out":3.5,"Storefront Route":0.5,"Hard Water Removal":3,"Gutter Cleaning":2,"Post-Construction":5}'),
    ('random.choice(["Me","Crew 2"])', 'random.choice(["Me","Tech 2"])'),
    ('9:random.choice([0,0,50,75,85])', '9:random.choice([0,0,0,25,30,40])'),
    ('13:round(random.uniform(12,30),2),14:random.randint(4,20)', '13:round(random.uniform(2,8),2),14:random.randint(2,16)'),
    ('ex+=[(date(2026,m,3),"Chemicals & detergents","Pool supply store",round(random.uniform(90,160),2)),(date(2026,m,5),"Insurance","Next Insurance",65),(date(2026,m,12),"Fuel","Shell",round(random.uniform(80,140),2)),(date(2026,m,22),"Equipment & repairs","Pressure Tek",round(random.uniform(20,120),2))]',
     'ex+=[(date(2026,m,3),"Supplies & solution","Window supply store",round(random.uniform(40,90),2)),(date(2026,m,5),"Insurance","Next Insurance",55),(date(2026,m,12),"Fuel","Shell",round(random.uniform(70,120),2)),(date(2026,m,22),"Water-fed pole / RO","Tucker",round(random.uniform(15,60),2))]'),
  ],
  shots=[
    ('ACC="#1F5E8C"', 'ACC="#5B4A8B"'),
    ("Pressure Washing Business Manager", "Window Cleaning Business Manager"),
    ("Price any job in under a minute — house size, stories, extra surfaces, add-ons and frequency", "Price any job in under a minute — panes, stories, French windows, add-ons and frequency"),
    ("Property details", "Job details"),
    ('"Crew labor, chemicals and mileage subtracted automatically"', '"Labor, supplies and mileage subtracted automatically"'),
    ('"House size, stories, surfaces, add-ons, discounts, hours & profit"', '"Panes, stories, French windows, add-ons, discounts, hours & profit"'),
    ('"Annual, 6-month and quarterly repeat dates with overdue alerts"', '"Storefront routes and quarterly homes with overdue alerts"'),
    ("#E7EFF7", "#EEEAF6"),
  ],
  guide=[
    ("#1F5E8C", "#5B4A8B"),
    ("Pressure Washing Business Manager", "Window Cleaning Business Manager"),
    ("Pressure-Washing-Business-Manager.xlsx", "Window-Cleaning-Business-Manager.xlsx"),
    ("crew names", "tech names"),
    ("enter house size, stories, extra surfaces, add-ons and frequency", "enter window panes, stories, French windows, add-ons and frequency"),
  ],
),
}

def apply(path, pairs, all_occ=False):
    s = open(path).read()
    for old, new in pairs:
        if old not in s:
            sys.exit(f"MISS in {os.path.basename(path)}: {old[:90]!r}")
        s = s.replace(old, new)
    open(path, "w").write(s)

key = sys.argv[1]; t = TRADES[key]
if os.path.exists(t["dir"]): shutil.rmtree(t["dir"])
shutil.copytree(SRC, t["dir"], ignore=shutil.ignore_patterns("*.png", "*.xlsx", "*.pdf", "img_*.html", "LISTING.md"))
apply(f'{t["dir"]}/build.py', t["build"])
apply(f'{t["dir"]}/demo.py', t["demo"])
apply(f'{t["dir"]}/shots.py', t["shots"])
apply(f'{t["dir"]}/guide.html', t["guide"])
# leftovers check: no pressure-washing words may survive
left = []
for f in ("build.py", "demo.py", "shots.py", "guide.html"):
    txt = open(f'{t["dir"]}/{f}').read()
    for w in ("Pressure", "pressure", "Soft Wash", "soft wash", "1F5E8C", "Flatwork", "Driveway"):
        if w in txt: left.append((f, w))
print("converted", key, "leftovers:", left)
