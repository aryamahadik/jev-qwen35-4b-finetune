#!/usr/bin/env python3
"""2WikiMultihopQA builder (C_DATA_SPEC v4 3.2 #3): comparison and bridge-comparison questions only (yes/no answers
and two-entity comparisons), gold = the dataset's answer. Shown context keeps every supporting-fact paragraph plus some
of the dataset's distractor paragraphs. Split by page title of the supporting paragraphs (10% mix-tuning dev); a
supporting paragraph with a sentence already in C1 golden_train drops the item; other such paragraphs are omitted.
Input: tmp/2wiki_cmp_train.jsonl (slimmed from the pinned train.json by slim_2wiki.py). Output: tmp/cand_2wiki.json.
v1.1 (review-public-1): the dev phase reads every dev-side item (not the 10% sample) and keeps an item only if its
own-side distractors reach the drawn context size (so dev rows show as many paragraphs as train rows); context
paragraphs deduped by (title, text) and normalised text before sampling (upstream
contexts repeat paragraphs); a paragraph with >= 50% of its word 10-grams in golden_train counts as seen; `--phase dev`
builds the dev rows and writes tmp/devx_2wiki.json, `--phase train` reads every Wikipedia set's devx: distractor
paragraphs come only from pages on the item's own side (is_dev_page), and a train item whose supporting paragraph,
or a distractor whose page, paragraph or sentence, is shown by any dev row is dropped / not shown; meta.page_titles
now lists every shown page (meta.supporting_titles the supporting ones); paragraph cap 1,500 tokens (card moved into
instructions on choice rows).
v1.2 (repair round 1, PREREG A29 a):
  - choice G6 root cause (options-only 0.62-0.64 vs 0.50): the gold option was the dataset's answer string and the
    other option was cut from the question, and items whose answer lacked the page title's disambiguator ('(film)')
    failed the title match and were dropped, so a '(film)' option was never gold. Both options are now the two
    spans of the question ('..., A or B?'), the gold is the span the answer matches (exactly, or without a trailing
    parenthesis), and the title check accepts either form;
  - yes/no G6 root cause (question-only 0.60-0.63): yes rates differ by question template ('located in the same
    country' mostly yes, 'born in the same place' always no). Yes/no pairs are now matched inside one template (the
    question with every shown page title removed) and one negation count (negcount k_syn and k_all), so every
    template and every G10 cell (wording x bin x negation count) holds whole yes/no pairs (twin_of links the pair, so
    a sealed-check drop removes and refills both);
  - entity-name cue (first v1.2 QC sample: question-only still 0.60 with template-matched pairs): the entity names in
    a yes/no question carry prior knowledge ('Darreh ... and ... Sofla' are both Iranian villages, so 'same country'
    is likely yes). A cross-fitted question score s(q) = P(yes | question words) (logistic regression on word 1-2
    grams of every train-side yes/no question, 5 folds by item; selection only, never a label input) now matches
    each yes unit with the no unit of the same template and negation counts whose score is closest
    (|s_yes - s_no| <= 0.10), so the question alone does not tell the label;
  - disambiguation cue (first v1.2 QC sample, options-only still 0.66): in 2Wiki, when exactly one of the two
    compared names carries a page disambiguator ('(film)', '(1949 film)'), the answer is the other one (1,802 of
    1,802 such items in a 20% scan of train). Choice items with exactly one disambiguated name are no longer used;
  - option cue balance (as QuALITY): a cross-fitted options-only score (logistic regression on word 1-2 grams of the
    option plus length features, 5 folds by item; selection only) marks rows whose gold is the higher-scored option;
    choice rows are taken with that share = 1/2 and 'gold is strictly longer' = 1/2 (cells (top, longest));
  - v1.2b (second QC sample: choice metadata-only 0.56, question+option 0.53): equal-length options counted as 'not
    longer' (so 'longest' still told the gold 53%), the cue score was linear in word count (1-word and 6+-word names
    are rarely gold, 3-4 words often), and the first-mentioned name is gold 53%. The cue score now adds one-hot
    length / word-count / digit features, first-mentioned, the question head crossed with them, and trees on the
    dense features; selection is swap-symmetric over (length relation, cue sign, |cue| quintile) cells (take_ch);
  - golden_train: v1.2 GoldenIndex on every shown paragraph and on the question;
  - `--qc N`: separate G6 QC sample from the same generator (items not in main, reserve or dev) to tmp/qcs_2wiki.json;
    with --qc every train item is read (else the 10% sample).
"""
from __future__ import annotations

