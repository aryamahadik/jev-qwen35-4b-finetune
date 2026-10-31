"""SOLVER A for T65: the static-taint label function over the SPEC (templates.label_spec), cross-checked against the stored canary witness for the dynamic
classes. CWE head rows: the class word of the spec's class. Solver B (a separate program) is an execution harness for the dynamic classes and an independent
AST pattern engine for the static-only ones (ROW_SCHEMA.md)."""
from . import config as C, specs as SP, templates as T


def gold_a(rec):
    spec = rec["spec"]
    if rec["head"] == "CWE":
        return C.CLASS_WORDS[spec["cls"]]
    lab = T.label_spec(spec["spec"])
    if spec["cls"] in C.DYNAMIC:
        if SP.label_from_witness(spec["witness"]) != lab:
            return None
    return lab
