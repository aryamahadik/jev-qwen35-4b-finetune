"""decision_spans with a ROLE per span (G10). Roles: negation/polarity, number, entity/path/flag, AUTHORITY.

AUTHORITY marks any span whose presence in the user turn creates or limits permission: consent naming, scope
declarations, boundaries, delegation pointers, values whose source is the user turn. Spans are produced by the
wording renderer (wording.py) from slot positions, so they are exact character offsets into the rendered turn.
A family may also export `spoken_view` (not used by L-A families: none of T50/T51/T53 has a spoken view).
"""
ROLE_NEGATION = "negation/polarity"
ROLE_NUMBER = "number"
ROLE_ENTITY = "entity/path/flag"
ROLE_AUTHORITY = "AUTHORITY"
ROLES = (ROLE_NEGATION, ROLE_NUMBER, ROLE_ENTITY, ROLE_AUTHORITY)


def make_span(turn_idx, slot, start, end, roles):
    for r in roles:
        if r not in ROLES:
            raise ValueError("unknown span role %r" % r)
    return {"turn": turn_idx, "slot": slot, "start": start, "end": end, "roles": sorted(roles)}


def check_spans(turns, spans):
    """Every span must index real text in its turn and carry >= 1 valid role."""
    for sp in spans:
        t = turns[sp["turn"]]["text"]
        if not (0 <= sp["start"] < sp["end"] <= len(t)):
            return False
        if not sp["roles"] or any(r not in ROLES for r in sp["roles"]):
            return False
    return True


def authority_spans(spans):
    return [s for s in spans if ROLE_AUTHORITY in s["roles"]]
