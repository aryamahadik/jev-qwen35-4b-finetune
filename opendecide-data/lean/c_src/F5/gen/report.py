"""Balance, quota and coverage report on an output set (G0 section 8 targets; negcount-based 2.1 quotas, XF02).
Targets are checked on the final selected set after crowd selection; on the candidate pool they are reported so the
selection step knows what it starts from. Hard asserts here are the generator-side ones (k_syn quotas, k_all >= 2
>= 30%, no-polarity <= 4.5%, deep rows <= 10%, k_all >= k on every row).

  python -m gen.report --set candidates|qc|mixdev
"""
from __future__ import annotations

import argparse
import collections
import json

from .common import OUT, read_jsonl


def rate(xs):
    return round(sum(xs) / len(xs), 4) if xs else None


def bucket(n):
    return str(n) if n < 4 else "4+"


def report(rows, side, cards, name):
    sid = {s["id"]: s for s in side}
    R = {"set": name, "rows": len(rows)}
    S = [sid[r["id"]] for r in rows]
    gold = {r["id"]: r["gold"] for r in rows}
    R["bases"] = len({s["base_id"] for s in S})
    R["cards"] = len({r["meta"]["card_id"] for r in rows})
    R["packs"] = len({r["meta"]["domain_pack"] for r in rows})
    R["styles"] = len({r["meta"]["format_style"] for r in rows})
    R["wordings"] = len({r["meta"]["wording_id"] for r in rows})
    R["by_sampler_rows"] = dict(collections.Counter(r["meta"]["sampler"] for r in rows))
    bases_by_s = collections.defaultdict(set)
    for s in S:
        bases_by_s[s["sampler"] + (":inv" if s["inverted"] else "")].add(s["base_id"])
    R["by_sampler_bases"] = {k: len(v) for k, v in sorted(bases_by_s.items())}
    R["by_row_type"] = dict(collections.Counter(s["row_type"] for s in S))
    R["yes_rate"] = rate([r["gold"] for r in rows])

    def cell(keyf, minn=1):
        d = collections.defaultdict(list)
        for s in S:
            d[keyf(s)].append(gold[s["id"]])
        return {str(k): {"n": len(v), "yes": rate(v)} for k, v in sorted(d.items(), key=lambda x: str(x[0]))
                if len(v) >= minn}
    R["yes_by_row_type"] = cell(lambda s: s["row_type"])
    R["yes_by_k_neg"] = cell(lambda s: s["k_neg"])
    R["yes_by_k_all"] = cell(lambda s: bucket(s["k_all"]))
    R["yes_by_j_t"] = cell(lambda s: bucket(s["j_t"]))
    R["yes_by_t_txt"] = cell(lambda s: bucket(s["t_txt"]))
    R["yes_by_sampler"] = cell(lambda s: s["sampler"])
    R["yes_by_world"] = cell(lambda s: s["world_cell"])
    R["yes_by_wording"] = cell(lambda s: s["wording"])
    R["yes_by_location"] = cell(lambda s: s["location"])
    fam = collections.defaultdict(list)
    for s in S:
        for f in set(s["families"]):
            fam[f].append(gold[s["id"]])
    R["yes_by_family"] = {f: {"n": len(v), "yes": rate(v)} for f, v in sorted(fam.items())}
    R["yes_by_sem_key"] = {}
    sk = collections.defaultdict(list)
    for s in S:
        for k in s["sem_keys"]:
            sk[k].append(gold[s["id"]])
    R["yes_by_sem_key"] = {k: {"n": len(v), "yes": rate(v)} for k, v in sorted(sk.items())}
    # k mixes
    vrows = [s for s in S if s["row_type"] in ("V", "Vp")]
    R["k_mix_all"] = {str(k): round(v / len(S), 4) for k, v in sorted(collections.Counter(s["k_neg"] for s in S).items())}
    R["k_mix_V"] = {str(k): round(v / len(vrows), 4) for k, v in
                    sorted(collections.Counter(s["k_neg"] for s in vrows).items())} if vrows else {}
    # negcount quotas (XF02, SC8)
    R["share_k_syn_ge1"] = rate([s["k_syn"] >= 1 for s in S])
    R["share_k_syn_ge2_with_aff_twin"] = rate([s["k_syn"] >= 2 and s["row_type"] in ("D", "N", "V", "Vp") for s in S])
    R["share_k_all_ge2"] = rate([s["k_all"] >= 2 for s in S])
    R["k_all_ge_k_every_row"] = all(s["k_all"] >= s["k_neg"] for s in S)
    # polarity
    R["yes_is_bad_share"] = rate([bool(s["yes_is_bad"]) and gold[s["id"]] == 1 or False for s in S])
    R["yes_is_bad_rows_share"] = rate([s["yes_is_bad"] for s in S])
    R["no_polarity_share"] = rate([s["no_polarity"] for s in S])
    # twins, attacks, depth
    R["attack_share"] = rate([s["row_type"] == "Vp" for s in S])
    paired = [s for s in S if s["pair_id"] and s["row_type"] in ("A", "N", "D", "V")]
    R["contrast_set_share"] = round(len(paired) / len(S), 4)
    R["deep_share"] = rate([r["meta"]["deep"] for r in rows])
    dep = {}
    for s in S:
        dep[s["base_id"]] = s["base_depth"]
    R["depth_ge3_bases_share"] = rate([d >= 3 for d in dep.values()])
    R["depth_mix_bases"] = dict(collections.Counter(dep.values()))
    R["decoy_share"] = rate([bool(s.get("decoy")) for s in S])
    R["text_negation_share"] = rate([s["j_t"] > 0 for s in S])
    R["short_card_bases_share"] = rate([s["card_form"] == "short" for s in {x["base_id"]: x for x in S}.values()])
    R["framed_share_by_row_type"] = {t: rate([s["frame"] == "framed" for s in S if s["row_type"] == t])
                                     for t in ("A", "N", "D", "V")}
    R["two_lcore_bases_share"] = rate([s["two_lcore"] for s in {x["base_id"]: x for x in S}.values()])
    # cards
    cs = {c["card_id"]: c for c in cards}
    per = collections.defaultdict(list)
    for r in rows:
        per[r["meta"]["card_id"]].append(r["gold"])
    dev = []
    for cid, g in per.items():
        if cid in cs:
            dev.append(abs(sum(g) / len(g) - cs[cid]["r_card"]))
    R["per_card_rate_abs_dev_max"] = round(max(dev), 4) if dev else None
    R["per_card_rate_abs_dev_mean"] = round(sum(dev) / len(dev), 4) if dev else None
    R["rows_per_card"] = {"min": min(len(v) for v in per.values()), "max": max(len(v) for v in per.values()),
                          "median": sorted(len(v) for v in per.values())[len(per) // 2]}
    R["inverted_cards"] = sum(1 for c in cards if c["inverted"] and c["card_id"] in per)
    R["fewshot_cards"] = sum(1 for c in cards if c["fewshot"] and c["card_id"] in per)
    R["defs_styles_rows"] = dict(collections.Counter(r["meta"]["defs_style"] for r in rows))
    R["world_cells_bases"] = dict(collections.Counter(s["world_cell"] for s in {x["base_id"]: x for x in S}.values()))
    # surface templates (G11): question template x frame
    qt = collections.Counter(s["template"] for s in S)
    R["question_templates"] = len(qt)
    R["question_template_max_share_excl_frame"] = round(max(qt.values()) / len(S), 4)
    fq = collections.Counter((s.get("frame_id"), s["template"]) for s in S)
    R["frame_x_question_templates"] = len(fq)
    R["frame_x_question_template_max_share"] = round(max(fq.values()) / len(S), 4)
    R["frame_x_question_template_top"] = [[list(k), v] for k, v in fq.most_common(5)]
    R["frames_used"] = dict(collections.Counter(s.get("frame_id") for s in S))
    # verbatim-overlap control (F5-R2-20): rows with j_q >= 1 whose negated clause (the base clause under the
    # L_neg entry) also appears verbatim in the text
    ov, ovy, nq = 0, [], 0
    for r in rows:
        s = sid[r["id"]]
        if s["j_q"] < 1:
            continue
        nq += 1
        pc = s.get("p_clause")
        if pc and pc.lower() in r["state"].lower():
            ov += 1
            ovy.append(r["gold"])
    R["verbatim_overlap_share"] = round(ov / nq, 4) if nq else None
    R["verbatim_overlap_yes"] = rate(ovy)
    return R


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", required=True)
    a = ap.parse_args(argv)
    name = {"candidates": "candidates_r1", "qc": "qc_sample", "mixdev": "mixdev_S5"}.get(a.set, a.set)
    rows = read_jsonl(OUT / f"{name}.jsonl")
    side = read_jsonl(OUT / f"{name}.F5_polarity.jsonl")
    cards = read_jsonl(OUT / f"{name}.cards.jsonl")
    R = report(rows, side, cards, name)
    json.dump(R, open(OUT / f"{name}.report.json", "w"), indent=1)
    print(json.dumps(R, indent=1)[:6000])


if __name__ == "__main__":
    main()
