"""c2_build/families/T29/dneg_stage3.py: stage 3 of the T29 double-negation round (fix iteration 2).

Reads the two Haiku G-LEX reads (haiku/dneg_i2/glex_tasks/answers/), records them on the rebuilt registry, admits the
wordings with 2/2 agreeing extractors (and wording_problems() once more), writes the pools/dneg/ supplement that
run_pilot_i2.py's loader reads (pilot_loaders.py is not edited), then runs the pilot steps 4-6 of the brief:

  4  tests (T29 folder + c2_build/tests) and the determinism check (rows / relations sha256 under PYTHONHASHSEED 1 and 2)
  5  the pilot into pilot_i2/ (program gates; G5-H and G3-H task files, not answered)
  6  A43 G6 at 6,000 rows into pilot_i2/G6_AT_6000.json (run_pilot_i2.py --g6, which has the supplement in its loader)

G13-seed: the seed pass (g13_c2.py seed) is a whole-block run over every eval-side target in one process; it is not run
here. The admitted wordings are listed in pilot_i2/G13_PENDING.txt for the batch run (a hit quarantines that wording).

  ../.venv/bin/python -B families/T29/dneg_stage3.py [--no-pilot] [--root DIR --pool DIR --out DIR]   (from lean/c2_build)
Exit 0 when the supplement was written with at least dneg_i2.MIN_ADMITTED_FOR_POOL admitted training wordings and every
pilot step it ran passed; 2 on a shortfall; 1 on a step failure.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from c2_kit import paths  # noqa: E402
from families.T29 import dneg_i2 as D  # noqa: E402

C2 = D.C2_BUILD
PY = sys.executable
RUN = "families/T29/run_pilot_i2.py"


def admit(root: Path, pool: Path) -> dict:
    state = json.loads((root / "stage2_state.json").read_text(encoding="utf-8"))
    reg = D.restore_registry(state)
    ids = sorted(f["form_id"] for f in state["forms"])
    batches = D.glex_batches(reg, ids)
    reads, probs = D.load_reads(batches, root)
    if probs:
        raise SystemExit(f"STOP: G-LEX answers are incomplete or unreadable: {probs[:8]}")
    invalid, n_rec = D.record_reads(reg, reads)
    out = D.write_supplement(reg, state, pool, {"recorded_per_read": n_rec, "invalid_reads": len(invalid)})
    out["invalid"] = invalid
    return out


def run(cmd: list, env_extra: dict | None = None, timeout: int = 7200) -> subprocess.CompletedProcess:
    env = dict(os.environ, **(env_extra or {}))
    return subprocess.run(cmd, cwd=C2, env=env, capture_output=True, text=True, timeout=timeout)


def pilot_steps(out: Path) -> dict:
    res = {}
    t = run([PY, "-B", "-m", "pytest", "-q", "-x", "families/T29", "tests"], timeout=3600)
    res["tests"] = {"returncode": t.returncode, "tail": t.stdout.strip().splitlines()[-3:]}
    shas = {}
    for seed in ("1", "2"):
        r = run([PY, "-B", RUN, "--dry-run"], {"PYTHONHASHSEED": seed})
        try:
            j = json.loads(r.stdout[r.stdout.index("{"):])
            shas[seed] = (j["rows_sha256"], j["relations_sha256"])
        except (ValueError, KeyError):
            shas[seed] = ("error", r.stderr.strip()[-300:])
    res["determinism"] = {"shas": shas, "identical": len(set(shas.values())) == 1 and shas["1"][0] != "error"}
    r = run([PY, "-B", RUN])
    res["pilot"] = {"returncode": r.returncode, "tail": r.stdout.strip().splitlines()[-25:]}
    g = run([PY, "-B", RUN, "--g6", "--n", "6000"])
    res["g6_at_6000"] = {"returncode": g.returncode, "tail": g.stdout.strip().splitlines()[-3:]}
    res["ok"] = (t.returncode == 0 and res["determinism"]["identical"] and r.returncode == 0 and g.returncode == 0)
    paths.write_text(out / "STAGE3_PILOT_STEPS.json", json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(D.ROOT))
    ap.add_argument("--pool", default=str(D.POOL))
    ap.add_argument("--out", default=str(D.HERE / "pilot_i2"))
    ap.add_argument("--no-pilot", action="store_true", help="admit and write the supplement only (tests)")
    a = ap.parse_args(argv)
    root, pool, out = Path(a.root), Path(a.pool), Path(a.out)
    adm = admit(root, pool)
    s = adm["summary"]
    lines = [f"{fid}\t{adm['admitted_texts'][fid]}" for fid in adm["admitted_form_ids"]]
    paths.write_text(out / "G13_PENDING.txt",
                     "# T29 double-negation wordings admitted in fix iteration 2, awaiting G13-seed (batch run: "
                     "g13_c2.py seed --block T29). form_id<TAB>text\n" + "\n".join(lines) + "\n")
    print(json.dumps({k: v for k, v in s.items()}, indent=1, ensure_ascii=False))
    if s["admitted_training"] < D.MIN_ADMITTED_FOR_POOL:
        print(f"SHORTFALL: {s['admitted_training']} admitted training wordings (< {D.MIN_ADMITTED_FOR_POOL})")
        return 2
    if a.no_pilot:
        return 0
    res = pilot_steps(out)
    print(json.dumps({k: (v if k == "ok" else {kk: vv for kk, vv in v.items() if kk != "tail"}) for k, v in res.items()},
                     indent=1, ensure_ascii=False, default=str))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
