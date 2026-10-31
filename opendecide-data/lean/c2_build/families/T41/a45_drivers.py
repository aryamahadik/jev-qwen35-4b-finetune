"""Which card (context) tokens / overlap features carry the choice label (G6 view c driver read). In memory."""
import collections, sys, math, json
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import pilot, pilot_loaders as PL
from families.T41 import run_pilot_i1 as RUN
n = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
RUN.register()
with PL.open_family("T41") as kit:
    b = pilot.build_pilot(kit, n, run_g15=False)
pl = kit.plugin
ch = [i for i in b.infos if i.row["qtype"] == "choice"]
labs = ["allow", "ask", "benign", "block"]
lab = [pl._decide(i.spec) for i in ch]
N = len(ch); base = collections.Counter(lab)
df = collections.Counter(); cnt = collections.defaultdict(collections.Counter)
for i, l in zip(ch, lab):
    for t in set(pilot.toks(i.context)):
        df[t] += 1; cnt[t][l] += 1
res = []
for t, d in df.items():
    if d < 40 or d > N - 40: continue
    chi = sum((cnt[t][l] - d * base[l] / N) ** 2 / (d * base[l] / N) for l in labs)
    res.append((chi, t, d, [round(cnt[t][l] / d, 2) for l in labs]))
res.sort(reverse=True)
print("N", N, "expected chi2 (3 dof) mean 3; top tokens by chi2:")
for r in res[:25]: print(round(r[0], 1), r[1], r[2], r[3])
print("n tokens tested", len(res), "n chi>16:", sum(1 for r in res if r[0] > 16))
# overlap of the option text with the context by label
ov = collections.defaultdict(list)
for i, l in zip(ch, lab):
    ct = set(pilot.toks(i.context))
    for o in i.row["options"]:
        k = pl._decide(i.spec) if o == i.row["gold"] else "x"
        ov[(k == l and o == i.row["gold"])].append(len(set(pilot.toks(o)) & ct))
print("overlap gold/non-gold mean", {k: round(sum(v) / len(v), 3) for k, v in ov.items()})
