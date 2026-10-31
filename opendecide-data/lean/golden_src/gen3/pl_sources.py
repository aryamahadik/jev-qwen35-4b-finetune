"""pl_sources: the propositions of yn2b family F4 (gen3_polarity_ladder; yn2b/SPEC.md section 5 F4).

(a) Human hard-gold label propositions on golden_train rows of S units.
    P = '"L" is the listed <label noun> that fits <the text> best'. L is the human gold label or the nearest wrong
    label (word overlap of the F4 definitions below, the ones the card shows). The card lists L plus the same
    near-miss bundle (gold, nearest wrong label and up to 4 more of the base row's labels) in shuffled order, so the
    card is built by one procedure whichever label L is. R2 fix (1 Oct, gen3_polarity_ladder.a_pair): the bundle
    keeps gold and the near miss a mutual nearest pair, and only labels that occur both as gold and as near miss in
    the pool are quoted, with truth(P) balanced per quoted label.
    The task lines and label definitions below are written for F4 (Claude-written, CPU only, no model). They restate
    each source's labelling rules in new words: the golden card text itself cannot be reused, because every golden
    card line and instruction is also in golden_dev, and SPEC 7.2 drops any yn2b unit that shares a 12-word run with a
    dev split (checked by the builder on every row).
(b) Program-decision propositions on F1, F2, F3 and F6 rows (their train / dev raw files): the decision a yes/no base
    question asks about, restated as a clause; truth(P) = that row's program gold. `proposition(key, row)` returns
    (kind, P) or None (a question form F4 does not use).
No label is computed here: (a) truth comes from the human gold, (b) from the source family's decide().
"""
from __future__ import annotations

