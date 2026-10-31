#!/usr/bin/env python3
"""MuSiQue builder (C_DATA_SPEC v4 3.2 #2): answerable vs unanswerable twins (MuSiQue-Full) and supporting-paragraph
choice (answerable items), labels from MuSiQue's human-validated answerable / is_supporting fields only.

Shown context: a subset of the 20 paragraphs (every flagged supporting paragraph and every twin-specific paragraph is
always kept; removing other paragraphs cannot change answerability). Twins share the same kept shared paragraphs in
the same positions. Split by page title of the supporting paragraphs (10% mix-tuning dev); any supporting or
twin-specific paragraph with a sentence already in C1 golden_train drops the item; other such paragraphs are omitted.
v1.1 (review-public-1):
  - golden_train: a paragraph with >= 50% of its word 10-grams in golden_train counts as seen (same drop / omit rule);
  - split: `--phase dev` builds the dev rows (an item is dev if any supporting page is a dev page) and writes
    tmp/devx_musique.json; `--phase train` reads every Wikipedia set's devx. Non-required paragraphs (distractors and
    fill) come only from pages on the item's own side (is_dev_page); a train item whose required paragraph or any
    shown paragraph has a title, paragraph or sentence shown by a dev row is dropped / not shown (lib/common.DevX);
  - both sides need enough own-side paragraphs for the drawn context size (same shown-count draw for dev and train);
  - paragraphs deduped by (title, text) and by normalised text before sampling;
  - choice rows: the gold supporting paragraph is drawn so that 'an option's title is in the question' carries no
    signal: a supporting paragraph whose title is in the question is gold with probability P_QTITLE when the item
    also has one whose title is not (review item 6);
  - 3A rows kept under 2,000 real tokens with the card now printed in instructions: paragraph cap 1,500.
v1.2 (repair round 1, PREREG A29 a):
  - G6 root cause (choice options-only 0.48-0.52 vs chance 0.29): the option text carried the page title, and
    MuSiQue's supporting pages concentrate on a few bridge entities (states, countries, cities), so a title alone
    predicted gold. Options now name the paragraph by its shown number only (lib/pools MU_STYLES "opt");
  - golden_train (spec 3.1 v2): v1.2 GoldenIndex (no shared word 10-gram, no >= 6-word line, no >= 8-word sentence)
    on every shown paragraph and on the question;
  - `--qc N`: the same generator also writes a separate G6 QC sample (spec 8 G6: >= 5,000 rows) from items not used
    by main, reserve or dev to tmp/qcs_musique.json (never a training or dev row).
Output: tmp/devrows_musique.json (dev phase), tmp/cand_musique.json (train phase), tmp/qcs_musique.json (--qc).
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
from common import (GoldenIndex, DevX, base_meta, is_dev_page, licence_string, make_row, ntok, own_side, rng,  # noqa
                    sha, stable_shuffle, write_devx, TMP)
from textnorm import norm  # noqa: E402
import pools as P  # noqa: E402
from pickbal import take_choice_balanced, longest_is_gold  # noqa: E402

DS = "musique"
DATASET = "MuSiQue"
SRC = HERE / "raw/musique/musique_full_v1.0_train.jsonl"
N_MAIN = {"yn": 600, "ch": 400}
RES_FRAC = 0.25
N_DEV = {"yn": 40, "ch": 30}
SHORT_CAP = 1500  # paragraphs only; keeps 3A rows under 2,000 real tokens (spec 6: non-long rows); v1.0 1650
# review item 6: P(a supporting paragraph whose title is in the question is gold) is set from the candidate pool so
# that P(gold | an option's title is in the question) is about 1/k (computed in main; logged in stats)
HOP_W = {"2hop": 1.0, "3hop1": 2.0, "3hop2": 2.0, "4hop1": 3.0, "4hop2": 3.0, "4hop3": 3.0}


def hops(qid):
    return int(qid.split("__")[0][0])


_PAREN = re.compile(r"\s*\([^()]*\)\s*$")


def qhas(question: str, title: str) -> bool:
    """The page title, or its base without a trailing '(disambiguation)', is a whole-word part of the question."""
    q = f" {norm(question)} "
    return any(t and f" {t} " in q for t in {norm(title), norm(_PAREN.sub("", title))})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["dev", "train"], required=True)
    ap.add_argument("--qc", type=int, default=0, help="G6 QC-sample rows per framing (train phase)")
    a_ = ap.parse_args()
    phase, QC = a_.phase, a_.qc
    DEV = phase == "dev"
    devx = None if DEV else DevX()
    st = Counter()
    # pass 1: ids, split, both versions present
    info = defaultdict(dict)
    with open(SRC) as f:
        for line in f:
            r = json.loads(line)
            sup_titles = [p["title"] for p in r["paragraphs"] if p["is_supporting"]]
            info[r["id"]]["A" if r["answerable"] else "U"] = sup_titles
    ids = [i for i, v in info.items() if "A" in v and "U" in v]
    st["ids_with_both"] = len(ids)
    split = {i: ("dev" if any(is_dev_page(t) for t in info[i]["A"] + info[i]["U"]) else "train") for i in ids}
    # weighted deterministic order (enrich 3-4 hop items a little)
    def order(pool, tag):
        keyed = []
        for i in pool:
            u = int(sha(f"{DS}|{tag}|{i}")[:12], 16) / 16 ** 12
            w = HOP_W.get(i.split("__")[0], 1.0)
            keyed.append((u ** (1.0 / w), i))
        return [i for _, i in sorted(keyed, reverse=True)]
    tr = [i for i in ids if split[i] == "train"]
    dv = [i for i in ids if split[i] == "dev"]
    tag = "dv" if DEV else "tr"
    ids_o = order(dv, "dv") if DEV else (order(tr, "tr") if QC else order(tr, "tr")[:7000])
    if DEV:
        want = {"yn": N_DEV["yn"] // 2, "ch": int(N_DEV["ch"] * 2.2)}
    else:
        want = {"yn": N_MAIN["yn"] // 2 + int(N_MAIN["yn"] * RES_FRAC) // 2 + QC // 2,
                "ch": int(N_MAIN["ch"] * (1 + RES_FRAC) * 2.2) + int(QC * 2.2)}
    need = set(ids_o)
    recs = defaultdict(dict)
    with open(SRC) as f:
        for line in f:
            r = json.loads(line)
            if r["id"] in need:
                recs[r["id"]]["A" if r["answerable"] else "U"] = r
    gi = GoldenIndex()
    lic = licence_string(DS)
    def pkey(p):
        return (p["title"], p["paragraph_text"])

    def dedup(keys):
        out, seen_t = [], set()
        for k in keys:
            n = norm(k[1])
            if k in out or n in seen_t:
                st["para_dedup"] += 1
                continue
            seen_t.add(n)
            out.append(k)
        return out

    def bad(k):  # v1.2b: the paragraph and its shown form (title line + text; qc_fix found 10-grams across the two)
        return gi.bad(k[1]) or gi.bad(k[0] + "\n" + k[1])

    def usable_fill(k):
        """A non-required paragraph: golden-clean, own-side page, and (train) nothing a dev row shows."""
        return bad(k) is None and own_side(k[0], DEV) and (devx is None or not devx.blocked(*k))

    def required_ok(keys, kind):
        for k in keys:
            why = bad(k)
            if why:
                st[f"{kind}_drop_golden_{why}"] += 1
                return False
        if devx is not None and any(devx.blocked(*k) or not own_side(k[0], False) for k in keys):
            st[f"{kind}_drop_required_on_dev_side"] += 1
            return False
        return True

    yn_units = {tag: []}
    ch_units = {tag: []}
    used_ids = set()
    for i in ids_o:
        if len(yn_units[tag]) >= want["yn"]:
            break
        if True:
            a, u = recs[i]["A"], recs[i]["U"]
            ka = dedup([pkey(p) for p in a["paragraphs"]])
            ku = dedup([pkey(p) for p in u["paragraphs"]])
            sa_ = {pkey(p) for p in a["paragraphs"] if p["is_supporting"]}
            su_ = {pkey(p) for p in u["paragraphs"] if p["is_supporting"]}
            S = [k for k in ka if k in set(ku)]
            Da = [k for k in ka if k not in set(ku)]
            Du = [k for k in ku if k not in set(ka)]
            if len(Da) != len(Du) or a["question"] != u["question"]:
                st["yn_skip_shape"] += 1
                continue
            if gi.bad(a["question"]):
                st["yn_drop_question_golden"] += 1
                continue
            must = set(Da) | set(Du) | ((sa_ | su_) & set(S))
            if not required_ok(sorted(must), "yn"):
                continue
            rest = [k for k in S if k not in must and usable_fill(k)]
            st["yn_para_not_usable"] += sum(1 for k in S if k not in must and not usable_fill(k))
            r = rng(DS, "yn", i)
            K = r.randint(6, 9)
            n_fill = max(0, K - len(Da) - len((sa_ | su_) & set(S)))
            if len(rest) < n_fill:
                st["yn_skip_few_own_side_paragraphs"] += 1
                continue
            keep_shared = [k for k in S if k in must] + r.sample(rest, n_fill)
            slots = [("S", k) for k in keep_shared] + [("D", j) for j in range(len(Da))]
            r.shuffle(slots)
            twins = {}
            for lab, D in (("A", Da), ("U", Du)):
                twins[lab] = [k if t == "S" else D[k] for t, k in slots]
            if max(ntok("\n\n".join(t + "\n" + x for t, x in twins[lab])) for lab in ("A", "U")) > SHORT_CAP:
                st["yn_skip_long"] += 1
                continue
            yn_units[tag].append({"id": i, "q": a["question"].strip(), "paras": twins, "hops": hops(i),
                                  "titles": sorted({t for t, _ in twins["A"] + twins["U"]})})
            used_ids.add(i)
    st[f"yn_units_{tag}"] = len(yn_units[tag])

    for i in ids_o:
        if len(ch_units[tag]) >= want["ch"]:
            break
        if i in used_ids:
            continue
        if True:
            a = recs[i]["A"]
            allk = dedup([pkey(p) for p in a["paragraphs"]])
            supset = {pkey(p) for p in a["paragraphs"] if p["is_supporting"]}
            sup = [k for k in allk if k in supset]
            non = [k for k in allk if k not in supset]
            if not required_ok(sup, "ch"):
                continue
            if gi.bad(a["question"]):
                st["ch_drop_question_golden"] += 1
                continue
            ans = [a["answer"]] + list(a.get("answer_aliases") or []) + [d["answer"] for d in a["question_decomposition"]]
            ans_n = [norm(x) for x in ans if x and len(norm(x)) >= 3]
            clean = [k for k in non if usable_fill(k) and not any(x in norm(k[1]) for x in ans_n)
                     and k[0] not in {s[0] for s in sup}]
            r = rng(DS, "ch", i)
            k_opt = r.choice([3, 4])
            K = r.randint(5, 8)
            n_dis = max(k_opt - 1, K - len(sup))
            if len(clean) < n_dis:
                st["ch_skip_few_own_side_distractors"] += 1
                continue
            dis = r.sample(clean, n_dis)
            shown = sup + dis
            r.shuffle(shown)
            q = a["question"].strip()
            sup_q = [k for k in sup if qhas(q, k[0])]
            sup_n = [k for k in sup if not qhas(q, k[0])]
            gq = r.choice(sup_q) if sup_q else None
            gn = r.choice(sup_n) if sup_n else None
            u_draw = r.random()
            opt_d = r.sample(dis, k_opt - 1)
            if ntok("\n\n".join(t + "\n" + x for t, x in shown)) > SHORT_CAP:
                st["ch_skip_long"] += 1
                continue
            ch_units[tag].append({"id": i, "q": q, "shown": shown, "gq": gq, "gn": gn, "u": u_draw, "opt_d": opt_d,
                                  "k": k_opt, "hops": hops(i), "dis_q": sum(qhas(q, k[0]) for k in opt_d)})
    st[f"ch_units_{tag}"] = len(ch_units[tag])
    # review item 6: choose P so that sum(gold title in q) ~= sum(distractor options with title in q / (k - 1))
    cu = ch_units[tag]
    target = sum(u["dis_q"] / (u["k"] - 1) for u in cu)
    forced = sum(1 for u in cu if u["gq"] and not u["gn"])
    both = sum(1 for u in cu if u["gq"] and u["gn"])
    p_q = min(1.0, max(0.0, (target - forced) / both)) if both else 0.0
    st["cue_pool_target_x100"], st["cue_pool_forced"], st["cue_pool_both"] = round(100 * target), forced, both
    st["cue_p_qtitle_x1000"] = round(1000 * p_q)
    # items whose every supporting title is in the question (gold title always in the question) are kept with the
    # probability that brings their count to the target when p_q is 0
    keep_forced = min(1.0, target / forced) if (forced and p_q == 0.0) else 1.0
    st["cue_keep_forced_x1000"] = round(1000 * keep_forced)
    kept = []
    for u in cu:
        if u["gq"] and not u["gn"] and u["u"] >= keep_forced:
            st["cue_forced_dropped"] += 1
            continue
        u["gold"] = u["gq"] if (u["gq"] and (not u["gn"] or u["u"] < p_q)) else u["gn"]
        u["gold_q"] = qhas(u["q"], u["gold"][0])
        kept.append(u)
    ch_units[tag] = kept

    def render(paras, sty):
        body = sty["join"].join(sty["para"].format(n=n + 1, title=t, text=x) for n, (t, x) in enumerate(paras))
        return body

    def yn_rows(units, tag):
        rows = []
        nw = len(P.MU_YN_WORDINGS)
        for j, u in enumerate(stable_shuffle(units, DS, "yn-o", tag)):
            w = P.MU_YN_WORDINGS[j % nw]
            sty = P.MU_STYLES[(j // nw) % len(P.MU_STYLES)]
            d = rng(DS, "defs", u["id"]).choices(P.DEFS_STYLES, weights=P.DEFS_WEIGHTS)[0]
            card = None if d == "none" else P.MU_YN_CARDS[(w["pol"], d)]
            pair = []
            for lab in ("A", "U"):
                state = sty["wrap"].format(paras=render(u["paras"][lab], sty), question=u["q"])
                pred = 1 if lab == "A" else 0
                gold = pred if w["pol"] == "aff" else 1 - pred
                meta = base_meta(family_block="3A", dataset=DATASET, record_id=f"{u['id']}#{'answerable' if lab == 'A' else 'unanswerable'}",
                                 licence=lic, sa=True, card_id=f"pub1_{DS}_yn_{w['id']}_{d}", wording_id=w["id"],
                                 defs_style=d, format_style=sty["id"], structure=f"{DS}|yn|{u['id']}|{lab}",
                                 edge=["answerability", "multi_hop"], depth=u["hops"],
                                 twin_kind="answerability_contrast",
                                 extra={"page_titles": u["titles"], "n_paragraphs": len(u["paras"][lab]),
                                        "human_label": {"answerable": lab == "A"}})
                pair.append(make_row(ds=DS, framing="yn", key=f"{u['id']}|{lab}", group=u["id"], state=state,
                                     instructions=w["text"], options=None, gold=gold,
                                     role="aff" if w["pol"] == "aff" else "neg", card=card, meta=meta))
            pair[0]["meta"]["twin_of"], pair[1]["meta"]["twin_of"] = pair[1]["id"], pair[0]["id"]
            rows += pair
        return rows

    def ch_rows(units, tag):
        rows = []
        nw = len(P.MU_CH_WORDINGS)
        for j, u in enumerate(stable_shuffle(units, DS, "ch-o", tag)):
            w = P.MU_CH_WORDINGS[j % nw]
            sty = P.MU_STYLES[(j // nw) % len(P.MU_STYLES)]
            d = rng(DS, "defs-ch", u["id"]).choices(P.DEFS_STYLES, weights=P.DEFS_WEIGHTS)[0]
            card = None if d == "none" else P.MU_CH_CARDS[d]
            pos = {k: n + 1 for n, k in enumerate(u["shown"])}
            lab = lambda k: sty["opt"].format(n=pos[k], title=k[0])  # noqa: E731
            opts = [lab(u["gold"])] + [lab(k) for k in u["opt_d"]]
            opts = stable_shuffle(opts, DS, "opts", u["id"])
            state = sty["wrap"].format(paras=render(u["shown"], sty), question=u["q"])
            meta = base_meta(family_block="3A", dataset=DATASET, record_id=f"{u['id']}#answerable", licence=lic,
                             sa=True, card_id=f"pub1_{DS}_ch_{w['id']}_{d}", wording_id=w["id"], defs_style=d,
                             format_style=sty["id"], structure=f"{DS}|ch|{u['id']}|{u['gold'][0]}",
                             edge=["multi_hop", "supporting_paragraph"], depth=u["hops"],
                             extra={"page_titles": sorted({t for t, _ in u["shown"]}), "n_paragraphs": len(u["shown"]),
                                    "human_label": {"gold_is_supporting": True, "distractors_supporting": False}})
            rows.append(make_row(ds=DS, framing="ch", key=u["id"], group=u["id"], state=state,
                                 instructions=w["text"], options=opts, gold=lab(u["gold"]), role="choice",
                                 card=card, meta=meta))
        return rows

    def lg(u):  # choice: longest-gold balance on the rendered option labels (titles vary in length)
        return len(u["gold"][0]) > max(len(k[0]) for k in u["opt_d"])

    def cue_stats(units, name):
        g = sum(u["gold_q"] for u in units)
        d = sum(u["dis_q"] for u in units)
        st[f"cue_{name}_gold_title_in_q"] = g
        st[f"cue_{name}_distractor_options_title_in_q"] = d
        st[f"cue_{name}_p_gold_given_title_in_q_x1000"] = round(1000 * g / max(1, g + d))

    if DEV:
        dev = yn_rows(yn_units["dv"][: N_DEV["yn"] // 2], "dev")
        dp, _ = take_choice_balanced(ch_units["dv"], N_DEV["ch"], f"{DS}-chdev", lambda u: u["k"], lg)
        cue_stats(dp, "dev")
        dev += ch_rows(dp, "dev")
        shown = [k for u in yn_units["dv"][: N_DEV["yn"] // 2] for lab in ("A", "U") for k in u["paras"][lab]]
        shown += [k for u in dp for k in u["shown"]]
        st["rows_dev"] = len(dev)
        st["dev_mean_paragraphs_x100"] = round(100 * sum(r["meta"]["n_paragraphs"] for r in dev) / max(1, len(dev)))
        st["devx"] = write_devx(DS, shown)
        (TMP / f"devrows_{DS}.json").write_text(json.dumps({"dev": dev, "stats": st}, ensure_ascii=False))
        print(json.dumps(st, indent=0))
        return
    out = {"main": [], "reserve": [], "dev": [], "stats": st}
    n_pairs = N_MAIN["yn"] // 2
    n_res_pairs = int(N_MAIN["yn"] * RES_FRAC) // 2
    assert len(yn_units["tr"]) >= n_pairs + n_res_pairs, "MuSiQue yes/no pool too small"
    out["main"] += yn_rows(yn_units["tr"][:n_pairs], "main")
    out["reserve"] += yn_rows(yn_units["tr"][n_pairs:n_pairs + n_res_pairs], "res")
    pick, left = take_choice_balanced(ch_units["tr"], N_MAIN["ch"], f"{DS}-ch", lambda u: u["k"], lg)
    res, left2 = take_choice_balanced(left, int(N_MAIN["ch"] * RES_FRAC), f"{DS}-chres", lambda u: u["k"], lg)
    if QC:  # separate G6 QC sample from the same generator: units not used by main / reserve (dev is another side)
        qy = yn_units["tr"][n_pairs + n_res_pairs: n_pairs + n_res_pairs + QC // 2]
        qc_ch, _ = take_choice_balanced(left2, min(QC, len(left2)), f"{DS}-chqc", lambda u: u["k"], lg)
        qcs = yn_rows(qy, "qc") + ch_rows(qc_ch, "qc")
        st["qc_rows_yn"], st["qc_rows_ch"] = 2 * len(qy), len(qc_ch)
        (TMP / f"qcs_{DS}.json").write_text(json.dumps({"qc": qcs}, ensure_ascii=False))
    cue_stats(pick, "main")
    cue_stats(res, "reserve")
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
