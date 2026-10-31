import sys, random, collections
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
from families.T40 import loader, edit as E, fixtures
loader.register()
D = collections.Counter(); rows=[]
for sd in range(150):
    g = E.draw_group(random.Random(sd), "S1", list(E.TRAIN_PACKS)[sd % len(E.TRAIN_PACKS)])
    vals = {f"F{k}": v for k, v in enumerate(g["code"]["idents"])}
    t1 = E.render_tokens(g["f1"], "F", vals); t2 = E.render_tokens(g["f2"], "F", vals)
    p1, p2 = E._prof_w8(t1), E._prof_w8(t2)
    D[tuple(a - b for a, b in zip(p1, p2))] += 1
    rows.append((t1, t2, p1, p2))
print(D.most_common(12))
for r in rows[:14]: print(repr(r[0]), repr(r[1]), r[2], r[3])
