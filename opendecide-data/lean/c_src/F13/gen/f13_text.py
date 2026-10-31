"""F13 renderer: model -> fmt1 Doc IR (state), card IR (G0 section 11 sentences, word for word), question, options,
edge. Grammar: f13_design.py. The parser (f13_parse.py) is written from G0 sections 2 / 7 / 11 and that grammar, and
never imports this module."""
from __future__ import annotations

import re

import f13_base as B

# ------------------------------------------------------------------------------------------------ G0 section 11 lines
SEM = {
    "01": ("Treat the document as complete: any rule, record, entry or other item of any kind ({kinds}) that it does "
           "not mention did not happen or does not exist. Every value a rule needs for the case is given or shown as "
           "'{marker}'. Some values are shown as '{marker}' and some parts are marked 'not included in this copy'; "
           "none of them is needed for any answer."),
    "02": ("A value shown as '{marker}' is not given in this copy, and neither is the content of a part marked 'not "
           "included in this copy'. A missing part can affect only what its label says it covers. Any rule, record, "
           "entry or other item of any kind ({kinds}) that the document neither mentions nor marks as missing does not "
           "exist. Every value a rule needs for the case is given or shown as '{marker}'. On a choice question, if the "
           "answer depends on something not given, choose '{nei}'."),
    "03": ("For 'Does the document establish that <claim>?': answer yes if the document shows the claim is true. If it "
           "shows the claim is false, or does not settle it, answer no."),
    "04": ("For 'Does the document settle whether <claim>?': answer yes if the document shows the claim is true or "
           "shows it is false; answer no if it leaves it open."),
    "05a": "'{none}' means the document settles the answer and none of the listed answers is correct.",
    "05b": "'{nei}' means the document does not settle the answer.",
    "06": "Use only this document and the case in the question. Do not use outside knowledge.",
    "09": "'If <C>, <X>' means <C> is enough for <X> unless a rule with higher precedence says otherwise.",
    "10": ("'At least <T>', 'no fewer than <T>' and 'no less than <T>' include <T>. 'At most <T>', 'up to <T>', 'no "
           "more than <T>' and 'not exceeding <T>' include <T>."),
    "11": ("'More than <T>', 'over <T>', 'above <T>' and 'exceeds <T>' do not include <T>. 'Less than <T>', 'fewer "
           "than <T>', 'below <T>' and 'under <T>' do not include <T>."),
    "13": ("'<A> or <B>' is met when at least one of them holds. When only one may hold, the document says 'either <A> "
           "or <B>, but not both'."),
    "15": ("'<D1> through <D2>' and 'from <D1> through <D2>' include both dates. 'Before <D>' and 'after <D>' exclude "
           "<D>. 'On or before <D>', 'by <D>' and 'on or after <D>' include <D>."),
    "16": ("A rule, version or exception effective <D> applies from <D> on. 'Valid through <D>' means it applies on <D> "
           "and not after. 'Repealed with effect from <D>' means it does not apply on <D> or after. 'No end date' means "
           "it has no end date of its own: it stops applying when a dated repeal or a replacement takes effect, and "
           "not before."),
    "17": ("For a case, use the rules and versions in force on its {gname}, and read every record, hold, condition, "
           "decision and action item as it stands at the end of that date."),
    "18": ("When a question asks 'as of <D>', answer for the end of that date: anything dated or taking effect on <D> "
           "counts; anything dated or taking effect after <D> does not count yet. Only 'as of' sets this date; a date "
           "that describes a case or an entry (for example 'filed on <D>') does not."),
    "19": ("'Within <N> days of <D>' means from <D> through the <N>th day after <D>, both included. Times are in {tz}. "
           "Entries may be listed out of time order: use the timestamps; entries with the same timestamp take effect "
           "in entry-number order."),
    "49": ("An entry '<configuration> rolled back to <version>' counts as <version> taking effect again at the time "
           "of that entry. Before that time, the versions in force are unchanged."),
    "21": "Amounts are exact as written. Nothing is rounded.",
    "23": "If two versions take effect on the same date, the higher revision number applies.",
    "24_specific": "A rule for a specific {kind} overrides a rule with no {kind} mark, whatever their dates.",
    "24_later": ("A rule with a later effective date overrides an earlier rule, even one for a specific {kind}. For a "
                 "rule with several versions, the date that counts is the effective date of the version that applies "
                 "to the case."),
    "25": ("An exception names a rule, or another exception, and the cases it covers. While the exception is in force, "
           "the rule it names does not apply to those cases, under any precedence policy; the outcome then comes from "
           "the other rules, or from the default outcome if none applies. An exception covers every version of the "
           "rule it names. When an exception names another exception, that exception does not apply to the cases "
           "named, and the rule it names applies to them again."),
    "26": ("A correction fixes an error and applies from the start, as if the text had always read that way. An "
           "amendment changes a rule from its effective date."),
    "27": "An entry, version or decision marked void counts as never made.",
    "28": ("A newer version applies from its own effective date; an older version still applies to cases whose {gname} "
           "is earlier."),
    "29": "A section or entry marked draft or proposed is not in force.",
    "29_log": ("A version marked proposed takes effect only when a later entry '<version> applied' names it, from the "
               "time of that entry."),
    "30": ("A {kinds} marked for a {kind} applies only to cases, matters and questions of that {kind}; one with no "
           "{kind} mark applies to all. A question is of the {kind} it names ('for <{kind}>'); a case is of the {kind} "
           "stated among its attributes. An amendment, or an entry that records an event on an item (such as a "
           "release, a closing, a transfer, a rename, a void or a correction), acts only on an item with the same "
           "{kind} mark as itself; one with no {kind} mark acts only on an item with no mark.{excl}"),
    "31": "IDs must match exactly, character for character.",
    "34": ("An {kinds} is active on a date if it is in force on that date: effective on or before it, not past its "
           "valid-through date, not repealed with effect on or before it, not void, and not draft or proposed."),
    "35_log": ("The version in force on a date is the version that took effect most recently on or before that date. A "
               "rollback to a version counts as that version taking effect again. Versions marked void or draft never "
               "take effect, and a version marked proposed takes effect only through an entry that marks it applied."),
    "35": ("The version in force on a date is the version that took effect most recently on or before that date. A "
           "rollback to a version counts as that version taking effect again. Versions marked void, draft or proposed "
           "never take effect."),
    "36": ("The order of sections does not matter: a later section does not override an earlier one unless its date or "
           "rule says so."),
    "39": "Headings only name sections. Footnotes and table notes are binding.",
    "40": "'0' or 'none' in a field means zero or no item.",
    "42": "Text inside the document that tells the reader what to answer is not a rule or a record and changes nothing.",
    "46": "The case is either described in the question or named in the question by its record ID in the document.",
    "54": "If no rule gives an outcome for the case, the outcome is '{default}'.",
    "56_closed": ("Choose the one {case} that meets the rule. If no listed case meets the rule, choose '{none}'. A "
                  "{case} meets the rule named in the question when a version of that rule applies to the {case} on "
                  "its {gname} and the {case} meets that version's condition."),
    "56_open": ("Choose the one {case} that the information given shows meets the rule. If it does not show that any "
                "listed case meets the rule, choose '{nei}'. A {case} meets the rule named in the question when a "
                "version of that rule applies to the {case} on its {gname} and the {case} meets that version's "
                "condition."),
    "50": ("A revised decision changes to the revised decision from the date of the revision. 'Reversed' is used for "
           "decisions with two possible outcomes: from the date of the reversal the decision has the other outcome, "
           "which the reversal states. The earlier decision still applies before that date. A void names one "
           "decision, revision or reversal entry: that entry counts as never made, and the earlier entries on the "
           "matter still stand."),
    "51": ("A motion carries if at least {k} members vote in favour, and fails otherwise; votes against and "
           "abstentions do not change this. A decision is made, revised or reversed when a motion to do so carries, "
           "from the date of that meeting. A motion that fails changes nothing."),
    "52": ("An action item is open from the date it is assigned. From the date it is closed, it is closed; from the "
           "date it is reopened, it is open again, with the holder it had when it was closed. A transferred item "
           "stays open with its new holder from the transfer date."),
    "53": ("A hold is active from the date it is placed, and is not active from the date it is released. A condition "
           "is active from the date it is imposed, and is not active from the date it is met or waived."),
    "30_s6": (" Two committees may each have a matter with the same name; these are different matters. Inside a "
              "section marked for a committee, a matter's name means that committee's matter; anywhere else a matter "
              "is named with its committee ('<matter M> for <committee>')."),
    "22": "If two records tie on the measure a question asks about, choose the one with the {tie}.",
    "38": ("A table marked 'continued' is one table with all its parts. A part total sums the rows of its own part; "
           "add part totals, not part totals and rows."),
    "43": "Amounts are in {unit} unless a column or line states another unit. No conversion is needed.",
    "44": ("An option such as '{r2} and {r5} only' is correct if exactly those records qualify, and wrong "
           "otherwise."),
    "60": "The possible {what} are {names}.",
    "61": ("An amendment to a rule or clause makes a new version of it, with the version ID the amendment states; that "
           "version takes effect on the amendment's effective date."),
}
CORE = {"01", "02", "03", "04", "05a", "05b", "06", "17", "18", "24_specific", "24_later", "30", "42", "46", "51", "54",
        "56_closed", "56_open", "60", "61"}
