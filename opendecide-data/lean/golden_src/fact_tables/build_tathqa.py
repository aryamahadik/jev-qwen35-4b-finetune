"""v14 golden, family fact_tables: raw rows for "tathqa" (TAT-HQA, Li et al., ACL 2022): verify the answer to a
HYPOTHETICAL question over a real annual-report table + text ("what would X be if Y were Z?").

Source : GitHub NExTplusplus/TAT-HQA @ 8b821d89f0fbfeceea07e4f5faf46b33150fee07,
         dataset_raw/tatqa_and_hqa_dataset_train.json ONLY (dev and dataset_test_hqa are never downloaded); only the
         questions with answer_type == "counterfactual" (the TAT-HQA part) are used. sha256 pinned below.
Licence: Apache-2.0 (LICENSE at the repo root, Apache License 2.0 full text).
Texts  : TAT-QA report contexts; hypothetical questions, their answers and derivations written by human annotators
         from a factual TAT-QA question (rel_question). No model-written text or labels.
Rows   : state = table + paragraphs + hypothetical question + proposed answer. Proposed = the human hypothetical answer
         (gold "yes" for "correct?") or a wrong answer (gold "no"), preferring the most instructive slip:
           ignores_hypothetical: the human answer to the linked FACTUAL question (the report's actual figure),
           else a program slip on the human derivation (another cell of the same row/column, wrong base, sum instead
           of average, sign flip of a plain "change", wrong scale when the report states only the gold scale),
           or for list/span answers another item of the same row/column.
         Candidates must be clearly different at the gold's precision. ~20% of rows ask "... is the proposed answer
         wrong?" (gold flips).
Filters: numeric answers must re-evaluate from the human derivation; at most 2 hypothetical questions per report
         context (the same contexts also feed key "tatqa", where they are capped at 3 factual questions);
         exact/near-dup states dropped; 13-word-run decontamination against our local non-held-out files;
         yes/no balanced per answer source.
         Reviewer fixes (strict review): "change" questions whose years run backwards are dropped (sign ambiguous);
         questions whose thousand/million/billion scale is never stated in the excerpt are dropped (e.g. 'thousand'
         annotated on a EUR-million table); sign-flip and cell-swap distractors follow the tatqa fixes.
Deterministic, CPU only (seed 20261101).   ../../../.venv/bin/python build_tathqa.py [--manifest]
"""
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict

import build_tatqa as T
import ft_common as C

KEY = "tathqa"
COMMIT = "8b821d89f0fbfeceea07e4f5faf46b33150fee07"
BASE = f"https://raw.githubusercontent.com/NExTplusplus/TAT-HQA/{COMMIT}/"
FILES = {
    "dataset_raw/tatqa_and_hqa_dataset_train.json": "715d78b160770b2aca7f5a8df870fb2c6b2b64bef5dbfc1e0b77ec35bd23bd2b",
    "LICENSE": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
}
LICENCE = f"Apache-2.0 (github.com/NExTplusplus/TAT-HQA/blob/{COMMIT}/LICENSE)"
CACHE = C.CACHE / "tathqa"
MAX_PER_CONTEXT = 2
NEG_SHARE = 0.2
MAX_STATE = 7000

Q_CORRECT = ("Using the report's table and text together with the question's hypothetical assumption, is the proposed "
             "answer correct?")
Q_WRONG = ("Using the report's table and text together with the question's hypothetical assumption, is the proposed "
           "answer wrong?")
DEFS = {
    "correct": {
        "yes": "The proposed answer is what the figures give after applying the question's hypothetical change (the "
               "assumed value replaces the reported one): same value at the precision shown, same sign, same unit "
               "or scale, and for lists exactly the right items.",
        "no": "The proposed answer is not the hypothetical result: it ignores the assumption and uses the reported "
              "figure, uses a wrong figure or base, sums instead of averaging, has the wrong sign or scale, or lists "
              "the wrong items.",
    },
    "wrong": {
        "yes": "It is wrong: it is not what the figures give after applying the question's hypothetical change, for "
               "example it keeps the reported figure, uses a wrong figure or base, or has the wrong sign, scale or "
               "items.",
        "no": "It is not wrong: it is exactly what the figures give after applying the question's hypothetical change, "
              "with the same value at the precision shown, the same sign and scale, and for lists the right items.",
    },
}