import re
import string
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ================================================================================================ (a) label sources
# source -> task (card line), label noun, text phrase, {label: definition}. Sources: human-labelled golden_train
# classification sets with a small fixed label set whose task is clear from the text alone (no MCQ answer letters,
# no labels named yes / no, no entity-pair relations), and none of them under the ship rule's name match with a dev
# split (asserted by the builder).
A_SOURCES = {
    "gd_storm_ef": {
        "task": "rate the tornado in this National Weather Service storm survey on the Enhanced Fujita scale, as "
                "the survey team did",
        "noun": "EF rating", "text": "this storm survey",
        "defs": {
            "EFU (unrated)": "Left unrated: the confirmed tornado hit nothing the survey could use to estimate its "
                             "wind, for example it crossed only open fields, water or empty land.",
            "EF0": "Weakest rating, gusts near 65 to 85 mph: light harm such as peeled shingles or siding, damaged "
                   "gutters, broken branches and toppled shallow-rooted trees.",
            "EF1": "Gusts near 86 to 110 mph: moderate harm such as badly stripped roofs, overturned or wrecked mobile "
                   "homes, lost outside doors, broken windows and many snapped or uprooted trees.",
            "EF2": "Gusts near 111 to 135 mph: considerable harm such as roofs ripped from sturdy houses, frame homes "
                   "pushed off their foundations, mobile homes destroyed and cars lifted off the ground.",
            "EF3": "Gusts near 136 to 165 mph: severe harm such as whole floors of sturdy houses destroyed, big "
                   "buildings badly hit, trains overturned, trees stripped of bark and heavy cars thrown.",
            "EF4": "Gusts near 166 to 200 mph: devastating harm such as well-built houses flattened, cars thrown and "
                   "large debris flying through the air.",
            "EF5": "Strongest rating, gusts above 200 mph: strong frame houses flattened and swept off their "
                   "foundations, reinforced concrete badly damaged and car-sized debris carried far.",
        }},
    "gd_saferproducts_severity": {
        "task": "pick the most serious outcome for the main victim of this consumer product report on the "
                "SaferProducts.gov severity scale",
        "noun": "severity level", "text": "this incident report",
        "defs": {
            "no incident, no injury": "A hazard or defect was spotted before anything happened: the product never "
                                      "failed, burned, broke or hurt anyone while in use.",
            "incident, but no injury": "The product did fail in use (it overheated, caught fire, broke or "
                                       "malfunctioned), yet nobody was physically hurt; at most property was damaged "
                                       "or there was a near miss.",
            "injury, no first aid or medical care": "The main victim was hurt, for example a minor burn, cut, bruise "
                                                    "or shock, but got no first aid and sought no medical care.",
            "injury, first aid by a non-medical person": "The main victim was hurt and was treated only by "
                                                         "themselves or another layperson, for example with ice, a "
                                                         "bandage, ointment or a store-bought remedy, never by a "
                                                         "doctor or clinic.",
            "injury, seen by a medical professional": "The highest care the main victim got came from a doctor, "
                                                      "dentist, nurse or urgent-care clinic outside an emergency "
                                                      "room, with no hospital stay.",
            "injury, emergency department treatment": "The main victim was treated in a hospital emergency room, "
                                                      "possibly after an ambulance ride, and went home without "
                                                      "being admitted.",
            "injury, hospital admission": "The main victim was admitted to hospital as an inpatient, for example an "
                                          "overnight stay, intensive care, a burn unit or surgery, and survived.",
            "death": "The main victim died because of the incident, whether at the scene or later.",
        }},
    "gd_onestop_level": {
        "task": "say at which of three learner reading levels this rewritten news passage is written",
        "noun": "reading level", "text": "this passage",
        "defs": {
            "elementary": "The simplest version (roughly CEFR A2-B1): short sentences with mostly one clause, very "
                          "common words, simple tenses, hard terms explained or left out, and few idioms.",
            "intermediate": "The middle version (roughly B1-B2): sentences of medium length with some subordinate "
                            "clauses, mostly everyday words with a few rarer ones, and only light simplification.",
            "advanced": "The unsimplified native newspaper text (roughly C1): long sentences with several clauses, "
                        "rich or technical vocabulary, idioms, figurative language and dense reported speech.",
        }},
    "gd_logicinference": {
        "task": "treat each sentence as a bare logical proposition, with no outside knowledge, and say what the "
                "premises settle about the statement",
        "noun": "verdict", "text": "the statement, given the premises",
        "defs": {
            "true": "The premises force the statement: whenever every premise is true, the statement is true as "
                    "well.",
            "false": "The premises force the opposite of the statement: whenever every premise is true, the "
                     "statement is false.",
            "undetermined": "The premises force neither the statement nor its opposite, for example when the step "
                            "would affirm the consequent or the premises never touch the claim.",
        }},
    "gd_infotabs_nli": {
        "task": "treating the infobox as current, say how the hypothesis relates to it, using only the infobox and "
                "widely known facts",
        "noun": "relation", "text": "the hypothesis and the infobox",
        "defs": {
            "Entailment": "Together with widely known facts and simple reasoning about dates, counts or "
                          "comparisons, the infobox makes the hypothesis certainly true.",
            "Contradiction": "Together with widely known facts and simple reasoning, the infobox makes the "
                             "hypothesis certainly false, including when the clash only shows through dates, counts "
                             "or roles.",
            "Neutral": "The hypothesis brings in details that neither the infobox nor common knowledge can settle, "
                       "so it might be true or false.",
        }},
    "gd_ncbi_disease": {
        "task": "classify the disease mention wrapped in <e> tags by the NCBI disease-mention categories",
        "noun": "category", "text": "the tagged disease mention",
        "defs": {
            "specific disease": "Used as a noun phrase, the mention names one particular disease with its own single "
                                "definition and no subtypes, such as a named syndrome or its abbreviation.",
            "disease class": "Used as a noun phrase, the mention names a broad family or category that covers many "
                             "particular diseases, such as cancer or neurodegenerative disorders.",
            "composite mention": "One unbroken stretch of text names two or more distinct diseases that cannot be "
                                 "pulled apart without losing meaning, such as breast and ovarian cancer.",
            "modifier": "The disease name does not stand as a disease noun phrase but describes something else, "
                        "such as a gene, a family or a group of patients.",
        }},
    "gd_wnut17": {
        "task": "classify the named entity wrapped in <e> tags in this post",
        "noun": "entity type", "text": "the tagged name",
        "defs": {
            "person": "A named individual, real or fictional, including first names, nicknames and stage names; "
                      "bands and teams do not count.",
            "location": "A named place such as a country, city, region, street, venue, building, landmark or natural "
                        "feature.",
            "group": "A named group of people that is not a business, such as a band, sports team, political party, "
                     "government agency, club or charity.",
            "corporation": "A named company or business, including websites, social networks, online services and TV "
                           "channels, even when the site or app itself is meant.",
            "product": "A named thing that is sold or used, such as a device, food or drink brand, clothing line, "
                       "software package or video game; websites count as corporations.",
            "creative work": "The title of a creative work such as a song, album, film, TV show, book, painting or "
                             "play; video games count as products.",
        }},
    "gd_slur_usage": {
        "task": "say how the potentially offensive word in this comment is being used",
        "noun": "usage", "text": "the word in this comment",
        "defs": {
            "derogatory": "The word expresses contempt for a targeted person or group: an insult, a label, a "
                          "stand-alone slur, a sexualised use, a sweeping claim about the group, or self-mockery.",
            "mention without contempt": "The word is talked about rather than aimed at anyone, for example quoted, "
                                        "discussed as a word, recalled from an event, or used to push back against "
                                        "bigotry, by someone not reclaiming it.",
            "reclaimed by the targeted group": "Someone from the targeted group uses the word with positive or "
                                               "neutral force about themselves or their community, for pride, "
                                               "solidarity or humour.",
            "different meaning": "The word is used in a sense that is not a slur at all, such as a slang term for a "
                                 "cigarette or a short name for a car part.",
        }},
    "gd_hatemoji_build_v14": {
        "task": "say which description fits this post, reading any emoji for what they stand for",
        "noun": "description", "text": "this post",
        "defs": {
            "not hateful": "The post carries no hate toward any protected group; using emoji, naming a group, "
                           "quoting or opposing hate, or attacking an unprotected target does not make it hateful.",
            "derogation": "The post openly belittles a protected group, with negative claims about its members' "
                          "character, ability or looks, or with slurs or emoji used as slurs.",
            "animosity": "The post shows hostility toward a protected group in an indirect or subtle way, through "
                         "sarcasm, stereotypes, backhanded remarks or loaded questions, without open slurs or "
                         "dehumanization.",
            "dehumanization": "The post denies that members of a protected group are fully human, comparing them to "
                              "animals, insects, dirt, disease or objects, often with matching emoji.",
            "threatening language": "The post states or backs an intent to harm, attack, kill or drive out members "
                                    "of a protected group, often with weapon emoji.",
        }},
}
A_TASK_KEY = "task"
A_HOLDS_KEY, A_FAILS_KEY = "the statement holds", "the statement fails"