MARKERS = ("[not provided]", "[not provided in this copy]", "[illegible in this copy]")
TI_LABELS = ("Contact list", "Staff directory", "Telephone and e-mail list")
NEI = "not enough information"
NONE_OPT = "none of the listed answers"


def art(w: str) -> str:
    return "an" if w[:1].lower() in "aeiou" else "a"


def join_or(xs: list) -> str:
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " or " + xs[-1]


def join_and(xs: list) -> str:
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


# ------------------------------------------------------------------------------------------------ values and conditions
OPW = {"ge": "at least", "le": "at most", "gt": "more than", "lt": "less than"}


def amount(v: int, unit: str | None) -> str:
    if unit is None:
        return str(v)
    if unit in ("%", "°C", "°F"):
        return f"{v}{unit}"
    return f"{v} {unit}"


def atom_text(a: dict, attrs_meta: dict) -> str:
    if a["op"] == "eq":
        return f"the {a['attr']} is {a['val']}"
    return f"the {a['attr']} is {OPW[a['op']]} {amount(a['val'], attrs_meta.get(a['attr']))}"


def cond_text(conds, join, attrs_meta) -> str:
    parts = [atom_text(a, attrs_meta) for a in conds]
    return (" and " if join == "all" else " or ").join(parts)


def end_text(end, df) -> str:
    if end[0] == "none":
        return "no end date"
    if end[0] == "through":
        return f"valid through {B.fmt_date(B.parse_date(str(end[1])) if isinstance(end[1], str) else end[1], df)}"
    return f"repealed with effect from {B.fmt_date(B.parse_date(str(end[1])) if isinstance(end[1], str) else end[1], df)}"


