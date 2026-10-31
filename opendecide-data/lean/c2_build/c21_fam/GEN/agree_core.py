"""Shared comparator for solver A's canonical spec versus solver B's parse-back (gate G-A2). Used by the batch harness (agree_ab.py) and by the
per-row check at creation (row_check.py). Pure functions; imports only the standard library.

Comparator rules (applied to BOTH sides): numeric strings compare by exact value; the lists that carry no stem order (LOGIC entities / preds,
CA-C4 options, TM-T4 plan tasks) compare as sorted lists; everything else compares in order. A predicate that A's spec holds but that no
sentence of the stem mentions ("unrendered_in_A_spec") cannot affect any answer and is reported as such, not as a defect.
"""
import json
import re
from fractions import Fraction

NUMERIC = re.compile(r"^-?\d+(?:\.\d+)?$")
UNORDERED = {("LG-L1", "entities"), ("LG-L1", "preds"), ("LG-L2", "entities"), ("LG-L2", "preds"), ("LG-L4", "entities"), ("LG-L4", "preds"),
             ("LG-L2", "options"), ("CA-C4", "options"), ("CA-C5", "given"), ("TM-T4", "tasks")}


def _num(x):
    if isinstance(x, bool):
        return None
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str) and NUMERIC.match(x):
        return Fraction(x)
    return None


def _key(x):
    return json.dumps(x, sort_keys=True)


def diff(a, b, path, form, out):
    """Collect index-free paths where a (solver A canon) and b (solver B parse) differ."""
    na, nb = _num(a), _num(b)
    if na is not None and nb is not None:
        if na != nb:
            out.append(path)
        return
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append(path + "." + k + "(only_B)")
            elif k not in b:
                out.append(path + "." + k + "(only_A)")
            else:
                diff(a[k], b[k], path + "." + k, form, out)
        return
    if isinstance(a, list) and isinstance(b, list):
        last = path.split(".")[-1]
        if last == "preds" and form.startswith("LG") and set(b) < set(a) and len(set(b)) == len(b):
            out.append(path + "(unrendered_in_A_spec)")   # A's spec holds a predicate that appears nowhere in the text
            return
        if (form, last) in UNORDERED:
            a = sorted(a, key=_key)
            b = sorted(b, key=_key)
        if len(a) != len(b):
            out.append(path + "[](length)")
            return
        for x, y in zip(a, b):
            diff(x, y, path + "[]", form, out)
        return
    if a != b:
        out.append(path)
