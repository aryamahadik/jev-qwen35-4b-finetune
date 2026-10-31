"""Assemble F6 outputs from the build files and run the generator-side gates.

  python -m gen.finalize <set> <build_tag>      set in {cand, qc, dev}

Gates (counts only): G1 meta keys; G3 (recorded per row by the build: parse + canonical compare + solver B); G15
(train_decoder.check_rows on every row, fmt1 loader_check again under a second random permutation, unit sizes,
real-tokenizer lengths with `instructions` counted twice); G18 (no ordinal rows); negcount quotas (k_syn / k_all,
XF02); held-out guard (fmt1.pool.refuse_held_out on training sets). Output rows never carry QC-only keys (s8).
"""
from __future__ import annotations

import json
import random
import re
import statistics
import sys
from collections import Counter, defaultdict

from . import common as C
from .common import OUT, TMP, read_jsonl, write_jsonl, sha256_file, progress
from fmt1 import card as fcard, pool as fpool

NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
META_REQ = {"family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed",
            "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id",
            "defs_style", "twin_of", "twin_kind", "text_source", "licence", "edge"}
META_OPT = {"persona_seed", "subtype"}
TOP = ["id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role", "card",
       "meta"]


def question_of(row: dict) -> str:
    from . import parse_f6 as PF, styles_f6 as ST
    W = {w["text"] for w in ST.wording_pool()}
    st = fpool.style(row["meta"]["format_style"])
    _, _, q = PF.split_instructions(row["instructions"], st, W)
    return q


def claim_of(q: str):
    from .lex import FRAMES
    from .parse_f6 import _tpl_rx
    for k in ("qdet_dneg", "qdet_leave", "qdet_imp", "qdet", "qest_est", "qest_show", "qest_det", "qplain_true"):
        m = _tpl_rx(FRAMES[k]).match(q)
        if m:
            return k, m.group("S")
    return "inversion", q


