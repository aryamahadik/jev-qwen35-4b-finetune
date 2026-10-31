"""Row schema for T67 and the view handed to SOLVER B (a separate Sonnet session that writes its own CODE; G1).

B sees only the G0-lite, the card schema and ROW_SCHEMA.md. `b_view(row)` is what B's harness gets per row: the rendered text (policy card, session notes
or table card, user turn, proposed call, file) and the lettered options a model sees. NOTHING else: no label, no spec, no meta, no manifest, no rule ids.
"""
import copy
import hashlib



def opaque_id(row_id):
    """Opaque id for B (same formula as LP_COMMON.util.opaque_id, repeated here so that this file imports the standard library only: solver B may import nothing else)."""
    return "b-" + hashlib.sha256(("od-solver-b-view|" + str(row_id)).encode("utf-8")).hexdigest()[:16]


ROW_FIELDS = ("row_id", "family", "head", "sub_block", "group_id", "gold", "gold_letter", "options", "question_form", "slots", "rendered", "names", "spec",
              "decision_spans", "witness_inputs", "meta", "manifest")
B_VIEW_FIELDS = ("row_id", "head", "sub_block", "rendered", "options", "witness_inputs")


def b_view(row):
    v = {k: copy.deepcopy(row[k]) for k in B_VIEW_FIELDS}
    v["options"] = [{"letter": o["letter"], "text": o["text"]} for o in row["options"]]
    v["witness_inputs"] = {"carrier": row["witness_inputs"]["carrier"], "head": row["witness_inputs"]["head"]}
    v["row_id"] = opaque_id(row["row_id"])          # the real id carries the group id (block name) and the cell letter: never shown to B
    v["sub_block"] = row["witness_inputs"]["carrier"]   # the block id names all-ALLOW / all-BLOCK blocks (P-d, P-e, K-d, C-d): B gets the carrier only
    return v


def validate_row(row):
    return ["missing field %s" % f for f in ROW_FIELDS if f not in row]
