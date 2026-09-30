"""Build the 2B distillation file data/v14_parts/train_2b_golden_kd.jsonl (FINETUNE_PLAN.md 3.3) from the frozen
golden_train.jsonl (read only, never modified) and 4B-E's sharded labels (od_gcp.py label). Same rows, same ids, same
order; only meta.teacher / meta.teacher_src (and meta.teacher4b, the raw read kept for audit) change:
  - human vote-share / near-miss / exact-probability teachers (meta.teacher, not blend50): unchanged;
  - blend50 teachers (in-sample for 4B-E): deleted; the row trains on smoothed gold;
  - gold_probs rows and the 3 csqa duplicate-option rows: no new teacher;
  - yes/no rows of a kd_full_src source (the 2B config's kd_full_src, e.g. gd_gen2_probability): no new teacher and
    no copied fresh teacher, because train_decoder uses a yes/no kd_full teacher ALONE as the target (no gold mixing):
    only their exact probabilities count, and the rest train on smoothed gold. Choice rows of those sources are not
    affected (train_decoder mixes their teacher with gold as usual), so they get 4B-E like any other row;
  - every other labelled row: meta.teacher = 4B-E ({"yes": p} or the full softmax), teacher_src = --teacher-src;
  - complement pairs where both rows have fresh 4B-E teachers: t_a <- (t_a + 1 - t_b) / 2, t_b <- 1 - t_a;
  - attacked twins (the 'b' side of inv): the clean partner's FINAL teacher is copied if it gives the gold answer
    (yes/no: p_yes >= 0.5 <=> gold = 1; choice: a unique argmax = gold), else meta.teacher is deleted. The teacher is
    never read on attacked text.
Prints the final kd-target count (= expect_kd_targets of the 2B config).

  python build_2b_kd.py --labels data/v14_label_shards/labels_q35_4b_pxE --shards-dir data/v14_label_shards
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

import shard_golden as sg

HERE = Path(__file__).resolve().parent


def kd_target(r):
    """Same rule as train_decoder.kd_target: only a non-empty dict is a distillation target."""
    t = (r.get("meta") or {}).get("teacher")
    return t if isinstance(t, dict) and t else None


def _drop_teacher(m):
    m.pop("teacher", None)
    m.pop("teacher_src", None)


def label_teacher(r, probs):
    """4B-E's read as a teacher dict: {"yes": p} for yes/no, {option: p} over exactly the row's options for choice."""
    if r["qtype"] == "noul":
        return {"yes": float(probs["yes"])}
    if set(probs) != set(r["options"]) or len(probs) != len(r["options"]):
        raise ValueError(f"{r['id']}: label keys {sorted(probs)[:5]} != options {r['options'][:5]}")
    return {o: float(probs[o]) for o in r["options"]}


def gives_gold(r, t) -> bool:
    """Does teacher t answer row r's gold? Yes/no: p_yes >= 0.5 <=> gold = 1. Choice: the unique argmax is the gold
    option (ties count as wrong)."""
    if r["qtype"] == "noul":
        return (float(t["yes"]) >= 0.5) == (r["gold"] == 1)
    if set(t) != set(r["options"]):
        return False
    top = max(float(v) for v in t.values())
    best = [o for o, v in t.items() if float(v) == top]
    return len(best) == 1 and best[0] == r["gold"]


def validate(rows, skip=()):
    """Teacher keys equal the options exactly and sum to 1 +- 0.01; yes/no values lie in [0, 1]; options are unique;
    no teacher_src is in kd_skip_src. Raises with examples."""
    bad = []
    for r in rows:
        t = kd_target(r)
        if t is None:
            continue
        m = r["meta"]
        if m.get("teacher_src") in skip:
            bad.append((r["id"], f"teacher_src {m.get('teacher_src')!r} is in kd_skip_src"))
        vals = [float(v) for v in t.values()]
        if not all(math.isfinite(v) and 0.0 <= v <= 1.0 for v in vals):
            bad.append((r["id"], f"teacher values outside [0, 1]: {vals[:4]}"))
        if r["qtype"] == "noul":
            if "yes" not in t:
                bad.append((r["id"], "yes/no teacher has no 'yes'"))
            continue
        o = r["options"]
        if len(set(o)) != len(o):
            bad.append((r["id"], "duplicate options"))
        if set(t) != set(o):
            bad.append((r["id"], f"teacher keys != options ({sorted(set(t) ^ set(o))[:4]})"))
        if abs(sum(vals) - 1.0) > 0.01:
            bad.append((r["id"], f"teacher sums to {sum(vals):.4f}"))
    if bad:
        raise ValueError(f"build_2b_kd: {len(bad)} invalid teacher(s), e.g. {bad[:5]}")


def build(rows, rels, labels, eligible, teacher_src="q35_4b_E", skip=("blend50",), kd_full=("gd_gen2_probability",)):
    """Returns (new rows, counts). rows are not modified (each output row has its own meta). labels: {id: probs} for
    exactly the eligible rows (shard_golden.select_rows); a label on any other row is an error."""
    extra = sorted(set(labels) - set(eligible))
    if extra:
        raise ValueError(f"{len(extra)} label(s) on rows that must not be labelled (attacked, in-sample, ...): {extra[:5]}")
    missing = sorted(set(eligible) - set(labels))
    if missing:
        raise ValueError(f"{len(missing)} eligible row(s) have no label: {missing[:5]}")
    n = Counter()
    out = [{**r, "meta": dict(r.get("meta") or {})} for r in rows]
    by_id = {r["id"]: r for r in out}
    if len(by_id) != len(out):
        raise ValueError("duplicate row ids")
    inv_b = {x["b"] for x in rels if x["type"] == "inv"}
    fresh = set()
    for r in out:
        m = r["meta"]
        if m.get("teacher_src") in skip:  # old in-sample model teachers (blend50)
            _drop_teacher(m)
            n["deleted_" + "_".join(skip)] += 1
        if r["id"] in inv_b:  # attacked twins: set below from the clean partner
            continue
        if r["id"] in sg.CSQA_DUP:
            _drop_teacher(m)
            n["csqa_dup_no_teacher"] += 1
            continue
        if m.get("gold_probs"):
            n["gold_probs_unchanged"] += 1
            continue
        if kd_target(r) is not None:  # human vote share, near-miss bundle, exact probability
            n["human_or_exact_unchanged"] += 1
            continue
        if r["source"] in kd_full and r["qtype"] == "noul":  # the teacher would be used alone: gold only
            n["kd_full_no_fresh_teacher"] += r["id"] in labels
            continue
        if r["id"] in labels:
            t = label_teacher(r, labels[r["id"]])
            m["teacher"], m["teacher_src"], m["teacher4b"] = t, teacher_src, dict(t)
            fresh.add(r["id"])
            n["fresh_teacher"] += 1
    comp = [(x["a"], x["b"]) for x in rels if x["type"] == "complement" and x["a"] in fresh and x["b"] in fresh]
    seen = Counter(i for p in comp for i in p)
    multi = [i for i, k in seen.items() if k > 1]
    if multi:
        raise ValueError(f"{len(multi)} row(s) in more than one complement pair with fresh teachers: {multi[:5]}")
    for a, b in comp:
        ra, rb = by_id[a], by_id[b]
        if ra["qtype"] != "noul" or rb["qtype"] != "noul" or ra["gold"] + rb["gold"] != 1:
            raise ValueError(f"complement pair {a}/{b} is not a yes/no pair with complementary golds")
        ta = (ra["meta"]["teacher"]["yes"] + 1.0 - rb["meta"]["teacher"]["yes"]) / 2
        ra["meta"]["teacher"] = {"yes": ta}
        rb["meta"]["teacher"] = {"yes": 1.0 - ta}
        n["complement_pairs_symmetrised"] += 1
    for x in rels:  # attacked twins last: they copy the partner's FINAL teacher
        if x["type"] != "inv":
            continue
        rb, ra = by_id.get(x["b"]), by_id.get(x["a"])
        if rb is None:
            continue
        m = rb["meta"]
        _drop_teacher(m)
        ta = kd_target(ra) if ra is not None else None
        if ta is None:
            n["twin_no_partner_teacher"] += 1
        elif rb["qtype"] != ra["qtype"] or (rb["qtype"] == "choice" and set(ta) != set(rb["options"])):
            n["twin_options_differ_deleted"] += 1
        elif not gives_gold(rb, ta):
            n["twin_partner_wrong_deleted"] += 1
        elif rb["source"] in kd_full and rb["qtype"] == "noul" and ra["meta"].get("teacher_src") == teacher_src:
            n["twin_kd_full_fresh_deleted"] += 1
        else:
            src = ra["meta"].get("teacher_src")
            m["teacher"] = dict(ta)
            m["teacher_src"] = f"{teacher_src}_clean_copy" if src == teacher_src else f"{src or 'human'}_clean_copy"
            n["twin_copied_" + ("fresh" if src == teacher_src else "human_or_exact")] += 1
    validate(out, skip)
    leak = [r["id"] for r in out if r["source"] in kd_full and r["qtype"] == "noul"
            and str(r["meta"].get("teacher_src") or "").startswith(teacher_src)]
    if leak:
        raise ValueError(f"{len(leak)} kd_full_src yes/no row(s) got a 4B teacher (used alone): {leak[:5]}")
    n["kd_targets"] = sum(kd_target(r) is not None for r in out)
    n["rows"] = len(out)
    return out, n


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--labels", required=True, help="label dir from od_gcp.py label (or one preds .jsonl)")
    ap.add_argument("--shards-dir", default="", help="checks every shard is done before reading the labels")
    ap.add_argument("--data-dir", default=str(sg.DATA))
    ap.add_argument("--golden", default="v14_parts/golden_train.jsonl")
    ap.add_argument("--relations", default="v14_parts/golden_relations.jsonl")
    ap.add_argument("--out", default="v14_parts/train_2b_golden_kd.jsonl", help="relative to --data-dir; a NEW file")
    ap.add_argument("--teacher-src", default="q35_4b_E")
    ap.add_argument("--kd-skip-src", default="blend50", help="comma list, as the 2B config's kd_skip_src")
    ap.add_argument("--kd-full-src", default="gd_gen2_probability", help="comma list, as the 2B config's kd_full_src")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--no-check-rows", dest="check_rows", action="store_false",
                    help="skip train_decoder.check_rows(rows, kd=0.5) on the result")
    a = ap.parse_args(argv)
    dd = Path(a.data_dir)
    golden, out = (dd / a.golden).resolve(), (dd / a.out).resolve()
    if out == golden:
        raise SystemExit("--out must be a new file, never the golden training file")
    if out.exists() and not a.overwrite:
        raise SystemExit(f"{out} exists; pass --overwrite")
    skip = tuple(s for s in a.kd_skip_src.split(",") if s)
    if any(a.teacher_src.startswith(s) for s in skip) or a.teacher_src in skip:
        raise SystemExit(f"--teacher-src {a.teacher_src!r} would match kd_skip_src {skip}")
    rows = sg.read_jsonl(golden)
    rels = sg.read_jsonl(dd / a.relations)
    lineage, _ = sg.lineage_keys(dd, warn=lambda s: print(s, file=sys.stderr))
    eligible = {r["id"] for r in sg.select_rows(rows, rels, lineage)[0]}
    labels = sg.load_labels(Path(a.labels), Path(a.shards_dir) if a.shards_dir else None)
    kd_full = tuple(s for s in a.kd_full_src.split(",") if s)
    new, n = build(rows, rels, labels, eligible, a.teacher_src, skip, kd_full)
    if a.check_rows:
        import train_decoder
        train_decoder.check_rows(new, 0.5)
    out.parent.mkdir(parents=True, exist_ok=True)
    sg.write_atomic(out, [json.dumps(r) for r in new])
    print(json.dumps({"out": str(out), **dict(sorted(n.items()))}, indent=1))
    print(f"kd targets: {n['kd_targets']}  (write this into expect_kd_targets)")
    return n


if __name__ == "__main__":
    main()
