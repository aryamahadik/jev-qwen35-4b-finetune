"""F10 standalone gate re-run on one output part (re-reads the rows from disk; never uses generator state):
  G3  parse the rendered row back (program parser / S7 lexicon parser) -> structure hash == meta.structure_hash
  G2  solver B (region algebra on the parsed card; S7 first fit on the parsed codebook) == gold
  G15 train_decoder.check_rows on the whole part + fmt1 loader_check per row under a seeded random permutation
      (gold letter maps back to the canonical gold); units share one call_id, <= 3 rows, <= 2 when a row >= 2,000
      tokens; real-tokenizer length of the served prompt (instructions printed twice) <= 7,900 (F10: A22 length ruling, see main)
  G18 F10 has no ordinal row: 0 rows may carry meta.option_level
  negcount quotas on yes/no rows (sidecar k_syn from negcount v1.1): syntactic negation >= 10%; double negation
      with an affirmative twin >= 2%
Usage: python qc/gates.py <part> [workers]   (part = candidates_r1 | qc_sample | mixdev_S5)"""
from __future__ import annotations

import hashlib
import json
import os
import statistics
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen"))
import common  # noqa: E402  (sets sys.path for fmt1, common tools, lean)
from common import OUT, sha256_file  # noqa: E402

_TOK = None
_REC = {}
_CARDS = {}


def tokenizer():
    global _TOK
    if _TOK is None:
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
        from transformers import AutoTokenizer
        _TOK = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    return _TOK


def served_tokens(row):
    import decoder_io as dio
    saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
    try:
        dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
        if row.get("options") and len(row["options"]) > len(dio.WIDE):
            U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            dio.WIDE = list(U) + [a + b for a in U for b in U]
        text = dio.render_chat(tokenizer(), dio.CYGNET_SYSTEM, dio.user_msg(dict(row), None))
    finally:
        dio.STYLE, dio.LAYOUT, dio.WIDE = saved
    return len(tokenizer()(text)["input_ids"])


def s7_record(scheme, record_id):
    import s7 as S
    if scheme not in _REC:
        d = {}
        for l in open(common.FMT2_DIR / "records" / S.REC_FILE[scheme]):
            r = json.loads(l)
            d[r["record_id"]] = r
        _REC[scheme] = d
    return _REC[scheme][record_id]


def g23_program(row, card):
    import canon
    import g3 as G3
    import parse as PZ
    from fmt1 import pool
    st = pool.style(row["meta"]["format_style"])
    try:
        pr = PZ.parse_program_row(row, st["container"], card["sampler"] if card["sampler"] != "S5" else "S1",
                                  card.get("pack_attrs"), card.get("prose_record"))
    except PZ.ParseError as e:
        return "parse: " + str(e)[:80], None
    q = pr["query"]
    q["wkind"] = G3.WK.get(q["wkind"], q["wkind"])
    if "description" in pr:
        import model as M
        q["desc"] = M.canon_def({"desc": pr["description"]}, "desc")
    h = canon.shash(canon.structure(pr["card_like"], q))
    g3 = None if h == row["meta"]["structure_hash"] else "structure_hash differs"
    try:
        gb = G3.solve_parsed(pr, row)
        g2 = None if gb == row["gold"] else f"solver B {gb!r} != gold"
    except PZ.ParseError as e:
        g2 = "solve: " + str(e)[:60]
    if G3.check_examples(pr):
        g3 = g3 or "examples fail"
    return g3, g2


