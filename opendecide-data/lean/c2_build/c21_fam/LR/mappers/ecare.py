"""LR-49 e-CARE (Causal_Reasoning task) mapper. Recast table below (Opus approves, G-R7 batch).

Own label: the crowd annotator's true hypothesis (label 0 = hypothesis1, 1 = hypothesis2, README of the release). Recast: the
dataset's own 2-way multiple choice, premise shown as context, option order shuffled (gold position balanced); the question form
follows the instance's own `ask-for` field (cause / effect). The conceptual-explanation field was never fetched. NEVER touched:
dev (quarantine; the test set is blind and not in the release).
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "ecare"
F_CAUSE, F_EFFECT = "lr_ecare_cause", "lr_ecare_effect"
FORMS = {F_CAUSE: "Which statement is the more plausible cause of the event described?",
         F_EFFECT: "Which statement is the more plausible effect of the event described?"}
RECAST_TABLE = {
    "dataset_id": "e-CARE (Waste-Wood/e-CARE) dataset/Causal_Reasoning/train.jsonl", "train_file": "train.jsonl",
    "split_field": "file name (dev quarantined; test is blind and not released)",
    "source_label_set": ["label 0 (hypothesis1 correct)", "label 1 (hypothesis2 correct)"],
    "recast_option_set": "hypothesis1 and hypothesis2, shuffled", "target_format": "Choice 2",
    "mapping": {"label": "the hypothesis with that index"}, "distractor_policy": "dataset's own implausible hypothesis",
    "declared_balancing": "50/50 cause/effect (round-robin by ask-for); gold position balanced by the row finisher",
    "declared_drops": ["duplicate (premise, hypothesis1, hypothesis2)", "identical hypotheses", "bad label or ask-for", "R12 guards"],
    "question_form_ids": [F_CAUSE, F_EFFECT], "span_selection_rule": "none", "expected_token_mean": 45,
}
META = {"dataset": DATASET, "lr_id": "LR-49", "family": "LR-reasoning", "tier": "C", "cap": 400, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    for r in lc.read_jsonl(os.path.join(d, "train.jsonl")):
        r["_src_line"] = "ecare:" + str(r["index"])
        yield r


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        sid = src["_src_line"]
        ask = str(src.get("ask-for", "")).strip().lower()
        h = [lc.normalise_ws(src.get("hypothesis1")), lc.normalise_ws(src.get("hypothesis2"))]
        prem = lc.normalise_ws(src.get("premise"))
        if ask not in ("cause", "effect") or src.get("label") not in (0, 1) or not prem or not all(h) or h[0] == h[1]:
            self.drops.add("bad_label_askfor_or_empty", sid)
            return []
        return [{"form": F_CAUSE if ask == "cause" else F_EFFECT, "kind": "choice", "context": prem, "options": h,
                 "gold_text": h[src["label"]], "source_row_id": sid, "extra": {"ask_for": ask}}]

    def independent_gold(self, src, cand):
        return lc.normalise_ws([src["hypothesis1"], src["hypothesis2"]][int(src["label"])])

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups, seen = {"cause": [], "effect": []}, set()
        for src in records:
            key = (lc.normalise_ws(src.get("premise")).lower(), frozenset([lc.normalise_ws(src.get("hypothesis1")).lower(),
                                                                         lc.normalise_ws(src.get("hypothesis2")).lower()]))
            if key in seen:
                self.drops.add("duplicate_item", src.get("_src_line"))
                continue
            seen.add(key)
            ask = str(src.get("ask-for", "")).strip().lower()
            groups.setdefault(ask if ask in ("cause", "effect") else "bad", []).append((src,))

        def make(item):
            out = []
            for cand in self.build(item[0], {}):
                r = self.finish_candidate(item[0], cand)
                if r:
                    out.append(r)
            return out
        return lc.round_robin_take(groups, "ecare%s" % self.seed, cap, make)
