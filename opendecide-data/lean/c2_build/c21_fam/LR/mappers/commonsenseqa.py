"""LR-47 CommonsenseQA (original release, train_rand_split.jsonl) mapper. Recast table below (Opus approves, G-R7 batch).

Own label: the crowd workers' answerKey. Recast: the dataset's own 5-way multiple choice, unchanged except for option order
(shuffled, gold position balanced). The question concept is not shown. Every choice text is the dataset's own (one ConceptNet
distractor and one worker-written distractor per question are part of the release). NEVER touched: dev, test (quarantine).
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "commonsenseqa"
FORM = "lr_csqa_pick"
FORMS = {FORM: "Which answer best completes or answers the question?"}
RECAST_TABLE = {
    "dataset_id": "CommonsenseQA original release (talmor, S3) train_rand_split.jsonl", "train_file": "train_rand_split.jsonl",
    "split_field": "file name", "source_label_set": ["answerKey A-E"], "recast_option_set": "the 5 given choices, shuffled",
    "target_format": "Choice 5", "mapping": {"answerKey": "the choice text with that label"},
    "distractor_policy": "dataset's own 4 distractors", "declared_balancing": "stratified over question_concept (round-robin)",
    "declared_drops": ["duplicate choice text", "missing answerKey", "R12 guards"], "question_form_ids": [FORM],
    "span_selection_rule": "none", "expected_token_mean": 40,
}
META = {"dataset": DATASET, "lr_id": "LR-47", "family": "LR-reasoning", "tier": "A", "cap": 400, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    for r in lc.read_jsonl(os.path.join(d, "train_rand_split.jsonl")):
        r["_src_line"] = "csqa:" + r["id"]
        yield r


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        q = src["question"]
        ch = q["choices"]
        key = src.get("answerKey")
        by = {c["label"]: lc.normalise_ws(c["text"]) for c in ch}
        if key not in by or len(ch) != 5:
            self.drops.add("missing_answer_key_or_not_5_choices", src["_src_line"])
            return []
        opts = [lc.normalise_ws(c["text"]) for c in ch]
        return [{"form": FORM, "kind": "choice", "context": lc.normalise_ws(q["stem"]), "options": opts, "gold_text": by[key],
                 "source_row_id": src["_src_line"], "extra": {"concept": q.get("question_concept")}}]

    def independent_gold(self, src, cand):
        letters = [c["label"] for c in src["question"]["choices"]]
        return lc.normalise_ws(src["question"]["choices"][letters.index(src["answerKey"])]["text"])

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups = {}
        for src in records:
            groups.setdefault(src["question"].get("question_concept") or "?", []).append((src,))

        def make(item):
            out = []
            for cand in self.build(item[0], {}):
                r = self.finish_candidate(item[0], cand)
                if r:
                    out.append(r)
            return out
        return lc.round_robin_take(groups, "csqa%s" % self.seed, cap, make)
