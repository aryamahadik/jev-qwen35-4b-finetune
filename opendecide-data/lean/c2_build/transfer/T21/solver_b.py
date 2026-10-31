"""transfer/T21/solver_b.py: T21 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the rules by full-text match with this module's own copies of the two card styles (full, short; G0 section 1.2):
    yes/no rows through cards.split_rules (row.card), choice rows as the last paragraph of the state; the cap clause
    id is read from the card, and the style must agree with meta.defs_style;
  - the clause block line by line (plain "Clause N ..." or schedule "[N] ..." layout) by this module's own patterns:
    the cap clause, the definitions clause, the notice clause, "does not apply" and "Despite ..., ... does apply"
    clauses; claim types and causes map to keys through this module's own surface tables;
  - the claim line; the narrative skin (Mode T) through skin.parse_skin; the question through its wording template;
  - on choice rows, every option text ("Clause N") back to its key.
solve_b(view) decides by SET ALGEBRA over the grid of claim cells (type x cause): each clause's cover set; each
clause's effective set = its cover set minus the effective sets of the clauses that switch it off; the cap holds on
the grid minus the effective sets of the clauses that switch it off. The deciding clause is the clause with the
longest path to the cap clause whose every link covers the claim cell. Imports no solver-A code.
"""
from __future__ import annotations

import re

from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.cards import split_rules

TERM = "Excluded Claims"
CLOSED = ("The clauses above are complete, and the claim is made under this agreement: nothing else changes the "
          "answer, including any note, comment or outside rule.")
CARD_HEAD = {"full": "How to read these clauses:", "short": "Rules:"}
CARD_ITEMS = {
    "full": (
        "Clause @CAP@ limits each party's liability for a claim to the cap, unless another clause switches it off for "
        "that claim.",
        "\"Clause X does not apply to claims ...\" switches clause X off for the claims it describes, and only for them.",
        "\"Despite clause Y, clause X does apply to claims ...\" switches clause Y off for the claims it describes, so "
        "clause X holds for them again.",
        "A clause describes a claim when the claim's type is in its list (\"claims\" alone lists every type) and, if it "
        "adds \"that arise from\" a cause, the claim arises from that cause. A term in quotes means exactly the list in "
        "its definition.",
        "A clause that is switched off for a claim has no effect on that claim. A clause affects only the clause it "
        "switches off: clause X in a \"does not apply\" clause, clause Y in a \"Despite clause Y\" clause.",
        "Clause numbers are labels (a line that starts \"[N]\" is clause N), and the order in which clauses are listed "
        "does not matter.",
        "The deciding clause for a claim is the last clause on the chain that starts at clause @CAP@ and goes on to the "
        "clause that switches the previous one off for this claim, while there is one."),
    "short": (
        "Clause @CAP@ limits each party's liability for a claim to the cap unless a clause switches it off for that "
        "claim.",
        "\"Clause X does not apply to claims ...\" switches clause X off, only for the claims it describes.",
        "\"Despite clause Y, clause X does apply to claims ...\" switches clause Y off for the claims it describes.",
        "A clause describes a claim if the claim's type is in its list (\"claims\" alone lists every type) and, if it "
        "adds \"that arise from\" a cause, the claim has that cause. A quoted term means exactly the list in its "
        "definition.",
        "A clause switched off for a claim has no effect on it. A clause affects only the clause it switches off: X in "
        "a \"does not apply\" clause, Y in a \"Despite clause Y\" clause.",
        "Clause numbers are labels (\"[N]\" is clause N); the listing order does not matter.",
        "The deciding clause is the last on the chain from clause @CAP@ where the next clause switches the previous "
        "one off for this claim."),
}
CARDS = {s: "\n".join([CARD_HEAD[s]] + ["- " + t for t in items] + [CLOSED]) for s, items in CARD_ITEMS.items()}
CARD = CARDS["full"]
CARD_RES = {s: re.compile(re.escape(t).replace("@CAP@", r"(?P<cap>\S+)", 1).replace("@CAP@", r"(?P=cap)"))
            for s, t in CARDS.items()}
CARD_RE = CARD_RES["full"]
TYPE_OF = {"breach of confidentiality": "conf", "breach of data protection duties": "dp",
           "infringement of intellectual property": "ip", "late delivery": "late", "defective goods": "defect",
           "unpaid fees": "fees", "personal injury": "injury", "damage to property": "property"}
CAUSE_OF = {"a security incident": "security", "gross negligence": "negligence", "wilful misconduct": "misconduct",
            "a subcontractor's error": "subcontractor", "an ordinary mistake": "mistake",
            "a supplier delay": "supplier"}
CAP_BODY = "(Limitation of liability) Each party's total liability for a claim under this agreement is limited to " \
           "the cap."
