"""LR-52 StrategyQA mapper (original release, unofficial 90% train). Recast table below (Opus approves, G-R7 batch).

Own label: the MTurk-written question's boolean answer. Recast: question-ONLY yes/no (no Wikipedia paragraph, no facts, no
decomposition, no term description is shown). Yes rate balanced to 50% by round-robin over the answer. NEVER touched: the
unofficial dev (the 10% held out of the official train), the official test (quarantine). Guard F5: the BIG-bench copy is never used.
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "strategyqa"
FORM = "lr_strategyqa_yesno"
FORMS = {FORM: "Is the answer to the question yes?"}
RECAST_TABLE = {
    "dataset_id": "StrategyQA original release (eladsegal/strategyqa data/strategyqa/train.json, unofficial 90% train)", "train_file": "train.jsonl.gz",
    "split_field": "file (unofficial dev and official test quarantined)", "source_label_set": ["true", "false"],
    "recast_option_set": ["Yes", "No"], "target_format": "yes/no", "mapping": {"true": "Yes", "false": "No"},
    "distractor_policy": "n/a", "declared_balancing": "50% yes (round-robin over the answer)",
    "declared_drops": ["duplicate question text", "non-boolean answer", "empty question", "R12 guards"],
    "question_form_ids": [FORM], "span_selection_rule": "none (question only)", "expected_token_mean": 25,
}
META = {"dataset": DATASET, "lr_id": "LR-52", "family": "LR-reasoning", "tier": "C", "cap": 300, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    import gzip
    import json
    with gzip.open(os.path.join(d, "train.jsonl.gz"), "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                r["_src_line"] = "strategyqa:" + r["qid"]
                yield r


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        sid = src["_src_line"]
        q = lc.normalise_ws(src.get("question"))
        if not isinstance(src.get("answer"), bool) or not q:
            self.drops.add("non_boolean_answer_or_empty", sid)
            return []
        return [{"form": FORM, "kind": "yesno", "context": q, "options": ["Yes", "No"], "gold_text": "Yes" if src["answer"] else "No",
                 "source_row_id": sid, "extra": {}}]

    def independent_gold(self, src, cand):
        return "Yes" if src["answer"] is True else "No"

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups, seen = {"Yes": [], "No": []}, set()
        for src in records:
            k = lc.normalise_ws(src.get("question")).lower()
            if k in seen:
                self.drops.add("duplicate_item", src.get("_src_line"))
                continue
            seen.add(k)
            groups.setdefault("Yes" if src.get("answer") is True else ("No" if src.get("answer") is False else "bad"), []).append((src,))

        def make(item):
            out = []
            for cand in self.build(item[0], {}):
                r = self.finish_candidate(item[0], cand)
                if r:
                    out.append(r)
            return out
        return lc.round_robin_take(groups, "sqa%s" % self.seed, cap, make)