def a_short(source: str) -> str:
    return source[3:] if source.startswith("gd_") else source


def a_proposition(source: str, label: str) -> str:
    s = A_SOURCES[source]
    return f'"{label}" is the listed {s["noun"]} that fits {s["text"]} best'


def a_meaning(source: str, label: str) -> tuple[str, str]:
    """The card's definition of the proposition: (holds, fails) (SPEC 5 F4: 'yes: L is the label that fits the text
    best among the listed labels; no: another listed label fits better', stated for the proposition itself)."""
    s = A_SOURCES[source]
    return (f'"{label}" fits {s["text"]} better than any other listed {s["noun"]} does.',
            f'another listed {s["noun"]} fits {s["text"]} better than "{label}" does.')


# ================================================================================================ (b) program decisions
B_HOLDS_KEY, B_FAILS_KEY = "the statement holds", "the statement fails"

# ---- F1 gen3_rule_chain (F1a outcome / record questions; F1b numeric claim questions)
_F1 = {
    "pos1": (re.compile(r'^Under the (?P<doc>.+?), is the outcome of this (?P<req>.+?) "(?P<x>[^"]+)"\?$'), "outcome"),
    "pos2": (re.compile(r'^Applying the (?P<doc>.+?) to the case file, is the outcome of this (?P<req>.+?) '
                        r'"(?P<x>[^"]+)", rather than a different outcome\?$'), "outcome"),
    "pos3": (re.compile(r'^Does the (?P<doc>.+?) give this (?P<req>.+?) the outcome "(?P<x>[^"]+)", rather than a '
                        r'different one\?$'), "outcome"),
    "jdg1": (re.compile(r'^The case file shows a decision recorded for this (?P<req>.+?)\. Is that recorded decision '
                        r'consistent with the (?P<doc>.+?), rather than at odds with it\?$'), "record"),
    "jdg2": (re.compile(r'^Is the decision recorded for this (?P<req>.+?) supported by the (?P<doc>.+?) when it is '
                        r'applied to the case file\?$'), "record"),
    "jdg3": (re.compile(r'^Is the decision recorded for this (?P<req>.+?) in line with the (?P<doc>.+?), rather than '
                        r'at odds with it\?$'), "record"),
    "bpos1": (re.compile(r"^Under the rules in the card, does the evidence establish the claim\?$"), "claim"),
    "bpos2": (re.compile(r"^Read with the card's rules, do the figures in the evidence establish the claim, rather "
                         r"than fail to establish it\?$"), "claim"),
    "bjdg1": (re.compile(r"^The fact-check log has an entry for this claim\. Is that entry consistent with the "
                         r"evidence under the card's rules, rather than at odds with it\?$"), "log"),
    "bjdg2": (re.compile(r"^Under the card's rules, is the fact-check log entry for this claim supported by the "
                         r"evidence\?$"), "log"),
}


