import sys, collections
sys.path.insert(0, "/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/8c6bd93f-d297-4aa4-a84b-ce310198beb1/scratchpad")
from dump import load
P, FX, pl, ctx = load("T06")
cnt = collections.Counter()
YES = {"yn_refund": 1, "yn_owed": 1, "yn_double": 1, "yn_not_refund": 0, "yn_no_right": 0, "yn_may_refuse": 0}
for seed in range(2000):
    for smp in pl.SAMPLERS:
        sp = pl.sample(seed, smp)
        specs = [sp] + [pl.derive(r.spec) for r in pl.relations(sp) if r.kind == "twin" and r.spec is not None]
        for s in specs:
            e = s.env(); q = s.qform
            R = e["REQUEST_DATE"]
            dd = (R - e["DELIVERY_DATE"]).days; dp = (R - e["POSSESSION_DATE"]).days; do = (R - e["ORDER_DATE"]).days
            rej = e["REASON"] == "faulty" and dd <= e["N_REJ"]
            excluded = e["GOODS"] in ("custom", "perishable") or (e["GOODS"] == "hygiene" and e["SEAL"] != "intact")
            wd = (not excluded) and dp <= e["N_WD"]
            pol = e["POLICY"]; P_ = e.get("P_DAYS")
            store = False
            if pol == "pol.t06.faulty_order": store = e["REASON"] == "faulty" and do <= P_
            elif pol == "pol.t06.mind_order": store = e["REASON"] != "faulty" and do <= P_
            elif pol == "pol.t06.any_order": store = do <= P_
            elif pol == "pol.t06.any_delivery": store = dd <= P_
            grants = [k for k, v in (("reject", rej), ("withdraw", wd), ("store", store)) if v]
            a = pl.solve_a(s)
            if q in YES:
                exp = int(bool(grants)) if YES[q] else int(not grants)
            elif q == "ch_rule":
                exp = grants[0] if len(grants) == 1 else ("none" if not grants else ("MULTI", grants))
            elif q == "ch_end_reject":
                exp = (e["DELIVERY_DATE"] + __import__("datetime").timedelta(days=e["N_REJ"])).isoformat()
            elif q == "ch_end_withdraw":
                exp = (e["POSSESSION_DATE"] + __import__("datetime").timedelta(days=e["N_WD"])).isoformat()
            else:
                exp = ("?", q)
            if exp != a and not (hasattr(a, "isoformat") and a.isoformat() == exp):
                cnt["mismatch"] += 1
                if cnt["mismatch"] < 8: print("MISMATCH", smp, seed, q, repr(a), repr(exp), e["GOODS"], e["SEAL"], e["REASON"], pol)
            cnt["n"] += 1
print(dict(cnt))
