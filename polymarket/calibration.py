"""Study 1: is the BTC 15-minute market's own price miscalibrated? Read-only on a SQLite snapshot.
Usage: python3 calibration.py /path/to/paper-snapshot.sqlite3   (never run against the live VPS database)"""
import sqlite3, os, json, re, bisect, sys
from datetime import datetime, timezone

p = os.path.abspath(sys.argv[1])
c = sqlite3.connect(f'file:{p}?mode=ro&immutable=1', uri=True)
settle = {s: int(v) for s, v, _ in c.execute("select * from shadow_settlements")}   # 1 = Up won

def end_ts(slug):  # slug time is the window start; resolution is 15 minutes later
    m = re.search(r'(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})z$', slug)
    d = datetime.strptime(m.group(1) + m.group(2) + m.group(3), '%Y-%m-%d%H%M').replace(tzinfo=timezone.utc)
    return d.timestamp() + 900

books = {}
for ts, slug, body in c.execute("select ts,slug,body from records where kind='book'"):
    if slug not in settle: continue
    b = json.loads(body)
    try:
        bid = float(b['bids'][0]['px']['value'])
        ask = float((b.get('offers') or b.get('asks'))[0]['px']['value'])
    except Exception:
        continue
    books.setdefault(slug, []).append((ts, bid, ask))

rows = []  # (seconds_before_end, slug, bid, ask, mid, up_won)
for slug, L in books.items():
    L.sort(); T = end_ts(slug); tss = [x[0] for x in L]
    for off in (600, 300, 180, 120, 60, 30):
        t = T - off; i = bisect.bisect_left(tss, t)
        cand = [j for j in (i - 1, i) if 0 <= j < len(L) and abs(L[j][0] - t) <= 20]
        if not cand: continue
        _, bid, ask = L[min(cand, key=lambda j: abs(L[j][0] - t))]
        if 0 < bid < ask < 1: rows.append((off, slug, bid, ask, (bid + ask) / 2, settle[slug]))

print('settled markets:', len(settle), ' with books:', len(books), ' rows:', len(rows))
for off in (600, 300, 180, 120, 60, 30):
    R = [r for r in rows if r[0] == off]
    if not R: continue
    print(f'\nT-{off}s n={len(R)} brier(mid)={sum((r[4]-r[5])**2 for r in R)/len(R):.4f}')
    fav = [(1 - r[2], 1 - r[5], 'Down') if r[4] <= 0.10 else (r[3], r[5], 'Up') for r in R if r[4] <= 0.10 or r[4] >= 0.90]
    if fav:
        print(f'  favorites>=90c n={len(fav)} winrate={sum(f[1] for f in fav)/len(fav):.3f} '
              f'gross EV/contract={sum(f[1]-f[0] for f in fav)/len(fav):+.4f} (before fees)')