def D(x, df) -> str:
    import datetime as dt
    return B.fmt_date(x if isinstance(x, dt.date) else dt.date.fromisoformat(str(x)), df)


# ------------------------------------------------------------------------------------------------ fact sentences (S1)
def fact_lines(f: dict, card: dict, names: dict) -> list:
    """One fact -> its sentences (the mark lines of an item travel with it). `names` maps plain label names to the
    row's rendering (plain / masked / swapped, SEM-59)."""
    df, am, item = card["date_form"], card["attr_units"], card["item"]
    ft = f["ft"]
    if ft in LC_FT:
        return lc_lines(f, card, names)
    if ft in ("crit", "excl"):
        return tab_lines(f, card, names)
    if ft in LE_FT:
        return log_lines(f, card, names)
    if ft == "rule":
        out = names.get(f["outcome"], f["outcome"])
        if f["form"] == "clause":
            lines = [f"Rule {f['rid']}, version {f['vid']}: if {cond_text(f['conds'], f['join'], am)}, the outcome for the "
                     f"{item} is {out}."]
        else:
            lines = [f"Amendment to rule {f['rid']}: version {f['vid']} amends version {f['amends']}; under version "
                     f"{f['vid']}, if {cond_text(f['conds'], f['join'], am)}, the outcome for the {item} is {out}."]
        if f["scope"] is not None:
            lines.append(f"Version {f['vid']} is marked for {f['scope']}.")
        lines.append(f"Version {f['vid']} status: {f['status']}.")
        if f.get("eff") is not None:
            lines.append(f"Version {f['vid']}: effective {D(f['eff'], df)}; {end_text(f['end'], df)}.")
        else:
            lines.append(f"Version {f['vid']}: {end_text(f['end'], df)}.")
        return lines
    if ft == "effreg":
        return [f"Version {f['vid']} of rule {f['rid']}: effective {D(f['eff'], df)}."]
    if ft == "void":
        return [f"Correction: {f['target']} is void."]
    if ft == "exc":
        lines = [f"Exception {f['eid']} to rule {f['rid']} covers every {item} whose "
                 f"{cond_text(f['conds'], f['join'], am)[4:]}."]
        if f["scope"] is not None:
            lines.append(f"Exception {f['eid']} is marked for {f['scope']}.")
        lines.append(f"Exception {f['eid']} status: {f['status']}.")
        lines.append(f"Exception {f['eid']}: effective {D(f['eff'], df)}; {end_text(f['end'], df)}.")
        return lines
    if ft == "inert":
        return [f["text"]]
    raise ValueError(ft)


def case_pairs(c: dict, card: dict) -> list:
    am, mk = card["attr_units"], card["marker"]
    pairs = []
    for k, v in c["attrs"].items():
        pairs.append([k, mk if v == "__TRACE__" else (amount(v, am.get(k)) if isinstance(v, int) else str(v))])
    pairs.append([card["scope_kind"], c["scope"]])
    pairs.append([card["gname"], D(c["gdate"], card["date_form"])])
    return pairs


def case_desc(c: dict, card: dict) -> str:
    """Case in the question / an inverted option: complete, single line, no 'as of', no ': '."""
    ps = case_pairs(c, card)
    return f"{art(card['item'])} {card['item']} with " + join_and([f"{k} {v}" for k, v in ps])


