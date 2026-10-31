"""Row JSON schema for T42c and the view handed to SOLVER B (a separate Sonnet session that writes its own CODE).

Solver B sees only the G0-lite and `ROW_SCHEMA.md`. `b_view(row)` is what B's harness is given per row: the carriers a
model would see plus `witness_inputs` (the structured call plan / typed domain, so B does not have to parse prose), and
NOTHING else: no label, no manifest, no distractor kinds, no generator metadata.
"""
import copy

ROW_FIELDS = ("row_id", "family", "head", "lang", "label", "question_form", "wording_id", "carriers", "prompt_text", "names",
              "witness_inputs", "meta", "manifest")
B_VIEW_FIELDS = ("row_id", "head", "lang", "carriers", "witness_inputs")


def b_view(row):
    v = {k: copy.deepcopy(row[k]) for k in B_VIEW_FIELDS}
    v["carriers"].pop("QUESTION_FORM", None)
    return v


def validate_row(row):
    miss = [f for f in ROW_FIELDS if f not in row]
    return ["missing field %s" % f for f in miss]
