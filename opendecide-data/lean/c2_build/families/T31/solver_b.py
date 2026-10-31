"""families/T31/solver_b.py: T31 solver B, written from G0_SPEC.md (sections 1, 1.1, 1.2), not from plugin.py.

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the record block (between "Records:" and "End of records.") line by line with this module's own regular
    expressions for the two G0 styles (list, log); the one time written in a second offset carries a bracketed
    restatement, which must be the same instant (epoch minutes by integer arithmetic, brute.epoch_minutes);
  - amount bands through the lexicon registry (admitted forms only), or the literal "of any size";
  - the narrative skin (Mode T) through skin.parse_skin; Mode F narrative facts are left to G3-H;
  - the rule block by exact comparison with the G0 card text (it fixes the track and the window-end rule);
  - the question through its wording template (its admitted meaning is the question form);
  - on choice rows, every option text back to its key (a person, "escalate", or a scope).
solve_b(view) decides by an interval scan in epoch minutes: every delegation, override, grant and grant scope is a
half-open interval [opens, closes) (closes = end + 1 under an inclusive end, cut at the first revocation minute;
an override never closes), scanned at the request minute; bands by an integer-cents sign table; a sub-agent's usable
set is the set intersection of the held sets down the chain. Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import datetime as dt
import re

from c2_kit import brute
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.cards import split_rules

CENTS = (("currency", "USD"), ("symbol", "$"))
NARRATIVE = {"REQUESTER": ("name", ()), "ITEM": ("name", ()), "REQ_ID": ("id", ())}
QUESTION = {"CANDIDATE": ("name", ()), "REQ_ID": ("id", ()), "REQ_AGENT": ("id", ()), "REQ_SCOPE": ("id", ())}
NEEDS = {"ch_approver": (), "yn_holder": ("CANDIDATE",), "yn_holder_dneg": ("CANDIDATE",),
         "yn_holder_other": ("CANDIDATE",), "yn_holder_not": ("CANDIDATE",), "yn_agent_ok": ("REQ_AGENT", "REQ_SCOPE"),
         "yn_agent_dneg": ("REQ_AGENT", "REQ_SCOPE"), "yn_agent_beyond": ("REQ_AGENT", "REQ_SCOPE"),
         "yn_agent_lacks": ("REQ_AGENT", "REQ_SCOPE"), "yn_agent_not": ("REQ_AGENT", "REQ_SCOPE"),
         "ch_scope": ("REQ_AGENT",)}
ASKS_POSITIVE = {"yn_holder": True, "yn_holder_dneg": True, "yn_holder_other": False, "yn_holder_not": False,
                 "yn_agent_ok": True, "yn_agent_dneg": True, "yn_agent_beyond": False, "yn_agent_lacks": False,
                 "yn_agent_not": False}
TRACK_OF = {q: ("appr" if q == "ch_approver" or q.startswith("yn_holder") else "agent") for q in NEEDS}
ESCALATE, ESCALATE_TEXT, NO_BAND = "escalate", "Escalate: no unique approver", "of any size"
SIGN_OK = {"cmp.le": (-1, 0), "cmp.lt": (-1,), "cmp.ge": (0, 1), "cmp.gt": (1,)}
NEVER = 10 ** 12                      # closing minute of an interval that never closes

# G0 v1.2 section 1.1: the card text in its three styles, copied from the spec (exact). A rule block is one of these,
# whatever the layout (yes/no rows: row.card; choice rows: the head of the instructions)
_END = {"incl": "through its end time (the end time is included)",
        "excl": "until its end time (the end time is excluded)"}
_END_SHORT = {"incl": "through its end time (included)", "excl": "until its end time (excluded)"}
_CW = "The listed records are complete: no other record exists."
_ESC = "\"Escalate: no unique approver\""
_TIMES = {False: "Compare times as instants.",
          True: "Compare times as instants; a time in another offset shows the same instant in square brackets."}
_APPR = {
    "full": (
        "- A delegation covers the request when the amount is in its band and the request time is from its start "
        "time {END}, before any revocation of it.\n"
        "- An override covers the request when the amount is in its band and the request time is at or after its "
        "issue time.\n"
        "- The first level with a covering record decides the approver (the holder of the accountable (A) role): "
        "overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person marked "
        "A in the standing RACI matrix.\n"
        "- If that level gives two different people, the answer is " + _ESC + ". {TIMES}\n"
        "- Listing order and who issued a record do not matter.\n" + _CW),
    "compact": (
        "- A delegation covers the request when the amount is in its band and the request time is from its start "
        "{END}, before any revocation of it; an override, when the amount is in its band and the request time is "
        "at or after its issue time.\n"
        "- The first level with a covering record decides the approver (the holder of the accountable (A) role): "
        "overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person marked "
        "A in the RACI matrix.\n"
        "- If that level gives two different people, the answer is " + _ESC + ". {TIMES}\n"
        "- Listing order and who issued a record do not matter. " + _CW),
    "short": (
        "- Delegation: covers the request if the amount is in its band and the request time is from its start "
        "{END}, before any revocation of it. Override: covers it if the amount is in its band and the request time "
        "is at or after its issue time.\n"
        "- Approver (holder of the accountable (A) role): the first level with a covering record decides; "
        "overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person "
        "marked A in the RACI matrix.\n"
        "- If that level gives two different people: " + _ESC + ". {TIMES}\n"
        "- Listing order and who issued a record do not matter. " + _CW)}
_AGENT = {
    "full": (
        "- Each agent holds one grant. An agent may use a scope at an instant exactly when its own grant lists "
        "the scope, the instant is from the grant's start time {END}, no revocation of that scope from that agent "
        "or of the whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made "
        "its grant) may use the scope at that instant.\n"
        "- {TIMES}\n"
        "- Listing order and who issued a revocation do not matter.\n" + _CW),
    "compact": (
        "- Each agent holds one grant. An agent may use a scope at an instant exactly when its own grant lists "
        "the scope, the instant is from the grant's start {END}, no revocation of that scope from that agent or of "
        "the whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its "
        "grant) may use the scope at that instant. {TIMES}\n"
        "- Listing order and who issued a revocation do not matter. " + _CW),
    "short": (
        "- Each agent holds one grant. It may use a scope at an instant exactly when its grant lists the scope, "
        "the instant is from the grant's start {END}, no revocation of that scope from that agent or of the "
        "whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its grant) "
        "may use the scope then. {TIMES}\n"
        "- Listing order and who issued a revocation do not matter. " + _CW)}
# (track, window-end rule, bracket sentence) -> {rule block text: style}
CARDS = {}
for _track, _styles in (("appr", _APPR), ("agent", _AGENT)):
    for _rule in _END:
        for _odd in _TIMES:
            CARDS[(_track, _rule, _odd)] = {
                text.replace("{END}", (_END if style == "full" else _END_SHORT)[_rule]).replace(
                    "{TIMES}", _TIMES[_odd]): style for style, text in _styles.items()}


class ParseError(ValueError):
    pass


def _t(n: str) -> str:
    return rf"(?P<{n}>[^\[\]\n|;]+?)(?: \[same instant: (?P<{n}_eq>[^\]\n]+)\])?"


_C = re.compile
BLOCK = _C(r"(?:\A|\n\n)Records:\n(?P<body>.*?)\nEnd of records\.(?=\n\n|\Z)", re.S)
# appr, list style
PROC_L = _C(r"Process: (?P<p>.+)")
MAT_L = _C(r"- (?P<role>.+?): (?P<person>.+) \[(?P<L>[ARCI])\]")
DEL_L = _C(r"- (?P<id>[^\s:]+): (?P<frm>.+?) delegates the A role to (?P<to>.+?), from " + _t("s") + " to " + _t("e")
           + r"; amounts (?P<band>.+)\.")
REV_L = _C(r"- (?P<id>[^\s,]+), issued " + _t("t") + r" by (?P<by>.+?): delegation (?P<target>\S+) is revoked\.")
OVR_L = _C(r"- (?P<id>[^\s,]+), issued " + _t("t") + r" by (?P<by>.+?): override, the A role goes to "
           r"(?P<person>.+?); amounts (?P<band>.+)\.")
REQ_L = _C(r"Request (?P<id>[^\s:]+): amount (?P<amt>.+?), made at " + _t("t") + r"\.")
# appr, log style
PROC_G = _C(r"process \| (?P<p>.+)")
MAT_G = _C(r"matrix \| (?P<role>.+?) \| (?P<person>.+?) \| (?P<L>[ARCI])")
DEL_G = _C(_t("s") + r" \| delegation (?P<id>\S+) starts \| (?P<frm>.+?) -> (?P<to>.+?) \| ends " + _t("e")
           + r" \| amounts (?P<band>.+)")
REV_G = _C(_t("t") + r" \| revocation (?P<id>\S+) issued \| by (?P<by>.+?) \| revokes (?P<target>\S+)")
OVR_G = _C(_t("t") + r" \| override (?P<id>\S+) issued \| by (?P<by>.+?) \| A role to (?P<person>.+?) \| "
           r"amounts (?P<band>.+)")
REQ_G = _C(_t("t") + r" \| request (?P<id>\S+) made \| amount (?P<amt>.+)")
# agent, list style
PRIN_L = _C(r"Principal: (?P<p>.+)")
GRANT_L = _C(r"- (?P<id>[^\s:]+): (?P<by>.+?) grants (?P<sub>sub-agent )?(?P<to>\S+) the scopes (?P<scopes>[^;]+); "
             r"in effect from " + _t("s") + " to " + _t("e") + r"\.")
RSC_L = _C(r"- (?P<id>[^\s,]+), issued " + _t("t") + r" by (?P<by>.+?): scope (?P<scope>\S+) is removed from "
           r"(?P<agent>\S+)\.")
RGR_L = _C(r"- (?P<id>[^\s,]+), issued " + _t("t") + r" by (?P<by>.+?): grant (?P<grant>\S+) is withdrawn in full\.")
AREQ_L = _C(r"Request (?P<id>[^\s:]+): at " + _t("t") + r", (?P<agent>\S+) (?:asks to use scope (?P<scope>\S+)|is "
            r"about to act)\.")
# agent, log style
PRIN_G = _C(r"principal \| (?P<p>.+)")
GRANT_G = _C(_t("s") + r" \| grant (?P<id>\S+) starts \| (?P<by>.+?) -> (?P<to>\S+) \| scopes (?P<scopes>.+?) \| ends "
             + _t("e"))
RSC_G = _C(_t("t") + r" \| revocation (?P<id>\S+) issued \| by (?P<by>.+?) \| scope (?P<scope>\S+) from (?P<agent>\S+)")
RGR_G = _C(_t("t") + r" \| revocation (?P<id>\S+) issued \| by (?P<by>.+?) \| grant (?P<grant>\S+) in full")
AREQ_G = _C(_t("t") + r" \| request (?P<id>\S+) made \| (?P<agent>\S+) \| (?:scope (?P<scope>\S+)|about to act)")


# ------------------------------------------------------------------------------------------------ reading values

def _when(m, n) -> str:
    """A printed time; a bracketed restatement (the one conversion, G0 S2) must be the same instant."""
    try:
        t = S.parse("datetime", m[n])
        same = S.parse("datetime", m[n + "_eq"]) if m[n + "_eq"] else None
    except S.SlotError as e:
        raise ParseError(f"time {m[n]!r}: {e}") from None
    if same is not None and (brute.epoch_minutes(t) != brute.epoch_minutes(same) or same.utcoffset() == t.utcoffset()):
        raise ParseError(f"{m[n]!r} and its bracket {m[n + '_eq']!r} are not one instant in two offsets")
    return t.isoformat()


def _name(text: str) -> str:
    return S.parse("name", text)


def _ident(text: str) -> str:
    return S.parse("id", text)


def _band(text: str, lexicon) -> list | None:
    if text == NO_BAND:
        return None
    sem, _form, vals = lexicon.parse_exact(text, {"X": ("cents", CENTS)}, admitted_only=True)
    if sem not in SIGN_OK:
        raise ParseError(f"band {text!r} reads as {sem}")
    return [sem, vals["X"]]


def _scopes(text: str) -> list:
    out = [_ident(x) for x in text.split(", ")]
    if len(set(out)) != len(out):
        raise ParseError("a grant lists a scope twice")
    return out


class _Lines:
    def __init__(self, lines):
        self.lines, self.i = lines, 0

    def peek(self):
        return self.lines[self.i] if self.i < len(self.lines) else None

    def take(self, rx, what):
        line = self.peek()
        m = rx.fullmatch(line) if line is not None else None
        if not m:
            raise ParseError(f"expected a {what} line, got {line!r}")
        self.i += 1
        return m

    def literal(self, text):
        if self.peek() != text:
            raise ParseError(f"expected {text!r}, got {self.peek()!r}")
        self.i += 1

    def maybe(self, *rxs):
        line = self.peek()
        if line is None:
            return None, None
        for rx in rxs:
            m = rx.fullmatch(line)
            if m:
                self.i += 1
                return rx, m
        return None, None

    def done(self):
        if self.i != len(self.lines):
            raise ParseError(f"unexpected line {self.peek()!r}")


# ------------------------------------------------------------------------------------------------ record blocks

def _appr_block(lines: list, log: bool, lexicon) -> dict:
    L = _Lines(lines)
    process = _name(L.take(PROC_G if log else PROC_L, "process")["p"])
    if not log:
        L.literal("Standing RACI matrix:")
    matrix = []
    while True:
        _rx, m = L.maybe(MAT_G if log else MAT_L)
        if m is None:
            break
        matrix.append([_name(m["role"]), _name(m["person"]), m["L"]])
    if not log:
        L.literal("Delegations:")
    dels = []
    while True:
        _rx, m = L.maybe(DEL_G if log else DEL_L)
        if m is None:
            break
        dels.append({"id": _ident(m["id"]), "from": _name(m["frm"]), "to": _name(m["to"]), "start": _when(m, "s"),
                     "end": _when(m, "e"), "band": _band(m["band"], lexicon)})
    notices = []
    if not log:
        if L.peek() == "Notices: none.":
            L.i += 1
        else:
            L.literal("Notices:")
    while True:
        rx, m = L.maybe(REV_G, OVR_G) if log else L.maybe(REV_L, OVR_L)
        if m is None:
            break
        rec = {"id": _ident(m["id"]), "time": _when(m, "t"), "by": _name(m["by"]), "target": None, "person": None,
               "band": None}
        if rx in (REV_G, REV_L):
            rec.update(kind="revoke", target=_ident(m["target"]))
        else:
            rec.update(kind="override", person=_name(m["person"]), band=_band(m["band"], lexicon))
        notices.append(rec)
    if not log and not notices and lines[L.i - 1] == "Notices:":
        raise ParseError("an empty notice section must read 'Notices: none.'")
    m = L.take(REQ_G if log else REQ_L, "request")
    L.done()
    try:
        amount = S.parse("cents", m["amt"], CENTS)
    except S.SlotError as e:
        raise ParseError(f"amount {m['amt']!r}: {e}") from None
    people = [p for _r, p, _l in matrix]
    heads = [p for _r, p, letter in matrix if letter == "A"]
    if len(heads) != 1 or len(set(people)) != len(people):
        raise ParseError("the matrix needs exactly one A and distinct people")
    ids = [d["id"] for d in dels]
    for d in dels:
        if d["from"] != heads[0] or d["to"] not in people or d["to"] == heads[0]:
            raise ParseError(f"delegation {d['id']} is not from the A holder to another listed person")
    for n in notices:
        if n["by"] not in people or (n["kind"] == "revoke" and n["target"] not in ids) or (
                n["kind"] == "override" and n["person"] not in people):
            raise ParseError(f"notice {n['id']} refers to an unknown person or delegation")
    return {"process": process, "matrix": matrix, "delegations": dels, "notices": notices,
            "request": {"id": _ident(m["id"]), "amount": amount, "time": _when(m, "t")}}


def _agent_block(lines: list, log: bool) -> dict:
    L = _Lines(lines)
    principal = _name(L.take(PRIN_G if log else PRIN_L, "principal")["p"])
    if not log:
        L.literal("Grants:")
    grants = []
    while True:
        _rx, m = L.maybe(GRANT_G if log else GRANT_L)
        if m is None:
            break
        by = m["by"]
        g = {"id": _ident(m["id"]), "by": by, "to": _ident(m["to"]), "scopes": _scopes(m["scopes"]),
             "start": _when(m, "s"), "end": _when(m, "e")}
        if not log and bool(m["sub"]) != (by != principal):
            raise ParseError(f"grant {g['id']}: 'sub-agent' marks exactly the grants made by an agent")
        grants.append(g)
    if not log:
        if L.peek() == "Revocations: none.":
            L.i += 1
        else:
            L.literal("Revocations:")
    revs = []
    while True:
        rx, m = L.maybe(RSC_G, RGR_G) if log else L.maybe(RSC_L, RGR_L)
        if m is None:
            break
        rec = {"id": _ident(m["id"]), "time": _when(m, "t"), "by": m["by"], "agent": None, "scope": None,
               "grant": None}
        if rx in (RSC_G, RSC_L):
            rec.update(agent=_ident(m["agent"]), scope=_ident(m["scope"]))
        else:
            rec["grant"] = _ident(m["grant"])
        revs.append(rec)
    if not log and not revs and lines[L.i - 1] == "Revocations:":
        raise ParseError("an empty revocation section must read 'Revocations: none.'")
    m = L.take(AREQ_G if log else AREQ_L, "request")
    L.done()
    # chain: the principal's grant first, then each grant made by the agent of the line before
    agents = [g["to"] for g in grants]
    if not grants or len(set(agents)) != len(agents):
        raise ParseError("grants: at least one, one per agent")
    for j, g in enumerate(grants):
        want = principal if j == 0 else grants[j - 1]["to"]
        if g["by"] != want:
            raise ParseError(f"grant {g['id']} is not made by {want}")
        if j == 0:
            g["by"] = _name(g["by"])
    by_id = {g["id"]: g for g in grants}
    for r in revs:
        if r["grant"] is not None:
            if r["grant"] not in by_id:
                raise ParseError(f"revocation {r['id']} names an unknown grant")
            r["agent"] = by_id[r["grant"]]["to"]
        elif r["agent"] not in agents:
            raise ParseError(f"revocation {r['id']} names an unknown agent")
        k = agents.index(r["agent"])
        if r["by"] not in (principal, agents[k - 1] if k else principal):
            raise ParseError(f"revocation {r['id']} is issued by neither the principal nor the parent agent")
    if _ident(m["agent"]) != agents[-1]:
        raise ParseError("the request is not made by the deepest agent of the chain")
    return {"principal": principal, "grants": grants, "revocations": revs,
            "request": {"id": _ident(m["id"]), "agent": agents[-1],
                        "scope": _ident(m["scope"]) if m["scope"] else None, "time": _when(m, "t")}}


# ------------------------------------------------------------------------------------------------ parse

def parse(row: dict, ctx) -> dict:
    state = row["state"]
    hits = list(BLOCK.finditer(state))
    if len(hits) != 1:
        raise ParseError(f"{len(hits)} record blocks in the row")
    blk = hits[0]
    if blk.start() == 0 or not state[:blk.start() + 2].endswith("\n\n"):
        raise ParseError("the narrative and the record block are not separated by one blank line")
    narrative = state[:blk.start()]
    lines = blk["body"].split("\n")
    head = lines[0]
    log = head.startswith(("process | ", "principal | "))
    track = "appr" if head.startswith(("Process: ", "process | ")) else "agent"
    rec = _appr_block(lines, log, ctx.lexicon) if track == "appr" else _agent_block(lines, log)
    rules, question = split_rules(row)         # yes/no rows: card + instructions; choice rows: rules, blank line, question
    if not rules:
        raise ParseError("rule block and question are not separated")
    rule = [(r, odd) for (tr, r, odd), texts in CARDS.items() if tr == track and rules in texts]
    if len(rule) != 1:
        raise ParseError("rule block does not match the G0 card text for its track")
    if rule[0][1] != ("[same instant: " in blk["body"]):
        raise ParseError("the bracket sentence appears exactly when a time carries a bracket")
    wording = ctx.skin(row["meta"]["wording_id"])
    qform = wording.qform
    if TRACK_OF.get(qform) != track:
        raise ParseError(f"question form {qform} does not belong to the {track} records")
    asked = K.match_template(wording.text, question, QUESTION)
    lacking = [k for k in NEEDS[qform] if k not in asked]
    if lacking:
        raise ParseError(f"wording lacks {lacking}")
    if "REQ_ID" in asked and asked["REQ_ID"] != rec["request"]["id"]:
        raise ParseError("the question names another request")
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        if not set(skin.decl) <= set(NARRATIVE):
            raise ParseError(f"skin declares slots outside {sorted(NARRATIVE)}")
        told = K.parse_skin(skin, narrative, NARRATIVE)
        if "REQUESTER" not in told or "ITEM" not in told:
            raise ParseError("narrative lacks the requester or the item")
        if "REQ_ID" in told and told["REQ_ID"] != rec["request"]["id"]:
            raise ParseError("the narrative names another request")
    view = {"track": track, "qform": qform, "style": "log" if log else "list", "end_rule": rule[0][0], **rec}
    if track == "appr":
        people = {p for _r, p, _l in rec["matrix"]}
        if qform == "ch_approver":
            view["question"] = {}
        else:
            if asked["CANDIDATE"] not in people:
                raise ParseError("the candidate is not in the matrix")
            view["question"] = {"candidate": asked["CANDIDATE"]}
    else:
        if asked["REQ_AGENT"] != rec["request"]["agent"]:
            raise ParseError("the question names another agent than the request")
        if qform == "ch_scope":
            if rec["request"]["scope"] is not None:
                raise ParseError("a which-scope question on a request that names its scope")
            view["question"] = {"agent": asked["REQ_AGENT"]}
        else:
            if asked["REQ_SCOPE"] != rec["request"]["scope"]:
                raise ParseError("the question names another scope than the request")
            view["question"] = {"agent": asked["REQ_AGENT"], "scope": asked["REQ_SCOPE"]}
    if skin.author_mode == "T":
        view.update(requester=told["REQUESTER"], item=told["ITEM"])
    if row["qtype"] == "choice":
        view["options"] = [_option_key(view, t) for t in row["options"]]
    return view


def _option_key(view: dict, text: str):
    if view["qform"] == "ch_approver":
        if text == ESCALATE_TEXT:
            return ESCALATE
        if text not in {p for _r, p, _l in view["matrix"]}:
            raise ParseError(f"option {text!r} is not a listed person")
        return text
    if view["qform"] == "ch_scope":
        if text not in {s for g in view["grants"] for s in g["scopes"]}:
            raise ParseError(f"option {text!r} is not a granted scope")
        return text
    raise ParseError(f"question {view['qform']} has no options")


# ------------------------------------------------------------------------------------------------ solve (interval scan)

def _minute(iso: str) -> int:
    return brute.epoch_minutes(dt.datetime.fromisoformat(iso))


def _band_ok(band, amount: int) -> bool:
    if band is None:
        return True
    diff = amount - band[1]
    return ((diff > 0) - (diff < 0)) in SIGN_OK[band[0]]


def _holder(view: dict) -> str:
    T, amount = _minute(view["request"]["time"]), view["request"]["amount"]
    pad = 1 if view["end_rule"] == "incl" else 0
    cut = {}
    for n in view["notices"]:
        if n["kind"] == "revoke":
            cut[n["target"]] = min(cut.get(n["target"], NEVER), _minute(n["time"]))
    table = [("delegation", _minute(d["start"]), min(_minute(d["end"]) + pad, cut.get(d["id"], NEVER)), d["to"],
              d["band"], 0) for d in view["delegations"]]
    table += [("override", _minute(n["time"]), NEVER, n["person"], n["band"], _minute(n["time"]))
              for n in view["notices"] if n["kind"] == "override"]
    live = [r for r in table if r[1] <= T < r[2] and _band_ok(r[4], amount)]
    over = [r for r in live if r[0] == "override"]
    if over:
        last = max(r[5] for r in over)
        who = {r[3] for r in over if r[5] == last}
    else:
        who = {r[3] for r in live}
    if len(who) == 1:
        return who.pop()
    if who:
        return ESCALATE
    return next(p for _r, p, letter in view["matrix"] if letter == "A")


def _usable_set(view: dict) -> set:
    T = _minute(view["request"]["time"])
    pad = 1 if view["end_rule"] == "incl" else 0
    cut_grant, cut_scope = {}, {}
    for r in view["revocations"]:
        m = _minute(r["time"])
        if r["grant"] is not None:
            cut_grant[r["grant"]] = min(cut_grant.get(r["grant"], NEVER), m)
        else:
            cut_scope[(r["agent"], r["scope"])] = min(cut_scope.get((r["agent"], r["scope"]), NEVER), m)
    held = {}
    for g in view["grants"]:
        opens = _minute(g["start"])
        closes = min(_minute(g["end"]) + pad, cut_grant.get(g["id"], NEVER))
        held[g["to"]] = {s for s in g["scopes"] if opens <= T < min(closes, cut_scope.get((g["to"], s), NEVER))}
    usable = None
    for g in view["grants"]:                      # principal's grant first, then down the chain
        usable = held[g["to"]] if usable is None else held[g["to"]] & usable
        if g["to"] == view["request"]["agent"]:
            return usable
    raise ParseError("the requesting agent holds no grant")


def solve_b(view: dict):
    q = view["qform"]
    if view["track"] == "appr":
        holder = _holder(view)
        if q == "ch_approver":
            return holder
        if holder == ESCALATE:
            raise ParseError("a yes/no approver question without a unique approver (never generated)")
        same = holder == view["question"]["candidate"]
        return int(same if ASKS_POSITIVE[q] else not same)
    usable = _usable_set(view)
    if q == "ch_scope":
        hits = [o for o in view["options"] if o in usable]
        if len(hits) != 1:
            raise ParseError(f"{len(hits)} options are usable (the question needs exactly one)")
        return hits[0]
    ok = view["question"]["scope"] in usable
    return int(ok if ASKS_POSITIVE[q] else not ok)
