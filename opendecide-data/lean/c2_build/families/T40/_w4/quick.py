import sys, collections, statistics as st
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
from families.T40 import loader, plugin as TP, fixtures
from families.T40 import edit as E, world as W
loader.register()
ctx = fixtures.make_ctx(); p = TP.T40Plugin(lexicon=ctx.lexicon)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
fails = collections.Counter(); B = collections.defaultdict(list); C = collections.defaultdict(list)
for sampler in ("S1", "S2", "S3", "S4"):
    for seed in range(1000, 1000 + N):
        c = TP.design(seed, sampler)
        if c["kind"] != "ch" or c["head"] not in "BC": continue
        try: sp = p.sample(seed, sampler)
        except Exception as e: fails[(c["head"], c["label"], str(e)[:60])] += 1; continue
        s = sp.structure; env = sp.env()
        if c["head"] == "B":
            B[c["label"]].append(dict(res=int(bool(s["results"])), prov=int(bool(s["request"]["provider"])), nt=len(s["tools"]),
                no=sum(env[t["mslot"]] == "no" for t in s["tools"]), ncl=len(s["request"]["clauses"])))
        else:
            vals = env
            o = E.render_tokens(s["old"], "O", env); n = E.render_tokens(s["new"], "N", env)
            f = E.render_tokens(E.file_tokens(s["code"]), "F", env)
            t=o+n; C[c["label"]].append(dict(d=len(n) - len(o), lo=len(o), ln=len(n), lf=len(f), par=t.count('('), brk=t.count('['), star=t.count('*'), q=t.count('"')))
print("fails", dict(fails))
for l, r in B.items():
    print("B", l, len(r), {k: round(sum(x[k] for x in r) / len(r), 3) for k in r[0]})
for l, r in C.items():
    print("C", l, len(r), {k: round(sum(x[k] for x in r) / len(r), 2) for k in r[0]}, "d!=0:", sum(x["d"] != 0 for x in r))
