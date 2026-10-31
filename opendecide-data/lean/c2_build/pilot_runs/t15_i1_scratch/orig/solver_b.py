"""families/T15/solver_b.py: T15 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts with this module's own readers:
  - the rule card (instructions, before the blank line) line by line against the G0 card wording (S15, S16): the
    programme, the year, every gate (its fact by the gate phrase, its comparator and limit through the lexicon
    registry, admitted forms only), the route programme and the gates it skips; or the claimant steps, the months
    clause (lexicon) and the tie-breaker order;
  - the facts block in its container (bullet lines, markdown table, JSON, CSV or the S4 interview); an attached
    "Note added to the case" line is recognised and skipped; values by slots.parse with this module's own units;
  - the case note through skin.parse_skin (CASE_ID, WORKER and SUBJECT; the subject must agree with the facts);
  - the question through its wording template (its admitted meaning is the question form); on choice rows every
    option text back to its key.
solve_b(view) decides by decision-table enumeration:
  gates      every gate's pass bit is a sign test on the integer difference fact - limit; a truth table over every
             pass / fail combination maps the failing gates that apply (the route's gates removed for an enrolled
             applicant) to the earliest gate letter, or to eligible; the row's bit vector is looked up in it;
  claimants  the people still in the running (filed a claim; months test as a sign table) meet in a pairwise duel
             table: a duel goes to the person ahead on the first tie-breaker, in card order, on which the two
             differ; the winner is the person who wins every duel (nobody in the running: nobody).
Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import itertools
import json
import re

from c2_kit import skin as K
from c2_kit import slots as S

CLOSED = "These rules and facts are complete, and only they decide the outcome."
NOTE = "Note added to the case: "
NOBODY_TEXT = "Nobody may claim the child"
CENTS = (("currency", "USD"), ("symbol", "$"))
MONTHS = (("unit", ("month", "months")),)
# fact id -> (facts label, kind, params, card gate phrase, interview question)   (G0_SPEC.md S2-S3, S17)
FACTS = {
    "gross": ("gross monthly income", "cents", CENTS, "gross monthly income is ", "What is your gross monthly income?"),
    "net": ("net monthly income", "cents", CENTS, "net monthly income is ",
            "And your net monthly income, after deductions?"),
    "assets": ("countable assets", "cents", CENTS, "countable assets are ", "What are your countable assets worth?"),
    "residence": ("time in the service area", "count", MONTHS, "the applicant has lived in the service area for ",
                  "How long have you lived in the service area?"),
    "age": ("age", "count", (("unit", ("year", "years")),), "the applicant's age is ", "How old are you?"),
    "tenure": ("time employed", "count", MONTHS, "the applicant has been employed for ",
               "How long have you been employed here?"),
    "hours": ("hours worked in the past year", "count", (("unit", ("hour", "hours")),),
              "hours worked in the past year are ", "How many hours did you work in the past year?"),
    "head": ("employees at the worksite", "count", (("unit", ("employee", "employees")),), "the worksite has ",
             "How many employees work at your worksite?"),
    "gpay": ("gross annual pay", "cents", CENTS, "gross annual pay is ", "What is your gross annual pay?"),
    "npay": ("take-home annual pay", "cents", CENTS, "take-home annual pay is ", "And your take-home annual pay?"),
}
DOMAINS = {"household": ("gross", "net", "assets", "residence", "age"),
           "work": ("tenure", "hours", "head", "gpay", "npay")}
ENROLL_LABEL = "enrolled in"
ENROLL_QUESTION = "Which other programme are you enrolled in?"
RELATIONS = ("mother", "father", "grandmother", "grandfather", "aunt", "uncle")
PARENT_LINE = "- A parent means the child's mother or father. Different people's months can overlap."
PARENT_WORDS = frozenset(("mother", "father"))
NOTE_SCHEMA = {"CASE_ID": ("id", ()), "WORKER": ("name", ()), "SUBJECT": ("name", ())}
QUESTION_SCHEMA = {"SUBJECT": ("name", ()), "PROG": ("name", ()), "ASKED": ("name", ())}

GATE_HEAD = re.compile(r"(?P<prog>[^\n]+) eligibility rules for (?P<year>\d{4}):")
GATE_INTRO = ("- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops "
              "at the first gate that fails, and that gate is the reason the applicant is not eligible.")
GATE_LINE = re.compile(r"- Gate (?P<letter>[A-D]): passed when (?P<rest>[^\n]+)\.")
ROUTE_LINE = re.compile(r"- Route: an applicant enrolled in (?P<prog>[^\n;]+) skips (?P<gates>Gate [A-D](?:(?:, | and )"
                        r"Gate [A-D])*); for that applicant, skipped gates count as passed, and every other gate still "
                        r"applies\.")
ELIGIBLE_LINE = "- An applicant who passes every gate that applies is eligible; any other applicant is not eligible."
CLAIM_HEAD = re.compile(r"(?P<prog>[^\n]+) rules for (?P<year>\d{4}): who may claim (?P<child>[^\n]+)\.")
STEP_THREE = ("- Step three: if more than one person is still in the running, apply the tie-breakers below in the "
              "order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the "
              "tie-breakers stop as soon as one person is left.")
TIE_LINE = re.compile(r"- (?P<ord>First|Second|Third) tie-breaker: (?P<text>[^\n]+)\.")
TIE_TEXT = {"a parent comes first, before a grandparent, aunt or uncle": "parent",
            "the person with whom {child} lived for more months comes first": "months",
            "the person with the higher annual income comes first": "income"}
OUTCOME_OPTION = re.compile(r"Not eligible: Gate (?P<letter>[A-D]) is the reason \((?P<label>[^()\n]+)\)")
FACT_HEADS = (
    ("gates", "json", re.compile(r"Facts for (?P<who>[^\n]+) \((?P<year>\d{4})\), as JSON:")),
    ("gates", "csv", re.compile(r"Facts for (?P<who>[^\n]+) \((?P<year>\d{4})\), as CSV with amounts in USD:")),
    ("gates", "plain", re.compile(r"Facts for (?P<who>[^\n]+) \((?P<year>\d{4})\):")),
    ("gates", "transcript", re.compile(r"Intake interview with (?P<who>[^\n]+) \((?P<year>\d{4})\):")),
    ("claimants", "json", re.compile(r"People who asked to claim (?P<who>[^\n]+) \((?P<year>\d{4})\), as JSON:")),
    ("claimants", "csv", re.compile(r"People who asked to claim (?P<who>[^\n]+) \((?P<year>\d{4})\), as CSV with "
                                    r"amounts in USD:")),
    ("claimants", "plain", re.compile(r"People who asked to claim (?P<who>[^\n]+) \((?P<year>\d{4})\):")),
    ("claimants", "transcript", re.compile(r"Interview notes for (?P<who>[^\n]+) \((?P<year>\d{4})\):")),
)
CHOICE_FORMS = ("ch_outcome", "ch_claimant")
GATE_FORMS = ("ch_outcome", "yn_eligible", "yn_dneg_eligible", "yn_ineligible", "yn_gate_stops", "yn_fails",
              "yn_not_eligible")
# Sign tables on the integer difference (fact - limit): does the fact meet the comparator?
MEETS = {"cmp.le": {-1: True, 0: True, 1: False}, "cmp.lt": {-1: True, 0: False, 1: False},
         "cmp.ge": {-1: False, 0: True, 1: True}, "cmp.gt": {-1: False, 0: False, 1: True}}
# Question table: (eligible?) or (does the asked person claim?) -> answer.
ANSWER = {"yn_eligible": {True: 1, False: 0}, "yn_dneg_eligible": {True: 1, False: 0},
          "yn_ineligible": {True: 0, False: 1}, "yn_gate_stops": {True: 0, False: 1},
          "yn_fails": {True: 0, False: 1}, "yn_not_eligible": {True: 0, False: 1},
          "yn_may_claim": {True: 1, False: 0}, "yn_dneg_claim": {True: 1, False: 0},
          "yn_barred": {True: 0, False: 1}, "yn_elsewhere": {True: 0, False: 1},
          "yn_fails_claim": {True: 0, False: 1}, "yn_may_not": {True: 0, False: 1}}


class ParseError(ValueError):
    pass


def _sign(x: int) -> int:
    return (x > 0) - (x < 0)


def _value(fid: str, raw: str):
    _label, kind, params, _phrase, _q = FACTS[fid]
    return S.parse(kind, raw, params)


def _bound(text: str, kind: str, params, ctx) -> tuple:
    """(sem, bound) of a comparator clause, through the lexicon (admitted forms only)."""
    sem, _form, vals = ctx.lexicon.parse_exact(text, {"BOUND": (kind, params)}, admitted_only=True)
    if len(vals) != 1:
        raise ParseError(f"comparator {text!r} holds {len(vals)} bounds")
    (v,) = vals.values()
    if not isinstance(v, int) or sem not in MEETS:
        raise ParseError(f"comparator {text!r} reads as {sem} {v!r}")
    return sem, v


# ------------------------------------------------------------------------------------------------ the card
def _gate_card(lines: list, ctx) -> dict:
    head = GATE_HEAD.fullmatch(lines[0])
    if not head or lines[1] != GATE_INTRO or lines[-1] != "- " + CLOSED or lines[-2] != ELIGIBLE_LINE:
        raise ParseError("gate card does not match the G0 wording")
    gates, route = [], None
    for ln in lines[2:-2]:
        m = GATE_LINE.fullmatch(ln)
        if m:
            if route is not None or m["letter"] != "ABCD"[len(gates)]:
                raise ParseError("gates are lettered A, B, C ... in order, before the route")
            hits = [fid for fid, x in FACTS.items() if m["rest"].startswith(x[3])]
            if len(hits) != 1:
                raise ParseError(f"gate phrase {m['rest']!r} names {len(hits)} facts")
            fid = hits[0]
            sem, bound = _bound(m["rest"][len(FACTS[fid][3]):], FACTS[fid][1], FACTS[fid][2], ctx)
            gates.append([fid, sem, bound])
            continue
        r = ROUTE_LINE.fullmatch(ln)
        if not r or route is not None:
            raise ParseError(f"unexpected card line {ln!r}")
        skips = re.findall(r"Gate ([A-D])", r["gates"])
        route = {"programme": r["prog"], "skips": skips}
    if not 2 <= len(gates) <= 4:
        raise ParseError(f"{len(gates)} gates")
    if route is not None:
        letters = "ABCD"[:len(gates)]
        if (sorted(set(route["skips"])) != route["skips"] or not set(route["skips"]) <= set(letters)
                or len(route["skips"]) >= len(gates)):
            raise ParseError("the route skips listed gates, in order, and never all of them")
    domains = {d for d, fids in DOMAINS.items() if {g[0] for g in gates} <= set(fids)}
    if len(domains) != 1 or len({g[0] for g in gates}) != len(gates):
        raise ParseError("the gates mix two domains or repeat a fact")
    return {"track": "gates", "prog": head["prog"], "year": int(head["year"]), "domain": domains.pop(),
            "gates": gates, "route": route}


def _claim_card(lines: list, ctx) -> dict:
    head = CLAIM_HEAD.fullmatch(lines[0])
    if not head or len(lines) != 11:
        raise ParseError("claimant card does not match the G0 wording")
    child, year = head["child"], head["year"]
    want = {1: f"- Only one person may claim {child}. Work through these steps in order.",
            2: f"- Step one: only people who filed a claim for {child} are considered.",
            4: STEP_THREE, 8: f"- If nobody is left after step two, nobody may claim {child}.", 9: PARENT_LINE,
            10: "- " + CLOSED}
    for i, text in want.items():
        if lines[i] != text:
            raise ParseError(f"claimant card line {i} differs from the G0 wording")
    step2 = re.fullmatch(r"- Step two: of those, only people with whom " + re.escape(child) + r" lived for "
                         r"(?P<clause>[^\n]+) in " + year + r" stay in the running\.", lines[3])
    if not step2:
        raise ParseError("step two does not match the G0 wording")
    sem, months = _bound(step2["clause"], "count", MONTHS, ctx)
    tie_text = {k.format(child=child): v for k, v in TIE_TEXT.items()}
    order = []
    for i, ordinal in zip((5, 6, 7), ("First", "Second", "Third")):
        m = TIE_LINE.fullmatch(lines[i])
        if not m or m["ord"] != ordinal or m["text"] not in tie_text:
            raise ParseError(f"tie-breaker line {lines[i]!r}")
        order.append(tie_text[m["text"]])
    if sorted(order) != sorted(TIE_TEXT.values()):
        raise ParseError("the three tie-breakers appear once each")
    if sem not in ("cmp.ge", "cmp.gt"):
        raise ParseError("the months step is a lower bound")
    return {"track": "claimants", "prog": head["prog"], "year": int(year), "subject": child, "min_sem": sem,
            "min_months": months, "order": order}


# ------------------------------------------------------------------------------------------------ the facts block
def _strip_note(lines: list) -> list:
    notes = [i for i, ln in enumerate(lines) if ln.startswith(NOTE)]
    if not notes:
        return lines
    if notes != [len(lines) - 1]:
        raise ParseError("an attached note is one line at the end of the facts block")
    return lines[:-1]


def _gate_facts(style: str, who: str, body: list) -> tuple:
    pairs = []
    if style == "plain" and body and body[0] == "| fact | value |":
        if len(body) < 3 or body[1] != "| --- | --- |":
            raise ParseError("facts table needs a header and a rule")
        for ln in body[2:]:
            m = re.fullmatch(r"\| ([^|\n]+) \| ([^|\n]+) \|", ln)
            if not m:
                raise ParseError(f"facts table row {ln!r}")
            pairs.append((m[1], m[2]))
    elif style == "plain":
        for ln in body:
            m = re.fullmatch(r"- ([a-z][a-z -]*[a-z]): ([^\n]+)", ln)
            if not m:
                raise ParseError(f"facts line {ln!r}")
            pairs.append((m[1], m[2]))
    elif style == "json":
        if len(body) != 1:
            raise ParseError("JSON facts are one line")
        obj = json.loads(body[0])
        if not isinstance(obj, dict) or any(not isinstance(v, str) for v in obj.values()):
            raise ParseError("JSON facts: one object of strings")
        pairs = [(k.replace("_", " "), v) for k, v in obj.items()]
    elif style == "csv":
        if not body or body[0] != "fact,value":
            raise ParseError("CSV facts need the header fact,value")
        for ln in body[1:]:
            parts = ln.split(",")
            if len(parts) != 2:
                raise ParseError(f"CSV facts row {ln!r}")
            pairs.append((parts[0], parts[1]))
    else:
        questions = {x[4]: x[0] for x in FACTS.values()}
        questions[ENROLL_QUESTION] = ENROLL_LABEL
        if len(body) % 2:
            raise ParseError("interview lines come in question / answer pairs")
        for q, a in zip(body[0::2], body[1::2]):
            if not q.startswith("Caseworker: ") or q[12:] not in questions:
                raise ParseError(f"interview question {q!r}")
            if not (a.startswith(who + ": ") and a.endswith(".")):
                raise ParseError(f"interview answer {a!r}")
            pairs.append((questions[q[12:]], a[len(who) + 2:-1]))
    labels = [p[0] for p in pairs]
    for domain, fids in DOMAINS.items():
        if labels == [FACTS[f][0] for f in fids] + [ENROLL_LABEL]:
            facts = {fid: _value(fid, raw) for fid, (_, raw) in zip(fids, pairs)}
            enrolled = pairs[-1][1]
            if not enrolled or enrolled != enrolled.strip():
                raise ParseError("empty enrolment")
            return domain, facts, enrolled
    raise ParseError(f"fact labels {labels} are not a G0 domain")


def _person(name: str, rel: str, months: str, income: str, filed: str) -> list:
    if rel not in RELATIONS or filed not in ("yes", "no"):
        raise ParseError(f"relationship {rel!r} / filed {filed!r}")
    return [S.parse("name", name), rel, S.parse("count", months, MONTHS), S.parse("cents", income, CENTS), filed]


def _claim_facts(style: str, child: str, body: list) -> list:
    people = []
    if style == "plain" and body and body[0].startswith("| person |"):
        want = (f"| person | relationship to {child} | months lived with {child} | annual income | filed a claim |",
                "| --- | --- | --- | --- | --- |")
        if tuple(body[:2]) != want:
            raise ParseError("claimant table header")
        for ln in body[2:]:
            m = re.fullmatch(r"\| ([^|\n]+) \| ([^|\n]+) \| ([^|\n]+) \| ([^|\n]+) \| ([^|\n]+) \|", ln)
            if not m:
                raise ParseError(f"claimant table row {ln!r}")
            people.append(_person(*m.groups()))
    elif style == "plain":
        rx = re.compile(r"- (?P<name>[^:;\n]+): relationship to " + re.escape(child) + r": (?P<rel>[a-z]+); months "
                        r"lived with " + re.escape(child) + r": (?P<months>[^;\n]+); annual income: (?P<inc>[^;\n]+); "
                        r"filed a claim: (?P<filed>[a-z]+)")
        for ln in body:
            m = rx.fullmatch(ln)
            if not m:
                raise ParseError(f"claimant line {ln!r}")
            people.append(_person(m["name"], m["rel"], m["months"], m["inc"], m["filed"]))
    elif style == "json":
        if len(body) != 1:
            raise ParseError("JSON claimants are one line")
        obj = json.loads(body[0])
        keys = ["name", "relationship", "months_lived_with_child", "annual_income", "filed_a_claim"]
        if set(obj) != {"people"} or not all(isinstance(o, dict) and list(o) == keys for o in obj["people"]):
            raise ParseError("JSON claimants: {'people': [objects with the five G0 keys]}")
        people = [_person(*[o[k] for k in keys]) for o in obj["people"]]
    elif style == "csv":
        if not body or body[0] != "name,relationship,months lived with child,annual income,filed a claim":
            raise ParseError("CSV claimant header")
        for ln in body[1:]:
            parts = ln.split(",")
            if len(parts) != 5:
                raise ParseError(f"CSV claimant row {ln!r}")
            people.append(_person(*parts))
    else:
        if len(body) % 8:
            raise ParseError("interview notes come in blocks of eight lines")
        for b in range(0, len(body), 8):
            blk = body[b:b + 8]
            m = re.fullmatch(r"Caseworker: (?P<name>[^,\n]+), how are you related to " + re.escape(child) + r"\?",
                             blk[0])
            if not m:
                raise ParseError(f"interview opening {blk[0]!r}")
            nm = m["name"]
            fixed = {4: "Caseworker: What was your annual income?", 6: f"Caseworker: Did you file a claim for {child}?"}
            if blk[4] != fixed[4] or blk[6] != fixed[6] or not re.fullmatch(
                    re.escape(f"Caseworker: How long did {child} live with you in ") + r"\d{4}\?", blk[2]):
                raise ParseError("interview questions differ from the G0 wording")
            rel = re.fullmatch(re.escape(f"{nm}: I am {child}'s ") + r"([a-z]+)\.", blk[1])
            answers = []
            for ln in (blk[3], blk[5], blk[7]):
                if not (ln.startswith(nm + ": ") and ln.endswith(".")):
                    raise ParseError(f"interview answer {ln!r}")
                answers.append(ln[len(nm) + 2:-1])
            if not rel:
                raise ParseError(f"interview relationship {blk[1]!r}")
            people.append(_person(nm, rel[1], *answers))
    names = [p[0] for p in people]
    if not 2 <= len(people) <= 4 or len(set(names)) != len(names):
        raise ParseError("2-4 people with distinct names")
    return people


def _facts_block(block: str) -> tuple:
    lines = _strip_note(block.split("\n"))
    for track, style, rx in FACT_HEADS:
        m = rx.fullmatch(lines[0])
        if m:
            return track, style, m["who"], int(m["year"]), lines[1:]
    return None


# ------------------------------------------------------------------------------------------------ parse
def parse(row: dict, ctx) -> dict:
    blocks = row["state"].split("\n\n")
    if len(blocks) != 2:
        raise ParseError("the state is a case note and a facts block, separated by one blank line")
    found = [(i, _facts_block(b)) for i, b in enumerate(blocks)]
    found = [(i, f) for i, f in found if f is not None]
    if len(found) != 1:
        raise ParseError(f"{len(found)} facts blocks")
    i, (track, style, who, year_f, body) = found[0]
    note = blocks[1 - i]
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    if skin.author_mode != "T":
        raise ParseError("T15 v1 reads Mode T case notes only")
    told = K.parse_skin(skin, note, NOTE_SCHEMA)
    if set(told) != set(NOTE_SCHEMA):
        raise ParseError(f"case note slots {sorted(told)}")
    card, sep, question = row["instructions"].partition("\n\n")
    if not sep or "\n" in question:
        raise ParseError("card and question are not separated")
    lines = card.split("\n")
    view = _gate_card(lines, ctx) if track == "gates" else _claim_card(lines, ctx)
    if view["track"] != track or view["year"] != year_f:
        raise ParseError("card and facts disagree on the track or the year")
    if track == "gates":
        domain, facts, enrolled = _gate_facts(style, who, body)
        if domain != view["domain"]:
            raise ParseError("the gates and the facts belong to two domains")
        view.update(subject=who, facts=facts, enrolled=enrolled)
    else:
        if who != view["subject"]:
            raise ParseError("card and facts name two children")
        view["people"] = _claim_facts(style, who, body)
    if told["SUBJECT"] != view["subject"]:
        raise ParseError("the case note names another subject")
    view.update(worker=told["WORKER"], case_id=told["CASE_ID"])
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, {k: v for k, v in QUESTION_SCHEMA.items() if k in wording.decl})
    if asked.get("SUBJECT", view["subject"]) != view["subject"] or asked.get("PROG", view["prog"]) != view["prog"]:
        raise ParseError("the question names another subject or programme")
    qform = wording.qform
    if (qform in GATE_FORMS) != (track == "gates"):
        raise ParseError(f"question {qform} does not fit a {track} card")
    view["qform"] = qform
    if track == "claimants":
        view["asked"] = asked.get("ASKED")
        if (view["asked"] is None) != (qform == "ch_claimant"):
            raise ParseError("a yes/no claimant question names one person; the choice question none")
        if view["asked"] is not None and view["asked"] not in [p[0] for p in view["people"]]:
            raise ParseError(f"the question asks about {view['asked']!r}, who is not listed")
    if row["qtype"] == "choice":
        view["options"] = [_option_key(view, t) for t in row["options"]]
    return view


def _option_key(view: dict, text: str):
    if view["qform"] == "ch_outcome":
        if text == "Eligible":
            return "eligible"
        m = OUTCOME_OPTION.fullmatch(text)
        letters = "ABCD"[:len(view["gates"])]
        if not m or m["letter"] not in letters:
            raise ParseError(f"unknown outcome option {text!r}")
        if FACTS[view["gates"][letters.index(m["letter"])][0]][0] != m["label"]:
            raise ParseError(f"option {text!r} names another fact than its gate")
        return "fail_" + m["letter"]
    if view["qform"] == "ch_claimant":
        if text == NOBODY_TEXT:
            return "none"
        if text not in [p[0] for p in view["people"]]:
            raise ParseError(f"option {text!r} is not a listed person")
        return text
    raise ParseError(f"question {view['qform']} has no options")


# ------------------------------------------------------------------------------------------------ solver B
def _gate_table(view: dict) -> tuple:
    letters = "ABCD"[:len(view["gates"])]
    route = view["route"]
    skipped = set(route["skips"]) if route is not None and view["enrolled"] == route["programme"] else set()
    table = {}
    for bits in itertools.product((1, 0), repeat=len(letters)):
        failing = [x for x, b in zip(letters, bits) if b == 0 and x not in skipped]
        table[bits] = ("fail_" + min(failing)) if failing else "eligible"
    row = tuple(1 if MEETS[sem][_sign(view["facts"][fid] - bound)] else 0 for fid, sem, bound in view["gates"])
    return table[row]


def _duel(a: list, b: list, order: list) -> int:
    """+1 when a is ahead of b on the first tie-breaker (card order) on which they differ, -1 when behind, 0 tie."""
    for tb in order:
        x = {"parent": int(a[1] in PARENT_WORDS), "months": a[2], "income": a[3]}[tb]
        y = {"parent": int(b[1] in PARENT_WORDS), "months": b[2], "income": b[3]}[tb]
        if x != y:
            return _sign(x - y)
    return 0


def _claim_table(view: dict):
    running = [p for p in view["people"]
               if p[4] == "yes" and MEETS[view["min_sem"]][_sign(p[2] - view["min_months"])]]
    if not running:
        return None
    duels = {(a[0], b[0]): _duel(a, b, view["order"]) for a in running for b in running if a[0] != b[0]}
    winners = [a[0] for a in running if all(duels[(a[0], b[0])] == 1 for b in running if b[0] != a[0])]
    if len(winners) != 1:
        raise ParseError("no single winner in the duel table (a full tie is never generated)")
    return winners[0]


def solve_b(view: dict):
    q = view["qform"]
    if view["track"] == "gates":
        outcome = _gate_table(view)
        return outcome if q == "ch_outcome" else ANSWER[q][outcome == "eligible"]
    winner = _claim_table(view)
    if q == "ch_claimant":
        return "none" if winner is None else winner
    return ANSWER[q][winner is not None and winner == view["asked"]]