# ------------------------------------------------------------------------------------------------ sections -> Doc IR
def section_block(sec: dict, card: dict, names: dict) -> dict:
    blocks = []
    if sec.get("trace"):
        t = sec["trace"]
        blocks.append({"type": "items", "items": [f"{t['label']} ({t['scope_label']}): not included in this copy."]})
        return {"type": "section", "heading": sec["heading"], "blocks": blocks}
    items = []
    if sec.get("scope"):
        items.append(f"{card['scope_kind'].capitalize()}: {sec['scope']}.")
    if sec.get("mdate"):
        items.append(f"Meeting date: {D(sec['mdate'], card['date_form'])}.")
    if sec.get("period"):
        items.append(f"Reporting period: {D(sec['period'][0], card['date_form'])} through "
                     f"{D(sec['period'][1], card['date_form'])}.")
    if any(f["ft"] == "table" for f in sec["facts"]):
        for f in sec["facts"]:
            if f["total"] is not None:
                items.append(f"Part total for part {f['part']} of table {f['name']} ({f['tmeas']}): "
                             f"{amount(f['total'], card['attr_units'].get(f['tmeas']))}.")
        if items:
            blocks.append({"type": "items", "items": items})
        for f in sec["facts"]:
            blocks.extend(table_blocks(f, card))
        return {"type": "section", "heading": sec["heading"], "blocks": blocks}
    for f in sec["facts"]:
        if f["ft"] == "case":
            if items:
                blocks.append({"type": "items", "items": items})
                items = []
            blocks.append({"type": "fields", "label": f"{card['item'].capitalize()} record {f['cid']}",
                           "pairs": case_pairs(f, card)})
            continue
        items.extend(fact_lines(f, card, names))
    if items:
        blocks.append({"type": "items", "items": items})
    return {"type": "section", "heading": sec["heading"], "blocks": blocks}


def doc_ir(doc: dict, names: dict) -> dict:
    card = doc["card"]
    return {"title": doc.get("title"), "meta": doc.get("meta") or [],
            "blocks": [section_block(s, card, names) for s in doc["sections"]]}


# ------------------------------------------------------------------------------------------------ card IR
def card_lines(card: dict, row: dict) -> list:
    """The card's SEM lines (G0 11): core lines always; lexicon lines on full cards where the trigger can occur on the
    card (row['short'] drops lexicon lines; each dropped line passes reading invariance, solver B)."""
    k = card["scope_kind"]
    out = []
    add = lambda key, **kw: out.append((key, SEM[key].format(**kw)))  # noqa: E731
    kinds = card["fact_kinds"]
    if card["world"] == "closed":
        add("01", kinds=join_or(kinds), marker=card["marker"])
        add("05a", none=NONE_OPT)
    else:
        add("02", kinds=join_or(kinds), marker=card["marker"], nei=NEI)
        add("05b", nei=NEI)
        if card.get("has_establish"):
            add("03")
        if card.get("has_settle"):
            add("04")
    add("06")
    if card.get("has_case"):
        add("17", gname=card["gname"])
        add("46")
    add("18")
    add("24_" + card["precedence"], kind=k)
    xk = [x + "s" for x in ("exception", "exclusion") if x in kinds]
    excl = f" This does not apply to {' or '.join(xk)}." if xk else ""
    add("30", kinds=join_or(card["scoped_kinds"]), kind=k, excl=excl)
    if card.get("lc") == "motion":
        out[-1] = ("30", out[-1][1] + SEM["30_s6"])
        add("51", k=card["vote_k"])
    add("42")
    add("54", default=row["names"].get(card["default"], card["default"]))
    if "amendment" in kinds:
        add("61")
    if card.get("inverted"):
        add("56_" + card["world"], case=card["item"], none=NONE_OPT, nei=NEI, gname=card["gname"])
    lex = []
    lexadd = lambda key, **kw: lex.append((key, SEM[key].format(**kw)))  # noqa: E731
    lexadd("09")
    if card.get("ops") & {"ge", "le"}:
        lexadd("10")
    if card.get("ops") & {"gt", "lt"}:
        lexadd("11")
    if card.get("has_or"):
        lexadd("13")
    lexadd("16")
    lexadd("23")
    if "exception" in kinds:
        lexadd("25")
        lexadd("34", kinds="exception")
    lexadd("26")
    lexadd("27")
    lexadd("28", gname=card["gname"])
    lexadd("29")
    if card.get("log"):
        lexadd("29_log")
        lexadd("19", tz=card["tz"])
        lexadd("49")
    lexadd("31")
    if card.get("tab") and card["sampler"] == "S4" or card.get("tables"):
        lexadd("15")
        lexadd("21")
        lexadd("38")
        u0 = next((m["unit"] for m in card["measures"] if m["unit"]), None)
        if u0:
            lexadd("43", unit=u0)
        if card.get("tie"):
            lexadd("22", tie="earlier record date" if card["tie"] == "date" else f"lower {card['item']} ID")
        lexadd("44", r2=card["ent_prefix"] + "-1002", r5=card["ent_prefix"] + "-1005")
    if "exclusion" in kinds:
        lexadd("34", kinds="exclusion")
    if card.get("lc"):
        lexadd("50")
        lexadd("53" if card["lc"] == "notice" else "52")
    lexadd("35_log" if card.get("log") else "35")
    lexadd("36")
    lexadd("39")
    if not row.get("short"):
        out.extend(lex)
    return out


def _rename(text: str, names: dict) -> str:
    """repair r3: card examples / few-shot excerpts carry the plain outcome names; a masked or swapped row renders
    them as the row's names (one pass, longest first, so no chained replacement; SEM-59, F13R2-09)."""
    pairs = {o: v for o, v in names.items() if o != v}
    if not pairs:
        return text
    rx = re.compile("|".join(r"(?<![\w-])" + re.escape(o) + r"(?![\w-])" for o in sorted(pairs, key=len, reverse=True)))
    return rx.sub(lambda m: pairs[m.group(0)], text)


