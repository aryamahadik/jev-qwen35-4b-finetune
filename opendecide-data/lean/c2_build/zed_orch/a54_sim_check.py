"""PLUMBING TEST ONLY (A54 4): write SIMULATED G-LEX answers (the declared meaning for every form) into a scratch copy of
haiku/heldout/extract, then run a54_rebuild_mixdev --check-only against it. Never writes a real answer file, a real mixdev
or a pool. The real G-LEX answers come from Haiku."""
import json, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / "zed_orch"))
import gen_full_c2 as G  # noqa: E402
import a54_heldout_overlay as OV  # noqa: E402
import a54_rebuild_mixdev as RB  # noqa: E402

SIM = HERE / "zed_orch" / "_sim_a54"
for fam in sys.argv[1:]:
    src = OV.held_dir(fam) / "extract"; ex = SIM / fam / "extract"
    if ex.parent.exists():
        shutil.rmtree(ex.parent)
    shutil.copytree(src, ex)
    with G.loader_patch(fam), OV.patched(fam, str(ex)):
        with G.PL.open_family(fam) as kit:
            reg = kit.ctx.lexicon
            man = json.loads((ex / "TASKS.json").read_text())
            for t in man["tasks"]:
                chunk = json.loads((ex / "chunks" / f"{t['task_id']}.json").read_text())
                key = json.loads((ex / "key" / f"{t['batch_id']}.json").read_text())["key"]
                ans = []
                for it in chunk["items"]:
                    fid = key[it["qid"]]
                    ans.append({"qid": it["qid"], "choice": reg.sems[reg.forms[fid].sem_id].meaning})
                a = Path(str(t["answer_file"]).replace(str(src), str(ex)))
                a.parent.mkdir(parents=True, exist_ok=True); a.write_text(json.dumps(ans))
    sys.argv = [sys.argv[0], "--check-only"]
    print(json.dumps(RB.rebuild(fam, str(ex)), default=str), flush=True)
    sys.argv = [sys.argv[0]] + [fam]
