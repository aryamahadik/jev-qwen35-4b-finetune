"""families/T31/haiku_heldout.py: Haiku authoring of DEV-ONLY (held-out) question wordings for the T31 S5 mixdev
(C2_DATA_SPEC 7.1; PREREG A53 follow-up, 16 Oct 2026). T31's wording pool has no held-out wording (0 of 180) and
plugin.pick() defaults to held_out=False, so S5 mixdev rows reuse training wordings (67 of 68 shared ids; 142 of 144
rows). This module writes the authoring tasks for held-out wordings with the family's own prompt, briefs, rules and
checks (haiku_author), loads their answers through haiku_author.load(), and writes the G-LEX 2/2 reads through
extract_build. It does NOT touch the pools, the plugin or the mixdev (the orchestrator merges admitted wordings with
held_out=True and rebuilds the mixdev).

  tasks     wording-held-appr (4 forms x 6 = 24 items), wording-held-agent (5 forms x 6 = 30 items): 54 items, 2 tasks
  folders   haiku/heldout/ (authoring: tasks/, answers/, chunks/, prompts/, key/, manifest/, TASKS.json)
            haiku/heldout/extract/ (G-LEX reads r*: tasks/, answers/, ...; TASKS.json)
Run (from lean/):  ../.venv/bin/python c2_build/families/T31/haiku_heldout.py plan | write | admit | glex
"""
from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from families.T31 import extract_build as EB  # noqa: E402
from families.T31 import haiku_author as HA  # noqa: E402

FAMILY = "T31"
ROOT = HERE / "haiku" / "heldout"
SEED = "t31-heldout-a53-v1"
HELD_N = 6
APPR_Q = ("ch_approver", "yn_holder", "yn_holder_other", "yn_holder_not")
AGENT_Q = ("yn_agent_ok", "yn_agent_beyond", "yn_agent_lacks", "yn_agent_not", "ch_scope")


def held_items(qforms: tuple) -> list:
    """haiku_author._wording_items' body for indices n .. n+HELD_N-1 of each form (style cycle continues past the
    training items); ids wording|<q>|<n..>"""
    out = []
    for q in qforms:
        meaning, required, _ = HA.QUESTION_MEANING[q]
        n = HA.WORDINGS[q]
        for i in range(n, n + HELD_N):
            id_ok = q != "ch_approver" or i % 2 == 0
            slots = {r.strip("{}"): "required, exactly once" for r in required}
            if "REQ_ID" not in slots:
                slots["REQ_ID"] = "optional, at most once" if id_ok else "leave it out"
            if q in ("yn_holder_not", "yn_agent_not"):
                rules = ["exactly one 'not', inside an embedded statement"]
            elif q in ("yn_holder_other", "yn_agent_lacks"):
                rules = ["no 'not' and no n't; the one implicit negation the meaning asks for only"]
            else:
                rules = ["no negation at all"]
            out.append((f"wording|{q}|{i:03d}",
                        {"brief": f"Meaning: {meaning} Style: "
                                  f"{HA.WORDING_STYLES[(i * 3 + len(q)) % len(HA.WORDING_STYLES)]}.",
                         "slots": slots, "rules": rules}))
    return out


def held_plan() -> list:
    info = {"pool": "wording", "register": "question", "held_out": True, "mode": "T"}
    return [(f"wording-held-{track}", "author_wording", held_items(qs), HA._wording_prompt(track),
             HA.FORBID_WORDING, {**info, "track": track})
            for track, qs in (("appr", APPR_Q), ("agent", AGENT_Q))]


@contextlib.contextmanager
def patched():
    old = (HA.ROOT, HA.SEED, HA.plan, EB.EXTRACT, EB.SEED)
    HA.ROOT, HA.SEED, HA.plan = ROOT, SEED, held_plan
    EB.EXTRACT, EB.SEED = ROOT / "extract", "t31-heldout-extract-a53-v1"
    try:
        yield
    finally:
        HA.ROOT, HA.SEED, HA.plan, EB.EXTRACT, EB.SEED = old


def plan_counts() -> dict:
    with patched():
        bs = HA.build_batches()
    return {"tasks": [{"task": i["task"], "task_id": b.chunks[0]["task_id"], "items": len(b.chunks[0]["items"])}
                      for i, b in bs]}


def write() -> dict:
    with patched():
        files, manifest = HA.files_for(HA.build_batches())
        paths.write_files(ROOT, files)
    return {"tasks": manifest["n_tasks"], "items": manifest["items_expected"]}


def _training_texts() -> set:
    d = json.loads((HERE / "pools_v2" / "wordings.json").read_text())
    rows = d if isinstance(d, list) else [r for v in d.values() if isinstance(v, list) for r in v]
    return {HA._norm(r["text"]) if hasattr(HA, "_norm") else " ".join(r["text"].lower().split()) for r in rows}


def admit(root: Path = ROOT) -> dict:
    """Answers -> admitted held-out wordings (haiku_author.load: G-SL, negcount, placeholders, lexicon add), minus texts
    equal to a training wording. Writes root/ADMITTED.json and PROBLEMS.json."""
    with patched():
        res = HA.load()
    train = _training_texts()
    norm = HA._norm if hasattr(HA, "_norm") else (lambda t: " ".join(t.lower().split()))
    ok, dup = [], []
    for sid, (sk, fid) in sorted(res["pools"]["wordings"].items()):
        rec = {"skin_id": sid, "form_id": fid, "qform": sk.qform, "text": sk.text, "slots": dict(sk.decl),
               "task_id": sk.haiku_task_id, "prompt_sha": sk.haiku_prompt_sha, "held_out": True}
        (dup if norm(sk.text) in train else ok).append(rec)
    rep = {"asked": HELD_N * (len(APPR_Q) + len(AGENT_Q)), "accepted": len(ok), "duplicate_of_training": len(dup),
           "dropped": len(res["drops"]), "tasks_missing": len(res["missing"]),
           "by_form": {q: sum(1 for r in ok if r["qform"] == q) for q in APPR_Q + AGENT_Q}}
    paths.write_json(root / "ADMITTED.json", {"admitted": ok, "dropped_duplicates": dup, "report": rep})
    paths.write_json(root / "PROBLEMS.json", [list(d) for d in res["drops"]] + [["missing", m] for m in res["missing"]])
    return rep


def glex(root: Path = ROOT) -> dict:
    """G-LEX extraction reads (2/2, extract_build.READS) over the admitted held-out wordings. Needs `admit` first."""
    with patched():
        res = HA.load()
        adm = {r["form_id"] for r in json.loads((root / "ADMITTED.json").read_text())["admitted"]}
        reg = res["pools"]["lexicon"]
        ok, bad = EB.lexicon_review(reg)
        fids = [f for f in ok if f in adm]
        files, tasks = EB.build_files(reg, fids, [], bad, {"forms_admitted": len(adm), "forms_unit_ok": len(fids)})
        paths.write_files(root / "extract", files)
    return {"forms_admitted": len(adm), "forms_unit_ok": len(fids), "tasks": len(tasks)}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    print(json.dumps({"plan": plan_counts, "write": write, "admit": admit, "glex": glex}[cmd](), indent=1))
