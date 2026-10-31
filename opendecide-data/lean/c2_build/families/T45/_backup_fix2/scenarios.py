"""families/T45/scenarios.py: the fault catalogue, the CANONICAL execution parameters and the surface mapping of T45.

A spec is (kind, fault, canonical params). `kind` is the real tool (git push to a local bare remote, an sqlite loader, a
localhost HTTP batch endpoint, make, unittest); `fault` has a TARGET label and next move (the draw is label-first: a draw
whose executed label differs is redrawn, never relabelled). Execution runs with canonical names (QBR, QTBL, ...) so one
execution serves every surface; `surface()` is an INJECTIVE renaming of keys and values (pack nouns, random ids, random
shas, random quantities) plus label-irrelevant padding items, so labels (which depend only on equalities between values)
cannot change; the name audit in the tests re-executes a sample with the surface names themselves.
"""
from __future__ import annotations

import random
import re

KINDS = ("git", "db", "http", "build", "tests")
FAULT_LABEL = {"ok": "SUCCESS", "already_done": "NEUTRAL", "swallowed": "SILENT_PARTIAL", "deferred": "SILENT_PARTIAL",
               "wrong_target": "SILENT_WRONG", "stale_noop": "SILENT_WRONG", "error_body": "SILENT_WRONG",
               "busy": "LOUD_RETRYABLE", "bad_arg": "LOUD_PERMANENT", "blocked": "LOUD_PERMANENT",
               "fail_midway": "LOUD_PERMANENT"}
KIND_FAULTS = {
    "git": ("ok", "already_done", "swallowed", "wrong_target", "stale_noop", "busy", "bad_arg", "blocked"),
    "db": ("ok", "already_done", "swallowed", "wrong_target", "stale_noop", "busy", "bad_arg", "blocked", "fail_midway"),
    "http": ("ok", "already_done", "swallowed", "deferred", "wrong_target", "stale_noop", "error_body", "busy", "bad_arg",
             "blocked"),
    "build": ("ok", "already_done", "swallowed", "wrong_target", "stale_noop", "busy", "bad_arg", "blocked", "fail_midway"),
    "tests": ("ok", "already_done", "swallowed", "wrong_target", "busy", "bad_arg", "blocked"),
}
HELD_OUT_FAULT = "stale_noop"                 # leave-one-fault-type-out: only the sealed split (sampler S5) draws it
TRAIN_FAULTS = {k: tuple(f for f in v if f != HELD_OUT_FAULT) for k, v in KIND_FAULTS.items()}

PACKS = {
    "shop": dict(table="orders", res="orders", nouns=["cart", "coupon", "invoice", "refund", "ledger", "parcel", "basket",
                                                      "voucher", "receipt", "catalog", "tariff", "payout"]),
    "library": dict(table="loans", res="loans", nouns=["shelf", "member", "fine", "reserve", "archive", "ticket", "stack",
                                                       "journal", "renewal", "index", "lending", "branch"]),
    "clinic": dict(table="visits", res="visits", nouns=["triage", "chart", "referral", "dosage", "ward", "intake", "roster",
                                                        "recall", "billing", "consult", "slot", "queue"]),
    "studio": dict(table="takes", res="takes", nouns=["mixdown", "track", "stem", "session", "patch", "reel", "cue",
                                                      "master", "demo", "overdub", "loop", "bounce"]),
    "school": dict(table="lessons", res="lessons", nouns=["grade", "syllabus", "rubric", "cohort", "quiz", "campus",
                                                          "module", "term", "seating", "report", "credit", "unit"]),
    "farm": dict(table="harvests", res="harvests", nouns=["silo", "orchard", "herd", "tractor", "paddock", "yield",
                                                          "irrigation", "barn", "crate", "soil", "feed", "plot"]),
    "harbor": dict(table="shipments", res="shipments", nouns=["berth", "manifest", "crane", "pier", "cargo", "tug",
                                                              "customs", "dock", "freight", "buoy", "tally", "hold"]),
    "lab": dict(table="samples", res="samples", nouns=["assay", "reagent", "plate", "batch", "culture", "rack", "run",
                                                       "protocol", "stain", "freezer", "vial", "gel"]),
}
PACK_NAMES = tuple(PACKS)
BRANCH_FORMS = ("fix-{n}", "feat-{n}", "rel-{n}", "{n}-sync", "hotfix-{n}", "{n}-cleanup")
VERBS = ("total", "refund", "parse", "lookup", "merge", "render", "export", "limit", "sort", "check")
DIRS = ("tests", "spec", "checks", "suite")
ART_FORMS = ("{n}", "{n}-core", "lib{n}", "{n}-cli")
NAME_WORDS = ("amber", "birch", "cedar", "delta", "ember", "fjord", "glade", "harbor", "iris", "juniper", "kelp", "lumen")


