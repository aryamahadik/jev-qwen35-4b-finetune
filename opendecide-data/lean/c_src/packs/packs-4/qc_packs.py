#!/usr/bin/env python3
"""packs-4 QC report (counts only; no pack text is printed). Reads packs.jsonl, writes tmp/qc_report.json.

Checks: theme and O*NET major-group spread; sub-object counts; duplicate person names across packs; inert facts that
name any decision word of their own pack (fix round 1: the same whole-word check as the build_packs.py lint, with
simple inflections, over statuses, outcomes, risk events, Boolean names and aliases, category field names and values,
taxonomy dimension names and values, quantity names, jargon terms and predicate phrases; F4/F7/F11 disjointness);
max ROUGE-L between setting texts, jargon definitions, unit definitions and inert facts (all pairs, both word splits;
G11 < 0.7); split hints.
"""
import collections
import json
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys  # noqa: E402
sys.path.insert(0, str(HERE))
import build_packs as B  # noqa: E402


def words(s):
    return re.findall(r"[a-z]+(?:-[a-z]+)*", s.lower())


def lcs(a, b):
    if len(a) < len(b):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def rouge(a, b):
    ta, tb = words(a), words(b)
    l_ = lcs(ta, tb) if ta and tb else 0
    if not l_:
        return 0.0
    p, r = l_ / len(tb), l_ / len(ta)
    return 2 * p * r / (p + r)


def main():
    packs = [json.loads(l) for l in (HERE / "packs.jsonl").read_text().splitlines() if l.strip()]
    rep = {"packs": len(packs), "themes": collections.Counter(p["theme"] for p in packs),
           "major_groups": len({p["persona"]["major_group"] for p in packs}),
           "split_hint": collections.Counter(p["split_hint"] for p in packs)}
    secs = ["roles", "entity_types", "items", "documents", "units", "quantities", "bool_fields", "cat_fields",
            "statuses", "outcomes", "predicates", "links", "actions", "risk_events", "taxonomy_dims", "jargon",
            "neg_affix_pairs", "inert_facts"]
    rep["per_pack_counts"] = {s: {"min": min(len(p[s]) for p in packs), "median": statistics.median(len(p[s]) for p in packs),
                                  "total": sum(len(p[s]) for p in packs)} for s in secs}
    rep["per_pack_counts"]["people"] = {"min": min(len(p["names"]["people"]) for p in packs),
                                        "total": sum(len(p["names"]["people"]) for p in packs)}
    ids = []
    for p in packs:
        def walk(o):
            if isinstance(o, dict):
                if "id" in o:
                    ids.append(o["id"])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(p)
    rep["objects_with_id"] = len(ids)
    rep["duplicate_ids"] = len(ids) - len(set(ids))
    names = collections.Counter(n["name"].lower() for p in packs for n in p["names"]["people"])
    rep["person_names_in_2plus_packs"] = sum(1 for v in names.values() if v > 1)
    inert_hits, kinds = 0, collections.Counter()
    for p in packs:
        vocab = B.decision_vocab(p)
        for f in p["inert_facts"]:
            h = B.inert_vocab_hits(f["text"], vocab)
            inert_hits += bool(h)
            kinds.update(k for k, _ in h)
    rep["inert_facts_reusing_own_vocab"] = inert_hits
    rep["inert_vocab_hit_kinds"] = dict(kinds)
    rep["inert_vocab_check"] = "build_packs.inert_vocab_hits (whole words + simple inflections; fix round 1)"
    best = 0.0
    for i in range(len(packs)):
        for j in range(i + 1, len(packs)):
            best = max(best, rouge(packs[i]["setting"], packs[j]["setting"]))
    rep["max_rouge_l_setting"] = round(best, 3)
    defs = [(p["id"], j["definition"]) for p in packs for j in p["jargon"]]
    best = 0.0
    for i in range(len(defs)):
        for j in range(i + 1, len(defs)):
            if defs[i][0] != defs[j][0]:
                best = max(best, rouge(defs[i][1], defs[j][1]))
    rep["max_rouge_l_jargon_definition_cross_pack"] = round(best, 3)
    for name, items in (("inert_fact", [(f["id"], f["text"]) for p in packs for f in p["inert_facts"]]),
                        ("unit_definition", [(u["id"], u["definition"]) for p in packs for u in p["units"]]),
                        ("jargon_definition", [(j["id"], j["definition"]) for p in packs for j in p["jargon"]])):
        pairs = B.g11_pairs(items, (B.words_of, B.toks_review), thr=0.0)
        rep[f"max_rouge_l_{name}_all_pairs"] = max((s for _, _, s in pairs), default=0.0)
        rep[f"{name}_pairs_rouge_l_ge_0.7"] = sum(1 for _, _, s in pairs if s >= 0.7)
    (HERE / "tmp" / "qc_report.json").write_text(json.dumps(rep, indent=1) + "\n")
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
