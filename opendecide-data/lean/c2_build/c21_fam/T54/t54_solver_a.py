"""T54 TOOL-NEED/PICK -- SOLVER A (gold inside the generator; reads the structured record, never the rendered prompt).

Implements G0-lite section 3.2 exactly, with the Opus rulings of 18 Oct (G0_APPROVALS): C1 = ANSWER only when the
answer content is present in the rendered context or card and a program locates it (a fact id in rec["facts"]);
"general knowledge the card allows" is deleted. Solver B is a separate session and is NOT here.

Record fields read (all structured):
  card (base card id), cards (all active card ids), tools [..], intent {...}, facts [..], fact (S4), call (S5), dag (S6).
"""
from tool_engine import dag as dagmod

S1_LABELS = ("CALL", "ASK", "NO_TOOL", "ANSWER")
S3_LABELS = ("CALL", "NO_TOOL", "ASK", "RESULT_MISSING")
S4_LABELS = ("WRITE", "READ_FIRST", "DONE_NO_CALL", "ASK")
S5_LABELS = ("GROUNDED", "UNGROUNDED")
CALL_BEARING = ("CALL", "WRITE", "READ_FIRST")                # call-bearing definition (ruling 4)

STRICT, DEFAULTS_OK = "card.t54.strict_ask", "card.t54.defaults_ok"
DECLARED_ALWAYS = ("case", "whitespace", "ordinal_digit")     # transformations every card allows


class SpecError(ValueError):
    """The record violates a rule the generator must guarantee (e.g. an ANSWER with no locatable fact)."""


def defaults_allowed(rec):
    """True iff the active card lets declared defaults count as a source."""
    base = rec["card"]
    if base == DEFAULTS_OK:
        return True
    if base == STRICT:
        return False
    raise SpecError("base card must be strict_ask or defaults_ok, got %r" % base)


def effective_source(arg, rec):
    """Source of one intent argument under the active card. A value nobody supplied (source 'none') becomes a
    card_default source only when the tool declares a default for it AND the card allows defaults."""
    s = arg["source"]
    if s == "none" and arg.get("default") is not None and defaults_allowed(rec):
        return "card_default"
    return s


def target_listed(rec):
    g = rec["intent"].get("target_group")
    return any(t["group"] == g for t in rec["tools"])


def _locate_fact(rec):
    ans = rec["intent"].get("answer")
    if not ans:
        raise SpecError("ANSWER row without an answer pointer")
    for f in rec.get("facts", []):
        if f["fact_id"] == ans["fact_id"] and f["where"] == ans["where"] and f["where"] in ("context", "card"):
            return f
    raise SpecError("answer fact %r not located in the %s" % (ans["fact_id"], ans.get("where")))


def gold_s1(rec):
    """S1 NEED4, first match wins."""
    intent = rec["intent"]
    if intent["type"] == "tool" and not target_listed(rec):          # 1. no listed tool fits
        return "NO_TOOL"
    if intent["type"] == "info":                                     # 2. non-tool-shaped
        _locate_fact(rec)                                            #    C1: a program must locate the answer
        return "ANSWER"
    for a in intent["args"]:                                         # 3. required param with no source
        if a["required"] and effective_source(a, rec) == "none":
            return "ASK"
    return "CALL"                                                    # 4.


def gold_s3(rec):
    """S3 LIMIT: the S1 rule after a deletion; RESULT_MISSING when a value's earlier result is absent."""
    intent = rec["intent"]
    if not target_listed(rec):
        return "NO_TOOL"
    for a in intent["args"]:
        if a["required"] and a["source"] == "missing_result":
            return "RESULT_MISSING"
    for a in intent["args"]:
        if a["required"] and effective_source(a, rec) == "none":
            return "ASK"
    return "CALL"


def satisfies(tool, intent):
    names = {p["name"] for p in tool["params"]}
    return tool["group"] == intent["target_group"] and all(a["param"] in names for a in intent["args"])


def gold_s2(rec):
    """S2 PICK: the unique listed tool whose (verb, entity, schema) satisfies the request spec. Returns the tool NAME.
    Two satisfying tools -> SpecError (the row is rejected by the generator)."""
    sat = [t for t in rec["tools"] if satisfies(t, rec["intent"])]
    if len(sat) != 1:
        raise SpecError("S2 needs exactly one satisfying tool, found %d" % len(sat))
    return sat[0]["name"]


def gold_s4(rec):
    """S4 PRECOND under card.t54.read_before_write."""
    f = rec["fact"]
    w = next(t for t in rec["tools"] if t["tid"] == f["write_tid"])
    args_sourced = all(effective_source(a, rec) != "none" for a in rec["intent"]["args"] if a["required"])
    if f["state"] == "observed_true":
        return "DONE_NO_CALL"
    if f["state"] == "observed_false":
        return "WRITE" if args_sourced else "ASK"
    if f["state"] != "unobserved":
        raise SpecError("fact state %r" % f["state"])
    if w["idempotent"]:
        return "WRITE"
    has_read = any(t["tid"] == f.get("read_tid") for t in rec["tools"]) and f.get("read_tid") is not None
    return "READ_FIRST" if has_read else "ASK"


def provenance_grounded(prov, rec):
    """Is one supplied value grounded? prov = {"kind": user_turn|prior_output_same_role|card_default|transform|none|
    wrong_role, "base": <kind of the base value for a transform>, "transform": id}."""
    k = prov["kind"]
    if k in ("user_turn", "prior_output_same_role"):
        return True
    if k == "card_default":
        return defaults_allowed(rec)
    if k == "transform":
        t = prov["transform"]
        ok_t = t in DECLARED_ALWAYS or t in rec.get("declared_conversions", [])
        return ok_t and provenance_grounded({"kind": prov["base"]}, rec)
    if k in ("none", "wrong_role"):
        return False
    raise SpecError("provenance kind %r" % k)


def gold_s5(rec):
    return "GROUNDED" if all(provenance_grounded(a["prov"], rec) for a in rec["call"]["args"]) else "UNGROUNDED"


# ---- S6 -----------------------------------------------------------------------------------------------------
def s6_ready_nodes(rec):
    d = rec["dag"]
    return dagmod.ready_set(d["nodes"], [tuple(e) for e in d["edges"]], d["done"])


def s6_canonical(rec, node_ids):
    """Canonical form of a call set: sorted tuple of equivalence-group ids (substitutable tools collapse)."""
    g = {n["id"]: n["group"] for n in rec["dag"]["node_tools"]}
    return dagmod.canonical_set(g, node_ids)


def gold_s6(rec):
    """Gold = the READY set (Kahn level 0 of the remaining DAG), as the option whose canonical form equals it.
    Exactly one option may match (generator assertion); returns that option's label."""
    ready = s6_ready_nodes(rec)
    want = s6_canonical(rec, ready)
    hits = [o["label"] for o in rec["options"] if tuple(o["canon"]) == want]
    if len(hits) != 1:
        raise SpecError("S6 needs exactly one option equal to the ready set, found %d" % len(hits))
    return hits[0]


def gold_label(rec):
    sb = rec["sub_block"]
    return {"s1_need4": gold_s1, "s2_pick": gold_s2, "s3_limit": gold_s3, "s4_precond": gold_s4,
            "s5_argground": gold_s5, "s6_parseq": gold_s6}[sb](rec)


def is_call_bearing(label):
    return label in CALL_BEARING
