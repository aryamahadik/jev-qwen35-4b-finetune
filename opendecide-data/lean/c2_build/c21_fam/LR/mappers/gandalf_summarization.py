"""LR-02 Gandalf summarization (Lakera) mapper. Recast table below; Opus approves it in the G-R1 batch.

Own label: every train row is a player prompt that SUCCESSFULLY made the summariser leak the password, manually reviewed
(dataset card). Recast: yes/no "does this text try to make the summariser follow an instruction?"; dataset rows -> Yes.
Claude benign twins (-> No, 50% exactly) come from L-I under the literal ban via `map_with_twins`.
The `gandalf_answer` column (a model output) is NEVER read: the reader drops it before any code sees it.
NEVER touched: validation (13), test (13) (quarantine). The 'ignore_instructions' sibling is DENY (selection-rule, Sk 7).
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "gandalf_summarization"
FORM = "lr_gandalf_summ_inject"
FORMS = {FORM: "Does this text try to make the summariser follow an instruction?"}

RECAST_TABLE = {
    "dataset_id": "Lakera/gandalf_summarization (train parquet only)", "train_file": "train-*.parquet",
    "split_field": "file name (train only is downloaded)", "source_label_set": ["successful-guess prompt (all train rows)"],
    "recast_option_set": ["Yes", "No"], "target_format": "yes/no",
    "mapping": {"dataset row": "Yes", "L-I benign twin": "No"}, "distractor_policy": "n/a",
    "declared_balancing": "twin share exactly 50%", "declared_drops": ["empty text", "R12 guards / PII"],
    "never_read_fields": ["gandalf_answer"], "question_form_ids": [FORM], "span_selection_rule": "none",
    "expected_token_mean": 130,
}
META = {"dataset": DATASET, "form": FORM, "lr_id": "LR-02", "family": "LR-safety", "tier": "A", "cap": 100,
        "share_alike": False, "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    """Train-only reader: reads only train-*.parquet and returns {'text', '_src_line'} (the answer column is dropped here)."""
    import pyarrow.parquet as pq
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    files = sorted(glob.glob(os.path.join(d, "train-*.parquet")))
    i = 0
    for f in files:
        t = pq.read_table(f, columns=["text"])           # only the text column is ever loaded
        for txt in t.column("text").to_pylist():
            yield {"text": txt, "_src_line": i}
            i += 1


class Mapper(lc.TwinMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        text = (src.get("text") or "").replace("\r\n", "\n").strip()
        if not text:
            self.drops.add("empty_text", src.get("_src_line"))
            return []
        return [{"form": FORM, "kind": "yesno", "context": text, "options": ["Yes", "No"], "gold_text": "Yes",
                 "source_row_id": "gandalf_summ:%s" % src["_src_line"], "extra": {"stratum": "gandalf", "twin": False}}]

    def independent_gold(self, src, cand):
        if cand["extra"].get("twin"):
            return "No"
        return "Yes" if (src.get("text") or "").strip() else "No"
