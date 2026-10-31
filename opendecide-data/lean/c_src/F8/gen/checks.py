"""F8 gate checks on the written files (re-run from the rows alone, never from generator memory).

  G3   every row re-parsed from its text by the independent parser; solver B re-solves; the answer must map to the
       row's gold option; the parsed render hash must equal the sidecar's render_hash (100%)
  G15  train_decoder.check_rows on every file; fmt1 loader_check on every row under 3 random option orders (gold
       letter maps back); relation units share one call_id and hold <= 3 rows; real-tokenizer length of the served
       prompt (Qwen3.5 chat template, cygnet system, schema_branch_mark; instructions appear twice) < 2,000 and
       <= 7,900
  G18  no F8 row carries meta.option_level (F8 rows are not ordinal in round 1; F8-R1-C3) - 100%
  negcount quotas (XF02): k_syn >= 1 on >= 12% of YN rows (floor 10%); k_syn >= 2 with an affirmative twin >= 3%
       (floor 2%)
  lints: text lints, source c_f8 not in kd_full_src, no S5 row or held-out style in a training file, no PRED
       gold_probs off the shown options, S5 rows only with held-out styles
Prints counts only.
"""
from __future__ import annotations

import collections
import json
import random
import re
import sys

import common as CM
import hashes as H
import lints
import parse as PZ
import solver_b as SB
from fmt1 import card as fcard
from fmt1 import pool as fpool


def sem_texts(raw: dict) -> dict:
    """{SEM base id: [line texts]} found in the row (for the lint exemptions)."""
    out = {}
    txt = "\n".join([raw.get("card") or "", raw.get("instructions") or ""] +
                    PZ.atoms(raw.get("state") or "", raw["meta"]["format_style"])["texts"])
    for ln in PZ.clean_lines(txt):
        m = PZ.match_sem(ln)
        if m:
            out.setdefault(m[0][:6], []).append(ln)
    return out


