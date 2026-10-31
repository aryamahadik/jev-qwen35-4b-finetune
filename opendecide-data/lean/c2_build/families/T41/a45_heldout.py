"""A45 held-out audit for T41 (in memory): every held-out value is unreachable from S1-S4, and S5 uses only held-out values.
  ../../.venv/bin/python -B families/T41/a45_heldout.py [seeds_per_sampler=1500]     (from c2_build)"""
import json, sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from c2_kit import plugin as KP
KP.FAMILIES.setdefault("T41", "agent")
from families.T41 import fixtures as FX, pools as P, carrier_bank as CB
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
pl, ctx = FX.make_plugin()
held_forms = {fid for fid, f in ctx.lexicon.forms.items() if f.held_out}
held_skins = {k for k, s in ctx.skins.items() if getattr(s, "held_out", False)}
held_packs = {p[0] for p in CB.PACKS if p[3]}
held_pack_names = {x for p in CB.PACKS if p[3] for x in [p[1], *p[2]]}
train_pack_names = {x for p in CB.PACKS if not p[3] for x in [p[1], *p[2]]}
lits_held = list(P.HELD_TOOLS) + [P.CARRIER_SURFACE[c] for c in P.HELD_OUT_CARRIERS]
dims = ("tool", "car", "pack", "register", "skin", "wording", "form")
seen = {s: {d: set() for d in dims} for s in pl.SAMPLERS}
text_hits = collections.Counter(); rows = 0
for s in pl.SAMPLERS:
    for seed in range(n):
        sp = pl.sample(seed, s); rr = pl.render(sp, ctx); env = sp.env(); m = rr.row["meta"]
        d = seen[s]
        d["tool"].add(sp.structure["tool"]); d["car"] |= {env["CAR1"], env["CAR2"]}; d["pack"].add(sp.pack)
        d["register"].add(rr.register); d["skin"].add(m["c2"]["skin_id"]); d["wording"].add(rr.wording_id)
        d["form"] |= set(m["c2"]["lexicon_ids"])
        if s != "S5":
            rows += 1
            txt = rr.text if isinstance(rr.text, str) else json.dumps(rr.row)
            full = txt + "\n" + json.dumps(rr.row, ensure_ascii=False)
            for lit in lits_held:
                if lit in full: text_hits["held literal:" + lit] += 1
            for nm in held_pack_names:
                if nm in full: text_hits["held pack name"] += 1
train = {d: set().union(*(seen[s][d] for s in pl.SAMPLERS if s != "S5")) for d in dims}
held_seen = seen["S5"]
held_vals = {"tool": set(P.HELD_TOOLS), "car": set(P.HELD_OUT_CARRIERS), "pack": held_packs, "register": set(P.NARRATIVE_HELD_OUT),
             "skin": held_skins, "wording": {k for k, s in ctx.skins.items() if getattr(s, "kind", "") == "wording" and getattr(s, "held_out", False)},
             "form": held_forms}
res = {"seeds_per_sampler": n, "train_rows_scanned": rows, "text_hits_in_training": dict(text_hits)}
ok = not text_hits
for d in dims:
    leak = sorted(train[d] & held_vals[d]); s5_outside = sorted(x for x in held_seen[d] if x not in held_vals[d]) if d != "wording" and d != "form" else []
    # S5 may mix held and training for wording / form (G0: held-out forms used only by S5, not exclusively held)
    res[d] = {"train_values": len(train[d]), "held_defined": len(held_vals[d]), "held_used_by_S5": len(held_seen[d] & held_vals[d]),
              "held_leaked_into_S1-S4": leak, "S5_values_not_held": s5_outside}
    ok &= not leak and not s5_outside
res["PASS"] = bool(ok)
Path("families/T41/A45_HELDOUT.json").write_text(json.dumps(res, indent=1, default=list))
print(json.dumps({"PASS": res["PASS"], **{d: (res[d]["held_defined"], res[d]["held_used_by_S5"], res[d]["held_leaked_into_S1-S4"], res[d]["S5_values_not_held"]) for d in dims}, "text_hits": res["text_hits_in_training"]}))