def card_ir(card: dict, row: dict) -> dict:
    """fmt1 card IR: reading rules (items), label schema (SEM-60 para + defs in the card's definition style), optional
    few-shot overlay. Label-name definition lines become option lines on choice rows (fmt1 choice_route)."""
    names = row["names"]
    lines = [t for _, t in card_lines(card, row)]
    shown = [names.get(o, o) for o in card["outcomes"]]
    blocks = [{"type": "items", "items": lines},
              {"type": "para", "text": SEM["60"].format(what="outcomes", names=join_and(shown))}]
    entries = []
    for o in card["outcomes"]:
        e = {"name": names.get(o, o), "text": card["defs"][o]}  # meaning only; never the plain name (SEM-59)
        if card["defs_style"] == "one_line_examples" and card.get("examples", {}).get(o) and not row.get("short"):
            e["examples"] = [_rename(x, names) for x in card["examples"][o][:2]]
        entries.append(e)
    blocks.append({"type": "defs", "variant": card["defs_variant"], "heading": "Outcomes", "entries": entries})
    if card.get("few_shot") and not row.get("short"):
        blocks.append({"type": "fewshot", "template": card["fewshot_template"], "heading": "Worked examples",
                       "examples": [{"case": _rename(e["case"], names), "answer": names.get(e["answer"], e["answer"])}
                                    for e in card["few_shot"]]})
    return {"title": f"How to read the {card['org']} {card['doc_noun']}", "blocks": blocks}


# ------------------------------------------------------------------------------------------------ inert facts
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")


def inert_pool(pack: dict, card: dict, r, n: int, forbidden=()) -> list:
    """n distinct inert sentences built from the pack (contacts, staff, schedules, glossary, resources, purpose,
    procedure steps, pack inert facts); each passes the SEM-62 lint (f13_base.inert_ok)."""
    people = pack["people"] or pack["roles"]
    roles = pack["roles"] or ["coordinator"]
    objs = pack["objects"] or [e["plural"] for e in pack["ents"]]
    docs = pack["doc_types"] or ["log sheet"]
    units = card["units"]
    gens = []
    gens.append(lambda: f"Contact for {r.choice(units)}: {r.choice(people)}, {r.choice(roles)}, telephone "
                        f"{r.randint(200, 989)} {r.randint(1000, 9999)}.")
    gens.append(lambda: f"{r.choice(people)} works as {r.choice(roles)} with the {r.choice(objs)}.")
    gens.append(lambda: f"The {r.choice(objs)} walk-round takes place every {r.choice(WEEKDAYS)} at "
                        f"{r.randint(7, 17):02d}:{r.choice(['00', '15', '30', '45'])}.")
    if pack["jargon"]:
        gens.append(lambda: f"Glossary: '{r.choice(pack['jargon'])}' is the local name for the {r.choice(objs)} "
                            f"kept by the {r.choice(roles)}.")
    gens.append(lambda: f"The {r.choice(units)} stock list names the {join_and(r.sample(objs, min(3, len(objs))))}.")
    gens.append(lambda: f"Step {r.randint(1, 9)} of the {r.choice(docs)} routine: the {r.choice(roles)} signs the "
                        f"{r.choice(docs)} and files it with the {r.choice(objs)}.")
    gens.append(lambda: f"Copies of the {r.choice(docs)} are kept in the {r.choice(objs)} cabinet.")
    pk = [s for s in pack["inert"] if B.inert_ok(s, forbidden)]
    if pk:
        gens.append(lambda: (lambda s: s[0].upper() + s[1:].rstrip(".") + ".")(r.choice(pk)))
    out, seen = [], set()
    tries = 0
    while len(out) < n and tries < n * 30:
        tries += 1
        s = r.choice(gens)()
        if s in seen or not B.inert_ok(s, forbidden):
            continue
        seen.add(s)
        out.append(s)
    return out


