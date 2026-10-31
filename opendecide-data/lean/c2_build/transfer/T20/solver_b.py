"""transfer/T20/solver_b.py: T20 solver B, written from G0_SPEC.md v3 (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the incident record first (list, table or export layout), the critical list and the maintenance window by this
    module's own patterns; times through slots.parse("datetime"), counts through slots.parse("count");
  - then the card, by a pattern built from this module's own copy of the G0 v3 card parts for the style (full or short)
    and the variants the record implies (Step 1 only when a window is declared, the times sentence only when the minute
    lines are not printed, the "reaches" sentence only on yes/no rows): the two impact thresholds, the escalation step
    and the nine matrix cells are read from the printed card itself. The card is found with cards.split_rules(row): in
    row.card on a yes/no row, at the head of the instructions on a choice row (rules, then the question);
  - the narrative skin (Mode T) through skin.parse_skin, the question through its wording template (or, for the
    program-written double-negation wordings, through this module's own copies of them);
  - on choice rows, every option text ("SEV1" ...) back to its key.
Printed minute counts must equal the epoch-minute differences of the printed times. A row outside the G0 R2 domain
(check not after opening, acknowledgement not in (opening, check], window start not before its end, a negative count,
a critical list without two distinct services) is refused (ParseError), never answered.
solve_b(view) SIMULATES: the impact band by scanning the thresholds, the base severity from the parsed matrix, then
the four steps in order (the exposure step is the card's own rule: its band condition and its effect, G0 v4 R8); escalation walks the clock minute by minute from opening to the check time (epoch minutes
from brute.epoch_minutes), raising one level at every due step not yet acknowledged. Imports no solver-A code.
"""
from __future__ import annotations

import re
from functools import lru_cache

from c2_kit import brute
from c2_kit import cards
from c2_kit import skin as K
from c2_kit import slots as S

CLOSED = ("The incident record, the critical list, the maintenance window and these rules are complete: "
          "nothing else changes the answer.")