def _f1(row):
    tpl = row["meta"]["tpl"]
    if tpl not in _F1:
        return None
    rx, kind = _F1[tpl]
    m = rx.match(row["instructions"])
    if not m:
        return None
    g = m.groupdict()
    if kind == "outcome":
        return "f1.outcome", f'the outcome of this {g["req"]} under the {g["doc"]} is "{g["x"]}"'
    if kind == "record":
        return "f1.record", f"the decision recorded in the case file for this {g['req']} is consistent with the {g['doc']}"
    if kind == "claim":
        return "f1b.claim", "under the rules in the card, the evidence establishes the claim"
    return "f1b.log", "under the card's rules, the fact-check log entry for this claim is consistent with the evidence"


# ---- F2 gen3_tool_guard (the confirmation-only predicate is not used: it is not a plain decision)
_F2 = {"may": ("f2.may", "the proposed call may run under the policy"),
       "judge": ("f2.verdict", "the verdict the guardrail logged for the proposed call is consistent with the policy"),
       "output": ("f2.output", "the assistant's output meets every requirement stated for it")}


def _f2(row):
    m = re.match(r"^(may|judge|output)\d+$", row["meta"]["tpl"] or "")
    return _F2[m.group(1)] if m else None


# ---- F3 gen3_state_track: invert the machine's yes/no question format to its fields, then state its JB yes-wording
_F3_FIXED = {"jdg.a": "the agent's recorded state is consistent with the log under the numbered rules",
             "jdg.b": "every value in the agent record is supported by the log and the numbered rules",
             "jdg.h": "every entry of the agent record matches what the log gives under the numbered rules"}
# The agent machine builds its question from whole sentence fields (gen3_state_track_sim.Agent.qfields: yq / yq2 /
# jy), so its two forms per domain are listed here, word for word as qfields writes them.
_F3_AGENT = {
    "agt.eq.a": [("Does the cart hold at least {s} of {e} {when}?", "The cart holds at least {s} of {e} {when}."),
                 ("Is {e} in the {s} folder {when}?", "{e} is in the {s} folder {when}.")],
    "agt.eq.b": [("Under the numbered rules, is the quantity of {e} in the cart {s} or more {when}?",
                  "The cart holds at least {s} of {e} {when}."),
                 ("Under the numbered rules, does the {s} folder hold {e} {when}?", "{e} is in the {s} folder {when}.")],
}
_F3_TABLE: dict | None = None


# F3 field shapes: {e} is always one id token (SO-..., TCK-..., RES-..., SKU-..., DESK-..., ACC-..., BK-..., FF-...,
# DOC-..., a file name); {when} is gen3_state_track_sim.when_text (the machine's end phrase or an ISO time). Pinning
# them keeps a name field ({s}, {u}) from swallowing part of its neighbour.
F3_FIELD_RX = {"e": r"\S+", "when": r"at (?:the end of the (?:log|chat|session)|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)"}


def fmt_regex(fmt: str, fields: dict | None = None) -> re.Pattern:
    """A str.format template -> an anchored regex with one named group per field (a repeated field must repeat);
    `fields` gives a pattern for some fields (default: any text, shortest first)."""
    out, seen = ["^"], set()
    for lit, field, _, _ in string.Formatter().parse(fmt):
        out.append(re.escape(lit))
        if field is not None:
            if field in seen:
                out.append(f"(?P={field})")
            else:
                seen.add(field)
                out.append(f"(?P<{field}>{(fields or {}).get(field, '.+?')})")
    out.append("$")
    return re.compile("".join(out))


def f3_table() -> dict:
    """tpl -> [(question regex, JB yes-statement template)] from the F3 machines (the R2-fixed MACH of
    gen3_state_track; their YN tables are the simulator's)."""
    global _F3_TABLE
    if _F3_TABLE is None:
        import gen3_state_track as g3
        t: dict = {}
        for M in g3.MACH.values():
            for fam, spec in M.YN.items():
                for tpl, qf in spec.get("q", {}).items():
                    if tpl in _F3_AGENT:
                        continue
                    t.setdefault(tpl, []).append((fmt_regex(qf, F3_FIELD_RX), spec["jb"][0]))
        for tpl, forms in _F3_AGENT.items():
            t[tpl] = [(fmt_regex(q, F3_FIELD_RX), jy) for q, jy in forms]
        _F3_TABLE = t
    return _F3_TABLE


def _clause(stmt: str, tpl: str) -> str:
    s = stmt.strip()
    if s.endswith("."):
        s = s[:-1]
    if not tpl.startswith("{"):  # a template word, not a name or an id: lower-case it inside the frame
        s = s[0].lower() + s[1:]
    return s