# ------------------------------------------------------------------------------------------------ questions
def q_text(doc: dict, names: dict) -> str:
    """The question (G0 2.5 / 3.1 / 3.2 forms). Case questions name the case (description or record ID) and no date;
    other questions name 'for <unit>' and 'as of <D>' once."""
    card, q = doc["card"], doc["query"]
    df = card["date_form"]
    if q["qk"] in ("qp_outcome",):
        cref = (f"{card['item']} record {q['case_ref']}" if q.get("case_ref") else case_desc(doc["case"], card))
        if q["form"] == "choice":
            return f"What is the outcome for {cref}?"
        o = names.get(q["claim"]["value"], q["claim"]["value"])
        claim = f"the outcome for {cref} is {o}"
        neg_claim = f"the outcome for {cref} is not {o}"
        if q["form"] == "yn":
            return {0: f"Is the outcome for {cref} {o}?", 1: f"Is it true that {neg_claim}?",
                    2: f"Is it not the case that {neg_claim}?"}[q.get("neg", 0)]
        if q["form"] == "establish":
            c = neg_claim if q.get("inner_neg") else claim
            return (f"Does the document fail to establish that {c}?" if q.get("neg", 0) % 2
                    else f"Does the document establish that {c}?")
        c = neg_claim if q.get("inner_neg") else claim
        return (f"Does the document fail to settle whether {c}?" if q.get("neg", 0) % 2
                else f"Does the document settle whether {c}?")
    if q["qk"] in LC_QK:
        return lc_q_text(doc, names)
    if q["qk"] in TAB_QK:
        return tab_q_text(doc, names)
    if q["qk"] in LG_QK:
        return log_q_text(doc, names)
    if q["qk"] == "qp_inverted":
        return f"Which of these cases meets rule {q['rid']}?"
    if q["qk"] in ("qr_version", "ag2_version"):
        return f"Which version of rule {q['rid']} is in force for {q['unit']} as of {D(q['date'], df)}?"
    if q["qk"] == "ag1_exc":
        return f"How many exceptions for {q['unit']} are active as of {D(q['date'], df)}?"
    raise ValueError(q["qk"])


# ------------------------------------------------------------------------------------------------ S2 / S6 (f13_lc)
LC_FT = ("dec", "dvoid", "dcorr", "hold", "lcond", "aitem")
LC_QK = ("qr_decision", "ag2_decision", "ag1_hold", "ag1_cond", "qr_holder", "ag1_items")
VERB = {"decision": "make", "revision": "revise"}


def lc_lines(f: dict, card: dict, names: dict) -> list:
    df = card["date_form"]
    ft = f["ft"]
    motion = card.get("lc") == "motion"
    if ft == "dec":
        m, o = f["matter"], names.get(f["outcome"], f["outcome"])
        if motion:
            if f["status"] == "proposed":
                return [f"Proposal to revise the decision on {m} so that {m} is {o}.", "Status: proposed."]
            a, b, c = f["votes"]
            return [f"Motion to {VERB[f['kind']]} the decision on {m} so that {m} is {o}: in favour {a}, against {b}, "
                    f"abstain {c}."]
        if f["kind"] == "decision":
            lines = [f"Decision notice on {m}, dated {D(f['date'], df)}: the outcome is {o}."]
        else:
            lines = [f"Revision notice on {m}, dated {D(f['date'], df)}: the decision is revised; the outcome is {o}."]
        if f["status"] == "proposed":
            lines.append("Status: proposed.")
        return lines
    if ft == "dvoid":
        if motion:
            return [f"Correction to the minutes of {D(f['date'], df)}: the {f['kind']} on {f['matter']} made at the "
                    f"meeting of {D(f['date'], df)} is void."]
        return [f"Correction to the {f['kind']} notice on {f['matter']} dated {D(f['date'], df)}: the notice is void."]
    if ft == "dcorr":
        new, old = names.get(f["new"], f["new"]), names.get(f["old"], f["old"])
        if motion:
            return [f"Correction to the minutes of {D(f['date'], df)}: in the motion to {VERB[f['kind']]} the decision "
                    f"on {f['matter']}, the outcome is {new}, not {old}."]
        return [f"Correction to the {f['kind']} notice on {f['matter']} dated {D(f['date'], df)}: the outcome is {new}, "
                f"not {old}."]
    if ft == "hold":
        tail = f"; released on {D(f['released'], df)}" if f["released"] else ""
        return [f"Hold {f['hid']} on {f['noun']} {f['eid']}: placed on {D(f['placed'], df)}{tail}.",
                f"Hold {f['hid']} is marked for {f['scope']}."]
    if ft == "lcond":
        tail = f"; {f['end'][0]} on {D(f['end'][1], df)}" if f["end"] else ""
        return [f"Condition {f['cnd']} on {f['noun']} {f['eid']}: imposed on {D(f['imposed'], df)}{tail}.",
                f"Condition {f['cnd']} is marked for {f['scope']}."]
    if ft == "aitem":
        parts = []
        for verb, who, d in f["events"]:
            parts.append(f"{verb} to {who} on {D(d, df)}" if who else f"{verb} on {D(d, df)}")
        return [f"Action item {f['aid']}: " + "; ".join(parts) + "."]
    raise ValueError(ft)


def lc_q_text(doc: dict, names: dict) -> str:
    card, q = doc["card"], doc["query"]
    on = D(q["date"], card["date_form"])
    qk, form, neg = q["qk"], q["form"], q.get("neg", 0)
    if qk in ("ag1_hold", "ag1_cond"):
        w = "holds" if qk == "ag1_hold" else "conditions"
        return f"How many {w} on {q['noun']} {q['eid']} for {q['unit']} are active as of {on}?"
    if qk == "ag1_items":
        return f"How many open action items for {q['unit']} have {q['holder']} as their holder as of {on}?"
    if qk in ("qr_decision", "ag2_decision"):
        subj = f"the decision on {q['matter']} for {q['unit']}"
        if form == "choice":
            return f"What is the decision on {q['matter']} for {q['unit']} as of {on}?"
        o = names.get(q["claim"]["value"], q["claim"]["value"])
        pos, negc = f"{subj} is {o}", f"{subj} is not {o}"
        yn0 = f"Is {subj} {o} as of {on}?"
    else:
        A = f"action item {q['aid']} for {q['unit']}"
        if form == "choice":
            return f"Who is the holder of {A} as of {on}?"
        h = q["claim"]["value"]
        pos, negc = f"{h} is the holder of {A}", f"{h} is not the holder of {A}"
        yn0 = f"Is {h} the holder of {A} as of {on}?"
    if form == "yn":
        return {0: yn0, 1: f"Is it true that {negc} as of {on}?", 2: f"Is it not the case that {negc} as of {on}?"}[neg]
    c = negc if q.get("inner_neg") else pos
    verb = "establish that" if form == "establish" else "settle whether"
    return f"Does the document {'fail to ' if neg % 2 else ''}{verb} {c} as of {on}?"