import argparse
import math
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from common import (GoldenIndex, DevX, base_meta, is_dev_page, licence_string, make_row, ntok, own_side, rng,  # noqa
                    sha, stable_shuffle, write_devx, TMP)
from textnorm import norm  # noqa: E402
import re  # noqa: E402
sys.path.insert(0, str(HERE.parents[1] / "common"))
import negcount  # noqa: E402
import pools as P  # noqa: E402
from pickbal import take_choice_balanced  # noqa: E402

DS = "2wiki"
DATASET = "2WikiMultihopQA"
SRC = TMP / "2wiki_cmp_train.jsonl"
N_MAIN = {"yn": 360, "ch": 240}
RES_FRAC = 0.25
N_DEV = {"yn": 24, "ch": 16}


def parse_other(q: str, ans: str):
    s = q.strip().rstrip("?").strip()
    tail = " or " + ans
    if s.endswith(tail):
        head = s[: -len(tail)]
        i = head.rfind(", ")
        return head[i + 2:].strip() if i >= 0 else None
    mid = ", " + ans + " or "
    i = s.find(mid)
    if i >= 0:
        return s[i + len(mid):].strip()
    return None


_PAREN = re.compile(r"\s*\([^()]*\)\s*$")


def forms(t: str) -> set:
    return {x for x in (norm(t), norm(_PAREN.sub("", t))) if x}


def parse_pair(q: str, titles_n: set):
    """The two compared spans of '..., A or B?' (v1.2): last ' or ' whose two spans both match a shown page title
    (exactly or without a trailing parenthesis)."""
    s = q.strip().rstrip("?").strip()
    idx = [m.start() for m in re.finditer(r" or ", s)]
    for i in reversed(idx):
        b = s[i + 4:].strip()
        head = s[:i]
        j = head.rfind(", ")
        if j < 0:
            continue
        a = head[j + 2:].strip()
        if a and b and forms(a) & titles_n and forms(b) & titles_n and not (forms(a) & forms(b)):
            return a, b
    return None


def tmpl_key(q: str, titles) -> str:
    """Question template: the normalised question with every shown page title (and its base without a trailing
    parenthesis) replaced by X."""
    s = " " + norm(q) + " "
    for t in sorted({f for x in titles for f in forms(x)}, key=len, reverse=True):
        s = s.replace(" " + t + " ", " X ")
        s = s.replace(" " + t + " ", " X ")
    return " ".join(s.split())


def qscore(us, tag, folds=5):
    """v1.2: cross-fitted P(yes | question words) for the yes/no units (selection balance only)."""
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    if not us:
        return
    y = np.array([int(u["ans"].lower() == "yes") for u in us])
    fo = np.array([int(sha(f"{DS}|qfold|{u['id']}")[:8], 16) % folds for u in us])
    for f in range(folds):
        tr, te = np.where(fo != f)[0], np.where(fo == f)[0]
        if len(set(y[tr])) < 2 or not len(te):
            for i in te:
                us[i]["qs"] = 0.5
            continue
        tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
        X = tv.fit_transform([us[i]["q"] for i in tr])
        m = LogisticRegression(C=1.0, max_iter=3000, solver="liblinear").fit(X, y[tr])
        for i, v in zip(te, m.predict_proba(tv.transform([us[i]["q"] for i in te]))[:, 1]):
            us[i]["qs"] = float(v)