def _f3(row):
    tpl = row["meta"]["tpl"]
    if tpl in _F3_FIXED:
        return "f3.record", _F3_FIXED[tpl]
    for rx, jy in f3_table().get(tpl, ()):
        m = rx.match(row["instructions"])
        if m:
            return "f3.state", _clause(jy.format(**m.groupdict()), jy)
    return None


# ---- F6 gen3_def_literal
_F6 = {
    "is0": (re.compile(r"^Under (?P<cl>.+?) of the (?P<doc>.+?), is the (?P<e>.+?) (?:(?P<a>an?) )?'(?P<t>[^']+)'\?$"),
            "the {e} is {a_}'{t}' under {cl} of the {doc}"),
    "is1": (re.compile(r"^Going by the definition in (?P<cl>.+?) and not by everyday usage, is the (?P<e>.+?) "
                       r"(?:(?P<a>an?) )?'(?P<t>[^']+)'\?$"),
            "the {e} is {a_}'{t}' by the definition in {cl}, not by everyday usage"),
    "is2": (re.compile(r"^Does the (?P<e>.+?) count as (?:(?P<a>an?) )?'(?P<t>[^']+)' as (?P<cl>.+?) defines that term\?$"),
            "the {e} counts as {a_}'{t}' as {cl} defines that term"),
    "is3": (re.compile(r"^Applying only the definition in (?P<cl>.+?), with no outside rules, does the (?P<e>.+?) "
                       r"qualify as (?:(?P<a>an?) )?'(?P<t>[^']+)'\?$"),
            "the {e} qualifies as {a_}'{t}' under the definition in {cl} alone"),
    "is4": (re.compile(r"^Taking (?P<cl>.+?) as the binding definition, should the (?P<e>.+?) be classed as "
                       r"(?:(?P<a>an?) )?'(?P<t>[^']+)'\?$"),
            "the {e} should be classed as {a_}'{t}' with {cl} as the binding definition"),
    "judge0": (re.compile(r"^Is the classification recorded in the (?P<reg>.+?) for this (?P<e>.+?) consistent with "
                          r"(?P<cl>.+?)\?$"),
               "the classification recorded in the {reg} for this {e} is consistent with {cl}"),
    "judge1": (re.compile(r"^Is the (?P<e>.+?)'s recorded classification supported by the definition in "
                          r"(?P<cl>.+?)\?$"),
               "the {e}'s recorded classification is supported by the definition in {cl}"),
    "judge2": (re.compile(r"^Does (?P<cl>.+?) support the classification the (?P<reg>.+?) records for the "
                          r"(?P<e>.+?)\?$"),
               "{cl} supports the classification the {reg} records for the {e}"),
    "judge3": (re.compile(r"^Under (?P<cl>.+?), is the classification on file for the (?P<e>.+?) consistent with the "
                          r"definition\?$"),
               "the classification on file for the {e} is consistent with the definition in {cl}"),
    "judge4": (re.compile(r"^Is the entry in the (?P<reg>.+?) for this (?P<e>.+?) backed by (?P<cl>.+?) as "
                          r"written\?$"),
               "the entry in the {reg} for this {e} is backed by {cl} as written"),
}


def _f6(row):
    tpl = row["meta"]["tpl"]
    if tpl not in _F6:
        return None
    rx, out = _F6[tpl]
    m = rx.match(row["instructions"])
    if not m:
        return None
    g = m.groupdict()
    g["a_"] = (g["a"] + " ") if g.get("a") else ""
    return ("f6.record" if tpl.startswith("judge") else "f6.term"), out.format(**g)


EXTRACTORS = {"gen3_rule_chain": _f1, "gen3_tool_guard": _f2, "gen3_state_track": _f3, "gen3_def_literal": _f6}
B_FAMILIES = tuple(EXTRACTORS)
RECORD_KINDS = ("f1.record", "f1b.log", "f2.verdict", "f2.output", "f3.record", "f6.record")


def proposition(key: str, row: dict):
    """(kind, P) for an affirmative (polarity 0) yes/no row of a source family, or None. P is a clause that reads
    after 'that'; truth(P) is the row's gold ('yes' -> True)."""
    m = row["meta"]
    if m["qkind"] != "yn" or m["polarity"] != 0 or m["role"] not in ("aff", "para") or m["view"] == "attack":
        return None
    out = EXTRACTORS[key](row)
    if out is None:
        return None
    kind, p = out
    p = p.strip()
    if not p or "\n" in p or "{" in p or "}" in p:
        return None
    return kind, p