# ------------------------------------------------------------------------------------------------ S4 tables (f13_tab)
TAB_QK = ("tq_count", "tq_argmax", "tq_cmp", "tq_crit", "tq_set", "ag3_sum", "ag3_count", "tp_outcome", "ag1_excl")


def col_label(k: str, card: dict) -> str:
    if k == "id":
        return f"{card['item'].capitalize()} ID"
    if k == "cat":
        return card["cat"]["name"].capitalize()
    if k == "date":
        return card["tie_date"].capitalize()
    u = card["attr_units"].get(k)
    return f"{k.capitalize()} ({u})" if u else k.capitalize()


def cell_text(k, v, card):
    if v == "__TRACE__":
        return card["marker"]
    if k == "date":
        return D(v, card["date_form"])
    return str(v)


def table_blocks(f: dict, card: dict) -> list:
    cap = f"Table {f['name']}" if f["part"] is None else (
        f"Part {f['part']} of table {f['name']}" + (" (continued)" if f["part"] > 1 else ""))
    out = [{"type": "table", "caption": cap, "columns": [col_label(k, card) for k in f["cols"]],
            "rows": [[cell_text(k, v, card) for k, v in zip(f["cols"], row)] for row in f["rows"]]}]
    return out


def tab_lines(f: dict, card: dict, names: dict) -> list:
    df = card["date_form"]
    if f["ft"] == "crit":
        o = names.get(f["outcome"], f["outcome"])
        return [f"Criterion {f['rid']}: {art(card['item'])} {card['item']} is {o} if "
                f"{cond_text(f['conds'], f['join'], card['attr_units'])}.",
                f"Criterion {f['rid']}: effective {D(f['eff'], df)}; no end date."]
    return [f"Exclusion {f['xid']} for {f['noun']} {f['eid']} is marked for {f['scope']}; effective {D(f['eff'], df)}; "
            f"{end_text(f['end'], df)}.", f"Exclusion {f['xid']} status: {f['status']}."]


OPWQ = {"ge": "at least", "le": "at most", "gt": "more than", "lt": "less than"}


def set_text(xs) -> str:
    return join_and(sorted(xs)) + " only"


def tab_q_text(doc: dict, names: dict) -> str:
    card, q = doc["card"], doc["query"]
    df = card["date_form"]
    qk, form, neg = q["qk"], q["form"], q.get("neg", 0)
    if qk == "ag1_excl":
        return f"How many exclusions for {q['unit']} are active as of {D(q['date'], df)}?"
    per = f"{D(q['period'][0], df)} through {D(q['period'][1], df)}"
    noun = card["item"]
    if qk == "tp_outcome":
        E = f"{noun} {q['ent']}"
        if form == "choice":
            return f"Under the report's criteria, what is the outcome for {E} for {per}?"
        o = names.get(q["claim"]["value"], q["claim"]["value"])
        pos, negc = f"{E} is {o} for {per}", f"{E} is not {o} for {per}"
        y0 = f"Under the report's criteria, is {E} {o} for {per}?"
        lead = "Under the report's criteria, "
        if form == "yn":
            return {0: y0, 1: f"{lead}is it true that {negc}?", 2: f"{lead}is it not the case that {negc}?"}[neg]
        c = negc if q.get("inner_neg") else pos
        verb = "establish that" if form == "establish" else "settle whether"
        return f"{lead}does the document {'fail to ' if neg % 2 else ''}{verb} {c}?"
    sel = f"table {q['table']} for {q['unit']} from {per}"
    mu = card["attr_units"].get(q["measure"])
    if qk in ("tq_count", "ag3_count"):
        return f"How many {card['plural']} in {sel} have {q['measure']} of {OPWQ[q['op']]} {amount(q['thr'], mu)}?"
    if qk == "tq_set":
        return f"Which {card['plural']} in {sel} have {q['measure']} of {OPWQ[q['op']]} {amount(q['thr'], mu)}?"
    if qk == "ag3_sum":
        return f"What is the total {q['measure']} in {sel}?"
    if qk == "tq_argmax":
        if form == "choice":
            return f"Which {noun} in {sel} has the highest {q['measure']}?"
        E = f"{noun} {q['claim']['value']}"
        pos, negc = f"{E} has the highest {q['measure']} in {sel}", f"{E} does not have the highest {q['measure']} in {sel}"
        y0 = f"Does {E} have the highest {q['measure']} in {sel}?"
    elif qk == "tq_crit":  # repair r6: criterion claim (slot-polar)
        E = f"{noun} {q['claim']['value']}"
        crit = f"{q['measure']} of {OPWQ[q['op']]} {amount(q['thr'], mu)}"
        pos, negc = f"{E} has {crit} in {sel}", f"{E} does not have {crit} in {sel}"
        y0 = f"Does {E} have {crit} in {sel}?"
    else:
        E1, E2 = f"{noun} {q['ent']}", f"{noun} {q['ent2']}"
        pos = f"the {q['measure']} of {E1} is higher than that of {E2} in {sel}"
        negc = f"the {q['measure']} of {E1} is not higher than that of {E2} in {sel}"
        y0 = f"Is the {q['measure']} of {E1} higher than that of {E2} in {sel}?"
    if form == "yn":
        return {0: y0, 1: f"Is it true that {negc}?", 2: f"Is it not the case that {negc}?"}[neg]
    c = negc if q.get("inner_neg") else pos
    verb = "establish that" if form == "establish" else "settle whether"
    return f"Does the document {'fail to ' if neg % 2 else ''}{verb} {c}?"


