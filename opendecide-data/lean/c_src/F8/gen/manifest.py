"""out/MANIFEST.json: counts, sha256, sampler / pack / style / form coverage, balance figures, gate results, problems.
Prints counts only (never row text)."""
from __future__ import annotations

import collections
import json
import statistics
import sys

import cards as CP
import common as CM
import packs_f8

FILES = {"candidates_r1": "train", "qc_sample": "train", "mixdev_S5": "dev"}


def _share(n, d):
    return round(100 * n / d, 2) if d else None


def describe(name: str) -> dict:
    rows = CM.read_jsonl(CM.OUT / f"{name}.jsonl")
    side = {x["id"]: x for x in CM.read_jsonl(CM.OUT / f"f8_controls_{name}.jsonl")}
    rels = CM.read_jsonl(CM.OUT / f"relations_{name}.jsonl")
    n = len(rows)
    C = collections.Counter
    m = [r["meta"] for r in rows]
    sd = [side[r["id"]] for r in rows]
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    per_card = C(x["card_id"] for x in m)
    out = {
        "rows": n, "sha256": CM.sha256_file(CM.OUT / f"{name}.jsonl"),
        "sidecar_sha256": CM.sha256_file(CM.OUT / f"f8_controls_{name}.jsonl"),
        "relations": len(rels), "relations_sha256": CM.sha256_file(CM.OUT / f"relations_{name}.jsonl"),
        "relation_types": dict(C(x["type"] for x in rels)),
        "cards": len(per_card), "rows_per_card": {"median": statistics.median(per_card.values()) if per_card else None,
                                                  "max": max(per_card.values()) if per_card else None,
                                                  "min": min(per_card.values()) if per_card else None},
        "card_size_rows": dict(C(x["card_size"] for x in sd)),
        "samplers": dict(sorted(C(x["sampler"] for x in m).items())),
        "packs": len({x["domain_pack"] for x in m}),
        "persona_seeded_rows": sum(1 for x in m if x.get("persona_seed")),
        "format_styles": len({x["format_style"] for x in m}),
        "containers": dict(C(__import__("fmt1.pool", fromlist=["pool"]).style(x["format_style"])["container"]
                             for x in m)),
        "wordings": len({x["wording_id"] for x in m}),
        "forms": dict(sorted(C(x["qform"] for x in sd).items())),
        "subtypes": dict(sorted(C(x["subtype"] for x in m).items())),
        "yn_share": _share(len(yn), n),
        "card_version": dict(C(x["card_version"] for x in sd)),
        "defs_style": dict(C(x["defs_style"] for x in m)),
        "world": dict(C(x["world"] for x in sd)),
        "twin_kind": dict(C(x["twin_kind"] for x in m)),
        "rows_in_flip_sets": sum(1 for r in rows if r["meta"]["twin_kind"] == "flip") * 2,
        "deep_share": _share(sum(1 for x in m if x["deep"]), n),
        "depth": dict(sorted(C(x["depth"] for x in m).items())),
        "edge_nonempty_share": _share(sum(1 for x in m if any(e.startswith("F8/") for e in x["edge"])), n),
        "masked_choice_share": _share(sum(1 for r, x in zip(rows, sd) if r["qtype"] == "choice" and
                                          x["masked"] == "masked"), len(ch)),
        "swapped_choice_share": _share(sum(1 for r, x in zip(rows, sd) if r["qtype"] == "choice" and
                                           x["masked"] == "swapped"), len(ch)),
        "max_tokens": max((x["ntok"] for x in sd), default=0),
        "median_tokens": statistics.median([x["ntok"] for x in sd]) if sd else None,
    }
    # yes / no balance (YN rows)
    if yn:
        g = [r["gold"] for r in yn]
        out["yes_rate"] = _share(sum(g), len(g))
        yb = [side[r["id"]]["yes_is_bad"] for r in yn]
        out["yes_is_bad_true_share"] = _share(sum(1 for x in yb if x is True), len(yb))
        out["yes_is_bad_null_share"] = _share(sum(1 for x in yb if x is None), len(yb))
        ks = [side[r["id"]]["k_syn"] for r in yn]
        out["k_syn>=1_share_of_yn"] = _share(sum(1 for k in ks if k >= 1), len(ks))
        aff_calls = {r["call_id"] for r in yn if side[r["id"]]["k_syn"] == 0}
        out["k_syn>=2_with_affirmative_share_of_yn"] = _share(
            sum(1 for r in yn if side[r["id"]]["k_syn"] >= 2 and r["call_id"] in aff_calls), len(ks))
        out["k_all_cells"] = dict(sorted(C(side[r["id"]]["k_all"] for r in yn).items()))
        out["yes_rate_by_k_all"] = {k: _share(sum(r["gold"] for r in yn if side[r["id"]]["k_all"] == k),
                                              sum(1 for r in yn if side[r["id"]]["k_all"] == k))
                                    for k in sorted({side[r["id"]]["k_all"] for r in yn})}
        thr = [r for r in yn if side[r["id"]]["yn_kind"] == "threshold"]
        out["threshold_yn_rows"] = len(thr)
        out["placement"] = dict(C(side[r["id"]]["placement"] for r in thr))
        out["comparator"] = dict(C(side[r["id"]]["comparator"] for r in thr))
        out["direction"] = dict(C(side[r["id"]]["direction"] for r in thr))
        out["yes_rate_by_placement"] = {p: _share(sum(r["gold"] for r in thr if side[r["id"]]["placement"] == p),
                                                  sum(1 for r in thr if side[r["id"]]["placement"] == p))
                                        for p in sorted({side[r["id"]]["placement"] for r in thr if
                                                         side[r["id"]]["placement"]})}
    if ch:
        def bucket(k):
            return "2-4" if k <= 4 else ("5-9" if k <= 9 else ("10-19" if k <= 19 else "20-60"))
        out["option_buckets"] = dict(C(bucket(len(r["options"])) for r in ch))
        out["gold_position_by_bucket"] = {}
        for b in ("2-4", "5-9", "10-19", "20-60"):
            pos = [r["options"].index(r["gold"]) / max(1, len(r["options"]) - 1) for r in ch
                   if bucket(len(r["options"])) == b]
            if pos:
                out["gold_position_by_bucket"][b] = round(statistics.mean(pos), 3)
        ab = [r for r in ch if any(o in ("Cannot be determined from the information given", "None of these")
                                   for o in r["options"])]
        out["abstain_shown_rows"] = len(ab)
        out["abstain_gold_share_where_shown"] = _share(sum(1 for r in ab if r["gold"] in (
            "Cannot be determined from the information given", "None of these")), len(ab))
        out["mean_1_over_n_where_shown"] = round(100 * statistics.mean(1 / len(r["options"]) for r in ab), 2) \
            if ab else None
        out["subset_class"] = dict(C(side[r["id"]]["subset_class"] for r in ch if side[r["id"]]["subset_class"]))
        tiers = [r for r in ch if side[r["id"]]["qform"] == "TIER"]
        out["tier_step"] = dict(C(side[r["id"]]["tier_step"] for r in tiers))
        out["distractor_rows"] = sum(1 for r in ch if side[r["id"]]["distractor_errors"])
    return out