def opt_feats(o: str, x: str, first: bool, qhead: str):
    """v1.2b option cue features for one option o against the other option x: length relation, length bin, word
    counts, digits, first-mentioned in the question, and the question head crossed with relation / position / digits
    (the second QC sample still showed metadata-only 0.56 and question+option 0.53 with a linear cue score)."""
    lo, lx = len(o), len(x)
    rel = ">" if lo > lx else "<" if lo < lx else "="
    wo, wx = min(8, len(o.split())), min(8, len(x.split()))
    do, dx = bool(re.search(r"[0-9]", o)), bool(re.search(r"[0-9]", x))
    f = {f"rel={rel}": 1.0, f"lb={min(9, lo // 20)}": 1.0, f"w={wo}": 1.0, f"wx={wo}|{wx}": 1.0, f"dg={do}|{dx}": 1.0,
         f"first={first}": 1.0, f"first={first}|rel={rel}": 1.0}
    for t in set(qhead.split()):
        f[f"q={t}|rel={rel}"] = 1.0
        f[f"q={t}|first={first}"] = 1.0
        f[f"q={t}|dg={do}"] = 1.0
        f[f"q={t}|w={wo}"] = 1.0
    return f, [lo, lx, wo, wx, float(do), float(dx), float(first), lo - lx, wo - wx, min(9, lo // 20)]


def optscore(us, folds=5):
    """v1.2b: cross-fitted options-only cue score (selection only, never a label input). Per option: logistic
    regression on word 1-2 grams + opt_feats one-hots, averaged with gradient-boosted trees on the dense opt_feats;
    u['d'] = score(gold) - score(other), 5 folds by item."""
    import numpy as np
    from scipy.sparse import hstack
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import TruncatedSVD
    from sklearn.linear_model import LogisticRegression
    if not us:
        return
    F, D, T, Q = [], [], [], []
    for u in us:
        for o, x, fs in ((u["ans"], u["other"], u["first"]), (u["other"], u["ans"], not u["first"])):
            f, d = opt_feats(o, x, fs, u["qhead"])
            F.append(f)
            D.append(d)
            T.append(o)
            Q.append(u["q"] + " || " + o)
    D = np.array(D, dtype=float)
    fo = np.array([int(sha(f"{DS}|ofold|{u['id']}")[:8], 16) % folds for u in us])
    for f in range(folds):
        tri, tei = np.where(fo != f)[0], np.where(fo == f)[0]
        if not len(te_ := tei):
            continue
        if not len(tri):
            for i in te_:
                us[i]["d"] = us[i]["d2"] = 0.0
            continue
        otr = np.ravel(np.column_stack([2 * tri, 2 * tri + 1]))
        ote = np.ravel(np.column_stack([2 * tei, 2 * tei + 1]))
        y = np.array([1, 0] * len(tri))
        tv, dv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True), DictVectorizer()
        Xtr = hstack([tv.fit_transform([T[i] for i in otr]), dv.fit_transform([F[i] for i in otr])]).tocsr()
        Xte = hstack([tv.transform([T[i] for i in ote]), dv.transform([F[i] for i in ote])]).tocsr()
        m1 = LogisticRegression(C=1.0, max_iter=3000, solver="liblinear").fit(Xtr, y)
        m2 = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, max_leaf_nodes=31,
                                            random_state=0).fit(D[otr], y)
        sc = (m1.predict_proba(Xte)[:, 1] + m2.predict_proba(D[ote])[:, 1]) / 2
        # v1.2b second cue: question + option text (word 1-2 grams -> 64-d SVD -> trees), the G6 (a) view
        tq = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
        Qtr = tq.fit_transform([Q[i] for i in otr])
        sv = TruncatedSVD(max(2, min(64, Qtr.shape[1] - 1, Qtr.shape[0] - 1)), random_state=0).fit(Qtr)
        m3 = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, max_leaf_nodes=31,
                                            random_state=0).fit(sv.transform(Qtr), y)
        sc2 = m3.predict_proba(sv.transform(tq.transform([Q[i] for i in ote])))[:, 1]
        for k, i in enumerate(tei):
            us[i]["d"] = float(sc[2 * k] - sc[2 * k + 1])
            us[i]["d2"] = float(sc2[2 * k] - sc2[2 * k + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["dev", "train"], required=True)
    ap.add_argument("--qc", type=int, default=0, help="G6 QC-sample rows per framing (train phase)")
    a_ = ap.parse_args()
    phase, QC = a_.phase, a_.qc
    DEV = phase == "dev"
    devx = None if DEV else DevX()
    st = Counter()
    gi = GoldenIndex()
    lic = licence_string(DS)
    def items():  # v1.2: streamed (the --qc run reads every item)
        with open(SRC) as f:
            for line in f:
                r = json.loads(line)
                if DEV:  # v1.1: every dev-side item is a candidate (own-side distractors are scarce on the dev side)
                    if not any(is_dev_page(t) for t, _ in r["supporting_facts"]):
                        continue
                elif not QC and int(sha(f"{DS}|keep|{r['_id']}")[:8], 16) % 10 != 0:
                    continue
                st["sampled_items"] += 1
                yield r
    units = {"tr": {"yes": [], "no": [], "ch": []}, "dv": {"yes": [], "no": [], "ch": []}}
    for r in items():
        ans = r["answer"].strip()
        sup_titles = sorted({t for t, _ in r["supporting_facts"]})
        ctx, seen_t = [], set()
        for t, sents in r["context"]:
            c = (t, " ".join(s.strip() for s in sents))
            if c in ctx or norm(c[1]) in seen_t:
                st["para_dedup"] += 1
                continue
            seen_t.add(norm(c[1]))
            ctx.append(c)
        titles_n = {f for t, _ in ctx for f in forms(t)}  # v1.2: both forms of every title
        if not all(norm(t) in titles_n for t in sup_titles):
            st["skip_sup_title_missing"] += 1
            continue
        tag = "dv" if any(is_dev_page(t) for t in sup_titles) else "tr"
        if (tag == "dv") != DEV:
            continue
        sup = [c for c in ctx if c[0] in sup_titles]
        if gi.bad(r["question"]):
            st["drop_question_golden"] += 1
            continue
        whys = [gi.bad(x) or gi.bad(t + "\n" + x) for t, x in sup]  # v1.2b: + shown form (title line + text)
        if any(whys):
            st[f"drop_golden_{[w for w in whys if w][0]}"] += 1
            continue
        if devx is not None and any(devx.blocked(t, x) for t, x in sup):
            st["drop_supporting_shown_by_dev"] += 1
            continue
        non = [c for c in ctx if c[0] not in sup_titles]
        clean = [c for c in non if (gi.bad(c[1]) or gi.bad(c[0] + "\n" + c[1])) is None and own_side(c[0], DEV)
                 and (devx is None or not devx.blocked(*c))]
        st["para_not_usable"] += len(non) - len(clean)
        rr = rng(DS, "ctx", r["_id"])
        K = rr.randint(5, 10)
        if DEV and len(clean) < K - len(sup):  # v1.1: dev rows show as many paragraphs as train rows draw
            st["dev_skip_few_own_side_paragraphs"] += 1
            continue
        keep = sup + rr.sample(clean, min(len(clean), max(0, K - len(sup))))
        rr.shuffle(keep)
        if ntok("\n\n".join(t + "\n" + x for t, x in keep)) > 1500:
            st["skip_long"] += 1
            continue
        u = {"id": r["_id"], "type": r["type"], "q": r["question"].strip(), "ans": ans, "paras": keep,
             "sup_titles": sup_titles, "depth": len(r["supporting_facts"]),
             "slen": sum(len(t) + len(x) + 3 for t, x in keep)}
        if ans.lower() in ("yes", "no"):
            q = r["question"].strip()
            u["tkey"] = (r["type"], tmpl_key(q, [t for t, _ in ctx]), negcount.k_syn(q), negcount.k_all(q))
            units[tag][ans.lower()].append(u)
        else:
            pr = parse_pair(r["question"], titles_n)
            if not pr:
                st["ch_skip_parse"] += 1
                continue
            if ("(" in pr[0]) != ("(" in pr[1]):
                st["ch_skip_one_side_disambiguated"] += 1
                continue
            hit = [x for x in pr if norm(ans) in forms(x)]
            if len(hit) != 1:
                st["ch_skip_answer_not_one_span"] += 1
                continue
            u["ans_raw"] = ans
            u["ans"] = hit[0]
            u["other"] = pr[1] if hit[0] == pr[0] else pr[0]
            u["first"] = hit[0] == pr[0]
            hq = r["question"].strip().rstrip("?").strip()
            u["qhead"] = norm(hq[: max(0, hq.rfind(", " + pr[0] + " or "))])
            units[tag]["ch"].append(u)
    for tg in units:
        for k, v in units[tg].items():
            st[f"pool_{tg}_{k}"] = len(v)

    def render(paras, sty):
        return sty["wrap"].format(paras=sty["join"].join(sty["para"].format(title=t, text=x) for t, x in paras))

    def yn_rows(pairs, tag):
        rows = []
        nw = len(P.TW_YN_WORDINGS)
        for j, (uy, un) in enumerate(stable_shuffle(pairs, DS, "yn-o", tag)):
            w = P.TW_YN_WORDINGS[j % nw]
            sty = P.TW_STYLES[(j // nw) % len(P.TW_STYLES)]
            d = rng(DS, "defs", uy["id"], un["id"]).choices(P.DEFS_STYLES, weights=P.DEFS_WEIGHTS)[0]
            card = None if d == "none" else P.TW_YN_CARDS[("aff", d)]
            pair = []
            for u, gold in ((uy, 1), (un, 0)):
                meta = base_meta(family_block="3A", dataset=DATASET, record_id=u["id"], licence=lic, sa=True,
                                 card_id=f"pub1_{DS}_yn_{w['id']}_{d}", wording_id=w["id"], defs_style=d,
                                 format_style=sty["id"], structure=f"{DS}|yn|{u['id']}",
                                 edge=["multi_hop", "comparison", u["type"]], depth=u["depth"],
                                 extra={"page_titles": sorted({t for t, _ in u["paras"]}), "supporting_titles": u["sup_titles"],
                                        "question_type": u["type"],
                                        "n_paragraphs": len(u["paras"]), "human_label": {"answer": u["ans"].lower()}})
                pair.append(make_row(ds=DS, framing="yn", key=u["id"], group=u["id"], state=render(u["paras"], sty),
                                     instructions=w["text"].format(question=u["q"]), options=None, gold=gold,
                                     role="aff", card=card, meta=meta))
            pair[0]["meta"]["twin_of"], pair[1]["meta"]["twin_of"] = pair[1]["id"], pair[0]["id"]
            for x in pair:
                x["meta"]["twin_kind"] = "template_matched_yes_no"
            cell = {(negcount.k_syn(fq(x)), negcount.k_all(x["instructions"])) for x in pair}
            if len(cell) != 1:  # both rows of a pair must sit in one G10 cell
                st["yn_pair_split_cells_dropped"] += 1
                continue
            rows += pair
        return rows

    def ch_rows(units_, tag):
        rows = []
        nw = len(P.TW_CH_WORDINGS)
        for j, u in enumerate(stable_shuffle(units_, DS, "ch-o", tag)):
            w = P.TW_CH_WORDINGS[j % nw]
            sty = P.TW_STYLES[(j // nw) % len(P.TW_STYLES)]
            d = rng(DS, "defs-ch", u["id"]).choices(P.DEFS_STYLES, weights=P.DEFS_WEIGHTS)[0]
            card = None if d == "none" else P.TW_CH_CARDS[d]
            opts = stable_shuffle([u["ans"], u["other"]], DS, "opts", u["id"])
            meta = base_meta(family_block="3A", dataset=DATASET, record_id=u["id"], licence=lic, sa=True,
                             card_id=f"pub1_{DS}_ch_{w['id']}_{d}", wording_id=w["id"], defs_style=d,
                             format_style=sty["id"], structure=f"{DS}|ch|{u['id']}",
                             edge=["multi_hop", "comparison", u["type"]], depth=u["depth"],
                             extra={"page_titles": sorted({t for t, _ in u["paras"]}), "supporting_titles": u["sup_titles"],
                                        "question_type": u["type"],
                                    "n_paragraphs": len(u["paras"]), "human_label": {"answer": u["ans_raw"]}})
            rows.append(make_row(ds=DS, framing="ch", key=u["id"], group=u["id"], state=render(u["paras"], sty),
                                 instructions=w["text"].format(question=u["q"]), options=opts, gold=u["ans"],
                                 role="choice", card=card, meta=meta))
        return rows

    def fq(x):
        ps = [p_.strip() for p_ in re.split(r"\n\s*\n", x["instructions"] or "") if p_.strip()]
        return ps[-1] if ps else ""

    for tg_ in units:  # v1.2 question scores and option cue scores (each side scored within itself)
        qscore(units[tg_]["yes"] + units[tg_]["no"], tg_)
        optscore(units[tg_]["ch"])

    def take_ch(pool, n, key):
        """v1.2b: swap-symmetric selection (the v1.2 cells (top, longest) counted equal-length options as 'not
        longer', so 'longest' still told the gold 53%). Each item has a signature (length relation of gold vs other
        >,<,=; signs of the two cue differences d (options + features) and d2 (question + option text); |d| and |d2|
        terciles). A cell and its swap (relation mirrored, both signs flipped, same terciles) get equal counts, so
        neither a length flag nor either cue score tells the gold; cell pairs are filled in proportion to capacity."""
        import bisect
        cuts = {}
        for dk in ("d", "d2"):
            ad = sorted(abs(u[dk]) for u in pool)
            cuts[dk] = [ad[int(len(ad) * q / 3)] for q in (1, 2)] if ad else []

        def sig(u):
            la, lo_ = len(u["ans"]), len(u["other"])
            return (">" if la > lo_ else "<" if la < lo_ else "=", "+" if u["d"] > 0 else "-",
                    "+" if u["d2"] > 0 else "-", bisect.bisect_right(cuts["d"], abs(u["d"])),
                    bisect.bisect_right(cuts["d2"], abs(u["d2"])))

        def swap(c):
            return ({">": "<", "<": ">", "=": "="}[c[0]], "-" if c[1] == "+" else "+", "-" if c[2] == "+" else "+",
                    c[3], c[4])
        by = {}
        for u in stable_shuffle(pool, DS, "toplg", key):
            by.setdefault(sig(u), []).append(u)
        prs = sorted({tuple(sorted([c, swap(c)], key=str)) for c in by}, key=str)
        cap = {p: min(len(by.get(p[0], [])), len(by.get(p[1], []))) for p in prs}
        half, tot = n // 2, sum(cap.values())
        if tot <= half:
            m = dict(cap)
        else:
            m = {p: int(half * cap[p] / tot) for p in prs}
            for p in sorted(prs, key=lambda p: (-(half * cap[p] / tot - m[p]), str(p))):
                if sum(m.values()) >= half:
                    break
                if m[p] < cap[p]:
                    m[p] += 1
        pk = [u for p in prs for c in p for u in by.get(c, [])[: m[p]]]
        st[f"toplg_short_{key}"] = n - len(pk)
        st[f"sym_gold_longer_{key}"] = sum(len(u["ans"]) > len(u["other"]) for u in pk)
        st[f"sym_gold_shorter_{key}"] = sum(len(u["ans"]) < len(u["other"]) for u in pk)
        st[f"sym_d_pos_{key}"] = sum(u["d"] > 0 for u in pk)
        st[f"sym_d2_pos_{key}"] = sum(u["d2"] > 0 for u in pk)
        ids = {id(u) for u in pk}
        return pk, [u for u in pool if id(u) not in ids]

    def pairs_for(tag, n_pairs, salt):
        """v1.2: a yes unit is paired only with a no unit of the same type, template and negation counts, the one
        with the closest question score (|s_yes - s_no| <= 0.10; greedy over the yes units in a seeded order).
        v1.2b: and a shown-text length within 10% (|log ratio| <= 0.10; closest by the sum of both scaled distances):
        the third QC sample showed metadata-only 0.53 from state length (yes states 2,583 chars vs no 2,331)."""
        import bisect
        out = []
        for typ in ("comparison", "bridge_comparison"):
            by = {}
            for lab in ("yes", "no"):
                for u in units[tag][lab]:
                    if u["type"] == typ:
                        by.setdefault(u["tkey"], {"yes": [], "no": []})[lab].append(u)
            prs = []
            for k in sorted(by, key=str):
                ys = stable_shuffle(by[k]["yes"], DS, salt, "y", *map(str, k))
                ns = sorted(by[k]["no"], key=lambda u: (u["qs"], u["id"]))
                keys = [u["qs"] for u in ns]
                for uy in ys:
                    if not ns:
                        break
                    lo_ = bisect.bisect_left(keys, uy["qs"] - 0.10)
                    hi_ = bisect.bisect_right(keys, uy["qs"] + 0.10)
                    cand = [j for j in range(lo_, hi_) if abs(math.log(ns[j]["slen"] / uy["slen"])) <= 0.10]
                    if not cand:
                        st[f"yn_unmatched_{tag}"] += 1
                        continue
                    best = min(cand, key=lambda j: (abs(math.log(ns[j]["slen"] / uy["slen"])) / 0.10 +
                                                    abs(keys[j] - uy["qs"]) / 0.10, j))
                    prs.append((uy, ns.pop(best)))
                    keys.pop(best)
            st[f"pairs_{tag}_{typ}"] = len(prs)
            out.append(stable_shuffle(prs, DS, salt, "pairs", typ))
        # mix types: 60% comparison, 40% bridge_comparison (bounded by availability)
        nc = min(len(out[0]), round(n_pairs * 0.6))
        nb = min(len(out[1]), n_pairs - nc)
        nc = min(len(out[0]), n_pairs - nb)
        return out[0][:nc] + out[1][:nb], out[0][nc:] + out[1][nb:]

    if DEV:
        dev_p, _ = pairs_for("dv", N_DEV["yn"] // 2, "dev")
        dev = yn_rows(dev_p, "dev")
        dp, _ = take_ch(units["dv"]["ch"], N_DEV["ch"], f"{DS}-chdev")
        dev += ch_rows(dp, "dev")
        shown = [k for a, b in dev_p for k in a["paras"] + b["paras"]] + [k for u in dp for k in u["paras"]]
        st["rows_dev"] = len(dev)
        st["dev_mean_paragraphs_x100"] = round(100 * sum(r["meta"]["n_paragraphs"] for r in dev) / max(1, len(dev)))
        st["devx"] = write_devx(DS, shown)
        (TMP / f"devrows_{DS}.json").write_text(json.dumps({"dev": dev, "stats": st}, ensure_ascii=False))
        print(json.dumps(st, indent=0))
        return
    out = {"main": [], "reserve": [], "dev": [], "stats": st}
    main_p, left_p = pairs_for("tr", N_MAIN["yn"] // 2, "main")
    out["main"] += yn_rows(main_p, "main")
    res_p = stable_shuffle(left_p, DS, "res")[: int(N_MAIN["yn"] * RES_FRAC) // 2]
    out["reserve"] += yn_rows(res_p, "res")
    pick, left = take_ch(units["tr"]["ch"], N_MAIN["ch"], f"{DS}-ch")
    res, left2 = take_ch(left, int(N_MAIN["ch"] * RES_FRAC), f"{DS}-chres")
    if QC:  # separate G6 QC sample from the same generator (units not in main / reserve; dev is the other side)
        qp = stable_shuffle(left_p, DS, "res")[int(N_MAIN["yn"] * RES_FRAC) // 2:][: QC // 2]
        qc_ch, _ = take_ch(left2, min(QC, len(left2)), f"{DS}-chqc")
        qcs = yn_rows(qp, "qc") + ch_rows(qc_ch, "qc")
        st["qc_rows_yn"], st["qc_rows_ch"] = sum(r["qtype"] == "noul" for r in qcs), len(qc_ch)
        (TMP / f"qcs_{DS}.json").write_text(json.dumps({"qc": qcs}, ensure_ascii=False))
    out["main"] += ch_rows(pick, "main")
    out["reserve"] += ch_rows(res, "res")
    st["main_mean_paragraphs_x100"] = round(100 * sum(r["meta"]["n_paragraphs"] for r in out["main"]) / len(out["main"]))
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
