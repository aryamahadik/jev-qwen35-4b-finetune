"""PLUMBING TEST ONLY (A55 d2/d3): drive a55_devforms (admit -> glex -> score) and the overlay with SIMULATED Haiku answers in a SCRATCH
copy of zed_orch/a55_dev/<FAM> (zed_orch/g13_attr/_a55_sim/<FAM>/). The simulated authoring answers are the family's own
training forms / wordings with one harmless filler word added (so they pass the family lint and differ from every pool entry); the
simulated G-LEX answers pick the declared meaning. This proves the file formats, the admission code, the freeze and that the
rebuild really draws the dev-only forms; it says NOTHING about Haiku's real answers. It never writes a real answer file, a real
FROZEN.json, a real mixdev or a pool. The real answers come from Haiku.

  ../.venv/bin/python -B zed_orch/a55_sim_check.py T24 T06 T07 T25   (from lean/c2_build)
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
for _p in (str(C2B), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

import a55_common as C  # noqa: E402
import a55_devforms as D  # noqa: E402
import a55_overlay as OV  # noqa: E402
from c2_kit import chunker  # noqa: E402

SIM = HERE / "g13_attr" / "_a55_sim"
FILLERS = ("exactly", "simply", "clearly", "plainly", "just", "indeed", "firmly", "directly")


def _tweak(ad, meta, base: str, seen: set, k: int) -> str | None:
    words = base.split(" ")
    for f in FILLERS:
        for pos in (1, 2, len(words) // 2):
            if pos >= len(words):
                continue
            t = " ".join(words[:pos] + [f] + words[pos:])
            if t in seen or t == base:
                continue
            lint_seen = set()
            if not ad.lint(meta, t, lint_seen):
                seen.add(t)
                return t
    return None


def simulate(fam: str, n_per_unit: int = 5) -> dict:
    src = D.dev_dir(fam)
    dst = SIM / fam
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("answers", "extract", "ADMITTED.json", "PROBLEMS.json", "FROZEN.json"))
    (dst / "answers").mkdir(exist_ok=True)
    with D.open_kit(fam) as kit:
        ad, b, plan, ui = D.build_batch(fam, kit)
        reg = kit.ctx.lexicon
        used: dict = {}
        seen: set = set()
        for c in b.chunks:
            ans = []
            for it in c["items"]:
                iid = b.key[it["qid"]]
                meta = plan[iid]
                sem = ad.sem_of(meta["unit"])
                bases = sorted(f.text for f in reg.forms.values() if f.sem_id == sem and not f.held_out)
                if "attr" in meta:                      # T25: the item asks for a wording with / without {ATTR}
                    bases = [t for t in bases if ("{ATTR}" in t) == bool(meta["attr"])]
                want = 1 if ad.answer_field == "text" else C.HOW_MANY // 2
                outs = []
                cnt = used.setdefault(meta["unit"], 0)
                for j in range(len(bases)):
                    if len(outs) >= want or cnt >= n_per_unit:
                        break
                    t = _tweak(ad, meta, bases[(cnt + j * 3) % len(bases)], seen, j)
                    if t:
                        outs.append(t)
                        cnt += 1
                used[meta["unit"]] = cnt
                ans.append({"qid": it["qid"], ("text" if ad.answer_field == "text" else "forms"):
                            (outs[0] if ad.answer_field == "text" and outs else outs if ad.answer_field != "text" else "")})
            (dst / b.answer_path(c["task_id"])).write_text(json.dumps(ans))
    # the tasks.json copied points at the real dir; the admission code reads answers under `root`
    adm = D.admit(fam, root=dst, checker=lambda recs: {"status": "scanned", "hit_ids": []})
    gl = D.write_glex(fam, root=dst)
    ex = dst / "extract"
    with D.open_kit(fam) as kit:
        reg = kit.ctx.lexicon
        cands = json.loads((dst / "ADMITTED.json").read_text())["candidates"]
        D._register(reg, cands, fam)
        plan_r = D._read_plan(fam, reg, cands, D.ADAPTERS[fam]())
        batches = D._read_batches(reg, plan_r, fam)
        by_fid = {c["form_id"]: c for c in cands}
        for rd, b in batches.items():
            for c in b.chunks:
                ans = []
                for it in c["items"]:
                    fid = b.key[it["qid"]]
                    ans.append({"qid": it["qid"], "meaning": reg.sems[by_fid[fid]["sem_id"]].meaning})
                (ex / b.answer_path(c["task_id"])).write_text(json.dumps(ans))
    sc = D.score(fam, root=dst)
    return {"family": fam, "admit": {k: adm[k] for k in ("n_candidates", "n_rejected", "run_checker")},
            "units_admission": {u: {k: v for k, v in d.items() if k in ("candidates", "rejected")} for u, d in adm["units"].items()},
            "glex": gl, "score": {k: sc[k] for k in ("units", "kinds", "votes", "answer_files_missing")}, "dir": str(dst.relative_to(C.LEAN))}


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(json.dumps(simulate(f), default=str, indent=1), flush=True)
