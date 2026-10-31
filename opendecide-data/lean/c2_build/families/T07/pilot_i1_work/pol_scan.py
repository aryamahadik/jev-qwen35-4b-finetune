"""Scan the frozen T07 wording pool with c2_kit.polarity (read only; prints flagged wordings per qform)."""
import sys
sys.path.insert(0, ".")
from collections import Counter, defaultdict
from c2_kit import polarity as POL
from families.T07 import load_v2 as L, plugin as P

NEG = tuple(sys.argv[1:]) or ()
pools = L.load_pools()
ctx = L.make_ctx(pools)
class Pl:                       # minimal stand-in carrying the opt-in attributes
    QFORMS = P.T07Plugin.QFORMS
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = NEG
    POLARITY_BASE = {}
    POLARITY_STRICT_FRAMES = bool(__import__("os").environ.get("STRICT"))
    POLARITY_SKIP = ()
bad = defaultdict(list)
tot = Counter()
for sid, sk in ctx.skins.items():
    if sk.kind != "wording": continue
    tot[sk.qform] += 1
    p = POL.form_problems(Pl, sk.qform, sk.text)
    if p: bad[sk.qform].append((sid, sk.held_out, sk.text, p))
for q, n in tot.items():
    print(q, "wordings", n, "flagged", len(bad[q]))
for q in bad:
    for sid, h, t, p in bad[q]:
        print("--", q, "held" if h else "train", sid); print("   ", t); print("   ", p)
