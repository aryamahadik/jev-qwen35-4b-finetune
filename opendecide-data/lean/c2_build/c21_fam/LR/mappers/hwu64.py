"""LR-13 HWU64 mapper (upstream xliuhw/NLU-Evaluation-Data, KFold_1 trainset). Recast table below (Opus approves, G-R3 batch).

Own label: scenario_intent chosen by the annotators for each MTurk-typed answer (arXiv 1903.05566). Recast: pick-one intent,
gold + (k-1) hard distractor intents (label-name overlap + TF-IDF logistic confusion fitted on the train items only),
k alternating 4 / 8 (64 intents > 8, LR-B1). Utterance = the user's own text with the [slot : value] annotation markup
replaced by the value. The question column (the scenario prompt) is not shown. NEVER touched: the KFold_1 test fold.
"""
import csv
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "hwu64"
FORM = "lr_hwu64_intent"
FORMS = {FORM: "Which intent does this request express?"}
RECAST_TABLE = {
    "dataset_id": "xliuhw/NLU-Evaluation-Data@f6071b496b17d71e6eb43f543af0707f4ff30557 KFold_1 trainset (upstream)",
    "train_file": "KFold_1_trainset/*.csv", "split_field": "directory (trainset vs testset)",
    "source_label_set": ["scenario_intent, 64 values (e.g. alarm_query)"], "recast_option_set": "gold intent + k-1 confusable intents",
    "target_format": "Choice k in {4, 8} (rotating)", "mapping": {"scenario;intent": "scenario_intent"},
    "distractor_policy": "name overlap + TF-IDF logistic confusion on the train items", "declared_balancing":
    "round-robin over the 64 intents; k alternates", "declared_drops": ["empty utterance", "R12 guards / PII"],
    "question_form_ids": [FORM], "span_selection_rule": "none", "expected_token_mean": 25,
}
META = {"dataset": DATASET, "form": FORM, "lr_id": "LR-13", "family": "LR-intent", "tier": "A", "cap": 500,
        "share_alike": False, "p1_realism": False, "recast_table": RECAST_TABLE}
_MARK = re.compile(r"\[\s*[^:\]]+?\s*:\s*([^\]]+?)\s*\]")


def clean_utterance(s):
    return lc.normalise_ws(_MARK.sub(r"\1", s or ""))


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    for p in sorted(glob.glob(os.path.join(d, "KFold_1_trainset", "*.csv"))):
        with open(p, "r", encoding="utf-8", newline="") as f:
            for i, row in enumerate(csv.DictReader(f, delimiter=";", quotechar='"')):
                # answerid repeats across users in the release, so the row index is part of the id
                row["_src_line"] = "%s:%s:%d" % (os.path.basename(p), row.get("answerid"), i)
                yield row


class Mapper(lc.ClassPickMapper):
    META = META
    FORMS = FORMS

    def item(self, src):
        text = clean_utterance(src.get("answer_from_user") or src.get("answer_from_anno"))
        sc, it = (src.get("scenario") or "").strip(), (src.get("intent") or "").strip()
        if not text or not sc or not it:
            return None
        return text, "%s_%s" % (sc, it), "hwu64:%s" % src["_src_line"]

    def independent_gold(self, src, cand):
        return "%s_%s" % (src["scenario"].strip(), src["intent"].strip())
