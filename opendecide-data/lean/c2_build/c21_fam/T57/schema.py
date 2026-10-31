"""Row JSON schema for T57 and the view handed to SOLVER B (a separate Sonnet session that writes its own CODE).

Solver B sees only the G0-lite and ROW_SCHEMA.md. Per row it receives `b_view(row, package)`: the rendered carriers, the
candidate patched trees (exact text, comments included), and the TASK PACKAGE of the row's module (reference tree, buggy tree,
the hidden-suite cases with their program-generated expectations, the visible case, the differential points). It receives NO
label, NO manifest, NO candidate kind or expected class, NO tags beyond what the hidden suite itself implies.
"""
import copy

from LC_COMMON import ir as I

from .base import files_of

B_VIEW_FIELDS = ("row_id", "head", "lang", "carriers", "b_inputs")


def task_package(task):
    lang = task["lang"]
    return {"task_uid": task["uid"], "module_id": task["id"], "lang": lang,
            "reference_files": files_of(task["ref_lo"], lang), "buggy_files": files_of(task["buggy_lo"], lang),
            "go_files": {k: v for k, v in __import__("LC_COMMON.render", fromlist=["x"]).render_module(task["ref_lo"], lang).items()
                         if k in ("go.mod", "vendor/modules.txt")},
            "visible_case": task["visible"], "hidden_cases": task["hidden"]["cases"], "differential_points": task["points"],
            "snapshot": task["snapshot"], "class_rules": ["NOFIX", "REGRESSION", "PARTIAL", "CORRECT"],
            "reset_name": task["ref_lo"]["meta"].get("reset_name"), "class_name": (task["ref_lo"]["cls"] or {}).get("name")}


def b_inputs(spec):
    task = spec["task"]
    return {"task_uid": task["uid"], "candidate_files": [c["files"] for c in spec["cands"]], "options": spec.get("options"),
            "visible_case": task["visible"]["name"]}


def b_view(row, packages):
    v = {k: copy.deepcopy(row[k]) for k in B_VIEW_FIELDS}
    v["carriers"].pop("QUESTION_FORM", None)
    v["package"] = packages[row["b_inputs"]["task_uid"]]
    return v