def g23_s7(row):
    import parse_s7 as PS
    import s7 as S
    from parse import ParseError
    cbid = row["meta"]["domain_pack"].split(":", 1)[1]
    cb = next(c for c in S.codebooks() if c["id"] == cbid)
    scheme = cb["scheme"]
    rec = s7_record(scheme, row["meta"]["text_source"]["record_id"])
    try:
        conds, names = PS.parse_codebook(row, S.lexicons()[scheme])
        q, asked, listed = PS.parse_question_s7(row["instructions"], names, row["qtype"])
    except ParseError as e:
        return "parse: " + str(e)[:80], None
    if row["state"] != rec["text"]:
        return "state is not the record text", None
    ti = None
    if scheme == "mams_atsa":
        terms = rec["ann"]["terms"]
        if asked is None or listed != [t["term"] for t in terms]:
            return "ATSA frame", None
        hits = [i for i, t in enumerate(terms) if t["term"] == asked]
        ti = hits[0] if len(hits) == 1 else None
    if row["qtype"] == "choice":
        q["shown"] = sorted(names.index(o) for o in row["options"])
        g = next(i for i, c in enumerate(conds) if c["op"] == "RESIDUAL" or S.cond(c, rec, ti, scheme))
        gb = names[g] if g in q["shown"] else None
    else:
        v = S.cond(conds[q["target"]], rec, ti, scheme)
        gb = int(v if q["neg"] in (0, 2) else not v)
    q["rec"] = rec["norm_sha256"]
    q["ti"] = ti
    h = PS.s7_hash(scheme, conds, q)
    return (None if h == row["meta"]["structure_hash"] else "structure_hash differs"), \
        (None if gb == row["gold"] else f"solver B {gb!r} != gold")


def one(args):
    row, card = args
    from fmt1 import card as fcard
    out = {"id": row["id"]}
    try:
        if row["meta"]["sampler"] == "S7":
            out["g3"], out["g2"] = g23_s7(row)
        else:
            out["g3"], out["g2"] = g23_program(row, card)
    except Exception as e:  # a crash is a gate failure, never skipped
        out["g3"] = f"crash {type(e).__name__}: {str(e)[:60]}"
        out["g2"] = None
    seed = hashlib.sha256(("g15|" + row["id"]).encode()).hexdigest()
    res = fcard.loader_check(row, seed=seed, check_rows=False)
    out["g15"] = None if res["ok"] else "|".join(res["problems"])[:120]
    out["tokens"] = served_tokens(row)
    out["g18"] = None if "option_level" not in row["meta"] else "option_level on a non-ordinal family"
    return out