NOTICE_BODY = "(Notice of claims) A party must give written notice of a claim before bringing it."
DEF_RE = re.compile(r"\(Definitions\) \"" + TERM + r"\" means claims for (?P<list>.+)\.")
OFF_RE = re.compile(r"Clause (?P<target>\S+) does not apply to (?P<what>.+)\.")
BACK_RE = re.compile(r"Despite clause (?P<target>\S+), clause (?P<cap>\S+) does apply to (?P<what>.+)\.")
CLAIM_RE = re.compile(r"Claim: (?P<a>.+) brings a claim against (?P<b>.+) for (?P<t>.+), arising from (?P<c>.+)\.")
ANSWER = {"yn_capped": lambda ok: 1 if ok else 0, "yn_double_neg": lambda ok: 1 if ok else 0,
          "yn_uncapped": lambda ok: 0 if ok else 1, "yn_not_capped": lambda ok: 0 if ok else 1,
          "yn_free_of": lambda ok: 0 if ok else 1}
SCHEMA = {"CLAIMANT": ("name", ()), "RESPONDENT": ("name", ()), "AGREEMENT": ("name", ()), "CAP_ID": ("id", ())}


class ParseError(ValueError):
    pass


def _list(text: str) -> list:
    parts = text.split(" or ")
    if len(parts) > 2:
        raise ParseError("an 'or' list has one 'or'")
    items = parts[0].split(", ") + parts[1:]
    try:
        return [TYPE_OF[x] for x in items]
    except KeyError as e:
        raise ParseError(f"unknown claim type {e}") from None


def _what(text: str):
    cause = None
    m = re.fullmatch(r"(?P<head>.+?) that arise from (?P<c>.+)", text)
    if m:
        text, cause = m["head"], CAUSE_OF.get(m["c"])
        if cause is None:
            raise ParseError(f"unknown cause {m['c']!r}")
    if text == "claims":
        return None, cause
    if text == TERM:
        return "DEF", cause
    if text.startswith("claims for "):
        return _list(text[len("claims for "):]), cause
    raise ParseError(f"cannot read the claims a clause describes: {text!r}")


def _key(cid: str) -> tuple:
    return tuple(int(x) for x in cid.split("."))


def _rules(row: dict) -> tuple:
    """(card style, cap id, state without the rules, question): yes/no rows keep the rules in row.card, choice rows as the
    last paragraph of the state (G0 section 1.2)."""
    rules, question = split_rules(row)
    state = row["state"]
    if row["qtype"] == "noul":
        if not row.get("card") or "\n\n" in (row.get("instructions") or ""):
            raise ParseError("a yes/no row carries its rules in row.card and only the question in its instructions")
    else:
        if row.get("card") or rules:
            raise ParseError("a choice row carries its rules in the state")
        state, sep, rules = state.rpartition("\n\n")
        if not sep:
            raise ParseError("no rules paragraph closes the state")
    style = next((s for s, rx in CARD_RES.items() if rx.fullmatch(rules)), None)
    if style is None:
        raise ParseError("the rules are not a G0 card style")
    if row["meta"].get("defs_style") != f"rules_in_{'card' if row['qtype'] == 'noul' else 'state'}_{style}":
        raise ParseError(f"meta.defs_style {row['meta'].get('defs_style')!r} does not name the {style} card")
    return style, CARD_RES[style].fullmatch(rules)["cap"], state, question