# the G0 v3 card, part by part (@NAME@ marks a value read from the printed card); two styles
PARTS = {
    "full": {
        "head": "SEV1 is the most severe, SEV4 the least.",
        "impact": "Impact: wide if @U2@ or more users, partial if @U1@ or more but fewer than @U2b@, otherwise minimal.",
        "base": ("Base severity (outage, degraded, cosmetic): wide @WO@, @WD@, @WC@; partial @PO@, @PD@, @PC@; "
                 "minimal @MO@, @MD@, @MC@."),
        "steps_w": ("Then, in order:\n"
                    "If opened inside the maintenance window (start included, end excluded): one level less "
                    "severe, never less severe than SEV4. The window has no other effect.\n"
                    "If the service is on the critical list and less severe than SEV2: SEV2.\n"
                    "A step falls due at each full @STEP@ after opening. Each step due at or before the check "
                    "time: one level more severe, never more severe than SEV1, unless acknowledged at or before that "
                    "step's time.\n"
                    "@XR@"),
        "steps_n": ("Then, in order:\n"
                    "If the service is on the critical list and less severe than SEV2: SEV2.\n"
                    "A step falls due at each full @STEP@ after opening. Each step due at or before the check "
                    "time: one level more severe, never more severe than SEV1, unless acknowledged at or before that "
                    "step's time.\n"
                    "@XR@"),
        "times": "Times are whole minutes at fixed UTC offsets, compared as points in time.",
        "reach": "An incident reaches a level when its severity is that level or more severe.",
    },
    "short": {
        "head": "SEV1 most severe, SEV4 least.",
        "impact": "Impact: wide if @U2@ or more users, partial if @U1@ or more but fewer than @U2b@, otherwise minimal.",
        "base": ("Base severity (outage, degraded, cosmetic): wide @WO@, @WD@, @WC@; partial @PO@, @PD@, @PC@; "
                 "minimal @MO@, @MD@, @MC@."),
        "steps_w": ("In order:\n"
                    "If opened inside the maintenance window (start included, end excluded): one level less "
                    "severe, never less severe than SEV4; no other effect.\n"
                    "If the service is on the critical list and less severe than SEV2: SEV2.\n"
                    "A step falls due at each full @STEP@ after opening; each step due at or before the check "
                    "time: one level more severe, never more severe than SEV1, unless acknowledged at or before that "
                    "step's time.\n"
                    "@XR@"),
        "steps_n": ("In order:\n"
                    "If the service is on the critical list and less severe than SEV2: SEV2.\n"
                    "A step falls due at each full @STEP@ after opening; each step due at or before the check "
                    "time: one level more severe, never more severe than SEV1, unless acknowledged at or before that "
                    "step's time.\n"
                    "@XR@"),
        "times": "Times are whole minutes at fixed UTC offsets, compared as points in time.",
        "reach": "An incident reaches a level when its severity is that level or more severe.",
    },
}
# the program-written double-negation questions (G0 v3 R12); read when a row's meta names no wording skin
PROGRAM_DN = (
    "Is it not the case that incident {INC_ID} does not reach {LEVEL} at the check time?",
    "At the check time, is it not true that incident {INC_ID} does not reach {LEVEL}?",
    "Under these rules, is it not the case that incident {INC_ID} does not reach {LEVEL} as of the check time?",
    "Is it not true that, as of the check time, incident {INC_ID} does not reach {LEVEL}?",
)
_GROUPS = {"U2": r"\d[\d,]*", "U1": r"\d[\d,]*", "STEP": r"\d+ minutes?", "WO": "SEV[1-4]", "WD": "SEV[1-4]",
           "WC": "SEV[1-4]", "PO": "SEV[1-4]", "PD": "SEV[1-4]", "PC": "SEV[1-4]", "MO": "SEV[1-4]",
           "MD": "SEV[1-4]", "MC": "SEV[1-4]"}


# G0 v4 R8: the exposure step is a per-card rule: "If customer data was exposed[ and the impact is ...]: <effect>."
_XR_RX = (r"If customer data was exposed(?P<XC>| with wide impact): "
          r"(?P<XE>SEV1|SEV2 or more severe|one level more severe)\.")
X_COND = {"": "any", " with wide impact": "wide"}
X_EFF = {"SEV1": "sev1", "SEV2 or more severe": "sev2", "one level more severe": "up"}


@lru_cache(maxsize=None)
def _card_rx(style: str, window: bool, one_offset: bool, yes_no: bool) -> re.Pattern:
    p = PARTS[style]
    items = [p["impact"], p["base"], p["steps_w" if window else "steps_n"]]
    if not one_offset:
        items.append(p["times"])
    if yes_no:
        items.append(p["reach"])
    body = re.escape("\n".join([p["head"]] + items + [CLOSED]))
    body = body.replace("@XR@", _XR_RX)
    for name in ("U2b", "U2", "U1", "STEP", "WO", "WD", "WC", "PO", "PD", "PC", "MO", "MD", "MC"):
        pat = _GROUPS[name.rstrip("b")]
        if name == "U2b":
            body = body.replace(re.escape("@U2b@"), r"(?P<U2b>" + pat + ")")
        else:
            body = body.replace(re.escape(f"@{name}@"), f"(?P<{name}>{pat})", 1)
    return re.compile(body)


USERS = (("unit", ("user", "users")),)
MINS = (("unit", ("minute", "minutes")),)
SEV_OF = {"SEV1": 1, "SEV2": 2, "SEV3": 3, "SEV4": 4}
SERVICES = ("payments", "login", "search", "checkout", "reports", "email", "storage", "chat")
FIELDS = ("opened", "users affected", "urgency reported", "customer data exposed", "acknowledged", "check time",
          "minutes from opening to the check", "minutes from opening to the acknowledgement")
