"""families/T32/dneg_stage3.py: F8 stage 3 (fix iteration 2): after the two Haiku G-LEX reads of the re-authored
yn_dneg_broken wordings exist (haiku/dneg_i2/glex/answers/), admit the wordings that pass G-LEX 2/2 into a pool supplement
(haiku/dneg_i2/pool_supplement.json) and re-run steps 4-6 of the brief.

run_pilot_i2.py's loader applies the supplement through dneg_stage2.apply_supplement (no edit to pilot_loaders.py).

  ../.venv/bin/python -B families/T32/dneg_stage3.py [--root DIR] [--admit-only]     (from lean/c2_build)

Steps after the admission (skipped with --admit-only; every command is bounded, logs in pilot_i2/):
  4  pytest of the T32 tests, `run_pilot_i2.py determinism --n 300`
  5  `run_pilot_i2.py run --n 1000`     (program gates, G5-H / G3-H task files, NOT answered)
  6  `zed_orch/g6_at_size.py T32 --dir pilot_i2`
G13-seed on the new wordings is NOT run here (not measured under 30 CPU minutes): they are listed in
pilot_i2/G13_PENDING.txt for the batch run.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))
sys.path.insert(0, str(HERE))
import dneg_stage2 as S2  # noqa: E402


def admit_glex(root: Path = S2.ROOT) -> dict:
    """G-LEX 2/2 admission of the stage-2 candidates; writes pool_supplement.json and pilot_i2/G13_PENDING.txt."""
    from c2_kit import chunker
    import importlib
    FZ = importlib.import_module("families.T32.freeze")
    root = Path(root)
    cands = json.loads((root / "candidates.json").read_text(encoding="utf-8"))["candidates"]
    reg = S2._registry()
    fids = S2._add_candidates(reg, [{**c, "slots": dict(c["slots"])} for c in cands])
    answers = {}
    for read, gb in S2.glex_batches(reg, fids, root):
        raw = {}
        for c in gb.chunks:
            ap = Path(c["answer_file"])
            if not ap.exists():
                raise SystemExit(f"no G-LEX answer yet: {ap}")
            raw[c["task_id"]] = json.loads(ap.read_text(encoding="utf-8"))
        out, _probs = chunker.load_answers(gb, raw)
        answers[read] = (out, gb)
    counts = FZ.record_lex(reg, answers)
    forms, dropped = [], []
    for c, fid in zip(cands, fids):
        f = reg.forms[fid]
        if reg.status(fid) == "admitted":
            forms.append({"text": f.text, "sem": f.sem_id, "slots": [list(s) for s in f.slots],
                          "haiku_task_id": f.haiku_task_id, "haiku_prompt_sha": f.haiku_prompt_sha,
                          "extractions": [list(e) for e in f.extractions], "form_id": fid})
        else:
            dropped.append({"text": f.text, "status": reg.status(fid), "extractions": [list(e) for e in f.extractions]})
    (root / "pool_supplement.json").write_text(json.dumps({"qform": S2.QFORM, "forms": forms, "dropped": dropped,
                                                           "glex_counts": counts}, indent=1, ensure_ascii=False))
    out_dir = C2_BUILD / "families" / "T32" / "pilot_i2" if root == S2.ROOT else root
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "G13_PENDING.txt").write_text("".join(f"{f['form_id']}\t{f['text']}\n" for f in forms))
    return {"admitted": len(forms), "dropped": len(dropped), "glex_counts": counts}


def _run(cmd: list, log: Path, timeout: int) -> int:
    py = sys.executable
    with open(log, "w") as fh:
        r = subprocess.run([py, "-B", *cmd], cwd=C2_BUILD, stdout=fh, stderr=subprocess.STDOUT, timeout=timeout)
    return r.returncode


def steps_4_to_6() -> dict:
    pdir = HERE / "pilot_i2"
    pdir.mkdir(exist_ok=True)
    res = {}
    res["tests"] = _run(["-m", "pytest", "-q", "-x", "families/T32"], pdir / "stage3_tests.log", 3600)
    res["determinism"] = _run(["families/T32/run_pilot_i2.py", "determinism", "--n", "300"],
                              pdir / "stage3_determinism.log", 3600)
    res["pilot"] = _run(["families/T32/run_pilot_i2.py", "run", "--n", "1000"], pdir / "stage3_pilot.log", 7200)
    res["g6_at_6000"] = _run(["zed_orch/g6_at_size.py", "T32", "--dir", "pilot_i2"], pdir / "stage3_g6.log", 7200)
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(S2.ROOT))
    ap.add_argument("--admit-only", action="store_true")
    a = ap.parse_args(argv)
    r = admit_glex(Path(a.root))
    print(json.dumps(r, indent=1))
    if not a.admit_only:
        if r["admitted"] == 0:
            print("no wording passed G-LEX 2/2: nothing to supplement; steps 4-6 not run", file=sys.stderr)
            return 1
        print(json.dumps(steps_4_to_6(), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