def main(part, workers=2):
    rows = [json.loads(l) for l in open(OUT / f"{part}.jsonl")]
    cards = {c["card_id"]: c for c in (json.loads(l) for l in open(OUT / f"{part}.cards.jsonl"))}
    sides = {s["id"]: s for s in (json.loads(l) for l in open(OUT / f"{part}.sidecar.jsonl"))}
    relp = OUT / f"{part}.relations.jsonl"
    rels = [json.loads(l) for l in open(relp)] if relp.exists() else []
    jobs = [(r, cards.get(r["meta"]["card_id"], {"sampler": r["meta"]["sampler"]})) for r in rows]
    with Pool(workers) as p:
        res = list(p.imap(one, jobs, chunksize=16))
    # whole-part check_rows (pinned A16 trainer, sha checked by fmt1)
    from fmt1 import card as fcard
    try:
        fcard._td().check_rows(rows)
        cr = "pass"
    except Exception as e:
        cr = f"FAIL {type(e).__name__}: {str(e)[:200]}"
    toks = {x["id"]: x["tokens"] for x in res}
    units = defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r["id"])
    byid = {r["id"]: r for r in rows}
    unit_bad = [u for u, v in units.items() if len(v) > 3 or (len(v) > 2 and max(toks[i] for i in v) >= 2000)]
    rel_bad = [x for x in rels if byid[x["a"]]["call_id"] != byid[x["b"]]["call_id"]]
    fails = {g: Counter(x[g] for x in res if x[g]) for g in ("g3", "g2", "g15", "g18")}
    yn = [r for r in rows if r["qtype"] != "choice"]
    tl = sorted(toks.values())
    rep = {"part": part, "file": f"{part}.jsonl", "sha256": sha256_file(OUT / f"{part}.jsonl"), "rows": len(rows),
           "G3": {"pass": sum(1 for x in res if not x["g3"]), "fail": sum(fails["g3"].values()),
                  "top": fails["g3"].most_common(5)},
           "G2": {"agree": sum(1 for x in res if not x["g2"] and not x["g3"]), "mismatch": sum(fails["g2"].values()),
                  "top": fails["g2"].most_common(5)},
           "G15": {"check_rows_whole_part": cr, "loader_perm_pass": sum(1 for x in res if not x["g15"]),
                   "loader_fail": sum(fails["g15"].values()), "top": fails["g15"].most_common(3),
                   "units": len(units), "unit_size_max": max(len(v) for v in units.values()),
                   "units_bad": len(unit_bad), "relations": len(rels), "relations_across_call_ids": len(rel_bad),
                   "tokens_max": tl[-1], "tokens_median": statistics.median(tl), "tokens_mean": round(sum(tl) / len(tl), 1),
                   "rows_ge_2000": sum(1 for t in tl if t >= 2000), "rows_gt_7900": sum(1 for t in tl if t > 7900)},
           "G18": {"applies": False, "ordinal_rows": 0, "rows_with_option_level": sum(fails["g18"].values())}}
    if yn and sides:
        ks = [sides[r["id"]]["k_syn"] for r in yn if r["id"] in sides]
        dneg = sum(1 for r in yn if r["meta"].get("twin_kind") == "dneg")
        rep["negcount"] = {"tool_sha256": sha256_file(common.COMMON_DIR / "negcount.py"), "yes_no_rows": len(yn),
                           "syntactic_neg_share": round(sum(1 for k in ks if k >= 1) / len(yn), 4),
                           "double_neg_with_affirmative_twin_share": round(dneg / len(yn), 4),
                           "k_syn_ge2_share": round(sum(1 for k in ks if k >= 2) / len(yn), 4)}
        rep["negcount"]["pass"] = part == "mixdev_S5" or (rep["negcount"]["syntactic_neg_share"] >= 0.10 and
                                                          rep["negcount"]["double_neg_with_affirmative_twin_share"] >= 0.02)
        if part == "mixdev_S5":
            rep["negcount"]["note"] = "dev items: the training-row negation quotas do not apply (anchors only)"
    # Length (Amendment A22, tmp/repair/LENGTH_RULING.md; proof tmp/repair/INFEASIBLE_length.md): every row <= 7,900
    # tokens (instructions counted twice); shares and buckets kept; the mix-level cap (rows >= 2,000 tokens <= 9% of
    # new rows and <= 30% of new-row tokens) is enforced by the mixer, so it is reported here, not gated.
    rep["G15"]["length_rule"] = "A22: rows <= 7,900 tokens (instructions twice); mix-level 2,000-token cap at the mixer"
    rep["G15"]["share_rows_ge_2000"] = round(rep["G15"]["rows_ge_2000"] / len(tl), 4)
    rep["G15"]["share_tokens_in_rows_ge_2000"] = round(sum(t for t in tl if t >= 2000) / max(1, sum(tl)), 4)
    rep["pass"] = (rep["G3"]["fail"] == 0 and rep["G2"]["mismatch"] == 0 and cr == "pass" and
                   rep["G15"]["loader_fail"] == 0 and not unit_bad and not rel_bad and
                   rep["G15"]["rows_gt_7900"] == 0 and rep["G18"]["rows_with_option_level"] == 0 and
                   (part == "mixdev_S5" or rep.get("negcount", {}).get("pass", False)))
    (OUT / f"{part}.gates.json").write_text(json.dumps(rep, indent=1))
    (OUT / f"{part}.gates_tokens.json").write_text(json.dumps(toks))
    bad = [x for x in res if x["g3"] or x["g2"] or x["g15"]]
    (OUT / f"{part}.gates_fail_ids.json").write_text(json.dumps([x["id"] for x in bad]))
    common.progress(f"gates {part}: rows {len(rows)} G3 fail {rep['G3']['fail']} G2 mismatch {rep['G2']['mismatch']} "
                    f"G15 {cr[:20]} loader fail {rep['G15']['loader_fail']} tokens max {tl[-1]} median "
                    f"{rep['G15']['tokens_median']}; pass {rep['pass']}")
    print(json.dumps(rep)[:2500])


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2)
