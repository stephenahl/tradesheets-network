"""Fill the product workbook with realistic sample data -> demo.xlsx (for listing images and testing)."""
import random
from datetime import date, timedelta
from openpyxl import load_workbook
random.seed(11)
wb=load_workbook('Airbnb-Host-Business-Manager.xlsx')
pp=wb['Properties']; bk=wb['Bookings']; xp=wb['Expenses']; sp=wb['Supplies']
props=[("Lakeview Cabin","12 Shore Rd",2,6,165,210,95,65,4,15,date(2024,5,1),"Lockbox 4471"),
("Downtown Loft","400 Main St #3B",1,4,129,159,75,50,2,10,date(2025,2,1),"Door code 2580"),
("Mountain A-Frame","88 Ridge Ln",3,8,225,295,150,110,6,20,date(2026,3,1),"Hot tub: check chlorine")]
for i,p in enumerate(props):
    for j,v in enumerate(p): pp.cell(5+i,1+j,v)
for r in range(5+len(props),25):
    for j in range(12): pp.cell(r,1+j).value=None
names=["Jordan P.","Sam R.","Priya K.","Alex M.","Taylor B.","Chris D.","Morgan L.","Jamie W.","Casey N.","Riley S.","Avery T.","Quinn H.","Drew F.","Logan C.","Harper G.","Reese J.","Emerson V.","Rowan Y."]
chan=["Airbnb"]*6+["Vrbo"]*2+["Direct booking"]*2
cleaners={"Lakeview Cabin":"Maria (cleaner)","Downtown Loft":"Me","Mountain A-Frame":"Sparkle Turnover Co."}
books=[]
for (n,_,_,mx,*_rest) in props:
    start=max(date(2026,1,2),_rest[6])
    d=start+timedelta(days=random.randint(0,4))
    while d<date(2026,12,10):
        summer = d.month in (6,7,8)
        L=random.choice([2,2,3,3,3,4,5]+([7,8] if summer else [])+([6] if n=="Mountain A-Frame" else []))
        out=d+timedelta(days=L)
        books.append([d,out,n,random.choice(names),random.choice(chan),random.randint(2,mx)])
        gap=random.choice([0,0,1,1,2,3]) if summer else random.choice([0,1,2,3,4,6,8])
        if d>date(2026,11,20): gap+=random.choice([2,5,9])     # far-future calendar is thinner
        d=out+timedelta(days=gap)
books.sort(key=lambda b:(b[0],b[2]))
TODAY=date(2026,10,20)
for k,b in enumerate(books):
    r=5+k; ci,co,n,g,ch,gs=b
    g=names[(k*7)%len(names)]
    past=co<=TODAY
    status="Booked"
    if k==len(books)//3: status="Cancelled"
    paid="Yes" if (past or ch!="Direct booking") else random.choice(["No","Yes"])
    vals={2:ci,3:co,4:n,5:g,6:ch,7:gs,9:None,13:random.choice([None,None,None,None,25,-20]),16:None,20:status,21:paid,22:cleaners[n],23:"Yes" if past else None,24:None}
    if ch=="Direct booking" and random.random()<0.3: vals[24]="Repeat guest"
    if n=="Mountain A-Frame" and random.random()<0.2: vals[24]="Bringing a dog: pet fee added"; vals[13]=50
    for c,v in vals.items(): bk.cell(r,c,v)
# one deliberate same-day turnover pair stays as generated; check a split-month stay exists
ex=[]
for m in range(1,13):          # fixed bills are scheduled all year; variable costs only up to now (Oct)
    past=m<=10
    for n,_,_,_,_,_,_,_,_,_,since,_ in props:
        if date(2026,m,1)<since: continue
        mort={"Lakeview Cabin":1150,"Downtown Loft":1650,"Mountain A-Frame":1900}[n]
        ex+=[(date(2026,m,1),n,"Mortgage interest / rent","Lender" if n!="Downtown Loft" else "Landlord","Monthly payment (interest portion)" if n!="Downtown Loft" else "Rent",mort),
             (date(2026,m,12),n,"Internet & streaming","Spectrum","Internet",65)]
        if past: ex.append((date(2026,m,8),n,"Utilities","City Power & Water","Electric + water",round(random.uniform(110,240),2)))
        if past and random.random()<0.45: ex.append((date(2026,m,random.randint(14,27)),n,"Repairs & maintenance","Handyman Joe",random.choice(["Fix leaky faucet","Replace smoke detector","Patch drywall","Hot tub service"]),round(random.uniform(60,260),2)))
    ex.append((date(2026,m,4),None,"Software & pricing tools","PriceLabs","Dynamic pricing (all listings)",59.97))
    if past: ex.append((date(2026,m,18),None,"Supplies & consumables","Costco","Restock: paper goods, coffee, soap",round(random.uniform(140,260),2)))
ex.sort(key=lambda e:(e[0],e[1] or ""))
for k,(d,n,c,v,desc,a) in enumerate(ex):
    for j,val in enumerate([d,n,c,v,desc,a,"Card","Yes"]): xp.cell(5+k,1+j,val)
for r in range(5+len(ex),8):
    for j in range(8): xp.cell(r,1+j).value=None
onhand=[14,8,32,1,10,40,12,5,3,1,4,2]
for i,v in enumerate(onhand): sp.cell(7+i,5,v)
for i in range(12): sp.cell(7+i,12,date(2026,10,random.randint(3,18)))
wb['Turnovers']['B4']=TODAY
q=wb['Pricing Calculator']; q['B5']="Lakeview Cabin"
wb['Monthly Summary']['B4']="Lakeview Cabin"
wb.save('demo.xlsx'); print(len(books),"bookings",len(ex),"expenses")