def main():
    paths = {rel: C.fetch(BASE + rel, CACHE / rel.split("/")[-1], sha) for rel, sha in FILES.items()}
    data = json.load(open(paths["dataset_raw/tatqa_and_hqa_dataset_train.json"]))  # TRAIN ONLY
    rng = random.Random(C.SEED)
    drop = Counter()
    ctxs = []
    for x in data:
        table = [[C.clean_cell(v, 10_000) for v in row] for row in x["table"]["table"]]
        paras = [C.clean_cell(p["text"], 100_000) for p in sorted(x["paragraphs"], key=lambda p: p["order"])]
        paras = [p for p in paras if p]
        table_text = C.render_table(table)
        para_text = "\n".join(paras)
        ctx_text = table_text + "\n" + para_text
        ctx_id = hashlib.sha256(ctx_text.encode()).hexdigest()[:16]
        idx, nums = T.cell_index(table)
        by_order = {str(q["order"]): q for q in x["questions"]}
        cands = []
        for q in x["questions"]:
            if q["answer_type"] != "counterfactual":
                continue
            if T.reversed_change(q["question"]):
                drop["change question with reversed years (sign ambiguous)"] += 1
                continue
            if T.scale_unstated(q["scale"], ctx_text):
                drop["answer scale not stated in the excerpt"] += 1
                continue
            rel = by_order.get(str(q.get("rel_question")))
            ans = q["answer"]
            numeric = isinstance(ans, (int, float)) and not isinstance(ans, bool)
            dis = []
            if numeric:
                qq = dict(q, answer_type="arithmetic")
                factor = T.consistent(qq, table_text, para_text)
                if factor is None:
                    drop["inconsistent human answer"] += 1
                    continue
                g = float(ans)
                dec = T.gold_decimals(ans)
                gold_txt = T.render_number(g, dec, q["scale"])
                if rel is not None and isinstance(rel["answer"], (int, float)) and not isinstance(rel["answer"], bool):
                    fv = float(rel["answer"])
                    if C.clearly_different(fv, g, dec) and rel["scale"] == q["scale"]:
                        dis.append((T.render_number(fv, dec, q["scale"]), "ignores_hypothetical"))
                dis += [(t, k) for t, k, _ in T.arithmetic_distractors(qq, table, nums, ctx_text, g, dec, factor)]
            else:
                items = ans if isinstance(ans, list) else [ans]
                items = [C.clean_cell(str(a), 10_000) for a in items if str(a).strip()]
                if not items:
                    drop["empty answer"] += 1
                    continue
                gold_txt = "; ".join(T.render_item(a, q["scale"]) for a in items)
                if rel is not None:
                    ritems = rel["answer"] if isinstance(rel["answer"], list) else [rel["answer"]]
                    rtxt = "; ".join(T.render_item(C.clean_cell(str(a), 10_000), rel["scale"]) for a in ritems)
                    if rtxt.strip() and {C.norm(str(a)) for a in ritems} != {C.norm(a) for a in items} \
                            and rel["answer_type"] in ("span", "multi-span", "count"):
                        dis.append((rtxt, "ignores_hypothetical"))
                if not dis:
                    qq = dict(q, answer=items, answer_type="multi-span" if len(items) > 1 else "span")
                    fn = T.multispan_distractors if len(items) > 1 else None
                    if fn:
                        dis = [(t, k) for t, k, _ in fn(qq, table, idx)]
                    else:
                        dis = [(t, k) for t, k, _ in T.span_distractors(qq, table, idx, ctx_text, [])]
            if T.OPEN_Q.search(q["question"]):
                dis = []
            dis = sorted({d for d in dis if T.light(d[0]) != T.light(gold_txt) and d[0].strip()})
            cands.append({"q": q, "gold_txt": gold_txt, "dis": dis, "numeric": numeric,
                          "stratum": ("number" if numeric else "items", q["answer_from"])})
        if cands:
            ctxs.append({"uid": ctx_id, "table_text": table_text, "para_text": para_text, "cands": cands})

    docs = {}
    for cx in ctxs:
        docs["ctx:" + cx["uid"]] = cx["table_text"] + "\n" + cx["para_text"]
        for cd in cx["cands"]:
            docs["q:" + cd["q"]["uid"]] = cd["q"]["question"]
    hit = C.local_decontam(docs)
    pool = []
    for cx in sorted(ctxs, key=lambda c: c["uid"]):
        if "ctx:" + cx["uid"] in hit:
            drop["13-gram overlap (context)"] += len(cx["cands"])
            continue
        cands = [cd for cd in cx["cands"] if "q:" + cd["q"]["uid"] not in hit]
        drop["13-gram overlap (question)"] += len(cx["cands"]) - len(cands)
        cands.sort(key=lambda cd: cd["q"]["uid"])
        rng.shuffle(cands)
        cands.sort(key=lambda cd: not cd["dis"])
        seen_q, chosen = set(), []
        for cd in cands:
            nq = C.norm(cd["q"]["question"])
            if nq in seen_q:
                continue
            seen_q.add(nq)
            chosen.append(cd)
            if len(chosen) >= MAX_PER_CONTEXT:
                break
        drop["over per-context cap"] += len(cands) - len(chosen)
        for cd in chosen:
            cd["ctx"] = cx
            pool.append(cd)

    by_st = defaultdict(list)
    for cd in pool:
        by_st[cd["stratum"]].append(cd)
    rows = []
    for st in sorted(by_st):
        lst = by_st[st]
        rng.shuffle(lst)
        can_no = [cd for cd in lst if cd["dis"]]
        k = min(len(can_no), len(lst) // 2)
        no_ids = {cd["q"]["uid"] for cd in can_no[:k]}
        yes = [cd for cd in lst if cd["q"]["uid"] not in no_ids][:k]
        drop["stratum balance"] += len(lst) - 2 * k
        for cd in can_no[:k]:
            # prefer distractors with the gold's sign (a lone minus sign must not give the label away)
            gneg = cd["gold_txt"].startswith("-")
            dis = [d for d in cd["dis"] if d[1] == "sign_flip" or d[0].startswith("-") == gneg] or cd["dis"]
            kinds = sorted({d[1] for d in dis})
            kind = "ignores_hypothetical" if "ignores_hypothetical" in kinds and rng.random() < 0.7 else rng.choice(kinds)
            rows.append((cd, rng.choice(sorted(d[0] for d in dis if d[1] == kind)), False, kind))
        for cd in yes:
            rows.append((cd, cd["gold_txt"], True, "human_gold"))

    rows.sort(key=lambda r: r[0]["q"]["uid"])
    rng.shuffle(rows)
    n_neg = int(round(NEG_SHARE * len(rows)))
    out, seen = [], set()
    for i, (cd, ans_txt, is_gold, kind) in enumerate(rows):
        q, cx = cd["q"], cd["ctx"]
        negq = i < n_neg
        state = (f"Company annual report excerpt\nTable:\n{cx['table_text']}\nText:\n{cx['para_text']}\n\n"
                 f"Hypothetical question: {C.clean_cell(q['question'], 10_000)}\nProposed answer: {ans_txt}")
        if len(state) > MAX_STATE:
            drop["state too long"] += 1
            continue
        ns = C.norm(state)
        if ns in seen:
            drop["duplicate state"] += 1
            continue
        seen.add(ns)
        gold = ("yes" if not is_gold else "no") if negq else ("yes" if is_gold else "no")
        edges = ["hypothetical"]
        if negq:
            edges.append("negation")
        if kind == "wrong_scale":
            edges.append("units")
        if cd["numeric"]:
            edges.append("numeric")
        if q["answer_from"] == "table-text":
            edges.append("multi_hop")
        edges.append("table")
        out.append({
            "key": KEY, "rid": q["uid"], "state": state, "instructions": Q_WRONG if negq else Q_CORRECT,
            "options": ["yes", "no"], "gold": gold, "soft": None,
            "meta": {"dataset": "NExTplusplus/TAT-HQA (github)", "config": "dataset_raw/tatqa_and_hqa_dataset_train.json"
                                                                         " (answer_type=counterfactual)",
                     "revision": f"git:{COMMIT}; sha256:{FILES['dataset_raw/tatqa_and_hqa_dataset_train.json']}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"answer": q["answer"], "derivation": q["derivation"], "scale": q["scale"],
                                    "answer_from": q["answer_from"], "rel_question": q.get("rel_question")},
                     "family": C.FAMILY, "edge": "hypothetical", "edge_all": edges,
                     "defs": "wrong" if negq else "correct", "proposed_is_gold": is_gold, "distractor": kind,
                     "context_id": cx["uid"]},
        })

    summ = C.check_rows(KEY, out)
    print("drops:", dict(drop))
    print("distractor kinds:", dict(Counter(r["meta"]["distractor"] for r in out)))
    C.write_outputs(KEY, out, DEFS)
    if "--manifest" in sys.argv:
        C.append_manifest({
            "key": KEY, "family": C.FAMILY, "dataset": "NExTplusplus/TAT-HQA (train, counterfactual questions)",
            "licence": LICENCE, "rows": summ["rows"], "qtype": "yesno", "yesno_share": round(summ["yesno_share"], 4),
            "edge_tags": summ["edge_tags"],
            "notes": ("Hypothetical ('what if') questions over annual-report tables. Yes rows = human hypothetical "
                      "answer (derivation re-checked); no rows mostly = the linked factual answer (ignores the "
                      "assumption), else a derivation slip. <=2 per context (contexts shared with key tatqa); 20% "
                      "negated question; 13-gram decontam."),
        })


if __name__ == "__main__":
    main()
