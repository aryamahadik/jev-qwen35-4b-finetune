"""Row schema for T66 and the view handed to SOLVER B (a separate Sonnet session that writes its own CODE; G1). B sees only the G0-lite and ROW_SCHEMA.md and
gets, per row, the RENDERED text and options a model sees plus the head; NOTHING else: no label, no spec, no witnesses, no construction ids."""
import copy
import hashlib



def opaque_id(row_id):
    """Opaque id for B (same formula as LP_COMMON.util.opaque_id, repeated here so that this file imports the standard library only: solver B may import nothing else)."""
    return "b-" + hashlib.sha256(("od-solver-b-view|" + str(row_id)).encode("utf-8")).hexdigest()[:16]


ROW_FIELDS = ("row_id", "family", "head", "sub_block", "group_id", "gold", "gold_letter", "options", "question_form", "slots", "rendered", "names", "spec",
              "witness_inputs", "meta", "manifest")
B_VIEW_FIELDS = ("row_id", "head", "sub_block", "rendered", "options", "witness_inputs")


def b_view(row):
    v = {k: copy.deepcopy(row[k]) for k in B_VIEW_FIELDS}
    v["options"] = [{"letter": o["letter"], "text": o["text"]} for o in row["options"]]
    v["row_id"] = opaque_id(row["row_id"])          # the real id's member letter orders the YES / BREAKING member first in a pair: never shown to B
    return v


def validate_row(row):
    return ["missing field %s" % f for f in ROW_FIELDS if f not in row]
