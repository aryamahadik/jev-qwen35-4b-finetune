"""LR-48 Social IQa v1.4 mapper. Recast table below (Opus approves, G-R7 batch).

Own label: the crowd majority-vote correct answer (train-labels.lst, 1 / 2 / 3 = answerA / B / C). Recast: the dataset's own
3-way multiple choice; the context and the question are shown as the situation, the three answers as options (shuffled, gold
position balanced). Wrong answers are human-written (handwritten incorrect or question-switched handwritten answers, shipped
README of the release). NEVER touched: dev (quarantine); the test set is hidden and not in the release.
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "social_iqa"
FORM = "lr_siqa_pick"
FORMS = {FORM: "Which answer best fits the situation and the question?"}
RECAST_TABLE = {
    "dataset_id": "Social IQa v1.4 (AI2 socialiqa-train-dev.zip) train.jsonl + train-labels.lst", "train_file": "train.jsonl",
    "split_field": "file name (dev.jsonl quarantined; test hidden)", "source_label_set": ["1", "2", "3"],
    "recast_option_set": "answerA, answerB, answerC, shuffled", "target_format": "Choice 3",
    "mapping": {"1": "answerA", "2": "answerB", "3": "answerC"}, "distractor_policy": "dataset's own two wrong answers",
    "declared_balancing": "round-robin over the question's first two words (question type); gold position balanced",
    "declared_drops": ["duplicate (context, question)", "missing or out-of-range label", "duplicate answer text", "R12 guards"],
    "question_form_ids": [FORM], "span_selection_rule": "none", "expected_token_mean": 70,
}
META = {"dataset": DATASET, "lr_id": "LR-48", "family": "LR-reasoning", "tier": "C", "cap": 400, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    labels = [l.strip() for l in open(os.path.join(d, "train-labels.lst"), encoding="utf-8")]
    for i, r in enumerate(lc.read_jsonl(os.path.join(d, "train.jsonl"))):
        r["label"] = labels[i] if i < len(labels) else None
        r["_src_line"] = "siqa:train#%d" % i
        yield r


def _qtype(q):
    return " ".join(lc.normalise_ws(q).lower().split()[:2]) or "?"


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        sid = src["_src_line"]
        ans = [lc.normalise_ws(src.get("answer" + k)) for k in "ABC"]
        lab = str(src.get("label", "")).strip()
        if lab not in ("1", "2", "3") or not all(ans) or not lc.normalise_ws(src.get("context")) or not lc.normalise_ws(src.get("question")):
            self.drops.add("bad_label_or_empty", sid)
            return []
        text = "Situation: %s\nQuestion: %s" % (lc.normalise_ws(src["context"]), lc.normalise_ws(src["question"]))
        return [{"form": FORM, "kind": "choice", "context": text, "options": ans, "gold_text": ans[int(lab) - 1],
                 "source_row_id": sid, "extra": {"qtype": _qtype(src["question"])}}]

    def independent_gold(self, src, cand):
        return lc.normalise_ws(src["answer" + "ABC"[int(str(src["label"]).strip()) - 1]])

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups, seen = {}, set()
        for src in records:
            k = (lc.normalise_ws(src.get("context")).lower(), lc.normalise_ws(src.get("question")).lower())
            if k in seen:
                self.drops.add("duplicate_item", src.get("_src_line"))
                continue
            seen.add(k)
            groups.setdefault(_qtype(src.get("question") or ""), []).append((src,))

        def make(item):
            out = []
            for cand in self.build(item[0], {}):
                r = self.finish_candidate(item[0], cand)
                if r:
                    out.append(r)
            return out
        return lc.round_robin_take(groups, "siqa%s" % self.seed, cap, make)