_LEVELS = ("category", (("surfaces", tuple((f"sev{i}", (f"SEV{i}",)) for i in range(1, 5))),))
SCHEMA = {"TEAM": ("name", ()), "REPORTER": ("name", ()), "INC_ID": ("id", ()), "LEVEL": _LEVELS, "LEVEL_NEXT": _LEVELS}


class ParseError(ValueError):
    pass


def _dt(text: str) -> str:
    return S.parse("datetime", text).isoformat()


def _record(text: str) -> tuple:
    """(incident id, service, {field: value text}, critical list text, window text) for any of the three layouts."""
    lines = text.split("\n")
    if lines[0] == "export incident:":
        lines = [x[2:] if x.startswith("  ") else x for x in lines[1:]]
        head = lines[0]
        pairs = [x.split(": ", 1) for x in lines[1:] if not x.startswith(("Critical services:",
                                                                           "Maintenance window:"))]
        tail = [x for x in lines[1:] if x.startswith(("Critical services:", "Maintenance window:"))]
    elif len(lines) > 1 and lines[1] == "| field | value |":
        head = lines[0]
        rows = [x for x in lines[3:] if x.startswith("| ")]
        pairs = [x[2:-2].split(" | ", 1) for x in rows]
        tail = [x for x in lines[3:] if not x.startswith("| ")]
    else:
        head = lines[0]
        pairs = [x[2:].split(": ", 1) for x in lines[1:] if x.startswith("- ")]
        tail = [x for x in lines[1:] if not x.startswith("- ")]
    hm = re.fullmatch(r"Incident (?P<id>\S+) on (?P<svc>[a-z]+):", head)
    if not hm or hm["svc"] not in SERVICES:
        raise ParseError("incident heading")
    fields = {}
    for p in pairs:
        if len(p) != 2 or p[0] not in FIELDS or p[0] in fields:
            raise ParseError(f"record field {p!r}")
        fields[p[0]] = p[1]
    if len(tail) != 2:
        raise ParseError("critical list and maintenance window lines")
    return hm["id"], hm["svc"], fields, tail[0][len("Critical services: "):], tail[1][len("Maintenance window: "):]


def _asked(row: dict, ctx, question: str) -> tuple:
    """(the question's placeholders read back, its question form)."""
    wid = row["meta"]["wording_id"]
    if wid:
        wording = ctx.skin(wid)
        return K.match_template(wording.text, question, SCHEMA), wording.qform
    for text in PROGRAM_DN:
        try:
            return K.match_template(text, question, SCHEMA), "yn_double_neg"
        except K.TemplateMismatch:
            continue
    raise ParseError("the question is neither an admitted wording nor a G0 v3 program wording")


