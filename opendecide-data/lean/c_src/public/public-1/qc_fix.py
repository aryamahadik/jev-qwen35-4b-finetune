#!/usr/bin/env python3
"""public-1 fix QC (counts and ids only; prints no row text). Checks the review-public-1 items on out/ files:

  leak   : mix-tuning-dev split (spec 3.1 / 10 S7): page titles shared dev vs train+reserve (meta titles), paragraphs
           of >= 25 words shared (review's block split), dev paragraphs sharing any >= 8-word sentence with a train or
           reserve row, SQuAD dev passages inside train/reserve states (normalised substring), train/reserve rows that
           show a dev-hash page, group / record / article overlap.
  golden : shown paragraphs with >= 50% of their word 10-grams in C1 golden_train (review method, tmp/golden_g10.npy);
           v1.2 (repair round 1): the gate fails on ANY shared 10-gram in any shown block of >= 10 words.
  dupes  : rows that show the same paragraph twice (normalised text of a block, >= 25 words).
  g15    : train_decoder.check_rows (kd 0 and 0.5); fmt1 card.loader_check on every row (cygnet + schema_branch_mark,
           random option order, gold letter maps back) with must_show = the row's card text (wherever it is routed);
           the card also inside decoder_io.user_msg in the od/text_first style; real-tokenizer length of the full chat
           prompt (<= 7,900; rows >= 2,000 counted); call-id units.
  cue    : MuSiQue choice rows, 'pick the option whose title is in the question' accuracy vs chance.

Usage: qc_fix.py --out-dir out [--cards tmp/row_cards.json] [--only leak,golden,dupes,g15,cue] --json logs/qc_fix.json
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE / "lib"))
from common import is_dev_page, norm_title  # noqa: E402
from textnorm import norm, sent_hashes  # noqa: E402

SNAP = os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/"
                          "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
SPLIT = re.compile(r"\n\s*\n|\n(?=\[\d+\] |Paragraph \d+: |## \d+\. |<doc |- |### |Title: )")
WIKI = ("c_pub_squad2", "c_pub_musique", "c_pub_2wiki")


def load(d, name):
    return [json.loads(l) for l in open(Path(d) / name)]


def state_text(r):
    st = r["state"] or ""
    if st.lstrip().startswith("{"):
        try:
            st = json.loads(st).get("passage", st)
        except Exception:  # noqa: BLE001
            pass
    return st


def blocks(r, min_words=25):
    out = []
    for b in SPLIT.split(state_text(r)):
        n = norm(b)
        if n.count(" ") + 1 >= min_words:
            out.append(n)
    return out


def bhash(n):
    return hashlib.sha1(n.encode()).hexdigest()


def titles(r):
    m = r["meta"]
    t = set()
    if m.get("page_title"):
        t.add(norm_title(m["page_title"]))
    for x in m.get("page_titles") or []:
        t.add(norm_title(x))
    for x in m.get("supporting_titles") or []:
        t.add(norm_title(x))
    return t


def check_leak(parts):
    res = {}
    tr = [r for r in parts["main"] + parts["reserve"] if r["source"] in WIKI]
    dv = [r for r in parts["dev"] if r["source"] in WIKI]
    tt = collections.Counter()
    for r in tr:
        for t in titles(r):
            tt[t] += 1
    dt = set().union(*(titles(r) for r in dv)) if dv else set()
    res["shared_titles_dev_vs_train_reserve"] = len(dt & set(tt))
    res["train_reserve_rows_showing_a_dev_title"] = sum(1 for r in tr if titles(r) & dt)
    # paragraphs (review block split, >= 25 words)
    trb = set()
    for r in tr:
        trb |= {bhash(b) for b in blocks(r)}
    res["dev_rows_sharing_a_paragraph_with_train_reserve"] = dict(collections.Counter(
        r["source"] for r in dv if {bhash(b) for b in blocks(r)} & trb))
    res["shared_paragraphs"] = len({bhash(b) for r in dv for b in blocks(r)} & trb)
    # sentence level (>= 8 words): any dev sentence inside a train / reserve row
    trs = set()
    for r in tr:
        trs |= set(sent_hashes(state_text(r)))
    res["dev_rows_sharing_a_sentence_with_train_reserve"] = dict(collections.Counter(
        r["source"] for r in dv if set(sent_hashes(state_text(r))) & trs))
    # SQuAD dev passages inside train / reserve states (normalised substring)
    sq_dev = set()
    for r in dv:  # the passage is the longest line of the state (JSON style: its "passage" field)
        if r["source"] == "c_pub_squad2":
            sq_dev.add(norm(max(state_text(r).split("\n"), key=len)))
    big = [norm(state_text(r)) for r in tr]
    res["squad_dev_passages"] = len(sq_dev)
    res["squad_dev_passages_inside_train_reserve_rows"] = sum(1 for p in sq_dev if any(p in s for s in big))
    # dev-hash pages shown in train / reserve rows (meta titles)
    res["train_reserve_rows_showing_a_dev_hash_page"] = dict(collections.Counter(
        r["source"] for r in tr if any(is_dev_page(t) for t in titles(r))))
    # review's 10-gram view: dev rows with any / > 50% of their state+instructions word 10-grams in train or reserve
    from grams import gram_hashes
    import numpy as np
    trg = np.unique(np.concatenate([gram_hashes((r["state"] or "") + " " + (r["instructions"] or "")) for r in tr]
                                   or [np.zeros(0, dtype=np.uint64)]))
    g10 = collections.Counter()
    for r in dv:
        g = gram_hashes((r["state"] or "") + " " + (r["instructions"] or ""))
        if g.size:
            share = float(np.isin(g, trg).mean())
            g10[r["source"] + ("|>50%" if share > 0.5 else "|any" if share > 0 else "|none")] += 1
    res["dev_rows_10gram_overlap_with_train_reserve"] = dict(g10)
    allp = parts["main"] + parts["reserve"]
    res["group_overlap"] = len({r["group_id"] for r in allp} & {r["group_id"] for r in parts["dev"]})
    res["article_overlap"] = len({r["meta"].get("article_id") for r in allp if r["meta"].get("article_id")}
                                 & {r["meta"].get("article_id") for r in parts["dev"] if r["meta"].get("article_id")})
    res["record_overlap"] = len({str(r["meta"]["text_source"]["record_id"]).split("#")[0] for r in allp}
                                & {str(r["meta"]["text_source"]["record_id"]).split("#")[0] for r in parts["dev"]})
    return res


def check_golden(parts, idx_path):
    from grams import GramIndex
    gi = GramIndex(idx_path)
    res = {"by": {}, "ids_ge_0.5": {}, "ids_any": {}}
    for p, rows in parts.items():
        for r in rows:
            k = f"{r['source']}|{p}"
            a = res["by"].setdefault(k, collections.Counter())
            mx = 0.0
            for b in SPLIT.split(state_text(r)):
                if len(b.split()) < 10:
                    continue
                c = gi.coverage(b)
                a["paras"] += 1
                a["cov_gt_0"] += c > 0
                a["cov_ge_0.2"] += c >= 0.2
                a["cov_ge_0.5"] += c >= 0.5
                mx = max(mx, c)
            if mx >= 0.5:
                res["ids_ge_0.5"].setdefault(p, []).append(r["id"])
            if mx > 0:
                res["ids_any"].setdefault(p, []).append(r["id"])
    res["by"] = {k: dict(v) for k, v in res["by"].items()}
    res["rows_ge_0.5"] = {p: len(v) for p, v in res["ids_ge_0.5"].items()}
    res["rows_any_shared_10gram"] = {p: len(v) for p, v in res["ids_any"].items()}
    res["ids_any"] = {p: v[:20] for p, v in res["ids_any"].items()}
    return res


def check_dupes(parts):
    res = collections.Counter()
    for p, rows in parts.items():
        for r in rows:
            if r["source"] not in WIKI:  # a story may repeat its own lines; only Wikipedia contexts are page sets
                continue
            bs = blocks(r, min_words=8)
            if len(bs) != len(set(bs)):
                res[f"{r['source']}|{p}"] += 1
    return dict(res)


_OPT = [re.compile(r"^Paragraph \d+ \((.*)\)$"), re.compile(r"^Paragraph \d+: (.*)$"),
        re.compile(r"^doc \d+ \((.*)\)$"), re.compile(r"^\d+\. (.*)$")]
_PAREN = re.compile(r"\s*\([^()]*\)\s*$")
_QRE = [re.compile(r"\n\nQuestion: (.*)$", re.S), re.compile(r"^Question: (.*?)\n\n", re.S),
        re.compile(r"\n# Question\n(.*)$", re.S)]


def check_cue(parts):
    """MuSiQue choice rows: rule 'pick the option whose page title (or its base without a trailing parenthesis) is a
    whole-word part of the question; else guess' vs chance (option titles parsed from the four option-label forms)."""
    res = {}
    for p, rows in parts.items():
        mu = collections.Counter()
        for r in rows:
            if r["source"] != "c_pub_musique" or r["qtype"] != "choice":
                continue
            st = r["state"]
            q = None
            for rx in _QRE:
                m = rx.search(st)
                if m:
                    q = m.group(1)
                    break
            if q is None:
                mu["question_not_parsed"] += 1
                continue
            qn = f" {norm(q)} "

            def title(o):
                for rx in _OPT:
                    m = rx.match(o)
                    if m:
                        return m.group(1)
                return o

            def has(o):
                t = title(o)
                return any(x and f" {x} " in qn for x in {norm(t), norm(_PAREN.sub("", t))})
            k = len(r["options"])
            hits = [o for o in r["options"] if has(o)]
            mu["rows"] += 1
            mu["chance"] += 1 / k
            mu["gold_title_in_q"] += r["gold"] in hits
            mu["distractor_options_title_in_q"] += sum(o != r["gold"] for o in hits)
            mu["rule_correct"] += (1 / len(hits) if r["gold"] in hits else 0) if hits else 1 / k
        if mu["rows"]:
            n = mu["rows"]
            g, d = mu["gold_title_in_q"], mu["distractor_options_title_in_q"]
            res[p] = {"rows": n, "rule_acc": round(mu["rule_correct"] / n, 4), "chance": round(mu["chance"] / n, 4),
                      "gold_title_in_q": g, "distractor_options_title_in_q": d,
                      "p_gold_given_title_in_q": round(g / max(1, g + d), 4),
                      "question_not_parsed": mu["question_not_parsed"]}
    return res


