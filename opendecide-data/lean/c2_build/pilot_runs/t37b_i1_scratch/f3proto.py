import sys, math
from collections import Counter
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from t37b import fixtures as FX, select as SEL, sources as SRC, author_pool as AP
recs = FX.stand_in_pool()
for i,t in enumerate(["Is the claim backed by the evidence?","Is the claim supported by the evidence?","Does the evidence back the claim?"]):
    recs.append(AP.record("gd_check_covid/support", t, "T37b-author_wording-standin-000", "0"*64) | {"reads":["same","same"],"status":"admitted"})
many = []
for r in FX.stand_in_pool():
    for k in range(25):
        t = r["template"][:-1] + f" (variant {k})?"
        many.append(AP.record(r["sem"], t, "T37b-author_wording-standin-000", "0"*64) | {"reads":["same","same"],"status":"admitted"})
pool = AP.Pool(many)
bases = SEL.eligible(FX.many_rows(60), [], status=FX.keep_all, strict_inputs=False)[0]
print(len(bases), len(pool.paraphrases))
for nc,ne in ((700,300),(1400,600)):
    plan, rep = SEL.plan_block(bases, n_complement=nc, n_equiv=ne, seed="t37b-test", equiv_pool=pool.choices())
    n=len(plan)
    print(nc,ne,'->',n, rep['kinds'], 'basis', rep['basis'], 'pass', rep['pass'], 'yes', rep['partner_yes_rate'], 'cap', max(1, math.floor(0.02*n)))
    print(' covid support equiv', sum(1 for i in plan if i.kind=='equiv' and i.base.entry.key=='gd_check_covid/support'))
    # fixed point
    order = sorted(bases, key=lambda b: SEL.uhash("t37b-test", "t37b-order", b.row["id"]))
    again = SEL._plan_once(order, SRC.FRAMES_TRAIN, nc, ne, "t37b-test", "train", max(1, math.floor(0.10*n)), max(1, math.floor(0.02*n)), pool.choices(), True)
    print(' fixed point', [i.pid for i in again]==[i.pid for i in plan], len(again))
