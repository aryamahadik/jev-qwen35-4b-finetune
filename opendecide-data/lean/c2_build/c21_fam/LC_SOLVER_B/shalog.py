"""Writes SHAS.json next to each solver_b (sha256 of every solver B file, of the shared LC_SOLVER_B engine, and of the generator /
solver A side files that the agreement harness imported). Run: python3 -m LC_SOLVER_B.shalog"""
import hashlib
import json
import os
import sys

from . import agreelib

FAM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILIES = ("T42c", "T57", "T56g")


def main():
    engine = agreelib.sha_tree(os.path.join(FAM, "LC_SOLVER_B"), exts=(".py", ".md", ".ini"))
    out = {}
    for fam in FAMILIES:
        root = os.path.join(FAM, fam)
        b = agreelib.sha_tree(os.path.join(root, "solver_b"), exts=(".py", ".md"))
        a_side = {k: v for k, v in agreelib.sha_tree(root, exts=(".py", ".md"), skip=("__pycache__", "tests", "solver_b")).items()}
        common = agreelib.sha_tree(os.path.join(FAM, "LC_COMMON"), exts=(".py",))
        comb = hashlib.sha256(json.dumps([b, engine], sort_keys=True).encode()).hexdigest()
        doc = {"family": fam, "solver_b_files": b, "shared_engine_LC_SOLVER_B": engine, "combined_solver_b_sha256": comb,
               "generator_side_files_imported_by_harness_only": a_side, "LC_COMMON_files_imported_by_harness_only": common}
        with open(os.path.join(root, "solver_b", "SHAS.json"), "w") as f:
            json.dump(doc, f, indent=1, sort_keys=True)
        out[fam] = comb
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