def check_g15(parts, cards):
    sys.path.insert(0, str(LEAN))
    sys.path.insert(0, str(LEAN / "c_src" / "formats" / "formats-1"))
    from fmt1 import card as fcard  # pinned decoder_io / train_decoder (sha checked by fmt1)
    dio = fcard._dio()
    td = fcard._td()
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(SNAP, local_files_only=True)
    res = {}
    for p, rows in parts.items():
        out = collections.Counter()
        for kd in (0.0, 0.5):
            try:
                td.check_rows(rows, kd=kd)
                out[f"check_rows_kd{kd}_pass"] = 1
            except Exception as e:  # noqa: BLE001
                out[f"check_rows_kd{kd}_FAIL"] = 1
                res.setdefault("errors", []).append(f"{p} kd{kd}: {str(e)[:200]}")
        fails = collections.Counter()
        lens = collections.defaultdict(list)
        over = []
        for r in rows:
            card = cards.get(r["id"]) if cards is not None else r.get("card")
            ms = [card] if card else []
            chk = fcard.loader_check(r, must_show=ms, seed="public1-fix-g15", check_rows=False)
            out["rows"] += 1
            if card:
                out["carded_rows"] += 1
            if not chk["ok"]:
                for pr in chk["problems"]:
                    fails[f"{r['source']}|{r['qtype']}|{pr[:60]}"] += 1
                if card and any("must_show" in pr for pr in chk["problems"]):
                    out["carded_rows_card_missing_cygnet"] += 1
            # card visible in od/text_first too
            saved = (dio.STYLE, dio.LAYOUT)
            try:
                dio.STYLE, dio.LAYOUT = "od", "text_first"
                m2 = dio.user_msg(r, list(range(len(r["options"]))) if r.get("options") else None)
            finally:
                dio.STYLE, dio.LAYOUT = saved
            if card and " ".join(card.split()) not in " ".join(m2.split()):
                out["carded_rows_card_missing_od"] += 1
            # real tokens of the served prompt (cygnet, schema_branch_mark)
            dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
            lr = dio.as_letter_row(r)
            perm = list(range(len(lr["options"])))
            txt = dio.render_chat(tok, dio.CYGNET_SYSTEM, dio.user_msg(r, perm))
            n = len(tok(txt, add_special_tokens=False)["input_ids"])
            lens[r["source"]].append(n)
            if n > 7900:
                over.append(r["id"])
        calls = collections.Counter(r["call_id"] for r in rows)
        big_units = sum(1 for r in rows if calls[r["call_id"]] > 1)
        res[p] = {**dict(out), "loader_fail_kinds": dict(fails), "rows_over_7900": over,
                  "rows_in_multi_row_call_units": big_units,
                  "real_tokens": {s: {"n": len(v), "median": sorted(v)[len(v) // 2], "max": max(v),
                                      "ge2000": sum(x >= 2000 for x in v)} for s, v in lens.items()},
                  "long_rows_ge2000": sum(x >= 2000 for v in lens.values() for x in v),
                  "tokens_total": sum(sum(v) for v in lens.values()),
                  "long_tokens": sum(x for v in lens.values() for x in v if x >= 2000)}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(HERE / "out"))
    ap.add_argument("--cards", default=None, help="json {row id: card text as authored} (else the row's card field)")
    ap.add_argument("--only", default="leak,golden,dupes,cue,g15")
    ap.add_argument("--json", default=None)
    ap.add_argument("--gate", action="store_true", help="exit 1 unless every review pass condition holds")
    a = ap.parse_args()
    parts = {"main": load(a.out_dir, "public1_rows_r1.jsonl"), "reserve": load(a.out_dir, "public1_reserve.jsonl"),
             "dev": load(a.out_dir, "public1_mtdev.jsonl")}
    only = set(a.only.split(","))
    res = {"rows": {p: len(v) for p, v in parts.items()}}
    if "leak" in only:
        res["leak"] = check_leak(parts)
    if "golden" in only:
        res["golden"] = check_golden(parts, HERE / "tmp" / "golden_g10.npy")
    if "dupes" in only:
        res["dupes"] = check_dupes(parts)
    if "cue" in only:
        res["cue"] = check_cue(parts)
    if "g15" in only:
        cards = json.load(open(a.cards)) if a.cards else None
        res["g15"] = check_g15(parts, cards)
    fails = []
    if a.gate:
        L = res.get("leak", {})
        for k in ("shared_titles_dev_vs_train_reserve", "train_reserve_rows_showing_a_dev_title", "shared_paragraphs",
                  "squad_dev_passages_inside_train_reserve_rows", "group_overlap", "article_overlap", "record_overlap"):
            if L.get(k, 0):
                fails.append(f"leak:{k}={L[k]}")
        for k in ("dev_rows_sharing_a_paragraph_with_train_reserve", "dev_rows_sharing_a_sentence_with_train_reserve",
                  "train_reserve_rows_showing_a_dev_hash_page"):
            if L.get(k):
                fails.append(f"leak:{k}")
        if res.get("golden", {}).get("rows_ge_0.5"):
            fails.append("golden:rows_ge_0.5")
        if res.get("golden", {}).get("rows_any_shared_10gram"):
            fails.append("golden:rows_any_shared_10gram")
        if res.get("dupes"):
            fails.append("dupes")
        for p, x in res.get("g15", {}).items():
            if p == "errors":
                fails.append("g15:check_rows")
                continue
            if x.get("loader_fail_kinds") or x.get("rows_over_7900") or x.get("carded_rows_card_missing_cygnet") \
                    or x.get("carded_rows_card_missing_od") or x.get("rows_in_multi_row_call_units"):
                fails.append(f"g15:{p}")
        res["gate"] = {"pass": not fails, "fails": fails}
    s = json.dumps(res, indent=1, default=str)
    if a.json:
        Path(a.json).write_text(s)
    print(s)
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
