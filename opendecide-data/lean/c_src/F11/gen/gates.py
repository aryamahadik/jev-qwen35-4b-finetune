"""F11 output gates on a built set (cand | qc | dev): G15, real-tokenizer length, negcount quotas, G18, G4 summary.

  python gen/gates.py <set>      -> tmp/gates_<set>.json (exit 2 if any hard gate fails)

G15: train_decoder.check_rows (pinned A16 trainer) on every row; fmt1 loader_check again under a second random
permutation (decoder_io.user_msg; gold letter maps back); units (call_id) <= 3 rows, <= 2 when a row has >= 2,000
tokens. Length: Qwen/Qwen3.5-4B tokenizer (local files), state + card + 2 x instructions + options <= 7,900.
negcount (brief 2.1): k_syn >= 1 on >= 10% of yes/no rows; double negation with an affirmative twin >= 2%.
G4: in-build MR-1 (option shuffle) and MR-3 (code-list permutation) results from tmp/build_<name>.json, plus the
relation and twin MRs re-verified from the output files: MR-4 inert (equiv), MR-14 attack (inv), MR-16 neg/dneg
(complement / equiv), MR-6 attr_flip / cut_cross and S7 focal_target / MR-15 defs_swap (twins checked inline by
solver B at build time). G2/G3 ran inline on every row in the build (check_failures must be 0).
"""
from __future__ import annotations

import json
import os
import random
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("RAYON_NUM_THREADS", "2")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "true")

import common  # noqa: E402,F401
import negcount  # noqa: E402
from common import OUT, TMP, progress, sha256_file  # noqa: E402
from fmt1 import card as fcard  # noqa: E402
from check import strip_question_block  # noqa: E402

NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
MAX_TOK = 7900


def load(path):
    return [json.loads(x) for x in open(path)]


_TOK = None


def tok():
    global _TOK
    if _TOK is None:
        from transformers import AutoTokenizer
        _TOK = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
    return _TOK


def lengths_batch(rows):
    """Served-prompt tokens per row id (toklen.served_lens: decoder_io cygnet + schema_branch_mark chat render, the
    G0 / G15 length; `instructions` and option texts printed twice)."""
    from toklen import served_lens
    return dict(zip([r["id"] for r in rows], served_lens(rows)))


def fields_batch(rows):
    texts = set()
    for r in rows:
        texts.update([r["state"] or "", r.get("card") or "", r["instructions"] or ""])
        texts.update(r.get("options") or ["Yes", "No"])
    texts = sorted(texts)
    n = {}
    B = 256
    for i in range(0, len(texts), B):
        chunk = texts[i:i + B]
        enc = tok()(chunk, add_special_tokens=False)["input_ids"]
        for t, e in zip(chunk, enc):
            n[t] = len(e)
    out = {}
    for r in rows:
        opts = r.get("options") or ["Yes", "No"]
        out[r["id"]] = n[r["state"] or ""] + n[r.get("card") or ""] + 2 * n[r["instructions"] or ""] + \
            sum(n[o] for o in opts)
    return out


