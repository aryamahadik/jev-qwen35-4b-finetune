"""F7 builder gates on an output file: G15 (train_decoder.check_rows, loader_check incl. gold-letter mapping under a
random permutation, units, real-tokenizer length with instructions counted twice), G18 ordinal target lint, G10 /
6.x balance and quota statistics, negcount-based checks (6.3), exact-duplicate check (G12). Prints / writes counts
only (no row text).

  python f7gates.py <rows.jsonl> [--relations <rel.jsonl>] [--out report.json] [--no-loader]
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import hashlib
import json
import math
import os
import random
import statistics
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
LEAN = HERE.parents[2]
sys.path.insert(0, str(LEAN / "c_src/formats/formats-1"))
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "c_src/common"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")

from fmt1 import card as fcard  # noqa: E402
from fmt1 import pool as fpool  # noqa: E402

import negcount  # noqa: E402


def chi2_uniform(counts: list[int]) -> float:
    """p-value of a chi-square goodness-of-fit test against the uniform distribution."""
    n = sum(counts)
    k = len(counts)
    if n == 0 or k < 2:
        return 1.0
    e = n / k
    x = sum((c - e) ** 2 / e for c in counts)
    return _chi2_sf(x, k - 1)


def _chi2_sf(x: float, df: int) -> float:
    # regularized upper incomplete gamma Q(df/2, x/2)
    a, xx = df / 2.0, x / 2.0
    if xx <= 0:
        return 1.0
    if xx < a + 1:
        s, term, n = 1.0 / a, 1.0 / a, 0
        while n < 500:
            n += 1
            term *= xx / (a + n)
            s += term
            if abs(term) < abs(s) * 1e-12:
                break
        return max(0.0, 1.0 - s * math.exp(-xx + a * math.log(xx) - math.lgamma(a)))
    b = xx + 1 - a
    c, d = 1e300, 1 / b
    h = d
    for i in range(1, 500):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1 / d
        de = d * c
        h *= de
        if abs(de - 1) < 1e-12:
            break
    return h * math.exp(-xx + a * math.log(xx) - math.lgamma(a))


def chi2_indep(table: dict) -> float:
    """p-value of a chi-square independence test on {(row, col): n}."""
    rows = sorted({r for r, _ in table})
    cols = sorted({c for _, c in table})
    if len(rows) < 2 or len(cols) < 2:
        return 1.0
    n = sum(table.values())
    rt = {r: sum(table.get((r, c), 0) for c in cols) for r in rows}
    ct = {c: sum(table.get((r, c), 0) for r in rows) for c in cols}
    x = 0.0
    for r in rows:
        for c in cols:
            e = rt[r] * ct[c] / n
            if e > 0:
                x += (table.get((r, c), 0) - e) ** 2 / e
    return _chi2_sf(x, (len(rows) - 1) * (len(cols) - 1))


def g18(row: dict, eps: Fraction = Fraction(5, 100)) -> bool:
    ol = row["meta"]["option_level"]
    K = len(row["options"])
    g = ol[row["gold"]]
    E = (1 - eps) * g + eps * Fraction(K - 1, 2)
    r = round(E)  # Python round is half-even on Fractions
    return set(ol) == set(row["options"]) and sorted(ol.values()) == list(range(K)) and r == g


def criteria_texts(row: dict) -> list[str]:
    """Level-definition and override texts (for the 6.3 negation share)."""
    out = []
    opts = row["options"]
    if row.get("card"):
        for ln in row["card"].split("\n"):
            if ln.startswith("- ") and ": " in ln:
                out.append(ln[2:].split(": ", 1)[1])
    for ln in row["instructions"].split("\n"):
        s = ln.strip().lstrip("> ").strip()
        for o in opts:
            for sep in (": ", " | ", "  "):
                if s.startswith(o + sep) or s.startswith("| " + o + " |"):
                    out.append(s[len(o) + len(sep):] if s.startswith(o + sep) else s.split("|")[2])
        if s.startswith("If ") and ", the level is at " in s:
            out.append(s[3:].split(", the level is at ")[0])
    return out


def absence_cues(row: dict) -> int:
    st = row["state"]
    n = 0
    import re
    n += len(re.findall(r"\b(had no|did not have|never had|has no|does not have)\b", st))
    n += len(re.findall(r"(?:[:=|]\s*|\.{3,}\s*|<td>|<dd>)(?:no|absent|N)\s*(?:$|\||</)", st, flags=re.M))
    n += len(re.findall(r": false\b|\": false", st))
    return n


def _pool_cells(tab: dict, min_n: int = 5) -> dict:
    """Pool sparse rows (cue counts) into their neighbour so expected counts are not tiny."""
    rows = sorted({r for r, _ in tab})
    tot = {r: sum(v for (rr, _), v in tab.items() if rr == r) for r in rows}
    keep = [r for r in rows if tot[r] >= min_n * 4] or rows
    out = collections.Counter()
    for (r, c), v in tab.items():
        rr = min(keep, key=lambda k: abs(k - r))
        out[(rr, c)] += v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows")
    ap.add_argument("--relations")
    ap.add_argument("--out")
    ap.add_argument("--no-loader", action="store_true")
    ap.add_argument("--no-tokens", action="store_true")
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.rows, encoding="utf-8")]
    rels = [json.loads(l) for l in open(a.relations, encoding="utf-8")] if a.relations else []
    rep = {"file": str(a.rows), "rows": len(rows), "sha256": hashlib.sha256(Path(a.rows).read_bytes()).hexdigest()}
    # ---------------------------------------------------------------- G15 check_rows + loader_check
    td = fcard._td()
    dio = fcard._dio()
    bad_cr = 0
    try:
        td.check_rows(rows)
    except ValueError as e:
        bad_cr = int(str(e).split(":")[1].split()[0]) if ":" in str(e) else -1
    rep["G15_check_rows_failures"] = bad_cr
    loader_fail = 0
    letter_by_K = collections.defaultdict(collections.Counter)
    gold_letter_fail = 0
    if not a.no_loader:
        for r in rows:
            rng = random.Random(int(hashlib.sha256(("G15perm:" + r["id"]).encode()).hexdigest()[:12], 16))
            perm = list(range(len(r["options"])))
            rng.shuffle(perm)
            res = fcard.loader_check(r, perm=perm, check_rows=False)
            if not res["ok"]:
                loader_fail += 1
            if res["gold_letter"] is None:
                gold_letter_fail += 1
            else:
                letter_by_K[len(r["options"])][res["gold_letter"]] += 1
    rep["G15_loader_check_failures"] = loader_fail
    rep["G15_gold_letter_map_failures"] = gold_letter_fail
    rep["G10_gold_letter_chi2_p_by_K"] = {k: round(chi2_uniform([c[x] for x in sorted(c)] +
                                                                [0] * (k - len(c))), 4) for k, c in letter_by_K.items()}
    # units
    units = collections.defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r)
    rep["units"] = len(units)
    rep["units_over_3_rows"] = sum(1 for u in units.values() if len(u) > 3)
    rel_ok = 0
    ids = {r["id"]: r for r in rows}
    for x in rels:
        ra, rb = ids.get(x["a"]), ids.get(x["b"])
        if ra and rb and ra["call_id"] == rb["call_id"] and ra["gold"] == rb["gold"]:
            rel_ok += 1
    rep["relations"] = len(rels)
    rep["relations_same_call_and_gold"] = rel_ok
    # ---------------------------------------------------------------- lengths (instructions counted twice)
    if not a.no_tokens:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
        saved = (dio.STYLE, dio.LAYOUT)
        dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
        try:
            texts = [dio.user_msg(r) for r in rows]
        finally:
            dio.STYLE, dio.LAYOUT = saved
        lens = []
        for i in range(0, len(texts), 256):
            enc = tok(texts[i:i + 256], add_special_tokens=False)["input_ids"]
            lens += [len(x) for x in enc]
        for r, n in zip(rows, lens):
            r["_tokens"] = n
        rep["tokens_max"] = max(lens)
        rep["tokens_over_7900"] = sum(1 for n in lens if n > 7900)
        rep["long_rows_ge_2000"] = sum(1 for n in lens if n >= 2000)
        rep["long_row_share"] = round(rep["long_rows_ge_2000"] / len(lens), 4)
        nonlong = [n for n in lens if n < 2000]
        rep["median_tokens_nonlong"] = statistics.median(nonlong) if nonlong else None
        by = collections.defaultdict(list)
        for r, n in zip(rows, lens):
            by[(r["meta"]["sampler"], r["meta"]["base_defs_style"])].append(n)
        rep["median_tokens_by_sampler_defs"] = {f"{s}|{d}": statistics.median(v) for (s, d), v in sorted(by.items())}
        rep["units_with_long_row_over_2_rows"] = sum(1 for u in units.values()
                                                    if len(u) > 2 and any(x.get("_tokens", 0) >= 2000 for x in u))
    # ---------------------------------------------------------------- G3 re-verification (independent parser + solver B)
    import f7build as FB
    import f7packs as PK
    import f7parse as PS
    import f7solveb as SB
    g3 = collections.Counter()
    for r in rows:
        pack = PK.pack_by_id(r["meta"]["domain_pack"])
        try:
            PC, cs, worked = PS.parse_row(r, pack)
            if PC["option_level"] != r["meta"]["option_level"]:
                g3["option_level_mismatch"] += 1
            elif SB.solve_b(PC, cs, pack) != r["meta"]["option_level"][r["gold"]]:
                g3["solver_b_mismatch"] += 1
            elif FB.parsed_structure_hash(PC, cs) != r["meta"]["structure_hash"]:
                g3["structure_hash_mismatch"] += 1
            elif any(SB.solve_b(PC, wc, pack) != PC["option_level"][ans] for wc, ans in worked):
                g3["worked_case_mismatch"] += 1
            else:
                g3["pass"] += 1
        except (PS.ParseFail, SB.SolveFail) as e:
            g3[f"fail:{type(e).__name__}"] += 1
    rep["G3_round_trip"] = dict(g3)
    rep["G3_pass_rate"] = round(g3["pass"] / len(rows), 6)
    # ---------------------------------------------------------------- G18
    rep["G18_ordinal_lint_pass"] = sum(1 for r in rows if g18(r))
    rep["G18_ordinal_lint_pass_eps008"] = sum(1 for r in rows if g18(r, Fraction(8, 100)))
    # ---------------------------------------------------------------- G12 exact duplicates
    seen = collections.Counter(hashlib.sha256(json.dumps([r["state"], r["instructions"], r["options"], r["card"]])
                                              .encode()).hexdigest() for r in rows)
    rep["G12_exact_duplicates"] = sum(c - 1 for c in seen.values() if c > 1)
    sh = collections.Counter((r["meta"]["structure_hash"], r["meta"]["card_id"]) for r in rows
                             if r["meta"]["twin_kind"] is None)
    rep["structure_hash_repeats_among_base_rows"] = sum(c - 1 for c in sh.values() if c > 1)
    # ---------------------------------------------------------------- balance and quotas
    by_s = collections.defaultdict(list)
    for r in rows:
        by_s[r["meta"]["sampler"]].append(r)
    q = {}
    for s, rs in sorted(by_s.items()):
        d = {"rows": len(rs), "cards": len({r["meta"]["card_id"] for r in rs})}
        lv = collections.defaultdict(collections.Counter)
        for r in rs:
            lv[r["meta"]["K"]][r["meta"]["option_level"][r["gold"]]] += 1
        d["gold_level_max_dev_pp_by_K"] = {k: round(max(abs(c[i] / sum(c.values()) - 1 / k) for i in range(k)) * 100, 2)
                                           for k, c in lv.items()}
        tw = collections.Counter(r["meta"]["twin_kind"] for r in rs)
        flip_rows = tw["fact_flip"] * 2
        d["fact_flip_pair_row_share"] = round(flip_rows / len(rs), 4)
        d["equiv_twin_share"] = round(tw["equiv"] / len(rs), 4)
        d["inv_twin_share"] = round(tw["inv"] / len(rs), 4)
        d["conv_row_share"] = round(sum(1 for r in rs if any(e["kind"] == "conv" for e in r["meta"]["edge"])) / len(rs), 4)
        d["conv_ids"] = dict(collections.Counter(e["conv"] for r in rs for e in r["meta"]["edge"] if e["kind"] == "conv"))
        bd = collections.Counter(e["placement"] for r in rs for e in r["meta"]["edge"] if e["kind"] == "boundary")
        nb = sum(bd.values())
        d["boundary_placement_share"] = {k: round(v / nb, 3) for k, v in bd.items()} if nb else {}
        d["boundary_rows"] = nb
        d["masked_row_share"] = round(sum(1 for r in rs if r["meta"]["label_form"] == "masked") / len(rs), 4)
        d["swapped_row_share"] = round(sum(1 for r in rs if r["meta"]["label_form"] == "swapped") / len(rs), 4)
        d["short_row_share"] = round(sum(1 for r in rs if r["meta"]["base_defs_style"] == "short") / len(rs), 4)
        d["deep_row_share"] = round(sum(1 for r in rs if r["meta"]["deep"]) / len(rs), 4)
        cards = {}
        for r in rs:
            cards.setdefault(r["meta"]["card_id"], collections.Counter())[r["meta"]["option_level"][r["gold"]]] += 1
        bad_cards = 0
        for cid, c in cards.items():
            K = next(r["meta"]["K"] for r in rs if r["meta"]["card_id"] == cid)
            n = sum(c.values())
            if n < 2 * K or any(c[i] not in (n // K, -(-n // K)) for i in range(K)):
                bad_cards += 1
        d["cards_failing_per_card_level_quota"] = bad_cards
        # longest option is gold
        lo = [1 if max(r["options"], key=len) == r["gold"] else 0 for r in rs]
        exp = statistics.mean(1 / len(r["options"]) for r in rs)
        d["longest_option_is_gold_minus_1_over_K_pp"] = round((statistics.mean(lo) - exp) * 100, 2)
        # 6.3: negated or implicit cue in criteria (k_all >= 1)
        crits = [t for r in rs if r["meta"]["twin_kind"] is None for t in criteria_texts(r)]
        if crits:
            d["criteria_k_all_ge1_share"] = round(sum(1 for t in crits if negcount.k_all(t) >= 1) / len(crits), 4)
        tab = collections.Counter()
        tab2 = collections.Counter()
        import f7packs as PK
        import f7parse as PS
        for r in rs:
            lvn = r["meta"]["option_level"][r["gold"]]
            _, cs, _ = PS.parse_row(r, PK.pack_by_id(r["meta"]["domain_pack"]))
            tab[(min(cs["absence_cues"], 6), lvn)] += 1
            tab2[(min(negcount.k_all(r["state"]), 6), lvn)] += 1
        d["absence_cues_vs_level_chi2_p"] = round(chi2_indep(_pool_cells(tab)), 4)
        d["state_k_all_vs_level_chi2_p"] = round(chi2_indep(_pool_cells(tab2)), 4)
        cf = [r["meta"]["case_features"] for r in rs]
        d["unmentioned_row_share"] = round(sum(1 for x in cf if x["unmentioned"]) / len(rs), 4)
        um = [r for r in rs if r["meta"]["case_features"]["unmentioned"]]
        if um:
            d["unmentioned_decisive_share"] = round(sum(1 for r in um if any(e.get("conv") == "C1" for e in
                                                                           r["meta"]["edge"])) / len(um), 4)
        d["missing_row_share"] = round(sum(1 for x in cf if x["missing"]) / len(rs), 4)
        d["plan_row_share"] = round(sum(1 for x in cf if x["plans"]) / len(rs), 4)
        d["partial_row_share"] = round(sum(1 for x in cf if x["partials"]) / len(rs), 4)
        d["repeat_row_share"] = round(sum(1 for x in cf if x["repeats"]) / len(rs), 4)
        d["inert_subject_share"] = round(sum(1 for x in cf if x["inert_subject"]) / len(rs), 4)
        d["distractor_share"] = round(sum(1 for x in cf if x["other"] == "distractor") / len(rs), 4)
        d["other_entity_inert_share"] = round(sum(1 for x in cf if x["other"] == "inert") / len(rs), 4)
        d["cue_target_missed"] = sum(1 for x in cf if x.get("cue_target_met") is False)
        two = collections.Counter()
        for r in rs:
            g = r["meta"]["option_level"][r["gold"]]
            for e in r["meta"]["edge"]:
                if e["kind"] == "conv":
                    two[(e["conv"], "above" if e["alt_level"] > g else "below")] += 1
        d["conv_direction"] = {f"{c}|{w}": n for (c, w), n in sorted(two.items())}
        if "_tokens" in rs[0]:
            d["median_tokens"] = statistics.median(r["_tokens"] for r in rs)
        q[s] = d
    rep["by_sampler"] = q
    rep["K_rows"] = dict(collections.Counter(r["meta"]["K"] for r in rows))
    rep["mode_rows"] = dict(collections.Counter(r["meta"]["mode"] for r in rows))
    rep["defs_style_rows"] = dict(collections.Counter(r["meta"]["defs_style"] for r in rows))
    rep["containers"] = dict(collections.Counter(r["meta"]["container"] for r in rows))
    rep["format_styles"] = len({r["meta"]["format_style"] for r in rows})
    rep["packs"] = len({r["meta"]["domain_pack"] for r in rows})
    rep["cards"] = len({r["meta"]["card_id"] for r in rows})
    rep["wordings"] = len({r["meta"]["wording_id"] for r in rows})
    rep["option_bucket_rows"] = {"2-4": sum(1 for r in rows if len(r["options"]) <= 4),
                                 "5-9": sum(1 for r in rows if 5 <= len(r["options"]) <= 9)}
    tmpl = collections.Counter((r["meta"]["sampler"], fpool.style(r["meta"]["format_style"])["skin"],
                                r["meta"]["mode"], r["meta"]["case_features"]["other"] is not None,
                                r["meta"]["case_features"]["inert_subject"]) for r in rows)
    rep["surface_templates"] = len(tmpl)
    rep["max_surface_template_share"] = round(max(tmpl.values()) / len(rows), 4)
    out = a.out or (str(a.rows) + ".gates.json")
    json.dump(rep, open(out, "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("by_sampler", "median_tokens_by_sampler_defs")},
                     default=str)[:3000])


if __name__ == "__main__":
    main()
