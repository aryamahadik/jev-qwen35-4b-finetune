"""A45 reseed audit (spec 3.3) on >= 6,000 specs: 3% re-drawn under an independent RNG salt; label flips and G3/solver-B parity."""
import random, sys, json
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from c2_kit import plugin as KP
KP.FAMILIES.setdefault("T41", "agent")
from families.T41 import fixtures as FX, plugin as TP
pl, ctx = FX.make_plugin()
specs = [pl.sample(900000 + s, smp) for smp in ("S1", "S2", "S3", "S4") for s in range(1500)]
sample = random.Random(41).sample(specs, k=int(0.03 * len(specs)))
other = TP.T41Plugin(lexicon=ctx.lexicon); other.RNG_SALT = "reseed"
flips = 0
for sp in sample:
    sp2 = other.sample(sp.seed, sp.sampler); deal = pl._deal(sp.sampler, sp.seed)
    if other._decide(sp2) != deal["label"] or pl._decide(sp) != deal["label"]: flips += 1; continue
    rr = other.render(sp2, ctx); view = other.parse(rr.row, other.ctx_for(sp2, ctx))
    if other.solve_b(view) != other.solve_a(sp2): flips += 1
r = {"specs": len(specs), "audited": len(sample), "flips": flips, "bar": "<= 1% (0 flips if < 100 audited)"}
Path("families/T41/A45_RESEED.json").write_text(json.dumps(r)); print(r)
