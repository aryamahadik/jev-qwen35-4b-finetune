"""W5 diagnostic: head C choice rows; per-label means of meta numeric features and of old/new fragment features. usage: diag_meta.py 3000"""
import sys, collections, json, math
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(C2))
import numpy as np
import pilot, pilot_loaders as PL
from families.T40 import loader, plugin as TP, edit as E
N = int(sys.argv[1]); H = "C"
loader.register()
with PL.open_family("T40") as kit:
    pl = kit.plugin; orig = pl.sample
    def samp(seed, sampler):
        c = TP.design(seed, sampler)
        if not (c["head"] == H and c["kind"] == "ch"): raise ValueError("skip")
        return orig(seed, sampler)
    pl.sample = samp
    b = pilot.build_pilot(kit, N, run_g15=False, max_attempts=40 * N)
    infos = b.infos
    by = collections.defaultdict(list)
    for i in infos:
        cat, num = pilot.meta_features(i)
        s = i.spec.structure; env = i.spec.env()
        o = E.render_tokens(s["old"], "O", env); n = E.render_tokens(s["new"], "N", env)
        num.update(dict(o_digits=sum(c.isdigit() for c in o), n_digits=sum(c.isdigit() for c in n), o_nums=len(pilot._nums(o)), n_nums=len(pilot._nums(n)),
                        o_len=len(o), n_len=len(n), o_nl=o.count("\n"), n_nl=n.count("\n"), same=float(o == n), o_alpha=sum(c.isalpha() for c in o),
                        n_sp=n.count(" "), o_sp=o.count(" "), o_punct=sum((not c.isalnum()) and c != " " for c in o), n_punct=sum((not c.isalnum()) and c != " " for c in n),
                        o_tab=o.count("\t"), n_semi=n.count(";"), o_brk=sum(o.count(c) for c in "()[]"), n_brk=sum(n.count(c) for c in "()[]"),
                        qlen=len(i.question), nopt_len=float(np.mean([len(x) for x in i.row["options"]])), tail_sp=float(n.endswith(" ")), o_tail_sp=float(o.endswith(" ")),
                        n_lead_sp=len(n) - len(n.lstrip(" ")), o_lead_sp=len(o) - len(o.lstrip(" "))))
        by[pl.label(i.spec)].append(num)
    keys = list(next(iter(by.values()))[0].keys())
    print("rows", len(infos), {k: len(v) for k, v in by.items()})
    allv = {k: np.array([r[k] for v in by.values() for r in v], float) for k in keys}
    rows = []
    for k in keys:
        sd = allv[k].std() or 1.0
        m = {l: float(np.mean([r[k] for r in v])) for l, v in by.items()}
        spread = (max(m.values()) - min(m.values())) / sd * 1.0
        rows.append((spread, k, m))
    for sp, k, m in sorted(rows, reverse=True):
        print(f"{sp:6.3f} {k:12s}", {l: round(x, 3) for l, x in sorted(m.items())})
