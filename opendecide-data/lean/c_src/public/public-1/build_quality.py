#!/usr/bin/env python3
"""QuALITY builder (C_DATA_SPEC v4 3.2 #4): long-document multiple choice from the human-written questions, options
and gold_label (validator consensus). Framings: (CH) the 4-option question; (NT) a "none of these" contrast pair from
one question: gold kept (gold + 2 distractors + none option, gold = the answer) and gold removed (3 distractors + none
option, gold = none). NT pairs use only questions where the writer and every untimed validator chose the gold and
every validator rated the question answerable. Article filter (logged per article): license/source is Gutenberg,
OANC/Slate or CC BY; Gutenberg transcriber notes and Project Gutenberg trademark lines stripped; article <= 7,200
real tokens and row <= 7,900. Split by article (10% mix-tuning dev). Articles with a sentence already in C1
golden_train are not used. Soft targets: untimed validator + writer vote shares on CH rows (meta.teacher,
teacher_src human_votes). Output: tmp/cand_quality.json, logs/quality_articles.json.
v1.1 (review-public-1): an article with a paragraph that has >= 50% of its word 10-grams in golden_train is not used;
choice-row cards are printed at the start of instructions (lib/common.make_row), and every row's length is the real
tokenizer length of the full chat prompt (decoder_io cygnet, schema_branch_mark) <= 7,900.
v1.2 (repair round 1, PREREG A29 a):
  - abstain policy (G7 / G10 / G6 root cause): the NT contrast pair showed the none option on 2 rows per question and
    made it gold on 1, so 'none' was gold on 50% of the rows that show it (G7 p0 = 1/4; options-only baselines picked
    it). NT is now ONE row per question: 'removed' (3 distractors + none, gold = none) on exactly 1 of every 4 NT rows
    (balanced over wording and none string), else 'kept' (gold + 2 distractors + none). The none option is gold on
    1/4 = 1/k of the rows that show it (G7) and wrong on 3/4 (G10 >= 50%);
  - option-cue balance (G6 root cause for the plain 4-option rows, options-only 0.30 vs 0.25 without the none
    option): QuALITY's human-written gold answers differ in wording and length from the distractors. A cross-fitted
    options-only cue score (logistic regressions on word 1-2 grams of the option, with and without option-length
    features, averaged; 10 folds by article, train articles only; never a label input) ranks each row's shown options. The G10 'longest option is
    gold' balance is generalised: rows are taken so that the gold is the top-cue option on 1/k of the rows and the gold's
    length rank is uniform over 1..k (kept NT rows: over the 4 shown options). Labels stay the dataset's gold;
  - golden_train: v1.2 GoldenIndex (no shared 10-gram, line or sentence) on every article paragraph, question and
    option.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from common import (GoldenIndex, base_meta, is_dev_record, licence_string, make_row, ntok, real_tokens, rng,  # noqa
                    sha, stable_shuffle, TMP, LOGS, MAX_ROW_TOKENS)
from textnorm import norm  # noqa: E402
import pools as P  # noqa: E402
from pickbal import take_choice_balanced, longest_is_gold  # noqa: E402

DS = "quality"
DATASET = "QuALITY"
SRC = HERE / "raw/quality/QuALITY.v1.0.1.htmlstripped.train"
ART_CAP = 7200
RES_FRAC = 0.25


def lic_class(r):
    lic = (r.get("license") or "")
    src = r.get("source") or ""
    if src == "Gutenberg" and "Project Gutenberg License" in lic:
        return "Gutenberg (US public domain; PG licence text)"
    if src == "Slate" and "anc.org/OANC/license" in lic:
        return "OANC/Slate (any use incl. commercial)"
    if src.startswith("misc-") and "CC BY 4.0" in lic:
        return "CC BY 4.0"
    return None


TN = re.compile(r"\[\s*Transcriber'?s?\s+Note:.*?\]", re.S | re.I)
REFERENTIAL = re.compile(r"^\s*(all|none|both|neither)\s+of\s+(the\s+)?(above|these|those|options|answers|choices)\b"
                         r"|^\s*(both|either)\s+[a-d]\s+(and|or)\s+[a-d]\b|^\s*[a-d]\s+and\s+[a-d]\b", re.I)
BOILER = [  # Gutenberg transcriber boilerplate (unbracketed form), never story text
    re.compile(r"Transcriber['\u2019]?s?\s+Note:?[ \t]*", re.I),
    re.compile(r"This\s+e-?text\s+was\s+produced\s+from\b[\s\S]{0,300}?\b(?:1[89]\d\d|20\d\d)\s*\.(?=\s|$)[ \t]*", re.I),
    re.compile(r"Extensive\s+research\s+did\s+not\s+uncover\s+any\s+evidence\s+that\s+the\s+U\.\s?S\.\s+copyright\s+on\s+this\s+publication\s+was\s+renewed\.[ \t]*", re.I),
    re.compile(r"Minor\s+spelling\s+and\s+typographical\s+errors\s+have\s+been\s+corrected\s+without\s+note\.[ \t]*", re.I),
]


def clean(text: str) -> tuple[str, dict]:
    log = {"transcriber_notes": len(TN.findall(text))}
    t = TN.sub("", text)
    n_bp = 0
    for pat in BOILER:
        t, k = pat.subn("", t)
        n_bp += k
    log["gutenberg_boilerplate_removed"] = n_bp
    lines = t.split("\n")
    pg = [ln for ln in lines if re.search(r"project gutenberg|gutenberg\.org|gutenberg-tm", ln, re.I)]
    log["pg_lines_removed"] = len(pg)
    t = "\n".join(ln for ln in lines if ln not in pg)
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n[ \t]+", "\n", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip(), log


def len_rank(shown, gold) -> int:
    """1 = the gold is strictly the longest shown option; ties count against the gold (rank = 1 + #options at least as
    long, other than the gold)."""
    lg = len(gold)
    return 1 + sum(1 for o in shown if o != gold and len(o) >= lg)


def cue_scores(cands, folds=10):
    """v1.2: cross-fitted options-only cue score per option (selection balance only, never a label input): logistic
    regression on tf-idf word 1-2 grams of the option text plus option-length features, averaged with a text-only
    logistic regression, 10 folds by article over the
    train candidates; dev candidates are scored by the model fitted on every train candidate."""
    import numpy as np
    from scipy.sparse import csr_matrix, hstack
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    def feats(u):
        L = [len(o) for o in u["opts"]]
        rows = []
        for j, o in enumerate(u["opts"]):
            m = [0.0] * 8
            m[sorted(L, reverse=True).index(L[j])] = 1.0
            m[4], m[5] = float(L[j] == max(L)), float(L[j] == min(L))
            m[6], m[7] = min(9, L[j] // 20) / 9, min(60, len(o.split())) / 60
            rows.append(m)
        return rows

    def fit(us):
        tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
        Xt = tv.fit_transform([o for u in us for o in u["opts"]])
        X = hstack([Xt, csr_matrix(np.array([m for u in us for m in feats(u)]))]).tocsr()
        y = np.array([int(j == u["g"]) for u in us for j in range(4)])
        return (tv, LogisticRegression(C=1.0, max_iter=3000, solver="liblinear").fit(X, y),
                LogisticRegression(C=1.0, max_iter=3000, solver="liblinear").fit(Xt, y))

    def score(model, us):
        tv, m, mt = model
        Xt = tv.transform([o for u in us for o in u["opts"]])
        X = hstack([Xt, csr_matrix(np.array([f for u in us for f in feats(u)]))]).tocsr()
        sc = (m.predict_proba(X)[:, 1] + mt.predict_proba(Xt)[:, 1]) / 2  # text+length and text-only, averaged
        for i, u in enumerate(us):
            u["cue"] = [float(x) for x in sc[4 * i: 4 * i + 4]]

    tr = cands["train"]["ch"] + cands["train"]["nt"]
    fold = lambda u: int(sha(f"{DS}|cuefold|{u['aid']}")[:8], 16) % folds  # noqa: E731
    for f in range(folds):
        score(fit([u for u in tr if fold(u) != f]), [u for u in tr if fold(u) == f])
    dv = cands["dev"]["ch"] + cands["dev"]["nt"]
    if dv:
        score(fit(tr), dv)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main", type=int, default=600, help="round-1 rows (600; 775 if Qasper's rows move here)")
    a = ap.parse_args()
    n_main = a.main
    n_nt = 2 * round(n_main * 0.4 / 2)          # v1.2: NT rows are single rows (was pairs)
    n_ch = n_main - n_nt
    n_dev = {"ch": 24, "nt": 16}
    st = Counter()
    gi = GoldenIndex()
    lic = licence_string(DS)
    rows_in = [json.loads(l) for l in open(SRC)]
    arts = {}
    qs = defaultdict(list)
    for r in rows_in:
        arts.setdefault(r["article_id"], r)
        for q in r["questions"]:
            qs[r["article_id"]].append(q)
    art_log = {}
    keep_art = {}
    for aid, r in arts.items():
        lc = lic_class(r)
        text, clog = clean(r["article"])
        n = ntok(text)
        rec = {"source": r["source"], "licence_class": lc, "tokens": n, **clog, "title": r["title"]}
        if lc is None:
            rec["kept"] = False; rec["why"] = "licence/source field not Gutenberg, OANC/Slate or CC BY"
        elif n > ART_CAP:
            rec["kept"] = False; rec["why"] = f"over {ART_CAP} tokens"
        elif gi.seen(text):
            rec["kept"] = False; rec["why"] = "sentence already in C1 golden_train"
        elif any(gi.bad(p) for p in text.split("\n\n") if p.strip()):
            rec["kept"] = False; rec["why"] = "a paragraph shares a 10-gram, line or sentence with C1 golden_train (v1.2)"
        else:
            rec["kept"] = True
            rec["split"] = "dev" if is_dev_record(DS, aid) else "train"
            keep_art[aid] = (r["title"].strip(), text)
        art_log[aid] = rec
        st["articles_kept" if rec.get("kept") else "articles_out"] += 1
    (LOGS / "quality_articles.json").write_text(json.dumps(art_log, indent=1, ensure_ascii=False))
    st.update(Counter(f"article_licence:{v['licence_class']}" for v in art_log.values() if v.get("kept")))

    cands = {"train": {"ch": [], "nt": []}, "dev": {"ch": [], "nt": []}}
    for aid, (title, text) in keep_art.items():
        split = art_log[aid]["split"]
        seenq = set()
        for q in qs[aid]:
            qn = norm(q["question"])
            if qn in seenq:
                continue
            seenq.add(qn)
            opts = [" ".join(o.split()) for o in q["options"]]  # v1.1: no line break inside an option (G15)
            if any(REFERENTIAL.search(o) for o in opts):
                st["q_option_refers_to_other_options"] += 1   # shuffling / dropping options would change its meaning
                continue
            if len({norm(o) for o in opts}) != 4 or any(not o for o in opts):
                st["q_bad_options"] += 1
                continue
            if gi.any_bad([q["question"]] + opts):
                st["q_drop_golden"] += 1
                continue
            g = int(q["gold_label"]) - 1
            if int(q["writer_label"]) - 1 != g:
                st["q_writer_ne_gold"] += 1
                continue
            vals = q.get("validation") or []
            votes = [int(v["untimed_answer"]) - 1 for v in vals] + [g]
            unanimous = all(int(v["untimed_answer"]) - 1 == g for v in vals) and len(vals) >= 3
            answerable = all(int(v.get("untimed_eval1_answerability", 0)) == 1 for v in vals)
            share = Counter(votes)
            teacher = {opts[i]: round(share.get(i, 0) / len(votes), 4) for i in range(4)}
            u = {"aid": aid, "qid": q["question_unique_id"], "q": q["question"].strip(), "opts": opts, "g": g,
                 "title": title, "text": text, "teacher": teacher, "difficult": int(q.get("difficult", 0))}
            r = rng(DS, "use", u["qid"])
            if unanimous and answerable and r.random() < 0.6:
                cands[split]["nt"].append(u)
            else:
                o2 = stable_shuffle(opts, DS, "opts", u["qid"])
                u["opts_sh"] = o2
                u["lg"] = longest_is_gold(o2, opts[g])
                cands[split]["ch"].append(u)
    for s in cands:
        for f in cands[s]:
            st[f"pool_{s}_{f}"] = len(cands[s][f])

    def ch_rows(units, tag):
        rows = []
        nw = len(P.QU_CH_WORDINGS)
        for j, u in enumerate(stable_shuffle(units, DS, "ch-o", tag)):
            w = P.QU_CH_WORDINGS[j % nw]
            sty = P.QU_STYLES[(j // nw) % len(P.QU_STYLES)]
            d = rng(DS, "defs", u["qid"]).choices(P.DEFS_STYLES, weights=P.DEFS_WEIGHTS)[0]
            card = None if d == "none" else P.QU_CH_CARDS[d]
            meta = base_meta(family_block="3B", dataset=DATASET, record_id=u["qid"], licence=lic, sa=False,
                             card_id=f"pub1_{DS}_ch_{w['id']}_{d}", wording_id=w["id"], defs_style=d,
                             format_style=sty["id"], structure=f"{DS}|ch|{u['qid']}", edge=["long_document"],
                             extra={"article_id": u["aid"], "article_licence": art_log[u["aid"]]["licence_class"],
                                    "teacher": u["teacher"], "teacher_src": "human_votes",
                                    "human_label": {"gold_label": u["g"] + 1, "difficult": u["difficult"]}})
            row = make_row(ds=DS, framing="ch", key=u["qid"], group=u["aid"],
                           state=sty["wrap"].format(title=u["title"], article=u["text"]),
                           instructions=w["text"].format(question=u["q"]), options=u["opts_sh"],
                           gold=u["opts"][u["g"]], role="choice", card=card, meta=meta)
            rows.append(row)
        return rows

    def nt_order(kept_u, removed_u, tag):
        """v1.2: interleave so that row j is 'removed' iff (j + j // 12) % 4 == 3 (1 in 4 per wording and none
        string)."""
        ku = stable_shuffle(kept_u, DS, "nt-o-k", tag)
        ru = stable_shuffle(removed_u, DS, "nt-o-r", tag)
        out = []
        while ku or ru:
            j = len(out)
            want_r = (j + j // 12) % 4 == 3
            src = ru if (want_r and ru) or not ku else ku
            u = src.pop(0)
            u["variant"] = "removed" if src is ru else "kept"
            out.append(u)
        return out

    def nt_rows(units, tag):
        rows = []
        nw = len(P.QU_NOTA_WORDINGS)
        for j, u in enumerate(units):
            w = P.QU_NOTA_WORDINGS[j % nw]
            sty = P.QU_STYLES[(j // nw) % len(P.QU_STYLES)]
            d = rng(DS, "defs-nt", u["qid"]).choices(P.DEFS_STYLES, weights=P.DEFS_WEIGHTS)[0]
            card = None if d == "none" else P.QU_NOTA_CARDS[d]
            r = rng(DS, "nt", u["qid"])
            nota = P.QU_NOTA_STRINGS[j % len(P.QU_NOTA_STRINGS)]
            gold_txt = u["opts"][u["g"]]
            dis = [o for i, o in enumerate(u["opts"]) if i != u["g"]]
            kept = stable_shuffle([gold_txt] + [o for o in dis if o != u["drop"]], DS, "ntk", u["qid"]) + [nota]
            removed = stable_shuffle(dis, DS, "ntr", u["qid"]) + [nota]
            pair = []
            for var, opts, gold in (("kept", kept, gold_txt), ("removed", removed, nota)):
                if var != u["variant"]:
                    continue
                meta = base_meta(family_block="3B", dataset=DATASET, record_id=u["qid"], licence=lic, sa=False,
                                 card_id=f"pub1_{DS}_nt_{w['id']}_{d}", wording_id=w["id"], defs_style=d,
                                 format_style=sty["id"], structure=f"{DS}|nt|{u['qid']}|{var}",
                                 edge=["long_document", "abstain_option"], twin_kind=None,
                                 extra={"article_id": u["aid"], "article_licence": art_log[u["aid"]]["licence_class"],
                                        "nota_variant": var, "abstain_gold": var == "removed",
                                        "human_label": {"gold_label": u["g"] + 1, "unanimous": True,
                                                        "difficult": u["difficult"]}})
                pair.append(make_row(ds=DS, framing="nt", key=f"{u['qid']}|{var}", group=u["aid"],
                                     state=sty["wrap"].format(title=u["title"], article=u["text"]),
                                     instructions=w["text"].format(question=u["q"]), options=opts, gold=gold,
                                     role="choice", card=card, meta=meta))
            rows += pair
        return rows

    def fits(rows):
        return all(real_tokens(x) <= MAX_ROW_TOKENS for x in rows)

    # ---- v1.2 option-cue balance -------------------------------------------------------------------------------
    cue_scores(cands)
    for s_ in cands:
        for u in cands[s_]["ch"]:
            shown = u["opts"]
            u["cell"] = (u["cue"][u["g"]] > max(c for i, c in enumerate(u["cue"]) if i != u["g"]),
                         len_rank(shown, u["opts"][u["g"]]))
        for u in cands[s_]["nt"]:
            dis = [i for i in range(4) if i != u["g"]]
            u["drop"] = u["opts"][rng(DS, "nt-drop", u["qid"]).choice(dis)]
            keep = [i for i in dis if u["opts"][i] != u["drop"]]
            shown = [u["opts"][i] for i in [u["g"]] + keep] + [P.QU_NOTA_STRINGS[0]]
            u["cell"] = (u["cue"][u["g"]] > max(u["cue"][i] for i in keep), len_rank(shown, u["opts"][u["g"]]))

    def take_cells(pool, n, key, k=4):
        """n units with gold top-cue on 1/k and the gold's length rank uniform over 1..k (cells (top, rank), target
        share (1/k if top else 1 - 1/k) / k). If a cell is short, its quota moves to a cell of the same 'top' class
        and the nearest free rank, else to a not-top cell (never to a top cell)."""
        by = defaultdict(list)
        for u in stable_shuffle(pool, DS, "cells", key):
            by[u["cell"]].append(u)
        quota = {}
        for top in (True, False):
            for rk in range(1, k + 1):
                quota[(top, rk)] = (1 / k if top else 1 - 1 / k) / k * n
        q = {c: int(v) for c, v in quota.items()}
        frac = sorted(quota, key=lambda c: -(quota[c] - int(quota[c])))
        for c in frac[: n - sum(q.values())]:
            q[c] += 1
        got, short = {}, 0
        for c in q:
            got[c] = by[c][: q[c]]
            short += q[c] - len(got[c])
        order = [(False, rk) for rk in (2, 3, 4, 1)] + [(True, rk) for rk in (2, 3, 4, 1)]
        for c in order:
            if short <= 0:
                break
            if c[0] and sum(len(v) for cc, v in got.items() if cc[0]) + 1 > round(n / k):
                continue
            more = by[c][len(got[c]): len(got[c]) + short]
            got[c] += more
            short -= len(more)
        picked = [u for v in got.values() for u in v]
        ids = {id(u) for u in picked}
        st[f"cells_short_{key}"] = short
        return picked, [u for u in pool if id(u) not in ids]

    out = {"main": [], "reserve": [], "dev": [], "stats": st}
    too_long = set()

    def take_ch(pool, n, key):
        """questions whose row is over 7,900 real tokens leave the pool and the balanced pick is redone."""
        while True:
            cand = [u for u in pool if u["qid"] not in too_long]
            got, left = take_cells(cand, n, key)
            rows = ch_rows(got, key)
            bad = {r["meta"]["text_source"]["record_id"] for r in rows if not fits([r])}
            if not bad:
                return rows, left
            too_long.update(bad)
            st[f"ch_token_drop_{key}"] += len(bad)

    def take_nt(pool, n, key):
        """n NT rows: n // 4 'removed' (+ rounding) and the rest 'kept' (cue/length balanced); token-checked."""
        n_r = round(n / 4)
        while True:
            cand = [u for u in pool if u["qid"] not in too_long]
            rem = stable_shuffle(cand, DS, "nt-rem", key)[:n_r]
            rid = {id(u) for u in rem}
            kept, _ = take_cells([u for u in cand if id(u) not in rid], n - n_r, key + "-kept")
            units = nt_order(kept, rem, key)
            rows = nt_rows(units, key)
            bad = {r["meta"]["text_source"]["record_id"] for r in rows if not fits([r])}
            if not bad:
                used = {id(u) for u in units}
                return rows, [u for u in pool if u["qid"] not in too_long and id(u) not in used]
            too_long.update(bad)
            st[f"nt_token_drop_{key}"] += len(bad)

    r_main, left = take_ch(cands["train"]["ch"], n_ch, "main")
    r_res, _ = take_ch(left, int(n_ch * RES_FRAC), "res")
    r_dev, _ = take_ch(cands["dev"]["ch"], n_dev["ch"], "dev")
    out["main"] += r_main; out["reserve"] += r_res; out["dev"] += r_dev
    nt_main, nt_left = take_nt(cands["train"]["nt"], n_nt, "nt-main")
    nt_res, _ = take_nt(nt_left, int(n_nt * RES_FRAC), "nt-res")
    nt_dev, _ = take_nt(cands["dev"]["nt"], n_dev["nt"], "nt-dev")
    out["main"] += nt_main
    out["reserve"] += nt_res
    out["dev"] += nt_dev
    for k in ("main", "reserve", "dev"):
        st[f"rows_{k}"] = len(out[k])
    st["target_main"] = n_main
    for k in ("main", "reserve", "dev"):  # v1.2b: rendered-row golden re-check (count; expected 0)
        st[f"post_golden_{k}"] = gi.post_check(out[k])
    (TMP / f"cand_{DS}.json").write_text(json.dumps(out, ensure_ascii=False))
    print(json.dumps(st, indent=0))


if __name__ == "__main__":
    main()