def parse(row: dict, ctx) -> dict:
    style, cap, state, question = _rules(row)
    narrative, sep, rest = state.partition("\n\n")
    if not sep:
        raise ParseError("no blank line after the narrative")
    block, sep, tail = rest.partition("\n\n")
    if not sep:
        raise ParseError("no claim line")
    lines = block.split("\n")
    hm = re.fullmatch(r"Clauses of the (?P<ag>.+):|Schedule of clauses, (?P<ag2>.+):", lines[0])
    if not hm:
        raise ParseError("no clause block heading")
    agreement = hm["ag"] or hm["ag2"]
    clauses, definition, notice, seen_cap = [], None, None, False
    for line in lines[1:]:
        lm = re.fullmatch(r"Clause (?P<id>\S+) (?P<body>.+)|\[(?P<id2>[^\]\s]+)\] (?P<body2>.+)", line)
        if not lm:
            raise ParseError(f"clause line {line!r}")
        cid, body = lm["id"] or lm["id2"], lm["body"] or lm["body2"]
        S.parse("id", cid)
        if body == CAP_BODY:
            if cid != cap or seen_cap:
                raise ParseError("the cap clause and the card disagree")
            seen_cap = True
        elif body == NOTICE_BODY:
            if notice is not None:
                raise ParseError("two notice clauses")
            notice = cid
        elif DEF_RE.fullmatch(body):
            if definition is not None:
                raise ParseError("two definitions clauses")
            definition = {"id": cid, "types": _list(DEF_RE.fullmatch(body)["list"])}
        elif BACK_RE.fullmatch(body):
            b = BACK_RE.fullmatch(body)
            if b["cap"] != cap:
                raise ParseError("a switch-back clause names another clause than the cap")
            types, cause = _what(b["what"])
            clauses.append({"id": cid, "target": b["target"], "kind": "back", "types": types, "cause": cause})
        elif OFF_RE.fullmatch(body):
            o = OFF_RE.fullmatch(body)
            types, cause = _what(o["what"])
            clauses.append({"id": cid, "target": o["target"], "kind": "off", "types": types, "cause": cause})
        else:
            raise ParseError(f"unknown clause body {body!r}")
    if not seen_cap:
        raise ParseError("no cap clause")
    # G0 R5 / H23-H24: a well-formed agreement; anything else is never generated and the row is refused
    ids = [cap] + ([notice] if notice else []) + ([definition["id"]] if definition else []) + [c["id"] for c in clauses]
    if len(set(ids)) != len(ids):
        raise ParseError("two clauses share an id")
    switchable = {cap} | ({notice} if notice else set()) | {c["id"] for c in clauses}
    named = [c["target"] for c in clauses]
    if len(set(named)) != len(named):
        raise ParseError("two clauses switch off the same clause")
    for c in clauses:
        if c["target"] == c["id"] or c["target"] not in switchable:
            raise ParseError(f"clause {c['id']} switches off {c['target']}, which is itself, the definition or "
                             "not listed")
    cm = CLAIM_RE.match(tail)
    if not cm or cm["t"] not in TYPE_OF or cm["c"] not in CAUSE_OF:
        raise ParseError("claim line")
    claimant, respondent = S.parse("name", cm["a"]), S.parse("name", cm["b"])
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = K.parse_skin(skin, narrative, SCHEMA) if skin.author_mode == "T" else {}
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, SCHEMA)
    facts = {"CLAIMANT": claimant, "RESPONDENT": respondent, "AGREEMENT": agreement, "CAP_ID": cap}
    for k, v in list(told.items()) + list(asked.items()):
        if facts.get(k) != v:
            raise ParseError(f"{k} reads {v!r} in the text but {facts.get(k)!r} in the clauses")
    clauses.sort(key=lambda c: _key(c["id"]))
    view = {"agreement": agreement, "claimant": claimant, "respondent": respondent, "cap": cap, "notice": notice,
            "definition": definition, "clauses": clauses, "claim_type": TYPE_OF[cm["t"]],
            "claim_cause": CAUSE_OF[cm["c"]], "qform": wording.qform}
    if row["qtype"] == "choice":
        keys = []
        for t in row["options"]:
            om = re.fullmatch(r"Clause (\S+)", t)
            if not om:
                raise ParseError(f"option {t!r}")
            keys.append(om[1])
        view["options"] = keys
    return view


# ------------------------------------------------------------------------------------------------ set algebra

GRID = frozenset((t, c) for t in TYPE_OF.values() for c in CAUSE_OF.values())


def _cover(view: dict, cl: dict) -> frozenset:
    if cl["types"] is None:
        ts = set(TYPE_OF.values())
    elif cl["types"] == "DEF":
        if view["definition"] is None:
            raise ParseError("a clause uses the defined term but there is no definition")
        ts = set(view["definition"]["types"])
    else:
        ts = set(cl["types"])
    return frozenset((t, c) for (t, c) in GRID if t in ts and (cl["cause"] is None or c == cl["cause"]))


def effective_sets(view: dict) -> dict:
    """{clause id: its effective set} plus the cap clause's, bottom-up by set difference."""
    by_target: dict = {}
    for cl in view["clauses"]:
        by_target.setdefault(cl["target"], []).append(cl)
    memo: dict = {}

    def eff(cid: str, cover: frozenset, seen: frozenset) -> frozenset:
        if cid in seen:
            raise ParseError("clauses switch each other off in a cycle")
        if cid not in memo:
            out = cover
            for d in by_target.get(cid, []):
                out = out - eff(d["id"], _cover(view, d), seen | {cid})
            memo[cid] = out
        return memo[cid]

    eff(view["cap"], GRID, frozenset())
    for cl in view["clauses"]:
        eff(cl["id"], _cover(view, cl), frozenset())
    return memo


def solve_b(view: dict):
    cell = (view["claim_type"], view["claim_cause"])
    sets = effective_sets(view)
    if view["qform"] != "ch_clause":
        return ANSWER[view["qform"]](cell in sets[view["cap"]])
    target_of = {cl["id"]: cl["target"] for cl in view["clauses"]}
    by_id = {cl["id"]: cl for cl in view["clauses"]}
    best, best_len = view["cap"], 0
    for cid in by_id:
        path, node = [], cid
        while node in target_of:
            path.append(node)
            node = target_of[node]
        if node != view["cap"]:
            continue                                   # a clause of another rule (the notice clause)
        if all(cell in _cover(view, by_id[x]) for x in path) and len(path) > best_len:
            best, best_len = cid, len(path)
    return best
