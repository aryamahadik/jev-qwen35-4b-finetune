"""LR-50 QuaRTz mapper. Recast table below (Opus approves, G-R7 batch).

Own label: the crowd answerKey. Recast: the dataset's own 2-way multiple choice (question as context, the two choice texts as
options, shuffled, gold position balanced). The background sentence (`para`) and all annotation fields were dropped at download
and are never read. NEVER touched: validation, test (quarantine).
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "quartz"
FORM = "lr_quartz_pick"
FORMS = {FORM: "Which option correctly answers the question or completes the sentence?"}
RECAST_TABLE = {
    "dataset_id": "QuaRTz (allenai/quartz revision in the download log) train split", "train_file": "train.jsonl.gz",
    "split_field": "parquet file name (validation and test quarantined)", "source_label_set": ["A", "B"],
    "recast_option_set": "the 2 given choices, shuffled", "target_format": "Choice 2", "mapping": {"answerKey": "the choice with that label"},
    "distractor_policy": "dataset's own other choice", "declared_balancing": "round-robin over the QRQA parent id (one background sentence's questions spread)",
    "declared_drops": ["duplicate question text", "missing answerKey", "not exactly 2 choices", "identical choice texts", "R12 guards"],
    "question_form_ids": [FORM], "span_selection_rule": "none", "expected_token_mean": 55,
}
META = {"dataset": DATASET, "lr_id": "LR-50", "family": "LR-reasoning", "tier": "C", "cap": 200, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    import gzip
    import json
    with gzip.open(os.path.join(d, "train.jsonl.gz"), "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                r["_src_line"] = "quartz:" + r["id"]
                yield r


def _parent(rid):
    parts = str(rid).split("-")
    return "-".join(parts[:2]) if len(parts) >= 2 else str(rid)


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        sid = src["_src_line"]
        ch = src.get("choices") or {}
        texts, labels = ch.get("text") or [], ch.get("label") or []
        key = src.get("answerKey")
        if len(texts) != 2 or len(labels) != 2 or key not in labels or not lc.normalise_ws(src.get("question")):
            self.drops.add("missing_key_or_not_2_choices", sid)
            return []
        opts = [lc.normalise_ws(t) for t in texts]
        return [{"form": FORM, "kind": "choice", "context": lc.normalise_ws(src["question"]), "options": opts,
                 "gold_text": opts[labels.index(key)], "source_row_id": sid, "extra": {"parent": _parent(src["id"])}}]

    def independent_gold(self, src, cand):
        by = dict(zip(src["choices"]["label"], src["choices"]["text"]))
        return lc.normalise_ws(by[src["answerKey"]])

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups, seen = {}, set()
        for src in records:
            k = lc.normalise_ws(src.get("question")).lower()
            if k in seen:
                self.drops.add("duplicate_item", src.get("_src_line"))
                continue
            seen.add(k)
            groups.setdefault(_parent(src.get("id", "")), []).append((src,))

        def make(item):
            out = []
            for cand in self.build(item[0], {}):
                r = self.finish_candidate(item[0], cand)
                if r:
                    out.append(r)
            return out
        return lc.round_robin_take(groups, "quartz%s" % self.seed, cap, make)
