"""families/T01/dneg_stage3.py: stage 3 of the T01 double-negation wordings (fix iteration 2; G0_SPEC_v4 12.1).

Input : the stage-2 state (haiku/dneg_i2/stage2_state.json, glex_tasks/) and the two independent Haiku reads of every
        wording (the answer files of glex_tasks/answers/).
Does  : 1. rebuilds the stage-2 registry and G-LEX batches (deterministic; the batch ids must equal the ones stage 2 wrote),
           records the reads (an answer file is used whole or not at all; a missing or invalid file gives no vote) and
           keeps a wording only when BOTH reads picked its own meaning (G-LEX 2/2; any other pick rejects it for good).
        2. re-checks the polarity of the kept wordings (c2_kit.polarity, strict frames) and stops when a form has fewer
           than 8 kept wordings (G0 target, never lowered; --allow-short only to inspect).
        3. append-and-freeze: pools_v2/dneg_i2_supplement.json (the six double-negation sems, the admitted forms with their
           reads, one wording row per form) and pools_v2/DNEG_I2_FREEZE.json (sha256 of the supplement and of the frozen
           pool files, which are never edited). run_pilot_i2.py's loader (dneg_i2.make_ctx_i2) merges the supplement.
        4. lists the new wordings in pilot_i2/G13_PENDING.txt for the batch G13-seed run (g13_c2.py seed needs the sealed
           exports, which a family agent never opens: the wordings are listed, never silently skipped).
        5. runs steps 4-6 of the fix loop into pilot_i2/ unless --no-run: the family tests, determinism (rows and
           relations sha256 under two PYTHONHASHSEEDs), the 1,000-row pilot (program gates, G5-H / G3-H task files, not
           answered) and G6 / G7 / G10 at 6,000 rows (pilot_i2/G6_AT_6000.json). Logs: pilot_i2/stage3_*.log.
No Haiku, no model, no network.

  ../../.venv/bin/python -B -m families.T01.dneg_stage3 [--no-run] [--root R] [--pools P] [--out O]   (lean/c2_build)
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
from families.T01 import dneg_i2 as D  # noqa: E402
from families.T01 import freeze_v2 as FV  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

PY = sys.executable
HERE = Path(__file__).resolve().parent
OUT_DEFAULT = HERE / "pilot_i2"


def admit(root: Path = D.ROOT) -> dict:
    """Record the G-LEX reads; return the admitted candidates and the registry (nothing is written)."""
    root = Path(root)
    glex_root = root / "glex_tasks"
    state = json.loads((root / "stage2_state.json").read_text(encoding="utf-8"))
    cands = state["candidates"]
    reg, fids, drops = D.glex_registry(cands)
    if drops or len(fids) != len(cands):
        raise RuntimeError(f"the stage-2 candidates no longer build a registry: {drops[:2]}")
    batches = D.glex_batches(reg, [c["form_id"] for c in cands])
    for label, b in batches:
        if state["batch_ids"].get(label) != b.batch_id:
            raise RuntimeError(f"G-LEX batch {label} differs from the one stage 2 wrote; rerun stage 2")
    reads, problems = Counter(), []
    for label, b in batches:
        for c in b.chunks:
            tid = c["task_id"]
            items = {it["qid"]: it for it in c["items"]}
            ans, rec = FV.read_answer_file("dneg-i2-glex", "extract_lex", tid, glex_root / b.answer_path(tid), items, ())
            reads[f"{label}:{rec['status']}"] += 1
            if ans is None:
                problems.append(f"{label} {tid}: {rec['status']} {rec['problems'][:1]}")
                continue
            for qid, a in ans.items():
                reg.record_extraction(b.key[qid], label, reg.meaning_to_sem("question", a["meaning"]))
    keep, per_form, rejected = [], Counter(), Counter()
    for c in cands:
        st = reg.status(c["form_id"])
        pol = POL.form_problems(P.T01, c["qform"], c["text"])
        if st == "admitted" and not pol:
            keep.append(c)
            per_form[c["qform"]] += 1
        else:
            rejected[f"{c['qform']}:{st if st != 'admitted' else 'polarity'}"] += 1
    return {"reg": reg, "keep": keep, "per_form": {q: per_form.get(q, 0) for q in D.FORMS}, "rejected": dict(rejected),
            "reads": dict(reads), "read_problems": problems[:40]}


def supplement_of(got: dict) -> dict:
    reg, keep = got["reg"], got["keep"]
    fids = {c["form_id"] for c in keep}
    j = reg.to_json()
    forms = [f for f in j["forms"] if f["form_id"] in fids]
    sems = [s for s in j["sems"] if s["sem_id"] in {f["sem_id"] for f in forms}]
    rows = [{"pid": c["iid"], "text": c["text"], "qform": c["qform"], "slots": c["slots"], "form_id": c["form_id"],
             "task_id": c["task_id"], "prompt_sha": c["prompt_sha"], "held_out": False,
             "g_lex": {"status": reg.status(c["form_id"]), "required": 2,
                       "reads": [list(e) for e in reg.forms[c["form_id"]].extractions]}}
            for c in sorted(keep, key=lambda c: (c["qform"], c["form_id"]))]
    return {"family": D.FAMILY, "version": D.VERSION,
            "kind": "append-only supplement to the frozen pools_v2 (G0_SPEC_v4 12.1; fix iteration 2)",
            "lexicon_sems": sorted(sems, key=lambda s: s["sem_id"]),
            "lexicon_forms": sorted(forms, key=lambda f: f["form_id"]), "wordings": rows, "per_form": got["per_form"]}


def _run(name: str, args: list, out: Path, timeout: int) -> dict:
    log = out / f"stage3_{name}.log"
    try:
        p = subprocess.run([PY, "-B", *args], cwd=C2_BUILD, capture_output=True, text=True, timeout=timeout)
        text, code = p.stdout + "\n--- stderr ---\n" + p.stderr, p.returncode
    except subprocess.TimeoutExpired:
        text, code = f"timeout after {timeout}s", 124
    log.write_text(text, encoding="utf-8")
    return {"step": name, "cmd": " ".join(args), "exit": code, "log": str(log)}


def run(root: Path = D.ROOT, *, pools_dir: Path = D.POOLS_DIR, out: Path = OUT_DEFAULT, frozen_dir: Path = D.POOLS_DIR,
        no_run: bool = False, allow_short: bool = False) -> dict:
    root, out = Path(root), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    got = admit(root)
    short = {q: n for q, n in got["per_form"].items() if n < D.MIN_ADMITTED}
    rep = {"family": D.FAMILY, "stage": 3, "admitted_per_form": got["per_form"], "min_per_form": D.MIN_ADMITTED,
           "short_forms": short, "rejected": got["rejected"], "reads": got["reads"],
           "read_problems": got["read_problems"], "freeze": None, "steps": []}
    if short and not allow_short:
        rep["verdict"] = ("STOP: fewer than 8 G-LEX 2/2 wordings for " + ", ".join(sorted(short))
                          + "; nothing frozen. Re-author those forms (4x candidates again; missing reads count as no vote) "
                            "and rerun stage 2 and 3.")
        paths.write_json(root / "stage3_report.json", rep)
        return rep
    rep["freeze"] = D.freeze_supplement(supplement_of(got), pools_dir=pools_dir, frozen_dir=frozen_dir)
    lines = ["# G13-seed pending: the new double-negation wordings (G-LEX 2/2 admitted, frozen in "
             f"pools_v2/{D.SUPPLEMENT}); run G13-seed on them in the batch run before the G5-H re-read.",
             "# pid\tqform\tform_id\ttext"]
    lines += [f"{c['iid']}\t{c['qform']}\t{c['form_id']}\t{c['text']}"
              for c in sorted(got["keep"], key=lambda c: (c["qform"], c["iid"]))]
    (out / "G13_PENDING.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    rep["g13"] = f"{len(got['keep'])} wordings listed in {out / 'G13_PENDING.txt'} (batch run)"
    if not no_run:
        for name, args, tmo in (
                ("tests", ["-m", "pytest", "-q", "-x", "families/T01"], 3000),
                ("determinism", ["families/T01/run_pilot_i2.py", "determinism"], 1800),
                ("pilot", ["families/T01/run_pilot_i2.py", "run"], 1800),
                ("g6_at_6000", ["families/T01/run_pilot_i2.py", "g6", "--n", "6000"], 3600)):
            r = _run(name, args, out, tmo)
            rep["steps"].append(r)
            if r["exit"] != 0 and name in ("tests", "determinism"):
                rep["verdict"] = f"STOP: {name} failed (see {r['log']})"
                break
        else:
            rep["verdict"] = "pilot_i2 written; read pilot_i2/PILOT_REPORT.json and G6_AT_6000.json"
    else:
        rep["verdict"] = "supplement frozen; steps 4-6 not run (--no-run)"
    paths.write_json(root / "stage3_report.json", rep)
    return rep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(D.ROOT))
    ap.add_argument("--pools", default=str(D.POOLS_DIR), help="where the supplement is frozen")
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--no-run", action="store_true")
    ap.add_argument("--allow-short", action="store_true")
    a = ap.parse_args(argv)
    rep = run(Path(a.root), pools_dir=Path(a.pools), out=Path(a.out), no_run=a.no_run, allow_short=a.allow_short)
    print(json.dumps({k: rep.get(k) for k in ("admitted_per_form", "short_forms", "freeze", "verdict")}, indent=1))
    return 0 if not rep["short_forms"] and "STOP" not in rep["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
