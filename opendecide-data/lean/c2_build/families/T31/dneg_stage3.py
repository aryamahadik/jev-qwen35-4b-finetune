"""families/T31/dneg_stage3.py: stage 3 of the T31 double-negation round (fix iteration 2).

Reads the two Haiku G-LEX reads (haiku/dneg_i2/glex_tasks/answers/<task_id>.json), records them on the rebuilt registry,
admits the wordings that 2/2 agreeing extractors chose the declared sense for (and wording_problems() once more), checks that
no frozen pools_v2 form regresses when they are merged, and writes the supplement pools_v2_dneg/ (lexicon_dneg.json,
wordings_dneg.json, QUARANTINE.json, MANIFEST.json) that run_pilot_i2.py's loader reads. pilot_loaders.py is not edited.
Then the pilot steps 4-6 of the iteration-2 brief, as subprocesses:

  4  tests (families/T31 + c2_kit/tests), and the determinism check: rows / relations sha256 of run_pilot_i2.py --dry-run
     under PYTHONHASHSEED 1 and 2 must be identical
  5  the pilot into pilot_i2/ (program gates; G5-H and G3-H task files, not answered)
  6  A43 G6 at 6,000 rows into pilot_i2/G6_AT_6000.json (run_pilot_i2.py --g6 --n 6000)

G13-seed: the seed pass (g13_c2.py seed) is a whole-block run over every eval-side target in one process, and it reads
families/T31/pools/ only; it is not run here. The admitted wordings are listed in pilot_i2/G13_PENDING.txt for the batch run
(a hit quarantines that wording; delete it from the supplement and re-run `--force --no-pilot` then the pilot).

  cd lean/c2_build
  ../.venv/bin/python -B families/T31/dneg_stage3.py [--no-pilot] [--force] [--allow-short]
                                                     [--root DIR --supp DIR --out DIR]
Exit 0: supplement written, every form has >= MIN_ADMITTED_PER_FORM wordings and every pilot step passed.
Exit 2: a shortfall (no pilot run unless --allow-short; the supplement is still written).  Exit 1: a step failed.
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
from families.T31 import dneg_i2 as D  # noqa: E402

C2 = D.C2_BUILD
PY = sys.executable
RUN = "families/T31/run_pilot_i2.py"


def admit(root: Path, supp: Path, force: bool = False) -> dict:
    adm = D.admit_glex(root)
    res = D.write_supplement(adm, supp, {"read_counts": adm["read_counts"],
                                         "answer_sha256": adm["answer_sha"]}, force=force)
    res["rejected"] = adm["rejected"]
    res["record_problems"] = adm["record_problems"]
    return res


def g13_pending_text(kept: list) -> str:
    lines = [f"{c['form_id']}\t{c['text']}" for c in kept]
    return ("# T31 double-negation wordings admitted in fix iteration 2 (G-LEX 2/2), awaiting G13-seed.\n"
            "# Not run in stage 3: g13_c2.py seed is a whole-block pass that reads families/T31/pools/ only. A hit quarantines "
            "that wording.\n# form_id<TAB>text\n" + "\n".join(lines) + "\n")


def run(cmd: list, env_extra: dict | None = None, timeout: int = 7200) -> subprocess.CompletedProcess:
    env = dict(os.environ, **(env_extra or {}))
    return subprocess.run(cmd, cwd=C2, env=env, capture_output=True, text=True, timeout=timeout)


def pilot_steps(out: Path, supp: Path, n_g6: int = 6000) -> dict:
    res = {}
    common = ["--supp-dir", str(supp), "--out-dir", str(out)]
    t = run([PY, "-B", "-m", "pytest", "-q", "-x", "families/T31", "c2_kit/tests"], timeout=3600)
    res["tests"] = {"returncode": t.returncode, "tail": t.stdout.strip().splitlines()[-3:]}
    shas = {}
    for seed in ("1", "2"):
        r = run([PY, "-B", RUN, "--dry-run", *common], {"PYTHONHASHSEED": seed})
        try:
            j = json.loads(r.stdout[r.stdout.index("{"):])
            shas[seed] = (j["rows_sha256"], j["relations_sha256"])
        except (ValueError, KeyError):
            shas[seed] = ("error", r.stderr.strip()[-300:])
    res["determinism"] = {"shas": shas, "identical": len(set(shas.values())) == 1 and shas["1"][0] != "error"}
    r = run([PY, "-B", RUN, *common])
    res["pilot"] = {"returncode": r.returncode, "tail": r.stdout.strip().splitlines()[-25:]}
    g = run([PY, "-B", RUN, "--g6", "--n", str(n_g6), *common])
    res["g6_at_6000"] = {"returncode": g.returncode, "tail": g.stdout.strip().splitlines()[-3:]}
    try:
        rep = json.loads((out / "PILOT_REPORT.json").read_text(encoding="utf-8"))
        d = rep["gates"]["G10"]["checks"]["double_negation_share"]
        res["double_negation_share"] = {"value": d["value"], "bar": d["bar"], "verdict": d["verdict"]}
        res["G10"] = rep["gates"]["G10"]["verdict"]
        res["pilot_gate_lines"] = [ln for ln in rep["gate_lines"] if not ln.startswith(("G3-H", "G5-H"))]
        res["g5h_g3h_tasks"] = {"G5-H": [t["task_file"] for t in rep["chunks"]["G5-H"]],
                                "G3-H": [t["task_file"] for t in rep["chunks"]["G3-H"]]}
        res["dneg_rows"] = rep["iteration"]["double_negation"]
    except (OSError, KeyError, ValueError) as e:
        res["pilot_report_error"] = str(e)
    res["ok"] = (t.returncode == 0 and res["determinism"]["identical"] and r.returncode == 0 and g.returncode == 0
                 and res.get("double_negation_share", {}).get("verdict") == "pass")
    paths.write_text(out / "STAGE3_PILOT_STEPS.json", json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(D.ROOT))
    ap.add_argument("--supp", default=str(D.SUPP))
    ap.add_argument("--out", default=str(D.HERE / "pilot_i2"))
    ap.add_argument("--no-pilot", action="store_true", help="admit and write the supplement only (tests)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing supplement MANIFEST")
    ap.add_argument("--allow-short", action="store_true", help="run the pilot although a form is short of wordings")
    a = ap.parse_args(argv)
    root, supp, out = Path(a.root), Path(a.supp), Path(a.out)
    res = admit(root, supp, a.force)
    man = res["manifest"]
    paths.write_text(out / "G13_PENDING.txt", g13_pending_text(res["kept"]))
    print(json.dumps({"counts": man["counts"], "short": man["short"], "read_counts": man["read_counts"],
                      "record_problems": res["record_problems"], "supplement": str(supp)}, indent=1, ensure_ascii=False))
    if man["short"] and not a.allow_short:
        print(f"SHORTFALL: forms below {D.MIN_ADMITTED_PER_FORM} admitted wordings: {man['short']}; no pilot run "
              "(re-author for the short forms, or --allow-short)")
        return 2
    if not res["kept"] or a.no_pilot:
        return 0 if res["kept"] else 2
    steps = pilot_steps(out, supp)
    print(json.dumps({k: (v if k in ("ok", "double_negation_share", "G10", "dneg_rows", "pilot_gate_lines")
                          else {kk: vv for kk, vv in v.items() if kk != "tail"} if isinstance(v, dict) else v)
                      for k, v in steps.items()}, indent=1, ensure_ascii=False, default=str))
    return 0 if steps["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
