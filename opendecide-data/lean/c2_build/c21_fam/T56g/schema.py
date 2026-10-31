"""Row JSON schema for T56g and the view handed to SOLVER B (a separate Sonnet session that writes its own CODE: its own
AST-based signature matchers per language and its own protected-path check from the diff paths).

B gets per row: the pristine base tree, the unified diff, the protected list and the task package (the held-out suite: rendered
files + structured cases). It gets NO label, NO manifest, NO transform-family id, NO subtype and NO signature output.
"""
import copy

from . import task as TK

B_FIELDS = ("row_id", "lang", "carriers")


def task_package(g):
    heldout_files = {}
    from LC_COMMON import suites
    heldout_files = suites.render_suite_files(g["ref_lo"], g["lang"], g["heldout"], g["ids"], "gho")
    return {"task": g["uid"], "lang": g["lang"], "base_tree": TK.base_tree(g), "heldout_files": heldout_files,
            "heldout_cases": g["heldout"]["cases"], "visible_path": TK.vis_path(g), "toolchain_files": TK.toolchain_files(g),
            "config_names": sorted(TK.CONFIG_NAMES)}


def b_view(row, packages):
    v = {k: copy.deepcopy(row[k]) for k in B_FIELDS}
    v["carriers"].pop("QUESTION_FORM", None)
    v["patched_tree"] = row["b_inputs"]["patched_tree"]
    v["protected"] = row["b_inputs"]["protected"]
    v["package"] = packages[row["b_inputs"]["task"]]
    return v
