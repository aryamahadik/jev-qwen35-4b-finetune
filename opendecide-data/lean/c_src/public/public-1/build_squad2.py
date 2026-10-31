#!/usr/bin/env python3
"""SQuAD 2.0 builder (C_DATA_SPEC v4 3.2 #1): answerability decisions from human is_impossible gold.

Framings: (YN) "does the passage answer the question?" over answerable/unanswerable contrast pairs from one paragraph;
(CH) "which listed question does / does not the passage answer?" (3-4 questions from one paragraph, exactly one of the
other kind). Train split only; MuSiQue dev/test single-hop ids dropped (by id and by question text); split by page
title (10% mix-tuning dev); paragraphs with any sentence already in C1 golden_train are not used.
v1.1 (review-public-1): a paragraph with >= 50% of its word 10-grams in golden_train is not used; two phases:
`--phase dev` builds the mix-tuning-dev rows and writes tmp/devx_squad2.json (titles, paragraph and sentence hashes
the dev rows show); `--phase train` (after every Wikipedia set's dev phase) drops every train paragraph whose page
title, paragraph or any sentence is shown by a dev row of SQuAD 2.0, MuSiQue or 2Wiki (lib/common.DevX).
v1.2 (repair round 1, PREREG A29 a):
  - yes/no G6 root cause (metadata-only 0.53-0.57): SQuAD 2.0's unanswerable questions differ in length from the
    answerable ones, and the wording polarity is in the metadata, so length x polarity predicted the label. A pair now
    uses the answerable / unanswerable questions of the paragraph whose lengths differ least (<= 2 characters);
  - choice G6 root cause (options-only / question+option 0.38-0.44 vs 0.36): the option count k was drawn from what
    each paragraph allows, so inverted rows (gold = the one unanswerable question) had larger k than direct rows and
    'unanswerable-looking' options were gold more often than 1/k. Rows are now taken in equal numbers of direct and
    inverted rows per k, so each style of question is gold in 1/k of the rows that show it;
  - question-style cue (G6 'question x wording' 0.53 and choice 'question + option' 0.40 vs 0.36 on the first v1.2 QC
    sample): SQuAD 2.0's unanswerable questions have a recognisable style (crowd edits of answerable ones), and the
    wording polarity / direct-vs-inverted framing tells which style is gold. A cross-fitted question-style score
    s(q) = P(unanswerable | question words) (logistic regression on word 1-2 grams over every train-side SQuAD 2.0
    question, 5 folds by article; selection only, never a label input) now (a) matches each yes/no pair on s
    (|s(a) - s(u)| <= 0.15, smallest first, with the length match) and (b) balances choice rows so that the gold is the
    option whose style points to it (direct: lowest s; inverted: highest s) on 1/k of the rows, and the longest on 1/k;
    v1.2b: units whose gold is tied for the longest option are not used (G10 splits a tie; 'longest' is then exact);
    v1.2c: exact cell quotas. A (k, framing) cell whose pool cannot fill the (style-top x longest) quotas is cut to
    the largest size that fills them exactly (never filled from other cells: the it6 QC sample ran out of units and
    took every unit, so the style-top share fell back to its natural rate and G6 read b 0.386 / a 0.389 vs 0.361);
    the per-k count is the same on both framings; unchanged when the pools are large enough (main, reserve, dev);
  - golden_train: v1.2 GoldenIndex on the paragraph and on every question used;
  - `--qc N`: separate G6 QC sample from the same row generators over paragraphs not used by main, reserve or dev (each
    such paragraph gives its yes/no pair and its choice row) to tmp/qcs_squad2.json.
Output: tmp/devrows_squad2.json (dev phase), tmp/cand_squad2.json {main, reserve, dev, stats} (train phase).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from common import (GoldenIndex, DevX, base_meta, is_dev_page, licence_string, make_row, rng, sha,  # noqa
                    stable_shuffle, write_devx, TMP)
from textnorm import norm  # noqa: E402
import pools as P  # noqa: E402
from pickbal import take_choice_balanced, longest_is_gold  # noqa: E402

DS = "squad2"
DATASET = "SQuAD 2.0"
N_MAIN = {"yn": 540, "ch": 360}
RES_FRAC = 0.25
N_DEV = {"yn": 36, "ch": 24}


def style_scores(data, folds=5):
    """v1.2: cross-fitted P(unanswerable | question words) for every SQuAD 2.0 train question (selection balance only).
    Fitted on train-side (non-dev page) questions, 5 folds by article; dev-side questions are scored by the model
    fitted on every train-side question."""
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    qs = []
    for art in data:
        title = art["title"].replace("_", " ")
        dev = is_dev_page(title)
        f = -1 if dev else int(sha(f"{DS}|stylefold|{title}")[:8], 16) % folds
        for para in art["paragraphs"]:
            for q in para["qas"]:
                qs.append((q["id"], q["question"].strip(), int(q["is_impossible"]), f))
    y = np.array([x[2] for x in qs])
    fo = np.array([x[3] for x in qs])
    out = {}

    def fit_score(tr, te):
        tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
        X = tv.fit_transform([qs[i][1] for i in tr])
        m = LogisticRegression(C=1.0, max_iter=3000, solver="liblinear").fit(X, y[tr])
        p = m.predict_proba(tv.transform([qs[i][1] for i in te]))[:, 1]
        for i, v in zip(te, p):
            out[qs[i][0]] = float(v)
    for f in range(folds):
        fit_score(np.where((fo >= 0) & (fo != f))[0], np.where(fo == f)[0])
    fit_score(np.where(fo >= 0)[0], np.where(fo < 0)[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["dev", "train"], required=True)
    ap.add_argument("--qc", type=int, default=0, help="G6 QC-sample rows per framing (train phase)")
    a_ = ap.parse_args()
    phase, QC = a_.phase, a_.qc
    devx = DevX() if phase == "train" else None
    gi = GoldenIndex()
    lic = licence_string(DS)
    drop = json.load(open(HERE / "raw/musique/dev_test_singlehop_questions_v1.0.json"))["squad2"]
    drop_ids = {d["id"] for d in drop}
    drop_q = {norm(d["question"]) for d in drop}
    data = json.load(open(HERE / "raw/squad2/train-v2.0.json"))["data"]
    st = Counter()
    sty = style_scores(data)
    pools = {"train": {"yn": [], "ch": []}, "dev": {"yn": [], "ch": []}}
    spare = {"yn": [], "ch": []}  # v1.2: the framing a paragraph was not drawn for (G6 QC sample only)
    for art in data:
        title = art["title"].replace("_", " ")
        for pi, para in enumerate(art["paragraphs"]):
            ctx = para["context"].strip()
            st["paragraphs"] += 1
            why = gi.bad(ctx) or gi.bad(title + "\n" + ctx)  # v1.2b: + shown form (title line + passage)
            if why:
                st[f"para_golden_{why}"] += 1
                continue
            split = "dev" if is_dev_page(title) else "train"
            if (split == "dev") != (phase == "dev"):
                continue
            if devx is not None and devx.blocked(title, ctx):
                st["para_train_blocked_by_devx"] += 1
                continue
            A, U, seenq = [], [], set()
            for q in para["qas"]:
                qn = norm(q["question"])
                if q["id"] in drop_ids or qn in drop_q:
                    st["q_drop_musique_devtest"] += 1
                    continue
                if not qn or qn in seenq:
                    st["q_dup_or_empty"] += 1
                    continue
                if gi.bad(q["question"]):
                    st["q_drop_golden"] += 1
                    continue
                seenq.add(qn)
                (U if q["is_impossible"] else A).append(q)
            gkey = sha(title + "|" + ctx)[:16]
            r = rng(DS, "para", gkey)
            # v1.2: the yes/no pair is length-matched (|len a - len u| <= 2) and style-matched (|s(a) - s(u)| <= 0.15),
            # smallest style gap first (ties broken by the paragraph's rng)
            prs = sorted((abs(sty[a["id"]] - sty[u["id"]]), r.random(), ai, ui)
                         for ai, a in enumerate(A) for ui, u in enumerate(U)
                         if abs(len(a["question"].strip()) - len(u["question"].strip())) <= 2)
            can_yn = bool(prs) and prs[0][0] <= 0.15
            if A and U and not can_yn:
                st["yn_no_matched_pair"] += 1
            can_ch = (len(A) >= 1 and len(U) >= 2) or (len(A) >= 2 and len(U) >= 1)
            if not (can_yn or can_ch):
                continue
            use = "yn" if (can_yn and (not can_ch or r.random() < 0.55)) else "ch"
            yn_u = {"title": title, "ctx": ctx, "g": gkey, "a": A[prs[0][2]], "u": U[prs[0][3]]} if can_yn else None
            if use == "yn":
                pools[split]["yn"].append(yn_u)
            if use == "ch" or (can_ch and split == "train"):
                inv_ok = len(A) >= 2 and len(U) >= 1
                norm_ok = len(A) >= 1 and len(U) >= 2
                inv = inv_ok and (not norm_ok or r.random() < 0.5)
                gold_pool, other_pool = (U, A) if inv else (A, U)
                k = r.choice([k for k in (2, 3, 4) if len(other_pool) >= k - 1] or [2])
                if len(other_pool) < k - 1:
                    continue
                gold = r.choice(gold_pool)
                others = r.sample(other_pool, k - 1)
                opts = [gold["question"].strip()] + [o["question"].strip() for o in others]
                if len({norm(o) for o in opts}) != len(opts):
                    st["ch_dup_option"] += 1
                    continue
                L_ = [len(o) for o in opts]
                if L_[0] == max(L_) and L_.count(max(L_)) > 1:
                    # v1.2b: gold tied for the longest option. G10 counts a tie as a 1/t share of 'longest is gold'
                    # while the balance below counts only a strictly longest gold, so the k=2 bucket read 52.9%.
                    st["ch_skip_gold_tied_longest"] += 1
                    continue
                opts = stable_shuffle(opts, DS, "opts", gkey)
                so = [sty[o["id"]] for o in others]
                top = sty[gold["id"]] > max(so) if inv else sty[gold["id"]] < min(so)
                cu = {"title": title, "ctx": ctx, "g": gkey, "inv": inv, "gold": gold, "top": top,
                      "others": others, "opts": opts, "k": k, "lg": longest_is_gold(opts, gold["question"].strip())}
                (pools[split]["ch"] if use == "ch" else spare["ch"]).append(cu)
            if use == "ch" and can_yn and split == "train":
                spare["yn"].append(yn_u)
    for s in pools:
        for f in pools[s]:
            st[f"pool_{s}_{f}"] = len(pools[s][f])
    st["spare_yn"], st["spare_ch"] = len(spare["yn"]), len(spare["ch"])

    def take_ch_kinv(cands, n_per_inv, key):
        """v1.2: n_per_inv direct and n_per_inv inverted rows with the SAME count per k on both sides (k allocated in
        proportion to min(direct, inverted) availability); longest-gold balanced inside each (k, inv) cell.
        Returns (picked, leftover)."""
        av = {(k, inv): [u for u in cands if u["k"] == k and u["inv"] == inv] for k in (2, 3, 4) for inv in (False, True)}
        m = {k: min(len(av[(k, False)]), len(av[(k, True)])) for k in (2, 3, 4)}
        tot = sum(m.values())
        n_per_inv = min(n_per_inv, tot)
        alloc, rem = {}, n_per_inv
        for i, k in enumerate((2, 3, 4)):
            alloc[k] = min(m[k], rem if i == 2 else round(n_per_inv * m[k] / max(1, tot)))
            rem -= alloc[k]
        for k in (2, 3, 4):  # top up rounding shortfalls
            extra = min(rem, m[k] - alloc[k])
            alloc[k] += extra
            rem -= extra
        # v1.2c: exact quotas on both framings; a cut is moved to another k only where that k still fills exactly
        capk = {k: min(feasible(av[(k, False)], m[k], k), feasible(av[(k, True)], m[k], k)) for k in (2, 3, 4)}
        for k in (2, 3, 4):
            cut = alloc[k] - min(alloc[k], capk[k])
            alloc[k] -= cut
            rem += cut
            st[f"cap_cut_{key}-k{k}"] = cut
        for k in (2, 3, 4):
            extra = min(rem, capk[k] - alloc[k])
            alloc[k] += extra
            rem -= extra
        picked, left = [], []
        for k in (2, 3, 4):
            for inv in (False, True):
                got, lf = take_top_lg(av[(k, inv)], alloc[k], f"{key}-k{k}-{inv}", k)
                picked += got
                left += lf
        return picked, left

    def quotas(n, k):
        want = {(t, l): n * (1 / k if t else 1 - 1 / k) * (1 / k if l else 1 - 1 / k)
                for t in (True, False) for l in (True, False)}
        q = {c: int(v) for c, v in want.items()}
        for c in sorted(want, key=lambda c: -(want[c] - int(want[c])))[: n - sum(q.values())]:
            q[c] += 1
        return q

    def feasible(pool, n, k):
        """v1.2c: the largest n' <= n whose (style-top x longest) quotas the pool fills exactly."""
        have = Counter((u["top"], u["lg"]) for u in pool)
        while n > 0 and any(v > have[c] for c, v in quotas(n, k).items()):
            n -= 1
        return n

    def take_top_lg(pool, n, key, k):
        """v1.2: n units with 'gold is the style-top option' on 1/k and 'gold is strictly longest' on about 1/k
        (cells (top, lg), target shares the product of the margins; a short cell's quota moves to a not-top cell)."""
        by = {}
        for u in stable_shuffle(pool, DS, "toplg", key):
            by.setdefault((u["top"], u["lg"]), []).append(u)
        q = quotas(n, k)
        got = {c: by.get(c, [])[: q[c]] for c in q}
        short = sum(q[c] - len(got[c]) for c in q)
        for c in ((False, False), (False, True)):
            more = by.get(c, [])[len(got[c]): len(got[c]) + short]
            got[c] += more
            short -= len(more)
        st[f"toplg_short_{key}"] = short
        pk = [u for v in got.values() for u in v]
        ids = {id(u) for u in pk}
        return pk, [u for u in pool if id(u) not in ids]

    def yn_rows(units, tag):
        rows = []
        n_w = len(P.SQ_YN_WORDINGS)
        units = stable_shuffle(units, DS, "yn-order", tag)
        for j, u in enumerate(units):
            w = P.SQ_YN_WORDINGS[j % n_w]
            sty = P.SQ_STYLES[(j // n_w) % len(P.SQ_STYLES)]
            d = rng(DS, "defs", u["g"]).choices(P.DEFS_STYLES, weights=P.DEFS_WEIGHTS)[0]
            card = None if d == "none" else P.SQ_YN_CARDS[(w["pol"], d)]
            ids = {}
            pair = []
            for q, answerable in ((u["a"], True), (u["u"], False)):
                question = q["question"].strip()
                state = sty["yn"].format(passage=u["ctx"], question=question, title=u["title"],
                                         title_json=json.dumps(u["title"], ensure_ascii=False),
                                         passage_json=json.dumps(u["ctx"], ensure_ascii=False),
                                         question_json=json.dumps(question, ensure_ascii=False))
                pred = 1 if answerable else 0
                gold = pred if w["pol"] == "aff" else 1 - pred
                card_id = f"pub1_{DS}_yn_{w['id']}_{d}"
                meta = base_meta(family_block="3A", dataset=DATASET, record_id=q["id"], licence=lic, sa=True,
                                 card_id=card_id, wording_id=w["id"], defs_style=d, format_style=sty["id"],
                                 structure=f"{DS}|yn|{q['id']}", edge=["answerability"], depth=1,
                                 twin_kind="answerability_contrast",
                                 extra={"page_title": u["title"], "human_label": {"is_impossible": not answerable}})
                row = make_row(ds=DS, framing="yn", key=q["id"], group=u["g"], state=state,
                               instructions=w["text"], options=None, gold=gold,
                               role="aff" if w["pol"] == "aff" else "neg", card=card, meta=meta)
                pair.append(row)
            pair[0]["meta"]["twin_of"] = pair[1]["id"]
            pair[1]["meta"]["twin_of"] = pair[0]["id"]
            rows += pair
        return rows

    def ch_rows(units, tag):
        rows = []
        norm_w = [w for w in P.SQ_CH_WORDINGS if not w["inv"]]
        inv_w = [w for w in P.SQ_CH_WORDINGS if w["inv"]]
        cnt = Counter()
        for u in stable_shuffle(units, DS, "ch-order", tag):
            ws = inv_w if u["inv"] else norm_w
            j = cnt[u["inv"]]
            cnt[u["inv"]] += 1
            w = ws[j % len(ws)]
            sty = P.SQ_STYLES[(j // len(ws)) % len(P.SQ_STYLES)]
            d = rng(DS, "defs-ch", u["g"]).choices(P.DEFS_STYLES, weights=P.DEFS_WEIGHTS)[0]
            card = None if d == "none" else P.SQ_CH_CARDS[(u["inv"], d)]
            state = sty["ch"].format(passage=u["ctx"], title=u["title"],
                                     title_json=json.dumps(u["title"], ensure_ascii=False),
                                     passage_json=json.dumps(u["ctx"], ensure_ascii=False))
            gq = u["gold"]
            card_id = f"pub1_{DS}_ch_{w['id']}_{d}"
            meta = base_meta(family_block="3A", dataset=DATASET, record_id=gq["id"], licence=lic, sa=True,
                             card_id=card_id, wording_id=w["id"], defs_style=d, format_style=sty["id"],
                             structure=f"{DS}|ch|{gq['id']}|" + "|".join(sorted(o["id"] for o in u["others"])),
                             edge=["answerability", "inverted" if u["inv"] else "direct"], depth=1,
                             extra={"page_title": u["title"], "option_record_ids": [gq["id"]] + [o["id"] for o in u["others"]],
                                    "inverted": u["inv"]})
            rows.append(make_row(ds=DS, framing="ch", key=gq["id"] + "|" + ("inv" if u["inv"] else "dir"), group=u["g"],
                                 state=state, instructions=w["text"], options=u["opts"], gold=gq["question"].strip(),
                                 role="choice", card=card, meta=meta))
        return rows

    if phase == "dev":
        dev = yn_rows(stable_shuffle(pools["dev"]["yn"], DS, "yn-dev")[: N_DEV["yn"] // 2], "dev")
        shown = [(u["title"], u["ctx"]) for u in stable_shuffle(pools["dev"]["yn"], DS, "yn-dev")[: N_DEV["yn"] // 2]]
        dp, _ = take_ch_kinv(pools["dev"]["ch"], N_DEV["ch"] // 2, f"{DS}-chdev")
        for inv in (False, True):
            dpi = [u for u in dp if u["inv"] == inv]
            dev += ch_rows(dpi, f"dev{inv}")
            shown += [(u["title"], u["ctx"]) for u in dpi]
        st["rows_dev"] = len(dev)
        st["devx"] = write_devx(DS, shown)
        (TMP / f"devrows_{DS}.json").write_text(json.dumps({"dev": dev, "stats": st}, ensure_ascii=False))
        print(json.dumps(st, indent=0))
        return
    out = {"main": [], "reserve": [], "dev": [], "stats": st}
    # yes/no pairs
    tr = stable_shuffle(pools["train"]["yn"], DS, "yn-pick")
    n_pairs, n_res = N_MAIN["yn"] // 2, int(N_MAIN["yn"] * RES_FRAC) // 2
    out["main"] += yn_rows(tr[:n_pairs], "main")
    out["reserve"] += yn_rows(tr[n_pairs:n_pairs + n_res], "res")
    # choice: half direct, half inverted, equal per k (v1.2); longest-gold balanced
    n = N_MAIN["ch"] // 2
    pick, left = take_ch_kinv(pools["train"]["ch"], n, f"{DS}-ch")
    res, left = take_ch_kinv(left, int(n * RES_FRAC), f"{DS}-chres")
    for inv in (False, True):
        out["main"] += ch_rows([u for u in pick if u["inv"] == inv], f"main{inv}")
        out["reserve"] += ch_rows([u for u in res if u["inv"] == inv], f"res{inv}")
    if QC:  # separate G6 QC sample: paragraphs not used by main / reserve (dev pages are the other side)
        used_g = {u["g"] for u in tr[:n_pairs + n_res]} | {u["g"] for u in pick + res}
        qy = [u for u in tr[n_pairs + n_res:] + stable_shuffle(spare["yn"], DS, "yn-spare") if u["g"] not in used_g]
        qy = qy[: QC // 2]
        qcands = [u for u in left + spare["ch"] if u["g"] not in used_g]
        qc_ch, _ = take_ch_kinv(qcands, QC // 2, f"{DS}-chqc")
        qcs = yn_rows(qy, "qc")
        for inv in (False, True):
            qcs += ch_rows([u for u in qc_ch if u["inv"] == inv], f"qc{inv}")
        st["qc_rows_yn"], st["qc_rows_ch"] = 2 * len(qy), len(qc_ch)
        (TMP / f"qcs_{DS}.json").write_text(json.dumps({"qc": qcs}, ensure_ascii=False))
    dv = json.loads((TMP / f"devrows_{DS}.json").read_text())
    out["dev"] = dv["dev"]
    for k, v in dv["stats"].items():
        st[f"dev_phase:{k}"] = v
    for k in ("main", "reserve", "dev"):
        st[f"rows_{k}"] = len(out[k])
    for k_ in ("main", "reserve", "dev"):  # v1.2b: rendered-row golden re-check (count; expected 0)
        st[f"post_golden_{k_}"] = gi.post_check(out[k_])
    (TMP / f"cand_{DS}.json").write_text(json.dumps(out, ensure_ascii=False))
    print(json.dumps(st, indent=0))


if __name__ == "__main__":
    main()
