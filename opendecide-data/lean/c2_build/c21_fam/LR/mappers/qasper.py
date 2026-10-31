"""LR-30 Qasper mapper (qasper-train-v0.3.json). Recast table below (Opus approves, G-R5 batch).

Own label: the annotators' answer type for each question about a paper: yes, no, or unanswerable (their own flags). Recast:
pick-one among Yes / No / Unanswerable over the question + title + abstract + PROGRAM-SELECTED paragraphs of the SAME paper
(LR-B10): every annotated evidence paragraph is kept; distractor paragraphs are other paragraphs of the same paper, in document
order; an unanswerable question has no evidence, so its paragraphs are a random selection of the same count distribution as the
answerable rows. Only questions on which ALL annotators agree on the label are used; evidence that is a figure/table caption
(FLOAT SELECTED) cannot be located as a paragraph, so those rows are dropped. Extractive and free-form answers are not part of this
recast (no yes/no label). Equal thirds over the 3 labels where available (declared). NEVER touched: dev, test (quarantine).
Span-position record for the R10 probe is kept in extra (span_n, gold_positions, gold_rel_pos, gold_len_tokens).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "qasper"
FORM = "lr_qasper_yes_no_unanswerable"
FORMS = {FORM: "According to the paper, is the answer to the question yes, no, or unanswerable?"}
OPTIONS = ["Yes", "No", "Unanswerable"]
BUDGET = 700
RECAST_TABLE = {
    "dataset_id": "allenai/qasper qasper-train-v0.3.json", "train_file": "qasper-train-v0.3.json",
    "split_field": "file name (dev in quarantine, test tarball in quarantine)",
    "source_label_set": ["answer.yes_no true", "answer.yes_no false", "answer.unanswerable true"],
    "recast_option_set": OPTIONS, "target_format": "Choice 3", "mapping": {"yes_no=true": "Yes", "yes_no=false": "No", "unanswerable": "Unanswerable"},
    "distractor_policy": "all 3 labels shown", "declared_balancing": "round-robin over Yes / No / Unanswerable until a label runs out; at most 2 rows per paper",
    "declared_drops": ["annotators disagree on the label", "evidence is a FLOAT SELECTED caption", "gold paragraphs over the budget",
                       "extractive / free-form answers", "R12 guards / PII"],
    "question_form_ids": [FORM], "span_selection_rule": "title + abstract + all evidence paragraphs + same-paper distractor paragraphs in document order, 700-token budget",
    "expected_token_mean": 620,
}
META = {"dataset": DATASET, "lr_id": "LR-30", "family": "LR-reading", "tier": "A", "cap": 800, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE, "native_abstain": "Unanswerable"}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    with open(os.path.join(d, "qasper-train-v0.3.json"), "r", encoding="utf-8") as f:
        for pid, paper in json.load(f).items():
            paper["_pid"] = pid
            paper["_src_line"] = "qasper:" + pid
            yield paper


def paragraphs(paper):
    out = []
    for sec in paper.get("full_text", []):
        for p in sec.get("paragraphs", []):
            t = lc.normalise_ws(p)
            if t:
                out.append((sec.get("section_name") or "", t))
    return out


def answer_label(a):
    """Label of ONE annotator answer: 'Yes' / 'No' / 'Unanswerable' / None (extractive or free-form)."""
    x = a["answer"]
    if x.get("unanswerable"):
        return "Unanswerable"
    if x.get("yes_no") is True:
        return "Yes"
    if x.get("yes_no") is False:
        return "No"
    return None


def question_label(q):
    labs = [answer_label(a) for a in q["answers"]]
    if not labs or any(l is None for l in labs) or len(set(labs)) != 1:
        return None
    return labs[0]


def evidence_paragraphs(q):
    ev = []
    for a in q["answers"]:
        for e in a["answer"].get("evidence", []):
            e = lc.normalise_ws(e)
            if e and e not in ev:
                ev.append(e)
    return ev


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        q = ctx["q"]
        lab = question_label(q)
        if lab is None:
            self.drops.add("annotators_disagree_or_not_yes_no", q.get("question_id"))
            return []
        paras = paragraphs(src)
        ev = evidence_paragraphs(q)
        gold_idx = []
        if lab != "Unanswerable":
            for e in ev:
                if e.startswith("FLOAT SELECTED"):
                    self.drops.add("evidence_is_float_caption", q.get("question_id"))
                    return []
                hit = next((i for i, (_, t) in enumerate(paras) if t == e or e in t), None)
                if hit is None:
                    self.drops.add("evidence_not_a_paragraph", q.get("question_id"))
                    return []
                gold_idx.append(hit)
            if not gold_idx:
                self.drops.add("no_evidence", q.get("question_id"))
                return []
        head = "%s\n\nAbstract: %s" % (lc.normalise_ws(src["title"]), lc.normalise_ws(src["abstract"]))
        budget = BUDGET - lc.approx_tokens(head) - lc.approx_tokens(q["question"]) - 10
        texts = ["[%s] %s" % (s, t) if s else t for s, t in paras]
        sid = "qasper:%s/%s" % (src["_pid"], q["question_id"])
        chosen, info = lc.select_spans(texts, gold_idx, budget, key=sid)
        if chosen is None:
            self.drops.add("R10_length_drop_" + info, sid)
            return []
        if lab == "Unanswerable" and not chosen:
            self.drops.add("no_paragraph_fits", sid)
            return []
        body = "\n\n".join(texts[i] for i in chosen)
        context = "Paper: %s\n\n%s\n\nQuestion: %s" % (head, body, lc.normalise_ws(q["question"]))
        return [{"form": FORM, "kind": "choice", "context": context, "options": list(OPTIONS), "gold_text": lab, "source_row_id": sid,
                 "native_abstain": lab == "Unanswerable",
                 "extra": dict(info, gold_label=lab, paper=src["_pid"], question_id=q["question_id"])}]

    def independent_gold(self, src, cand):
        qid = cand["extra"]["question_id"]
        q = next(x for x in src["qas"] if x["question_id"] == qid)
        kinds = set()
        for a in q["answers"]:
            ans = a["answer"]
            kinds.add("U" if ans["unanswerable"] else ("Y" if ans["yes_no"] is True else ("N" if ans["yes_no"] is False else "X")))
        assert len(kinds) == 1 and "X" not in kinds
        return {"U": "Unanswerable", "Y": "Yes", "N": "No"}[kinds.pop()]

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups = {o: [] for o in OPTIONS}
        for paper in records:
            for q in paper.get("qas", []):
                lab = question_label(q)
                if lab:
                    groups[lab].append((paper, q))

        def make(item):
            paper, q = item
            out = []
            for cand in self.build(paper, {"q": q}):
                r = self.finish_candidate(paper, cand)
                if r:
                    out.append(r)
            return out
        return lc.round_robin_take(groups, "qasper%s" % self.seed, cap, make, unit_of=lambda it: it[0]["_pid"], unit_limit=2)
