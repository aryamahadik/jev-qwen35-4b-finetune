"""JOB3 audit B: what do the plain disposition words mean in the C1 golden set's own card definitions (counts + a
truncated top definition per source)."""
import json, re, collections
P="/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl"
WORDS=["decline","reject","hold","escalate","stop","refuse","approve","ask","deny","continue","observe","human"]
rx={w:re.compile(r"^"+w, re.I) for w in WORDS}
by=collections.defaultdict(lambda: collections.defaultdict(collections.Counter))   # word -> source -> definition -> n
for line in open(P):
    r=json.loads(line)
    if r['qtype']!='choice' or not r.get('card'): continue
    for ln in r['card'].split("\n"):
        if ln.startswith("- ") and ": " in ln:
            lab,d=ln[2:].split(": ",1)
            for w,p in rx.items():
                if p.match(lab):
                    by[w][r['source']][(lab,d[:110])]+=1
out={}
for w in WORDS:
    srcs=by[w]
    tot=sum(sum(c.values()) for c in srcs.values())
    print(f"== {w}: {tot} card lines, {len(srcs)} sources")
    for s,c in sorted(srcs.items(), key=lambda kv:-sum(kv[1].values()))[:5]:
        (lab,d),n=c.most_common(1)[0]
        print(f"   {s:28s} lines={sum(c.values()):6d} distinct={len(c):5d} top: [{lab[:30]}] {d}")
