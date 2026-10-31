"""Coverage and balance statistics over F2 rows, computed from meta and edge alone (3.8: QC computes every section 6
target from meta and edge)."""
from __future__ import annotations

from collections import Counter, defaultdict


def _tags(r):
    return set(r["meta"]["edge"])


def _tag(r, p):
    for t in r["meta"]["edge"]:
        if t.startswith(p):
            return t[len(p):]
    return None


def schema_of(r):
    return r["meta"]["card_id"].split(".")[-2]


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def stats(rows, rels=()):
    n = len(rows)
    S = {"rows": n}
    S["by_sampler"] = dict(Counter(r["meta"]["sampler"] for r in rows))
    S["by_schema"] = dict(Counter(schema_of(r) for r in rows))
    S["by_twin_kind"] = dict(Counter(r["meta"]["twin_kind"] or "base" for r in rows))
    S["relations"] = dict(Counter(x["type"] for x in rels))
    S["cards"] = len({r["meta"]["card_id"] for r in rows})
    S["packs"] = len({r["meta"]["domain_pack"] for r in rows})
    S["format_styles"] = len({r["meta"]["format_style"] for r in rows})
    S["wordings"] = len({r["meta"]["wording_id"] for r in rows})
    S["defs_styles"] = dict(Counter(r["meta"]["defs_style"] for r in rows))
    per_card_w = defaultdict(set)
    per_card_rows = Counter()
    for r in rows:
        per_card_w[r["meta"]["card_id"]].add(r["meta"]["wording_id"])
        per_card_rows[r["meta"]["card_id"]] += 1
    S["wordings_per_card_min"] = min((len(v) for v in per_card_w.values()), default=0)
    S["rows_per_card_max"] = max(per_card_rows.values(), default=0)
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    S["yes_no_share"] = round(len(yn) / n, 4) if n else None
    if yn:
        S["yes_rate"] = round(sum(r["gold"] for r in yn) / len(yn), 4)
        aff = [r for r in yn if _tag(r, "neg:") == "0"]
        S["tf_share_affirmative"] = round(sum(1 for r in aff if _tag(r, "tf:") == "1") / max(1, len(aff)), 4)
        S["k_syn_ge1_share"] = round(sum(1 for r in yn if int(_tag(r, "syn:")) >= 1) / len(yn), 4)
        S["k_syn_ge2_share"] = round(sum(1 for r in yn if int(_tag(r, "syn:")) >= 2) / len(yn), 4)
        pol = [_tag(r, "pol:") for r in yn if _tag(r, "pol:")]
        S["bad_yes_share"] = round(sum(1 for p in pol if p == "bad_yes") / max(1, len(pol)), 4)
        cells = defaultdict(lambda: [0, 0])
        for r in yn:
            key = (r["meta"]["wording_id"], _tag(r, "cue:"))
            cells[key][0] += r["gold"]
            cells[key][1] += 1
        S["yes_rate_by_cue"] = {c: round(sum(v[0] for k, v in cells.items() if k[1] == c) /
                                         max(1, sum(v[1] for k, v in cells.items() if k[1] == c)), 4)
                                for c in sorted({k[1] for k in cells})}
        cmpf = Counter(_tag(r, "cmp:") for r in yn)
        S["cmp_family"] = dict(cmpf)
        for fam in ("incl", "excl"):
            rs = [r for r in yn if _tag(r, "cmp:") == fam]
            if rs:
                S[f"yes_given_{fam}"] = round(sum(r["gold"] for r in rs) / len(rs), 4)
        S["boundary_zone_share"] = round(sum(1 for r in yn if _tag(r, "boundary:") in ("at", "below1", "above1")) /
                                         len(yn), 4)
    if ch:
        ks = [len(r["options"]) for r in ch]
        S["option_buckets"] = {b: round(c / len(ch), 4) for b, c in Counter(bucket(k) for k in ks).items()}
        ab = defaultdict(lambda: [0, 0, 0.0])
        for r in ch:
            ab_kind = _tag(r, "abst:")
            if ab_kind:
                b = bucket(len(r["options"]))
                gold_ab = r["gold"].startswith("None of the listed") or r["gold"] in ("Cannot be determined",
                                                                                       "Not enough information",
                                                                                       "Cannot tell from the record")
                ab[(ab_kind, b)][0] += int(gold_ab)
                ab[(ab_kind, b)][1] += 1
                ab[(ab_kind, b)][2] += 1.0 / len(r["options"])
        S["abstain_gold_vs_1_over_k"] = {f"{k[0]}:{k[1]}": {"n": v[1], "gold_rate": round(v[0] / v[1], 4),
                                                            "mean_1_over_k": round(v[2] / v[1], 4)}
                                         for k, v in ab.items()}
        S["named_options"] = dict(Counter(_tag(r, "named:") for r in ch if _tag(r, "named:")))
    S["depth_groups"] = dict(Counter(("c" if "stated_intermediate" in _tags(r) else
                                      "d" if r["meta"]["deep"] else
                                      ("a" if r["meta"]["depth"] == 1 else "b")) for r in rows))
    adj = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        t = _tags(r)
        for x in ("cap", "floor", "exc", "round", "partial", "roll", "hol", "ext", "clamp"):
            if f"has:{x}" in t:
                adj[x][0] += 1
                adj[x][1] += int(f"bind:{x}" in t)
                adj[x][2] += int(f"dec:{x}" in t)
    S["adjustments"] = {x: {"has": v[0], "bind_rate": round(v[1] / v[0], 3), "dec_rate": round(v[2] / v[0], 3)}
                        for x, v in adj.items() if v[0]}
    S["money_format"] = dict(Counter(_tag(r, "money:") for r in rows if _tag(r, "money:")))
    S["b1_forms"] = dict(Counter(_tag(r, "b1:") for r in rows if _tag(r, "b1:")))
    S["world"] = dict(Counter(_tag(r, "world:") for r in rows))
    S["sem_decisive_rows_share"] = round(sum(1 for r in rows if any(t.startswith("sem:") for t in r["meta"]["edge"])) /
                                         max(1, n), 4)
    S["noop_fact_share"] = round(sum(1 for r in rows if "noop:1" in _tags(r)) / max(1, n), 4)
    flip_sets = set()
    for r in rows:
        if r["meta"]["twin_kind"] in ("boundary", "clause_flip", "premise_removed"):
            flip_sets.add(r["meta"]["twin_of"])
    in_sets = sum(1 for r in rows if (r["meta"]["twin_kind"] in ("boundary", "clause_flip", "premise_removed")) or
                  (r["meta"]["twin_kind"] is None and r["id"] in flip_sets))
    S["label_flip_twin_set_share"] = round(in_sets / max(1, n), 4)
    S["attack_twin_share"] = round(sum(1 for r in rows if r["meta"]["twin_kind"] == "attack") / max(1, n), 4)
    S["inert_twin_share"] = round(sum(1 for r in rows if r["meta"]["twin_kind"] == "inert") / max(1, n), 4)
    toks = sorted(r["meta"].get("tokens", 0) for r in rows)
    if toks:
        S["tokens"] = {"median": toks[len(toks) // 2], "max": toks[-1], "ge_1900": sum(1 for t in toks if t >= 1900)}
    S["structure_hashes_distinct_bases"] = len({r["meta"]["structure_hash"] for r in rows if not r["meta"]["twin_kind"]})
    return S