def _sample_bad(R, m, k):
    start = R.randrange(0, m - k + 1)
    return list(range(start, start + k))


def exec_params(R: random.Random, kind: str, fault: str) -> dict:
    """Canonical (name-free) execution parameters. Label-blind quantities are drawn first."""
    m = R.choice((3, 4))
    p = {"fault": fault, "m": m, "variant": R.randrange(2), "extra": 0, "extra_names": [], "nb": 1}
    kbad = R.choice((1, 2)) if m > 3 else 1
    if kind == "git":
        p.update(br="QBR", other="QOTH", feat="QFEAT", tags=["QTG0", "QTG1"][:R.choice((1, 2))],
                 intent_tags=bool(R.random() < 0.35), noise=["QNZ0"])
        if fault in ("ok", "already_done") and not p["intent_tags"]:
            p["tags"] = ["QTG0"]
    elif kind == "db":
        p.update(table="QTBL", items=[(1001 + i, 2 + i) for i in range(m)], dup_at=R.randrange(1, m),
                 bad_rows=_sample_bad(R, m, kbad) if fault == "swallowed" else (_sample_bad(R, m, 1) if fault == "bad_arg" else []))
    elif kind == "http":
        p.update(res="QRES", items=[(1001 + i, f"QN{i}") for i in range(m)], noise=["QW0"], rate_q=R.randrange(1, m),
                 bad_rows=_sample_bad(R, m, kbad) if fault == "swallowed" else [])
    elif kind == "build":
        p.update(names=[f"QA{i}" for i in range(m)], ver=7, old_present=bool(R.random() < 0.6) and fault not in ("swallowed", "fail_midway"), noise=["QNZ0"],
                 bad_rows=_sample_bad(R, m, kbad) if fault in ("swallowed", "fail_midway") else [])
    else:
        p.update(dir="QD0", bad_dir="QD1", bad_mod="test_QL0", bad_tests=["test_QL1", "test_QL2"],
                 names=[(f"test_QM{i % 3}", f"test_QT{i}") for i in range(m)], fail_at=R.randrange(m),
                 bad_rows=_sample_bad(R, m, kbad) if fault == "swallowed" else [])
    # irrelevant parameters are pinned to a constant so one execution serves every draw of the same structure
    if not (kind == "git" and fault in ("wrong_target", "bad_arg")) and not (kind == "http" and fault == "error_body"):
        p["variant"] = 0
    if not (kind == "tests" and fault in ("busy", "blocked")):
        p["fail_at"] = 0 if kind == "tests" else p.get("fail_at")
    if not (kind == "db" and fault == "fail_midway") and kind == "db":
        p["dup_at"] = 1
    if not (kind == "http" and fault == "deferred") and kind == "http":
        p["rate_q"] = 1
    if kind == "build" and fault not in ("ok", "wrong_target", "busy", "bad_arg", "blocked"):
        p["old_present"] = fault in ("stale_noop",) and False
    if kind == "git":
        if fault != "swallowed" and not (fault in ("ok", "already_done") and p["intent_tags"]):
            p["tags"] = ["QTG0"]
        if fault not in ("ok", "already_done"):
            p["intent_tags"] = False
    return p


def faults_for(kind: str, label: str, *, held_out: bool) -> tuple:
    pool = KIND_FAULTS[kind] if held_out else TRAIN_FAULTS[kind]
    return tuple(f for f in pool if FAULT_LABEL[f] == label)


def target_move(fault: str, variant: int) -> str:
    base = {"ok": "ADVANCE", "already_done": "ADVANCE", "swallowed": "REPAIR_ARGS", "deferred": "RETRY",
            "wrong_target": "REPAIR_ARGS", "stale_noop": "REPAIR_ARGS", "busy": "RETRY", "bad_arg": "REPAIR_ARGS",
            "blocked": "ESCALATE", "fail_midway": "REPAIR_ARGS"}
    if fault == "error_body":
        return "REPAIR_ARGS" if variant == 0 else "ESCALATE"
    return base[fault]


# ------------------------------------------------------------------------------------------------ surface mapping
CANON_RE = re.compile(r"Q[A-Z]+[0-9]?")