def parse(row: dict, ctx) -> dict:
    rules, question = cards.split_rules(row)
    narrative, sep, rest = row["state"].partition("\n\n")
    if not sep:
        raise ParseError("no blank line after the narrative")
    block, _sep, _attack = rest.partition("\n\n")
    inc, svc, f, crit, mw = _record(block)
    cm = None
    for style in ("full", "short"):
        cm = _card_rx(style, mw != "none declared", "minutes from opening to the check" in f,
                      row["qtype"] == "noul").fullmatch(rules)
        if cm:
            break
    if not cm or cm["U2"] != cm["U2b"]:
        raise ParseError("the card is not the G0 v3 card for this record")
    crit_list = crit.split(", ")
    if len(crit_list) != 2 or len(set(crit_list)) != 2 or any(c not in SERVICES for c in crit_list):
        raise ParseError("critical list")
    window = None
    if mw != "none declared":
        a, b = mw.split(" to ")
        window = [_dt(a), _dt(b)]
    if f.get("customer data exposed") not in ("yes", "no") or f.get("urgency reported") not in (
            "outage", "degraded", "cosmetic"):
        raise ParseError("exposure or urgency field")
    ack = None if f["acknowledged"] == "not acknowledged" else _dt(f["acknowledged"])
    view = {"incident": S.parse("id", inc), "service": svc, "users": S.parse("count", f["users affected"], USERS),
            "urgency": f["urgency reported"], "exposed": f["customer data exposed"], "open": _dt(f["opened"]),
            "ack": ack, "check": _dt(f["check time"]),
            "m_check": S.parse("count", f["minutes from opening to the check"], ())
            if "minutes from opening to the check" in f else None,
            "m_ack": S.parse("count", f["minutes from opening to the acknowledgement"], ())
            if "minutes from opening to the acknowledgement" in f else None,
            "step": S.parse("count", cm["STEP"], MINS), "u1": S.parse("count", cm["U1"], ()),
            "u2": S.parse("count", cm["U2"], ()),
            "matrix": [f"sev{SEV_OF[cm[k]]}" for k in ("WO", "WD", "WC", "PO", "PD", "PC", "MO", "MD", "MC")],
            "xrule": [X_COND[cm["XC"]], X_EFF[cm["XE"]]],
            "critical": crit_list, "window": window}
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = K.parse_skin(skin, narrative, SCHEMA) if skin.author_mode == "T" else {}
    asked, qform = _asked(row, ctx, question)
    if asked.get("INC_ID", view["incident"]) != view["incident"]:
        raise ParseError("the question names another incident")
    if "LEVEL" in asked and "LEVEL_NEXT" in asked:
        raise ParseError("a question names two levels")
    view.update(asked=asked.get("LEVEL_NEXT", asked.get("LEVEL")), qform=qform)
    if skin.author_mode == "T":
        view.update(team=told["TEAM"], reporter=told["REPORTER"])
    if row["qtype"] == "choice":
        view["options"] = [f"sev{SEV_OF[t]}" for t in row["options"]]
    return view


def _minute(iso: str) -> int:
    return brute.epoch_minutes(S.parse("datetime", iso, (), "iso"))


def solve_b(view: dict):
    t0, tc = _minute(view["open"]), _minute(view["check"])
    ta = _minute(view["ack"]) if view["ack"] else None
    if view["m_check"] is not None and view["m_check"] != tc - t0:
        raise ParseError("printed minutes to the check disagree with the times")
    if view["m_ack"] is not None and (ta is None or view["m_ack"] != ta - t0):
        raise ParseError("printed minutes to the acknowledgement disagree with the times")
    if not t0 < tc or (ta is not None and not t0 < ta <= tc) or view["users"] < 0 or (
            view["window"] is not None and not _minute(view["window"][0]) < _minute(view["window"][1])):
        raise ParseError("the record is outside the G0 R2 domain")
    users = view["users"]
    row = 0 if users >= view["u2"] else (1 if users >= view["u1"] else 2)
    col = ("outage", "degraded", "cosmetic").index(view["urgency"])
    level = int(view["matrix"][row * 3 + col][-1])
    if view["window"] is not None and _minute(view["window"][0]) <= t0 < _minute(view["window"][1]):
        level = min(4, level + 1)
    if view["service"] in view["critical"] and level > 2:
        level = 2
    for m in range(1, tc - t0 + 1):                     # walk the clock one minute at a time
        if m % view["step"] == 0 and (ta is None or ta - t0 > m):
            level = max(1, level - 1)
    if view["exposed"] == "yes":
        cond, eff = view["xrule"]
        if cond == "any" or (cond == "partial" and row <= 1) or (cond == "wide" and row == 0):
            level = {"sev1": 1, "sev2": min(level, 2), "up": max(1, level - 1)}[eff]
    q = view["qform"]
    if q == "ch_sev":
        return f"sev{level}"
    if q == "yn_below":                                  # at the named level or less severe
        return int(level >= int(view["asked"][-1]))
    reaches = level <= int(view["asked"][-1])
    return int(reaches) if q in ("yn_reaches", "yn_double_neg") else int(not reaches)
