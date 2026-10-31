"""families/T33/dneg_stage3.py: stage 3 of the double-negation wordings (fix iteration 2; G0_SPEC section 9 G2).

Input : the stage-2 state (authoring answers in haiku/dneg_i2/tasks/, G-LEX task files in glex_tasks/) and the two
        independent Haiku reads of every form (the answer files of glex_tasks/).
Does  : 1. re-derives the stage-2 pieces (deterministic) and records the reads (haiku_author.record_extractions): a form
           is admitted only when both reads pick its meaning (G-LEX 2/2); any other pick rejects it for good.
        2. keeps the wordings of admitted forms, re-checks their polarity (c2_kit.polarity) and refuses to go on when a
           form has fewer than 8 (G0 target, never lowered; --allow-short only to inspect).
        3. append-and-freeze: pools/dneg_i2_supplement.json (wording skins + their lexicon forms with the reads) and
           pools/DNEG_I2_FREEZE.json (sha256 of the supplement and of the four frozen pool files). The frozen pool
           files are never edited; run_pilot_i2.py's loader (dneg_i2.load_ctx_i2) merges the supplement.
        4. lists the new wordings in pilot_i2/G13_PENDING.txt for the batch G13-seed run (there is no local G13-seed
           runner for T33 in c2_build, so the wordings are always listed, never silently skipped).
        5. runs steps 4-6 of the fix loop into pilot_i2/ unless --no-run: the family tests, determinism (rows and
           relations sha256 under two PYTHONHASHSEEDs), the 1,000-row pilot (program gates, G5-H / G3-H task files, not
           answered) and the A43 G6 / G7 / G10 run at 6,000 rows (pilot_i2/G6_AT_6000.json). Logs: pilot_i2/stage3_*.log.

No Haiku, no model, no network.

  ../../.venv/bin/python -B -m families.T33.dneg_stage3 [--no-run] [--root R] [--pools P] [--out O]   (lean/c2_build)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from families.T33 import dneg_i2 as D  # noqa: E402
from families.T33 import haiku_author as H  # noqa: E402
from families.T33 import plugin as T  # noqa: E402

PY = sys.executable
OUT_DEFAULT = H.HERE / "pilot_i2"


def admit(root: Path = D.ROOT) -> dict:
    """Record the G-LEX reads and return the admitted wording skins and forms (nothing is written)."""
    root = Path(root)
    tasks_root, glex_root = root / "tasks", root / "glex_tasks"
    pieces = H.load_pieces(tasks_root)
    reg = pieces["registry"]
    gl = json.loads((glex_root / "TASKS.json").read_text(encoding="utf-8"))
    bs = [(n, H.batch_from_disk(glex_root, bid)) for n, bid in gl["batches"].items()]
    rec = H.record_extractions(reg, bs, glex_root)
    keep, per_form, rejected = [], Counter(), Counter()
    for s in pieces["skins"].values():
        if s.kind != "wording" or s.qform not in D.FORMS:
            continue
        st = [reg.status(f) for f in s.lexicon_ids]
        if st and all(x == "admitted" for x in st) and not POL.form_problems(T.T33Plugin, s.qform, s.text):
            keep.append(s)
            per_form[s.qform] += 1
        else:
            rejected[f"{s.qform}:{st[0] if st else 'no_form'}"] += 1
    fids = {f for s in keep for f in s.lexicon_ids}
    j = reg.to_json()
    forms = [f for f in j["forms"] if f["form_id"] in fids]
    sems = [x for x in j["sems"] if x["sem_id"] in {f["sem_id"] for f in forms}]
    return {"skins": keep, "forms": forms, "sems": sems, "per_form": {q: per_form.get(q, 0) for q in D.FORMS},
            "rejected": dict(rejected), "reads": rec["reads"], "read_problems": rec["problems"][:40]}


def _run(name: str, args: list, out: Path, timeout: int) -> dict:
    log = out / f"stage3_{name}.log"
    try:
        p = subprocess.run([PY, "-B", *args], cwd=C2_BUILD, capture_output=True, text=True, timeout=timeout)
        text, code = p.stdout + "\n--- stderr ---\n" + p.stderr, p.returncode
    except subprocess.TimeoutExpired:
        text, code = f"timeout after {timeout}s", 124
    log.write_text(text, encoding="utf-8")
    return {"step": name, "cmd": " ".join(args), "exit": code, "log": str(log)}


def run(root: Path = D.ROOT, *, pools_dir: Path = H.POOLS, out: Path = OUT_DEFAULT, frozen_dir: Path = H.POOLS,
        no_run: bool = False, allow_short: bool = False) -> dict:
    root, out = Path(root), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    got = admit(root)
    short = {q: n for q, n in got["per_form"].items() if n < D.MIN_ADMITTED}
    rep = {"family": H.F, "stage": 3, "admitted_per_form": got["per_form"], "min_per_form": D.MIN_ADMITTED,
           "short_forms": short, "rejected": got["rejected"], "reads": got["reads"],
           "read_problems": got["read_problems"], "freeze": None, "steps": []}
    if short and not allow_short:
        rep["verdict"] = ("STOP: fewer than 8 admitted wordings for " + ", ".join(sorted(short))
                          + "; nothing frozen. Re-author those forms (4x candidates again) and rerun stage 2 and 3.")
        paths.write_text(root / "stage3_report.json", json.dumps(rep, indent=1) + "\n")
        return rep
    rep["freeze"] = D.freeze_supplement(
        H.skins_to_json(got["skins"]), got["forms"],
        {"per_form": got["per_form"], "reads": got["reads"], "wording_ids": sorted(s.skin_id for s in got["skins"])},
        sems_json=got["sems"], pools_dir=pools_dir, frozen_dir=frozen_dir)
    lines = ["# G13-seed pending: the new double-negation wordings (G-LEX 2/2 admitted, frozen in "
             f"pools/{D.SUPPLEMENT}); run G13-seed on them in the batch run before the G5-H re-read.",
             "# skin_id\tqform\tform_id\ttext"]
    lines += [f"{s.skin_id}\t{s.qform}\t{','.join(s.lexicon_ids)}\t{s.text}"
              for s in sorted(got["skins"], key=lambda s: (s.qform, s.skin_id))]
    (out / "G13_PENDING.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    rep["g13"] = f"{len(got['skins'])} wordings listed in {out / 'G13_PENDING.txt'} (no local runner; batch run)"
    if not no_run:
        for name, args, tmo in (
                ("tests", ["-m", "pytest", "-q", "-x", "families/T33"], 3000),
                ("determinism", ["families/T33/run_pilot_i2.py", "determinism"], 1800),
                ("pilot", ["families/T33/run_pilot_i2.py", "run"], 1800),
                ("g6_at_6000", ["families/T33/run_pilot_i2.py", "g6", "--n", "6000"], 3600)):
            r = _run(name, args, out, tmo)
            rep["steps"].append(r)
            if r["exit"] != 0 and name in ("tests", "determinism"):
                rep["verdict"] = f"STOP: {name} failed (see {r['log']})"
                break
        else:
            rep["verdict"] = "pilot_i2 written; read pilot_i2/PILOT_REPORT.json and G6_AT_6000.json"
    else:
        rep["verdict"] = "supplement frozen; steps 4-6 not run (--no-run)"
    paths.write_text(root / "stage3_report.json", json.dumps(rep, indent=1) + "\n")
    return rep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(D.ROOT))
    ap.add_argument("--pools", default=str(H.POOLS), help="where the supplement is frozen")
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--no-run", action="store_true")
    ap.add_argument("--allow-short", action="store_true")
    a = ap.parse_args(argv)
    rep = run(Path(a.root), pools_dir=Path(a.pools), out=Path(a.out), no_run=a.no_run, allow_short=a.allow_short)
    print(json.dumps({k: rep.get(k) for k in ("admitted_per_form", "short_forms", "freeze", "verdict")}, indent=1))
    return 0 if not rep["short_forms"] and "STOP" not in rep["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