def main(argv=None):
    tag = (argv or sys.argv[1:])[0]
    name = NAMES[tag]
    rows = load(OUT / f"{name}.jsonl")
    rels = load(OUT / f"{name}.relations.jsonl")
    build = json.load(open(TMP / f"build_{name}.json"))
    rep = {"set": tag, "rows": len(rows), "relations": len(rels), "rows_sha256": sha256_file(OUT / f"{name}.jsonl"),
           "relations_sha256": sha256_file(OUT / f"{name}.relations.jsonl")}
    hard = []
    # ---- G2 / G3 (inline at build)
    rep["G2_G3_inline_check_failures"] = build["check_failures"]
    if build["check_failures"]:
        hard.append("G2/G3 inline check failures")
    # ---- meta
    rep["rows_without_format_style"] = sum(1 for r in rows if not r["meta"].get("format_style"))
    if rep["rows_without_format_style"]:
        hard.append("format_style missing")
    ids = [r["id"] for r in rows]
    rep["duplicate_ids"] = len(ids) - len(set(ids))
    if rep["duplicate_ids"]:
        hard.append("duplicate ids")
    # ---- G15
    td = fcard._td()
    try:
        td.check_rows(rows)
        rep["G15_check_rows"] = "pass"
    except BaseException as e:      # noqa: BLE001
        rep["G15_check_rows"] = f"FAIL {str(e)[:200]}"
        hard.append("G15 check_rows")
    lf, lf_ids = 0, []
    for r in rows:
        rr = random.Random(f"g15b:{r['id']}")
        n = len(r["options"]) if r["qtype"] == "choice" else 2
        perm = list(range(n))
        rr.shuffle(perm)
        res = fcard.loader_check(r, perm=perm, check_rows=False)
        if not res["ok"]:
            lf += 1
            lf_ids.append(r["id"])
    rep["G15_loader_fail_second_perm"] = lf
    rep["G15_loader_fail_ids"] = lf_ids[:20]
    if lf:
        hard.append("G15 loader_check")
    fl = list(fields_batch(rows).values())
    rep["tokens_fields_x2instr"] = {"median": statistics.median(fl), "max": max(fl), "min": min(fl),
                                    "over_2000": sum(t >= 2000 for t in fl), "over_7900": sum(t > MAX_TOK for t in fl),
                                    "note": "field sum only (report); the binding length is tokens_served"}
    toks = lengths_batch(rows)
    tl = list(toks.values())
    rep["tokens_served"] = {"median": statistics.median(tl), "max": max(tl), "min": min(tl),
                            "over_900": sum(t > 900 for t in tl), "over_2000": sum(t >= 2000 for t in tl),
                            "over_7900": sum(t > MAX_TOK for t in tl),
                            "measure": "decoder_io.render_chat(CYGNET_SYSTEM, user_msg) cygnet+schema_branch_mark, "
                                       "Qwen3.5-4B tokenizer"}
    if rep["tokens_served"]["over_7900"]:
        hard.append("length > 7,900")
    units = defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r["id"])
    sizes = Counter(len(u) for u in units.values())
    rep["G15_unit_sizes"] = {str(k): v for k, v in sorted(sizes.items())}
    rep["G15_units_over_3"] = sum(v for k, v in sizes.items() if k > 3)
    rep["G15_units_over_2_with_long_row"] = sum(1 for u in units.values()
                                                if len(u) > 2 and any(toks[x] >= 2000 for x in u))
    if rep["G15_units_over_3"] or rep["G15_units_over_2_with_long_row"]:
        hard.append("G15 unit size")
    # ---- G18 (ordinal rows)
    rep["G18_ordinal_rows"] = sum(1 for r in rows if (r["meta"].get("option_level") is not None) or
                                  any(re.search(r"\b(level|tier|grade|band)\s*\d", o, re.I)
                                      for o in (r.get("options") or [])))
    rep["G18"] = "n/a (no ordinal rows)" if rep["G18_ordinal_rows"] == 0 else "CHECK"
    if rep["G18_ordinal_rows"]:
        hard.append("G18 ordinal rows present")
    # ---- negcount quotas
    yn = [r for r in rows if r["qtype"] == "noul"]
    ks = {}
    for r in yn:
        _, q = strip_question_block(r["instructions"])
        ks[r["id"]] = negcount.count(q or "").k_syn
    gold = {r["id"]: r["gold"] for r in rows}
    rel_by = defaultdict(list)
    for x in rels:
        rel_by[x["a"]].append(x)
        rel_by[x["b"]].append(x)
    dneg = 0
    for r in yn:
        if ks[r["id"]] >= 2:
            for x in rel_by[r["id"]]:
                o = x["a"] if x["b"] == r["id"] else x["b"]
                if x["type"] == "equiv" and ks.get(o) == 0 and gold.get(o) == r["gold"]:
                    dneg += 1
                    break
    n_yn = max(1, len(yn))
    k1 = sum(1 for v in ks.values() if v >= 1)
    rep["negation"] = {"yes_no_rows": len(yn), "k_syn_ge1": k1, "k_syn_ge1_share": round(k1 / n_yn, 4),
                       "dneg_with_affirmative_twin": dneg, "dneg_share": round(dneg / n_yn, 4),
                       "k_syn_hist": dict(Counter(ks.values()))}
    if tag != "dev" and (k1 / n_yn < 0.10 or dneg / n_yn < 0.02):
        hard.append("negcount quota")
    # ---- G4
    tk = {r["id"]: r["meta"]["twin_kind"] for r in rows}
    mr = Counter()
    mr_rows = set()
    bad = Counter()
    MRK = {"inert": "MR-4", "attack": "MR-14", "neg": "MR-16", "dneg": "MR-16"}
    for x in rels:
        a, b, t = x["a"], x["b"], x["type"]
        if a not in gold or b not in gold:
            bad["relation row missing"] += 1
            continue
        k = MRK.get(tk.get(b)) or MRK.get(tk.get(a)) or "rel:" + t
        ok = (gold[a] == gold[b]) if t in ("equiv", "inv") else \
            (t == "complement" and isinstance(gold[a], int) and gold[b] == 1 - gold[a])
        mr[k + (" pass" if ok else " FAIL")] += 1
        if ok:
            mr_rows.update((a, b))
        else:
            bad[k] += 1
    TWK = {"attr_flip": "MR-6", "cut_cross": "MR-6", "focal_target": "MR-6 (S7 focal target)",
           "defs_swap": "MR-15"}
    for r in rows:
        k = TWK.get(r["meta"]["twin_kind"])
        if k:
            mr[k + " pass (solver B inline)"] += 1
            mr_rows.update((r["id"], r["meta"]["twin_of"]) if r["meta"]["twin_of"] else (r["id"],))
    ib = build.get("g4_inbuild", {})
    for k, v in ib.items():
        mr[k] += v
        if "FAIL" in k:
            bad[k] += v
    n_ib = sum(v for k, v in ib.items() if k.endswith(" pass"))
    rep["G4"] = {"results": dict(sorted(mr.items())), "failures": dict(bad),
                 "rows_in_relation_or_twin_mrs": len(mr_rows), "inbuild_mr_tests": n_ib,
                 "mr_ids": sorted({k.split(" ")[0] for k in mr if "pass" in k})}
    if bad:
        hard.append("G4 failures")
    if tag != "dev" and (len(rep["G4"]["mr_ids"]) < 3 or len(mr_rows) + n_ib < 1000):
        hard.append("G4 coverage")
    rep["hard_failures"] = hard
    (TMP / f"gates_{tag}.json").write_text(json.dumps(rep, indent=1))
    progress(f"gates {tag}: rows {len(rows)}, hard failures {hard or 'none'}; tokens max "
             f"{rep['tokens_served']['max']}; k_syn>=1 {rep['negation']['k_syn_ge1_share']}, dneg "
             f"{rep['negation']['dneg_share']}; G4 {rep['G4']['mr_ids']}")
    print(json.dumps({k: v for k, v in rep.items() if k not in ("G15_loader_fail_ids",)}, indent=1)[:2500])
    if hard:
        sys.exit(2)


if __name__ == "__main__":
    main()