def check_file(path, side_path, rels_path, tools, *, training: bool, s5: bool) -> dict:
    rows = CM.read_jsonl(path)
    sides = {x["id"]: x for x in CM.read_jsonl(side_path)} if side_path else {}
    rels = CM.read_jsonl(rels_path) if rels_path else []
    rep = collections.Counter()
    td = fcard._td()
    td.check_rows(rows)
    rep["check_rows_ok"] = len(rows)
    held = fpool.held_out_style_ids()
    maxtok = 0
    tok_hist = collections.Counter()
    yn_rows = [r for r in rows if r["qtype"] == "noul"]
    for r in rows:
        m = r["meta"]
        rep["rows"] += 1
        # provenance / lints
        if r["source"] != CM.SOURCE or r["source"] in CM.KD_FULL_SRC:
            rep["fail:source"] += 1
        if "option_level" in m:
            rep["fail:G18_option_level"] += 1
        if "teacher" in m:
            rep["fail:teacher"] += 1
        if training and (m["sampler"] == "S5" or m["format_style"] in held):
            rep["fail:held_out_in_training"] += 1
        if s5 and (m["sampler"] != "S5" or m["format_style"] not in held):
            rep["fail:s5_not_held_out"] += 1
        for k in ("family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed",
                  "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id",
                  "defs_style", "twin_of", "twin_kind", "text_source", "licence", "edge", "subtype"):
            if k not in m:
                rep[f"fail:meta_missing:{k}"] += 1
        if m["depth"] > 6:
            rep["fail:depth>6"] += 1
        if r["qtype"] == "choice" and m.get("gold_probs") is not None:
            if set(m["gold_probs"]) != set(r["options"]):
                rep["fail:gold_probs_keys"] += 1
        st = sem_texts(r)
        probs = lints.lint_row({**r, "_q": None}, st)
        for p in probs:
            rep["fail:lint:" + p[:50]] += 1
        # G3: parse, solve, map to gold, render hash
        try:
            P = PZ.parse_row(r)
            S2 = PZ.assemble(P, r)
            rb = SB.solve(S2)
            keys = PZ.option_keys(S2, r)
            gold_text = r["gold"] if r["qtype"] == "choice" else ("Yes" if r["gold"] == 1 else "No")
            want = keys.get(gold_text)
            got = rb["ans"]
            if S2["form"] == "rank_order" and isinstance(got, tuple) and S2.get("subset") and \
                    got.index(S2["subset"]["X"]) not in S2["subset"]["pos"]:
                got = "NOTA"
            if want != got:
                rep["fail:G3_solverB_vs_gold"] += 1
            else:
                rep["G3_solverB_agree"] += 1
            if side_path:
                if H.render_hash(S2) == sides[r["id"]]["render_hash"]:
                    rep["G3_render_hash_match"] += 1
                else:
                    rep["fail:G3_render_hash"] += 1
            if S2["form"] == "pred":
                gp = rb.get("gold_probs")
                if gp is None or abs(max(m["gold_probs"].values()) - float(max(gp))) > 1e-12:
                    rep["fail:pred_gold_probs"] += 1
        except Exception as e:  # noqa: BLE001
            rep["fail:G3_parse:" + type(e).__name__ + ":" + str(e)[:40]] += 1
        # G15: loader_check under 3 random orders, exact token length
        rng = random.Random(CM.h64("g15", r["id"]))
        n = len(r["options"]) if r["qtype"] == "choice" else 2
        okall = True
        for t in range(3):
            perm = list(range(n))
            rng.shuffle(perm)
            res = fcard.loader_check(r, perm=perm, check_rows=False)
            okall &= res["ok"]
        rep["G15_loader_ok" if okall else "fail:G15_loader"] += 1
        ntok = tools.tokens_exact(r, perm)
        maxtok = max(maxtok, ntok)
        tok_hist[min(ntok // 250 * 250, 2000)] += 1
        if ntok >= 2000:
            rep["fail:len>=2000"] += 1
        if ntok > 7900:
            rep["fail:len>7900"] += 1
    # relation units
    by_call = collections.defaultdict(list)
    for r in rows:
        by_call[r["call_id"]].append(r["id"])
    for c, ids in by_call.items():
        if len(ids) > 3:
            rep["fail:unit>3"] += 1
    rid = {r["id"]: r for r in rows}
    for x in rels:
        if x["a"] in rid and x["b"] in rid and rid[x["a"]]["call_id"] != rid[x["b"]]["call_id"]:
            rep["fail:relation_call_id"] += 1
    # negcount quotas on YN rows (k_syn from the sidecar, computed by c_src/common/negcount.py)
    if sides and yn_rows:
        ks = [sides[r["id"]]["k_syn"] for r in yn_rows]
        rep["yn_rows"] = len(yn_rows)
        rep["yn_ksyn>=1"] = sum(1 for k in ks if k >= 1)
        twins = {r["meta"]["twin_of"] for r in rows if r["meta"]["twin_of"]}
        # k_syn >= 2 rows whose affirmative partner (same call_id, k_syn 0) is in the file
        call_aff = {r["call_id"] for r in yn_rows if sides[r["id"]]["k_syn"] == 0}
        rep["yn_ksyn>=2_with_aff"] = sum(1 for r in yn_rows if sides[r["id"]]["k_syn"] >= 2 and r["call_id"] in call_aff)
    rep["max_tokens"] = maxtok
    rep["tok_hist"] = dict(sorted(tok_hist.items()))
    return dict(rep)


if __name__ == "__main__":
    import build
    tools = build.Tools()
    out = {}
    for spec in sys.argv[1:]:
        name, rows, side, rels, kind = spec.split(",")
        out[name] = check_file(rows, side or None, rels or None, tools, training=(kind == "train"),
                               s5=(kind == "dev"))
        print(name, json.dumps(out[name])[:3000], flush=True)