def main():
    ps = packs_f8.load()
    man = {"family": "F8", "spec": {"path": "c_src/F8/G0_SPEC.md", "sha256": CM.sha256_file(CM.SPEC),
                                     "frozen_sha256": CM.SPEC_SHA256},
           "gen_version": CM.GEN_VERSION, "generated_utc": CM.now(),
           "inputs": {"formats-1 MANIFEST": CM.sha256_file(CM.FMT1 / "MANIFEST.json"),
                      "formats-2 family_pools": CM.sha256_file(CM.FMT2 / "wordings" / "family_pools.jsonl"),
                      "packs-3": CM.sha256_file(CM.PACKS / "packs-3" / "packs-3.jsonl"),
                      "packs-4": CM.sha256_file(CM.PACKS / "packs-4" / "packs.jsonl"),
                      "negcount.py": CM.sha256_file(CM.COMMON / "negcount.py"),
                      "markers.json": CM.sha256_file(CM.COMMON / "markers.json"),
                      "decoder_io.py": CM.sha256_file(CM.LEAN / "decoder_io.py"),
                      "train_decoder.py": CM.sha256_file(CM.LEAN / "train_decoder.py")},
           "code_sha256": {p.name: CM.sha256_file(p) for p in sorted(CM.GEN.glob("*.py"))},
           "data_sha256": {p.name: CM.sha256_file(p) for p in sorted((CM.GEN / "data").glob("*.json"))},
           "packs_available": {"train": sum(1 for p in ps if p["split"] == "train"),
                               "heldout_S5": sum(1 for p in ps if p["split"] == "heldout")},
           "files": {}}
    # 3.H.1 / G1 parents (mixer note 6 Oct): every pack set, wording set, format pool and real-text parent rows derive
    # from. F8 has no public or real-outcome data parent; O*NET titles enter only as pack persona seeds (2.1 F4).
    man["parents"] = ["gd_onet_occupation (persona seeds via packs; main occupation titles only)",
                      "c_src/packs/packs-3 (Claude-written domain packs)",
                      "c_src/packs/packs-4 (Claude-written domain packs)",
                      "c_src/formats/formats-1 (format styles, card styles, masked label ids, few-shot templates)",
                      "c_src/formats/formats-2/wordings/family_pools.jsonl (instruction wordings)",
                      "c_src/F8/gen/data/lexicon.json and facts.json (Claude-written F8 lexicon)"]
    for name in FILES:
        if (CM.OUT / f"{name}.jsonl").exists():
            man["files"][name] = describe(name)
    extra = CM.TMP / "gates.json"
    if extra.exists():
        man["gates"] = json.load(open(extra))
    probs = CM.TMP / "problems.json"
    if probs.exists():
        man["problems"] = json.load(open(probs))
    with open(CM.OUT / "MANIFEST.json", "w") as f:
        json.dump(man, f, indent=1, sort_keys=False)
    print(json.dumps({k: {kk: v[kk] for kk in ("rows", "cards", "packs", "format_styles")}
                      for k, v in man["files"].items()}))


if __name__ == "__main__":
    main()
