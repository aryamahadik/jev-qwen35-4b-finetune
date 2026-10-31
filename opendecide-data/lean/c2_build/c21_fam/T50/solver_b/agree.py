"""Agreement harness T50: lane generator (in memory, no rows written) vs solver A gold vs solver B.

Run (from c21_fam):  python3 -m T50.solver_b.agree [--limit N]
Nothing is written to the repository. Output: counts only (no item text).
"""
import argparse
import collections
import hashlib
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FAM = os.path.dirname(os.path.dirname(_HERE))
if _FAM not in sys.path:
    sys.path.insert(0, _FAM)


def make_rowview(spec, rendering):
    d = spec.state.to_dict()
    rv = {
        "card": spec.card,
        "state": d,
        "user_turns": [{"form": t.form, "slots": dict(t.slots)} for t in spec.user_turns],
        "history": [{"author": h.author, "carrier": h.carrier, "path": h.path, "text": h.text,
                     "approved_by_user": h.approved_by_user} for h in spec.history],
        "text": rendering["text"],
        "view": rendering.get("view", "primary"),
        "egress_facts": None,
    }
    if spec.egress is not None:
        rv["egress_facts"] = {"visibility": spec.egress.visibility, "scope_host": spec.egress.scope_host}
    ed = edit_view(spec, rendering)
    if ed is not None:
        rv["edit"] = ed
    return rv


_EDIT_KEYS = ("carrier", "path", "old", "new", "old_string", "new_string", "content", "patch", "diff")


def edit_view(spec, rendering):
    """Block G: the edit payload that is VISIBLE in the rendered row (carrier, path, old / new span, content, patch); never the
    path class, zone, consumer flag or any gold field. The generator's block-G field names are not in the spec text, so this
    reads `rendering["edit"]` or `spec.edit` (dict or object) and keeps only the visible keys; B also parses rendering["text"]."""
    ed = rendering.get("edit") if isinstance(rendering, dict) else None
    if ed is None:
        ed = getattr(spec, "edit", None)
    if ed is None:
        return None
    if not isinstance(ed, dict):
        ed = ed.to_dict() if hasattr(ed, "to_dict") else {k: getattr(ed, k, None) for k in _EDIT_KEYS}
    return {k: ed[k] for k in _EDIT_KEYS if ed.get(k) is not None}


def sha_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def generate_specs():
    from T50.blocks import plan
    from T50.generator import DropLedger, build_cell
    led = DropLedger()
    specs = []
    for c in plan():
        specs += build_cell(c, led)
    return specs, led


def run(specs, label_row, limit=None):
    stats = collections.Counter()
    classes = collections.Counter()
    by_fam = collections.Counter()
    rows = 0
    dis = []
    for s in specs:
        for r in s.renderings:
            if not r.get("roundtrip", True):
                continue
            rows += 1
            if limit and rows > limit:
                break
            rv = make_rowview(s, r)
            b = label_row(rv)
            a = (s.gold.label, s.gold.reason, s.gold.tier)
            bb = (b["label"], b["reason"], b["tier"])
            stats["rows"] += 1
            stats["label_agree"] += int(a[0] == bb[0])
            stats["triple_agree"] += int(a == bb)
            stats["reason_agree"] += int(a[1] == bb[1])
            stats["tier_agree"] += int(a[2] == bb[2])
            if a != bb:
                key = (s.intent, a, bb, tuple(sorted(set(b.get("gaps", [])))), b.get("opaque"))
                classes[key] += 1
                dis.append((s.spec_id, r["role"], key))
    return stats, classes, dis


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--top", type=int, default=60)
    a = ap.parse_args()
    from T50.solver_b.t50_b import label_row
    specs, led = generate_specs()
    stats, classes, dis = run(specs, label_row, a.limit)
    n = stats["rows"]
    print("rows", n, "generator drops", led.count())
    for k in ("label_agree", "triple_agree", "reason_agree", "tier_agree"):
        print(k, stats[k], "%.2f%%" % (100.0 * stats[k] / max(1, n)))
    print("disagreement classes", len(classes), "rows", sum(classes.values()))
    for k, v in classes.most_common(a.top):
        print(v, k)
