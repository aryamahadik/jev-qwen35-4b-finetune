"""LR-54 BoardgameQA mapper (tasksource/Boardgame-QA mirror, train parquet; programmatic gold, no LLM). Recast table below.

Own label: the solver-derived label proved / disproved / unknown of the defeasible-reasoning question. Recast: pick-one among
Proved / Disproved / Unknown over the dataset's own natural-language `example` (game state + rules + preferences + question). The
`proof` field (it states the answer) and the symbolic `theory` / `goal` fields are never read. Rows over the token cap are dropped
(never cut). Equal thirds over the labels (declared; the native abstain label Unknown keeps >= its source share). Round-robin over
`config` (depth / distractor variants) inside each label. NEVER touched: valid, test (quarantine).
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "boardgameqa"
FORM = "lr_boardgameqa_verdict"
FORMS = {FORM: "Based on the game state, the rules and the rule preferences, is the statement proved, disproved, or unknown?"}
OPTIONS = ["Proved", "Disproved", "Unknown"]
MAP = {"proved": "Proved", "disproved": "Disproved", "unknown": "Unknown"}
RECAST_TABLE = {
    "dataset_id": "tasksource/Boardgame-QA (mirror of Kazemi et al. 2023) train parquet", "train_file": "train-*.parquet",
    "split_field": "file name", "source_label_set": ["proved", "disproved", "unknown"], "recast_option_set": OPTIONS,
    "target_format": "Choice 3", "mapping": MAP, "distractor_policy": "all 3 labels shown",
    "declared_balancing": "equal thirds by label, round-robin over config", "declared_drops": ["example over the token cap", "R12 guards"],
    "never_read_fields": ["proof", "theory", "goal"], "question_form_ids": [FORM], "span_selection_rule": "none (whole example; no cut)",
    "expected_token_mean": 700,
}
META = {"dataset": DATASET, "lr_id": "LR-54", "family": "LR-reasoning", "tier": "A", "cap": 400, "share_alike": False,
        "p1_realism": False, "recast_table": RECAST_TABLE, "native_abstain": "Unknown"}


def read_train(train_dir=None):
    import pyarrow.parquet as pq
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    i = 0
    for f in sorted(glob.glob(os.path.join(d, "train-*.parquet"))):
        t = pq.read_table(f, columns=["example", "label", "config"])         # proof / theory / goal are never loaded
        for ex, lab, cfg in zip(t.column("example").to_pylist(), t.column("label").to_pylist(), t.column("config").to_pylist()):
            yield {"example": ex, "label": lab, "config": cfg, "_src_line": "bgqa:%d" % i}
            i += 1


class Mapper(lc.BaseMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        text = lc.normalise_ws(src["example"])
        if not text or src["label"] not in MAP:
            self.drops.add("empty_or_unknown_label", src["_src_line"])
            return []
        gold = MAP[src["label"]]
        return [{"form": FORM, "kind": "choice", "context": text, "options": list(OPTIONS), "gold_text": gold,
                 "source_row_id": src["_src_line"], "native_abstain": gold == "Unknown", "extra": {"config": src["config"]}}]

    def independent_gold(self, src, cand):
        return {"proved": "Proved", "disproved": "Disproved", "unknown": "Unknown"}[src["label"]]

    def map_records(self, records, ctx=None, cap=None, select_key=None):
        cap = cap if cap is not None else META["cap"]
        groups = {}
        for src in records:
            if src["label"] in MAP and lc.approx_tokens(src["example"]) <= lc.TOKEN_ROW_MAX - 40:
                groups.setdefault((src["label"], src["config"]), []).append((src,))
            elif src["label"] in MAP:
                self.drops.add("R6_example_over_cap_precheck", src["_src_line"])
        # label thirds, then round-robin over config inside a label
        by_label = {}
        for (lab, cfg), items in groups.items():
            by_label.setdefault(lab, {})[cfg] = items

        def make(item):
            out = []
            for cand in self.build(item[0], {}):
                r = self.finish_candidate(item[0], cand)
                if r:
                    out.append(r)
            return out
        per = {lab: cap // len(MAP) + (1 if i < cap % len(MAP) else 0) for i, lab in enumerate(sorted(MAP))}
        rows = []
        for lab in sorted(MAP):
            rows += lc.round_robin_take(by_label.get(lab, {}), "bgqa%s%s" % (lab, self.seed), per[lab], make)
        return rows