def main():
    set_name, tag = sys.argv[1], sys.argv[2]
    rows = read_jsonl(TMP / f"build_{tag}_rows.jsonl")
    sides = read_jsonl(TMP / f"build_{tag}_side.jsonl")
    rels = read_jsonl(TMP / f"build_{tag}_rels.jsonl")
    fails = read_jsonl(TMP / f"build_{tag}_fail.jsonl")
    sys.path.insert(0, str(C.COMMON))
    import negcount
    from . import toklen
    td = fcard._td()           # the pinned A16 trainer (fmt1 refuses any other version)
    rep = {"set": set_name, "rows": len(rows)}
    # ---- G1 meta keys
    bad_meta = 0
    for r in rows:
        if list(r.keys()) != TOP:
            bad_meta += 1
            continue
        mk = set(r["meta"])
        if not META_REQ <= mk or mk - META_REQ - META_OPT:
            bad_meta += 1
    rep["G1_meta_bad"] = bad_meta
    # ---- G15
    td.check_rows(rows)
    rep["G15_check_rows"] = "pass"
    lf = 0
    for r in rows:
        rng = random.Random(f"g15b:{r['id']}")
        n = len(r["options"]) if r["qtype"] == "choice" else 2
        perm = list(range(n))
        rng.shuffle(perm)
        res = fcard.loader_check(r, perm=perm, check_rows=False)
        lf += not res["ok"]
    rep["G15_loader_fail_second_perm"] = lf
    units = defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r)
    sizes = Counter(len(u) for u in units.values())
    rep["G15_unit_sizes"] = dict(sizes)
    rep["G15_units_over_3"] = sum(v for k, v in sizes.items() if k > 3)
    side_by = {s["id"]: s for s in sides}
    toks = [side_by[r["id"]]["tokens"] for r in rows]
    ptoks = [side_by[r["id"]]["prompt_tokens"] for r in rows]
    rep["tokens_fields_x2instr"] = {"median": statistics.median(toks), "max": max(toks), "min": min(toks),
                                    "over_1900": sum(t > 1900 for t in toks), "over_7900": sum(t > 7900 for t in toks),
                                    "share_500_900": round(sum(500 <= t <= 900 for t in toks) / len(toks), 3)}
    rep["tokens_full_prompt"] = {"median": statistics.median(ptoks), "max": max(ptoks)}
    rep["units_with_row_ge_2000_tokens"] = sum(1 for u in units.values()
                                               if any(side_by[x["id"]]["tokens"] >= 2000 for x in u))
    # ---- G3 (from the build) and G18
    rep["G3_fail"] = sum(1 for s in sides if s.get("g3"))
    rep["G3_bug_units_not_emitted"] = sum(1 for f in fails if f.get("g3_bug"))
    rep["G18_ordinal_rows"] = sum(1 for r in rows if (r["meta"].get("option_level") is not None) or
                                  any(re.search(r"\b(level|tier|grade|band)\s*\d", o, re.I)
                                      for o in (r["options"] or [])))
    # ---- negcount (XF02)
    yn = [r for r in rows if r["qtype"] == "noul"]
    ks, ka = {}, {}
    for r in yn:
        q = question_of(r)
        c = negcount.count(q)
        fr, S = claim_of(q)
        cs = negcount.count(S)
        side_by[r["id"]].update({"k_syn": c.k_syn, "k_all": c.k_all, "k_syn_S": cs.k_syn, "k_all_S": cs.k_all,
                                 "k_syn_frame": c.k_syn - cs.k_syn, "k_all_frame": c.k_all - cs.k_all,
                                 "question_frame": fr})
        ks[r["id"]], ka[r["id"]] = c.k_syn, c.k_all
    n_yn = len(yn)
    rel_by = defaultdict(list)
    for x in rels:
        rel_by[x["b"]].append(x)
    gold = {r["id"]: r["gold"] for r in rows}
    dneg = 0
    for r in yn:
        if ks[r["id"]] >= 2:
            for x in rel_by[r["id"]]:
                if x["type"] == "equiv" and ks.get(x["a"]) == 0 and gold.get(x["a"]) == r["gold"]:
                    dneg += 1
                    break
    rep["negation"] = {"yes_no_rows": n_yn, "k_syn_ge1": sum(1 for v in ks.values() if v >= 1),
                       "k_syn_ge1_share": round(sum(1 for v in ks.values() if v >= 1) / max(1, n_yn), 4),
                       "dneg_with_affirmative_twin": dneg, "dneg_share": round(dneg / max(1, n_yn), 4),
                       "k_all_hist": dict(Counter(ka.values()))}
    # ---- balance snapshot (candidate pool; selection re-balances per G9/G10)
    rep["yes_rate"] = round(sum(r["gold"] for r in yn) / max(1, n_yn), 4)
    by_form = Counter((r["meta"]["sampler"], r["meta"]["subtype"]) for r in rows)
    rep["sampler_x_form"] = {f"{a}|{b}": v for (a, b), v in sorted(by_form.items())}
    rep["gold_class"] = {f"{a}|{b}": v for (a, b), v in Counter((s["form"], s["gold_class"]) for s in sides).most_common()}
    rep["k_hist_choice"] = dict(sorted(Counter(len(r["options"]) for r in rows if r["qtype"] == "choice").items()))
    rep["twins"] = dict(Counter(r["meta"]["twin_kind"] for r in rows if r["meta"]["twin_kind"]))
    in_sets = {r["group_id"] for r in rows if r["meta"]["twin_kind"] in ("premise", "world", "unit", "evidence")}
    rep["rows_in_contrast_sets"] = sum(1 for r in rows if r["group_id"] in in_sets)
    rep["rows_in_contrast_sets_share"] = round(rep["rows_in_contrast_sets"] / max(1, len(rows)), 4)
    rep["relations"] = dict(Counter(x["type"] for x in rels))
    rep["cards"] = len({r["meta"]["card_id"] for r in rows})
    rep["packs"] = len({r["meta"]["domain_pack"] for r in rows})
    rep["rows_per_card_max"] = max(Counter(r["meta"]["card_id"] for r in rows).values())
    rep["styles"] = len({r["meta"]["format_style"] for r in rows})
    rep["wordings"] = len({r["meta"]["wording_id"] for r in rows})
    rep["defs_styles"] = dict(Counter(r["meta"]["defs_style"] for r in rows))
    rep["edges"] = dict(Counter(e for r in rows for e in r["meta"]["edge"]))
    rep["depth"] = dict(Counter(r["meta"]["depth"] for r in rows))
    rep["frames"] = dict(Counter(side_by[r["id"]].get("frame_id") for r in rows))
    rep["n_gaps"] = dict(Counter(side_by[r["id"]].get("n_gaps") for r in rows))
    rep["label_forms"] = dict(Counter(side_by[r["id"]].get("label_form") for r in rows if r["qtype"] == "choice"))
    rep["build_failures"] = len(fails)
    fy = defaultdict(list)
    for r in yn:
        fy[side_by[r["id"]].get("frame_id")].append(r["gold"])
    rep["yes_rate_per_frame"] = {k: [len(v), round(sum(v) / len(v), 3)] for k, v in sorted(fy.items())}
    ch = [r for r in rows if r["qtype"] == "choice" and side_by[r["id"]]["form"] in ("c_out", "c_rec")]
    rep["abstain_gold_share_c_out_c_rec"] = dict(Counter(side_by[r["id"]]["gold_class"] for r in ch))
    rep["valence_yes_no"] = dict(Counter(str(side_by[r["id"]].get("valence")) for r in yn))
    tk = defaultdict(list)
    for r in rows:
        tk[f"{r['meta']['sampler']}|{r['meta']['subtype']}"].append(side_by[r["id"]]["tokens"])
    rep["tokens_median_by_cell"] = {k: statistics.median(v) for k, v in sorted(tk.items())}
    rep["relaxed_specs"] = sum(1 for s in sides if (s.get("spec") or {}).get("relaxed"))
    # G15: 20 rendered prompts per family for reading
    from fmt1 import card as _fc
    dio = _fc._dio()
    pick = []
    seen = Counter()
    for r in rows:
        k = (r["meta"]["sampler"], r["meta"]["subtype"])
        if seen[k] < 2 and len(pick) < 20:
            seen[k] += 1
            pick.append(r)
    with open(TMP / f"g15_prompts_{set_name}.txt", "w") as f:
        for r in pick:
            n = len(r["options"]) if r["qtype"] == "choice" else 2
            with _fc._serving(dio, n):
                f.write(f"===== {r['id']} gold={r['gold']}\n" + dio.user_msg(r, None) + "\n\n")
    # ---- held-out guard
    if set_name != "dev":
        out = fpool.refuse_held_out(rows, strict_unknown=True)
        rep["held_out_guard"] = out
    else:
        rep["dev_styles_held_out"] = all(fpool.style(r["meta"]["format_style"])["held_out"] for r in rows)
        rep["dev_sampler_S5"] = all(r["meta"]["sampler"] == "S5" for r in rows)
    # ---- write
    OUT.mkdir(exist_ok=True)
    base = NAMES[set_name]
    write_jsonl(OUT / f"{base}.jsonl", rows)
    write_jsonl(OUT / f"{base}.relations.jsonl", rels)
    slim = []
    for s in sides:
        s2 = {k: v for k, v in s.items() if k not in ("struct",)}
        slim.append(s2)
    write_jsonl(OUT / f"{base}.qc_side.jsonl", slim)
    write_jsonl(TMP / f"{base}.struct.jsonl", [{"id": s["id"], "kind": s["kind"], "form": s["form"],
                                                "struct": s["struct"]} for s in sides])
    rep["files"] = {f"{base}.jsonl": sha256_file(OUT / f"{base}.jsonl"),
                    f"{base}.relations.jsonl": sha256_file(OUT / f"{base}.relations.jsonl"),
                    f"{base}.qc_side.jsonl": sha256_file(OUT / f"{base}.qc_side.jsonl")}
    json.dump(rep, open(TMP / f"report_{set_name}.json", "w"), indent=1, default=str)
    progress(f"finalize {set_name}: rows {len(rows)}, G1 bad {bad_meta}, G3 fail {rep['G3_fail']}, G15 loader fail "
             f"{lf}, tokens max {rep['tokens_fields_x2instr']['max']}, k_syn>=1 {rep['negation']['k_syn_ge1_share']}, "
             f"dneg {rep['negation']['dneg_share']}")
    print(json.dumps(rep, indent=1, default=str)[:4000])


if __name__ == "__main__":
    main()
