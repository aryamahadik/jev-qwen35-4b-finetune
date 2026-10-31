"""families/T07/haiku_heldout.py: Haiku RE-AUTHORING of dev-only (held-out) question wordings for the T07 S5 mixdev
(C2_DATA_SPEC 7.1; PREREG A53 follow-up, 16 Oct 2026). T07's pool has 39 held-out wordings for all 7 forms, but at
generation time the polarity screen leaves none usable for yn_dneg_gets (10 of 10 mixdev rows) and few for yn_not_gets
(4 of 20 rows), so `_pick_wording` falls back to training wordings (14 of 150 rows). This module asks for 8 new held-out
wordings per form for those two forms (16 wordings; same prompt, brief and rules as authoring.py's `word-held` task),
admits them with authoring.lint_wording_v2 (lint + the polarity rule), and writes the G-LEX 2/2 reads through
haiku/extract_build.py. It does NOT touch the pools, the plugin or the mixdev.

  task      word-held2 (one task, 2 items, 16 wordings), piece ids t07-<VERSION>h2-wordheld-<qform>-00
  folders   haiku/heldout/ (authoring: tasks/, answers/, chunks/, prompts/, key/, manifest/, plan/, TASKS.json)
            haiku/heldout/extract/ (G-LEX reads r1, r2: tasks/, answers/, ...; TASKS.json)
Run (from lean/):  ../.venv/bin/python c2_build/families/T07/haiku_heldout.py plan | write | admit | glex
"""
from __future__ import annotations

import contextlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from families.T07 import authoring as A  # noqa: E402

FAMILY = "T07"
ROOT = HERE / "haiku" / "heldout"
FORMS = ("yn_dneg_gets", "yn_not_gets")
HOW_MANY = 8
_ORIG_BUILD = A.build_tasks


def _captured_items() -> list:
    """The items of authoring.build_tasks()' own `word-held` task, captured at its _batch call (nothing is written)."""
    seen = {}
    orig = A._batch

    def spy(kind, name, items, prompt):
        if name == "word-held":
            seen["items"] = items
        return orig(kind, name, items, prompt)

    A._batch = spy
    try:
        _ORIG_BUILD()
    finally:
        A._batch = orig
    return seen["items"]


def build() -> tuple:
    items, plan = [], {}
    for iid, body in _captured_items():
        qf = iid.split("-wordheld-")[1].rsplit("-", 1)[0]
        if qf not in FORMS:
            continue
        nid = iid.replace(f"t07-{A.VERSION}-wordheld-", f"t07-{A.VERSION}h2-wordheld-")
        body = json.loads(json.dumps(body))
        body["brief"]["how_many"] = HOW_MANY
        body["rules"] = [f"{HOW_MANY} wordings with exactly this meaning", "each listed placeholder exactly once"]
        items.append((nid, body))
        plan[nid] = {"piece": "wording", "qform": qf, "held_out": True}
    b = A._batch("author_wording", "word-held2", items, A.WORDING_PROMPT)
    return [A.Task("word-held2", "author_wording", "wordings", b, HOW_MANY * len(items), True, "wordings")], plan


@contextlib.contextmanager
def patched():
    old = A.build_tasks
    A.build_tasks = build
    try:
        yield
    finally:
        A.build_tasks = old


def plan_counts() -> dict:
    tasks, plan = build()
    return {"task_id": tasks[0].task_id, "items": len(plan), "wordings_asked": tasks[0].outputs, "forms": list(FORMS)}


def write() -> dict:
    tasks, plan = build()
    files, manifest = A.files(tasks, plan, ROOT)
    paths.write_files(ROOT, files)
    return {"tasks": manifest["n_tasks"], "outputs_expected": manifest["outputs_expected"]}


def _extract_module():
    spec = importlib.util.spec_from_file_location("t07_extract_build", HERE / "haiku" / "extract_build.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["t07_extract_build"] = mod
    spec.loader.exec_module(mod)
    return mod


def admit(root: Path = ROOT) -> dict:
    """Answers -> admitted held-out wordings: authoring.collect (lint_wording) + lint_wording_v2 (polarity), minus texts
    equal (normalised) to a pool wording. Writes root/ADMITTED.json and PROBLEMS.json."""
    with patched():
        got = A.collect(root)
    pool = json.loads((HERE / "pools" / "wordings.json").read_text())
    pool = pool if isinstance(pool, list) else [r for v in pool.values() if isinstance(v, list) for r in v]
    have = {A.norm(r["text"]) if hasattr(A, "norm") else " ".join(r["text"].lower().split()) for r in pool}
    norm = A.norm if hasattr(A, "norm") else (lambda t: " ".join(t.lower().split()))
    ok, bad = [], []
    for p in got["pieces"]:
        m = p["meta"]
        if m.get("piece") != "wording":
            continue
        probs = list(p["lint"]) + A.polarity_problems(m["qform"], p["value"])
        (bad if probs or norm(p["value"]) in have else ok).append({**p, "problems": probs})
    rep = {"asked": HOW_MANY * len(FORMS), "accepted": len(ok), "rejected": len(bad),
           "by_form": {q: sum(1 for r in ok if r["meta"]["qform"] == q) for q in FORMS},
           "collect_problems": len(got["problems"])}
    paths.write_json(root / "ADMITTED.json", {"admitted": ok, "rejected": bad, "report": rep})
    paths.write_json(root / "PROBLEMS.json", got["problems"])
    return rep


def glex(root: Path = ROOT) -> dict:
    """G-LEX reads r1 and r2 (2/2) over the admitted held-out wordings. Needs `admit` first. Writes root/extract/."""
    EB = _extract_module()
    adm = json.loads((root / "ADMITTED.json").read_text())["admitted"]
    drops = []
    reg, origin = EB.build_registry(adm, drops)
    fids = sorted(f for f, o in origin.items() if o["origin"] == "haiku_wording" and reg.forms[f].unit_ok)
    files, rows = {}, []
    for read in ("r1", "r2"):
        out, r = EB.batch_files(EB.lex_batch(reg, fids, read), read, root / "extract")
        files.update(out)
        rows += r
    files["TASKS.json"] = json.dumps({"family": FAMILY, "stage": "heldout-extract", "n_tasks": len(rows),
                                      "forms_for_admission": len(fids), "required_reads_per_form": 2, "tasks": rows,
                                      "registry_drops": drops}, ensure_ascii=False, indent=1) + "\n"
    paths.write_files(root / "extract", files)
    return {"forms_admitted": len(adm), "forms_unit_ok": len(fids), "tasks": len(rows)}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    print(json.dumps({"plan": plan_counts, "write": write, "admit": admit, "glex": glex}[cmd](), indent=1))
