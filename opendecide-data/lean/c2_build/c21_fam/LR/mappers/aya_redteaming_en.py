"""LR-01 Aya Red-teaming (English) mapper. Recast table below; Opus approves it in the G-R1 batch.

Own label: every dataset row is a human red-team prompt with >= 1 harm category written by paid native speakers
(arXiv 2406.18682). Recast: yes/no "does this request ask for harmful content?"; dataset rows -> Yes.
Benign twins (-> No) are Claude-written by L-I under the program-enforced literal ban and handed in through
`map_with_twins(..., twins)`; the twin share is EXACTLY 50% (R11). The explanation / translation fields are never read.
NEVER touched: non-English files, any rephrased mix, the frozen 10% hold-out (quarantine store).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import lr_common as lc  # noqa: E402

DATASET = "aya_redteaming_en"
FORM = "lr_aya_harm_request"
FORMS = {FORM: "Does this request ask for harmful content?"}

RECAST_TABLE = {
    "dataset_id": "CohereLabs/aya_redteaming@5a16fee03c19d681b4f3527b6a750e1ed4d434c7 (English file only)",
    "train_file": "aya_eng.train.jsonl", "split_field": "none (own seeded 10% hold-out by prompt id, frozen in the downloader)",
    "source_label_set": ["harm_category: non-empty list of harm categories"],
    "recast_option_set": ["Yes", "No"], "target_format": "yes/no",
    "mapping": {"dataset row (harm_category non-empty)": "Yes", "L-I benign twin": "No"},
    "distractor_policy": "n/a (yes/no)", "declared_balancing": "twin share exactly 50%",
    "declared_drops": ["language != English", "harm_category empty", "R12 guards / PII"],
    "question_form_ids": [FORM], "span_selection_rule": "none (prompts are one sentence)",
    "expected_token_mean": 45,
}

META = {"dataset": DATASET, "form": FORM, "lr_id": "LR-01", "family": "LR-safety", "tier": "A", "cap": 300,
        "share_alike": False, "p1_realism": False, "recast_table": RECAST_TABLE}


def read_train(train_dir=None):
    """Train-only reader (R2): opens exactly one file name; anything else in the folder is never read."""
    d = lc.guard_train_path(train_dir or lc.raw_train_dir(DATASET))
    for r in lc.read_jsonl(os.path.join(d, "aya_eng.train.jsonl")):
        yield r


def _harm_cats(src):
    v = src.get("harm_category")
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except ValueError:
            v = [v] if v.strip() else []
    return [c for c in (v or []) if str(c).strip()]


class Mapper(lc.TwinMapper):
    META = META
    FORMS = FORMS

    def build(self, src, ctx):
        if str(src.get("language", "")).lower() not in ("english", "eng", "en"):
            self.drops.add("A82_9_non_english", src.get("_src_line"))
            return []
        prompt = lc.normalise_ws(src.get("prompt"))
        cats = _harm_cats(src)
        if not prompt or not cats:
            self.drops.add("no_prompt_or_no_harm_category", src.get("_src_line"))
            return []
        sid = "aya:%s" % src.get("_src_line")
        return [{"form": FORM, "kind": "yesno", "context": prompt, "options": ["Yes", "No"], "gold_text": "Yes",
                 "source_row_id": sid, "extra": {"stratum": cats[0], "twin": False}}]

    def independent_gold(self, src, cand):
        if cand["extra"].get("twin"):
            return "No"           # benign by construction (L-I, literal ban)
        # dataset rows: the dataset's own annotation says harmful iff it lists a harm category
        return "Yes" if len(_harm_cats(src)) > 0 else "No"