# ------------------------------------------------------------------------------------------------ S3 logs (f13_log)
LE_FT = ("le_ver", "le_app", "le_rb", "le_void", "le_stat", "le_noop")
LG_QK = ("lg_version", "ag2_config", "lg_status", "lg_count", "ag3_lcount")


def cfg_unit(card, cfg):
    return next((c["unit"] for c in card.get("cfgs") or [] if c["name"] == cfg), None)


def log_lines(f: dict, card: dict, names: dict) -> list:
    """'<time> | <entry no> | <actor> | <text>' (one line per entry, SEM-19)."""
    pre = f"{D(f['date'], card['date_form'])} {f['time']} | {f['no']} | {f['actor']} | "
    ft = f["ft"]
    if ft == "le_ver":
        return [pre + f"Version {f['vid']} of the {f['cfg']} recorded; status {f['status']}; value "
                f"{amount(f['value'], cfg_unit(card, f['cfg']))}."]
    if ft == "le_app":
        return [pre + f"{f['vid']} applied."]
    if ft == "le_rb":
        return [pre + f"{f['cfg']} rolled back to {f['vid']}."]
    if ft == "le_void":
        return [pre + f"VOID entry {f['target']}."]
    if ft == "le_stat":
        return [pre + f"Status of {f['noun']} {f['eid']} set to {names.get(f['status'], f['status'])}."]
    if ft == "le_noop" and f.get("cfg"):  # repair r9-2: version no-op (mention decoy)
        if f["verb"] == "viewed":
            return [pre + f"Record of version {f['eid']} of the {f['cfg']} viewed by {f['user']}."]
        return [pre + f"Comment added to the record of version {f['eid']} of the {f['cfg']} by {f['user']}."]
    if ft == "le_noop":
        if f["verb"] == "viewed":
            return [pre + f"Record of {f['noun']} {f['eid']} viewed by {f['user']}."]
        return [pre + f"Comment added to the record of {f['noun']} {f['eid']} by {f['user']}."]
    raise ValueError(ft)


def log_q_text(doc: dict, names: dict) -> str:
    card, q = doc["card"], doc["query"]
    on = D(q["date"], card["date_form"])
    qk, form, neg = q["qk"], q["form"], q.get("neg", 0)
    u = q["unit"]
    if qk in ("lg_count", "ag3_lcount"):
        S = names.get(q["filt"], q["filt"])
        return f"How many log entries for {u} set the status of {art(q['noun'])} {q['noun']} to {S} as of {on}?"
    if qk == "ag2_config":
        return f"What is the value of the {q['cfg']} in force for {u} as of {on}?"
    if qk == "lg_version":
        if form == "choice":
            return f"Which version of the {q['cfg']} is in force for {u} as of {on}?"
        subj = f"version {q['claim']['value']} of the {q['cfg']}"
        pos, negc = f"{subj} is in force for {u}", f"{subj} is not in force for {u}"
        yn0 = f"Is {subj} in force for {u} as of {on}?"
    else:
        R = f"{q['noun']} {q['eid']} for {u}"
        if form == "choice":
            return f"What is the status of {R} as of {on}?"
        o = names.get(q["claim"]["value"], q["claim"]["value"])
        pos, negc = f"the status of {R} is {o}", f"the status of {R} is not {o}"
        yn0 = f"Is the status of {R} {o} as of {on}?"
    if form == "yn":
        return {0: yn0, 1: f"Is it true that {negc} as of {on}?", 2: f"Is it not the case that {negc} as of {on}?"}[neg]
    c = negc if q.get("inner_neg") else pos
    verb = "establish that" if form == "establish" else "settle whether"
    return f"Does the document {'fail to ' if neg % 2 else ''}{verb} {c} as of {on}?"
