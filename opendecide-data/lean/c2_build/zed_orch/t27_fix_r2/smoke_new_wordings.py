"""Smoke test of the overlay with FABRICATED new wordings (test_redo5's ch_next and yn_beyond sentences through the real redo5 chain in scratch):
the pools wrapper adds them, the kit admits them (G-LEX), the generator draws them, every unit passes the program gates.
Never writes admitted_wordings.json. Prints counts only."""
import json, shutil, sys
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    sys.path.insert(0, p)
mode = sys.argv[1]
PAY = HERE / "scratch" / "smoke_payload.json"
if mode == "make":
    import redo5 as R5
    import test_redo5 as T5
    d = HERE / "scratch" / "smoke_r5"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    R5.write_tasks(d)
    rep = R5.load(d, answers=T5._answers(d), batches=R5.build_batches(d))
    R5.glex_write(d / "extract", rep["kept"])
    p = R5.glex_plan(rep["kept"])
    reg = p["reg"]
    for read, b in p["batches"]:
        path = d / "extract" / b.answer_path(b.chunks[0]["task_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({q: reg.sems[reg.forms[f].sem_id].meaning for q, f in b.key.items()}))
    p2 = R5.glex_plan(rep["kept"])
    out = R5.glex_check(d / "extract", p2)
    PAY.write_text(json.dumps(R5.admitted_payload(p2, out)))
    shutil.rmtree(d, ignore_errors=True)
    print("payload written", PAY.name)
    sys.exit(0)
pay = json.loads(PAY.read_text())
new_ids = {w["piece_id"] for w in pay["wordings"]}
import gen_full_c2 as G
import pilot
import overlay as O
src = G.quarantine_sources("T27")
banned = set().union(*map(set, src.values()))
with O.patched(extra=pay):
    with G.loader_patch("T27"):
        with G.PL.open_family("T27") as kit0:
            kit, _x = G.apply_exclusions(kit0, banned)
            n_tr = {q: sum(1 for s in kit.ctx.skins.values() if s.kind == "wording" and s.qform == q and not s.held_out)
                    for q in ("ch_next", "yn_beyond")}
            b = pilot.build_pilot(kit, 200, seed_base=2_000_000, run_g15=True)
res = {"new_in_payload": len(new_ids), "training_skins_in_kit": n_tr, "rows": len(b.infos),
       "units_dropped": b.stats["units_dropped"], "drops_by_gate": b.stats["drops_by_gate"], "notes": kit.notes[-2:]}
for q in ("ch_next", "yn_beyond"):
    use = Counter(i.row["meta"]["wording_id"] for i in b.infos if i.row["meta"]["qform"] == q)
    res[q] = {"rows": sum(use.values()), "new_wordings_used": sum(1 for k in use if k in new_ids),
              "new_rows": sum(v for k, v in use.items() if k in new_ids), "spread": [min(use.values()), max(use.values())]}
print(json.dumps(res))
PAY.unlink()
