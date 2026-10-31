"""Row schema for T65 and the SOLVER B view. B (a separate session; code only) sees the rendered text and options plus the head: no label, no spec, no witness."""
import copy
import hashlib



def opaque_id(row_id):
    """Opaque id for B (same formula as LP_COMMON.util.opaque_id, repeated here so that this file imports the standard library only: solver B may import nothing else)."""
    return "b-" + hashlib.sha256(("od-solver-b-view|" + str(row_id)).encode("utf-8")).hexdigest()[:16]


ROW_FIELDS = ("row_id", "family", "head", "sub_block", "group_id", "gold", "gold_letter", "options", "question_form", "slots", "rendered", "names", "spec", "witness_inputs",
              "meta", "manifest")
B_VIEW_FIELDS = ("row_id", "head", "sub_block", "rendered", "options", "witness_inputs")


def b_view(row):
    v = {k: copy.deepcopy(row[k]) for k in B_VIEW_FIELDS}
    v["options"] = [{"letter": o["letter"], "text": o["text"]} for o in row["options"]]
    v["witness_inputs"] = {"head": row["witness_inputs"]["head"], "class_group": row["witness_inputs"].get("class_group")}
    v["row_id"] = opaque_id(row["row_id"])          # the real id ends in -a (YES member) / -b (NO member) / -c (CWE head row): never shown to B
    if row["head"] == "CWE":
        v["sub_block"] = "CWE"                       # for a CWE head row the sub-block IS the gold class: B must find the class from the code
    return v


def validate_row(row):
    return ["missing field %s" % f for f in ROW_FIELDS if f not in row]