def surface(R: random.Random, kind: str, pack: str, p: dict) -> dict:
    """Injective renaming maps (canonical string -> surface string) for identifiers (`names`) and for whole values
    (`vals`), plus the kind's key syntax for padding items. R is seeded from the row key (label-blind)."""
    pk = PACKS[pack]
    nouns = list(pk["nouns"])
    R.shuffle(nouns)
    names, vals = {}, {}
    if kind == "git":
        forms = list(BRANCH_FORMS)
        R.shuffle(forms)
        names["QBR"] = forms[0].format(n=nouns[0])
        names["QOTH"] = forms[1].format(n=nouns[1])
        names["QFEAT"] = forms[2].format(n=nouns[2])
        names["QNZ0"] = forms[3].format(n=nouns[3])
        for i, t in enumerate(p["tags"]):
            names[t] = f"v{R.randrange(1, 4)}.{R.randrange(0, 9)}.{R.randrange(0, 9)}"
        names["QTG1"] = names.get("QTG1", "v9.9.9")
        if names["QTG0"] == names["QTG1"]:
            names["QTG1"] = "v0.9.9"
    elif kind == "db":
        names["QTBL"] = pk["table"]
        ids = sorted(R.sample(range(1000, 9990), len(p["items"]) + 12))
        for i, (iid, _) in enumerate(p["items"]):
            names[str(iid)] = str(ids[i])
        pool = R.sample(range(2, 60), 20)
        for q in range(2, 20):
            vals[str(q)] = str(pool[q])
    elif kind == "http":
        names["QRES"] = pk["res"]
        ids = R.sample(range(1000, 9990), len(p["items"]))
        for i, (iid, _) in enumerate(p["items"]):
            names[str(iid)] = str(ids[i])
        words = R.sample(NAME_WORDS, 12)
        for i in range(len(p["items"])):
            vals[f"QN{i}"] = f"{words[i]}"
            vals[f"QN{i}_old"] = f"{words[i]}-old"
        vals["QW0"] = words[10]
    elif kind == "build":
        for i in range(len(p["names"])):
            names[f"QA{i}"] = ART_FORMS[R.randrange(len(ART_FORMS))].format(n=nouns[i])
        names["QNZ0"] = nouns[8] + "-lib"
        ver = R.randrange(3, 40)
        vals["r7"], vals["r6"] = f"r{ver}", f"r{ver - 1}"
        vals["r1"] = "r1"
    else:
        dirs = R.sample(DIRS, 2)
        names["QD0"], names["QD1"] = dirs
        for i in range(3):
            names[f"QM{i}"] = nouns[i]
        verbs = R.sample(VERBS, 8)
        for i in range(len(p["names"])):
            names[f"QT{i}"] = f"{nouns[i % 3]}_{verbs[i]}"
        names["QL0"] = nouns[5]
        names["QL1"] = f"{nouns[5]}_{verbs[5]}"
        names["QL2"] = f"{nouns[5]}_{verbs[6]}"
    if kind == "git":
        # shas: any 7-hex value maps to a random 7-hex value (injective by construction in apply_vals)
        vals["__sha__"] = ""
    return {"names": names, "vals": vals, "pack": pack, "nouns": nouns}


def _sub_names(text: str, names: dict) -> str:
    for k in sorted(names, key=len, reverse=True):
        text = text.replace(k, names[k])
    return text


class Mapper:
    """Applies the surface mapping to commands, keys and values; shas get a random 7-hex per distinct canonical sha."""

    def __init__(self, R: random.Random, sm: dict, kind: str):
        self.R, self.sm, self.kind = R, sm, kind
        self.sha = {}

    def text(self, s: str) -> str:
        return _sub_names(s, self.sm["names"])

    def key(self, k: str) -> str:
        if self.kind == "tests":                     # "QD0/test_QM0.test_QT0": names only
            return self.text(k)
        return self.text(k)

    def val(self, v: str) -> str:
        if self.kind == "git" and re.fullmatch(r"[0-9a-f]{7}", v):
            if v not in self.sha:
                self.sha[v] = "".join(self.R.choice("0123456789abcdef") for _ in range(7))
            return self.sha[v]
        vm = self.sm["vals"]
        if v in vm:
            return vm[v]
        if self.kind == "http":
            for k in sorted(vm, key=len, reverse=True):
                if k in v:
                    v = v.replace(k, vm[k])
            return v
        return self.text(v)

    def state(self, st: dict) -> dict:
        return {self.key(k): self.val(v) for k, v in st.items()}
