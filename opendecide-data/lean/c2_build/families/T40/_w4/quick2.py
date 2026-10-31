import sys, collections, numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
from families.T40 import loader, plugin as TP, fixtures
from families.T40 import edit as E
loader.register()
ctx = fixtures.make_ctx(); p = TP.T40Plugin(lexicon=ctx.lexicon)
N = int(sys.argv[1]); C = collections.defaultdict(list)
for sampler in ("S1", "S2", "S3", "S4"):
    for seed in range(1000, 1000 + N):
        c = TP.design(seed, sampler)
        if c["kind"] != "ch" or c["head"] != "C": continue
        try: sp = p.sample(seed, sampler)
        except Exception: continue
        s = sp.structure; env = sp.env()
        o = E.render_tokens(s["old"], "O", env); n = E.render_tokens(s["new"], "N", env)
        d = {}
        d.update(o_digits=sum(ch.isdigit() for ch in o), n_digits=sum(ch.isdigit() for ch in n), o_nums=len(__import__('re').findall(r"\d+(?:[.,]\d+)?", o)),
                 n_nums=len(__import__('re').findall(r"\d+(?:[.,]\d+)?", n)), o_len=len(o), n_len=len(n), o_nl=o.count("\n"),
                 o_alpha=sum(ch.isalpha() for ch in o), o_sp=o.count(" "), n_sp=n.count(" "), o_punct=sum((not ch.isalnum()) and ch != " " for ch in o),
                 n_punct=sum((not ch.isalnum()) and ch != " " for ch in n), o_tab=o.count("\t"), n_semi=n.count(";"), n_slash=n.count("/"),
                 o_brk=sum(o.count(ch) for ch in "()[]"), n_brk=sum(n.count(ch) for ch in "()[]"), o_lead=len(o)-len(o.lstrip(" ")),
                 n_lead=len(n)-len(n.lstrip(" ")), n_tail=len(n)-len(n.rstrip(" ")), o_tail=len(o)-len(o.rstrip(" ")), same=float(o==n),
                 kind_dig=float(any(a!=b and a.isdigit() for a,b in zip(o,n))), diffpos=next((k for k,(a,b) in enumerate(zip(o,n)) if a!=b), -1),
                 ndiff=sum(a!=b for a,b in zip(o,n)))
        C[TP.T40Plugin.label(p, sp) if False else c["label"]].append(d)
keys = list(next(iter(C.values()))[0])
print({l: len(v) for l, v in C.items()})
allv = {k: np.array([r[k] for v in C.values() for r in v], float) for k in keys}
out = []
for k in keys:
    sd = allv[k].std() or 1.0; m = {l: np.mean([r[k] for r in v]) for l, v in C.items()}
    out.append(((max(m.values()) - min(m.values())) / sd, k, m))
for sp, k, m in sorted(out, reverse=True): print(f"{sp:5.2f} {k:9s}", {l: round(float(x), 2) for l, x in sorted(m.items())})
