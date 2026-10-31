import sys, json, pickle, collections
sys.dont_write_bytecode = True
from pathlib import Path
C2 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
for p in (str(C2), str(C2 / "families" / "T27")):
    sys.path.insert(0, p)
import pilot_loaders as PL, run_pilot as RP, run_pilot_i2 as R2
R2._install_supplement(); PL.LOADERS["T27"] = RP._t27; PL.open_family = RP._redirect(R2.OUT_NAME)
with PL.open_family("T27") as kit:
    from families.T27 import plugin as P
    pl = kit.plugin
    idx = pl._index()
    print("forms admitted", sum(len(v) for v in idx.values()), "supplement in lex:", sum(1 for f in pl.lexicon.forms if f.split('#')[0].startswith('req.') and pl.lexicon.forms[f].source=='haiku' and pl.lexicon.forms[f].haiku_prompt_sha=='ovl_i2'))
    tasks = [t for t in sorted(P.TASK_SCOPE) if idx.get(t) and P.TASK_SCOPE[t]]
    ga = [a for a in P.ACTIONS if idx.get(f"req.{a}.gate")]
    for s in ("S1","S2","S3","S4"):
        prm = P.SAMPLER_PARAMS.get(s)
        if prm is None: continue
        plan = pl._ovl_plan(prm, idx, tasks, ga)
        print(s, "plan", None if plan is None else plan.shares)

    from families.T27 import overlap as OV
    import collections
    prm = P.SAMPLER_PARAMS["S2"]
    joint = P.beyond_joint(tuple(tasks), tuple(ga), prm["p_obj"], prm["p_sib"])
    cells, cum = joint
    mass = [cum[0]] + [cum[i]-cum[i-1] for i in range(1,len(cum))]
    tot = cum[-1]
    m = pl._ovl()
    nob, share, bycount = [], collections.Counter(), collections.Counter()
    for (t, acts), ms in zip(cells, mass):
        b = m.bands(idx, t, acts)
        bycount[tuple(sorted(b))] += ms / tot
        if not b: nob.append((t, acts, round(ms/tot, 5)))
        for l in b: share[l] += ms / tot / len(b)
    print("beyond cells", len(cells), "no band:", len(nob), "mass", round(sum(x[2] for x in nob), 4))
    print("band-set mass", {k: round(v, 4) for k, v in bycount.items()})
    print("shares", {k: round(v, 4) for k, v in share.items()})
    print("examples no band", nob[:6])
    ds = []
    for t in tasks:
        sc = P.TASK_SCOPE[t]
        ds += [(t, (sc[0], sc[0]))] if len(sc) == 1 else [(t, (a, b)) for a in sc for b in sc]
    act = [l for l in OV.BANDS if share[l] > 1e-9]
    miss = collections.Counter()
    ex = []
    for t, acts in ds:
        b = m.bands(idx, t, acts)
        for l in act:
            if l not in b:
                miss[l] += 1
                if len(ex) < 8: ex.append((t, acts, l, sorted(b)))
    print("do_step cells", len(ds), "active levels", act, "missing per level", dict(miss), ex)

    print("---- per task/action coverage (gate forms)")
    miss_pairs = collections.defaultdict(set)
    for t in tasks:
        for a in P.TASK_SCOPE[t]:
            b = m.bands(idx, t, (a, a))
            have = sorted(b)
            if 'partial' not in b or 'none' not in b:
                print(t, a, "bands", have)
            nf = len(idx[f"req.{a}.gate"])
    sup = [f for f in pl.lexicon.forms if pl.lexicon.forms[f].haiku_prompt_sha=='ovl_i2' and pl.lexicon.forms[f].sem_id.endswith('.gate')]
    print("supplement gate forms", len(sup), collections.Counter(pl.lexicon.forms[f].sem_id for f in sup))
    print("gate forms per action (orig+sup):", {a: len(idx[f"req.{a}.gate"]) for a in P.ACTIONS})
